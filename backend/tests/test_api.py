import unittest
from datetime import timedelta
from concurrent.futures import ThreadPoolExecutor
import os
import tempfile

from fastapi.testclient import TestClient

from app.main import CSRF_COOKIE, SESSION_COOKIE, app, now, store


class ApiTests(unittest.TestCase):
    def setUp(self):
        self.db = tempfile.NamedTemporaryFile(suffix='.sqlite3', delete=False)
        self.db.close()
        store.configure(self.db.name); store.sessions.clear()
        self.client = TestClient(app)

    def tearDown(self):
        store.close(); os.unlink(self.db.name)

    def login(self, subject):
        token, csrf = store.create_session(subject, subject, f"{subject}@example.test")
        self.client.cookies.set(SESSION_COOKIE, token)
        self.client.cookies.set(CSRF_COOKIE, csrf)
        self.client.headers.update({"X-CSRF-Token": csrf})

    def test_auth_required_without_local_session(self):
        self.assertEqual(self.client.get('/boards').status_code, 401)

    def test_expired_session_has_no_workspace_access(self):
        self.login('expired')
        token = next(iter(store.sessions))
        store.sessions[token]['expires_at'] = now() - timedelta(seconds=1)
        self.assertEqual(self.client.get('/session').status_code, 401)

    def test_private_lifecycle_and_archived_search(self):
        self.login('alice')
        board = self.client.post('/boards', json={'name': 'Work'}).json()
        task = self.client.post(f"/boards/{board['id']}/tasks", json={'title': 'Ship API'}).json()
        self.assertEqual(task['status'], 'todo')
        self.assertEqual(self.client.patch(f"/boards/{board['id']}/tasks/{task['id']}/status", json={'status': 'done', 'version': 1}).json()['status'], 'done')
        self.client.post(f"/boards/{board['id']}/archive")
        result = self.client.get('/search/tasks?q=api').json()
        self.assertEqual(result[0]['boardId'], board['id']); self.assertTrue(result[0]['archived'])
        self.client.post(f"/boards/{board['id']}/restore")

    def test_foreign_resources_are_unavailable(self):
        self.login('alice')
        board = self.client.post('/boards', json={'name': 'Private'}).json()
        task = self.client.post(f"/boards/{board['id']}/tasks", json={'title': 'Secret'}).json()
        self.client.cookies.clear(); self.client.headers.pop('X-CSRF-Token', None); self.login('bob')
        self.assertEqual(self.client.get(f"/boards/{board['id']}").status_code, 404)
        self.assertEqual(self.client.get(f"/boards/{board['id']}/tasks/{task['id']}").status_code, 404)
        self.assertEqual(self.client.get('/search/tasks?q=secret').json(), [])

    def test_stale_write_and_deleted_task_cannot_be_resurrected(self):
        self.login('alice')
        board = self.client.post('/boards', json={'name': 'Conflicts'}).json()
        task = self.client.post(f"/boards/{board['id']}/tasks", json={'title': 'Draft'}).json()
        newer = self.client.patch(f"/boards/{board['id']}/tasks/{task['id']}", json={'title': 'Newer', 'description': '', 'status': 'todo', 'version': 1}).json()
        stale = self.client.patch(f"/boards/{board['id']}/tasks/{task['id']}", json={'title': 'Stale', 'description': '', 'status': 'todo', 'version': 1})
        self.assertEqual(stale.status_code, 409); self.assertEqual(stale.json()['latest']['title'], newer['title'])
        self.assertEqual(self.client.delete(f"/boards/{board['id']}/tasks/{task['id']}?version=2").status_code, 204)
        self.assertEqual(self.client.patch(f"/boards/{board['id']}/tasks/{task['id']}", json={'title': 'Resurrect', 'description': '', 'status': 'todo', 'version': 2}).status_code, 404)

    def test_validation_and_csrf(self):
        self.login('alice')
        self.assertEqual(self.client.post('/boards', json={'name': '   '}).status_code, 400)
        self.assertEqual(self.client.post('/boards', json={'name': 'No CSRF'}, headers={'X-CSRF-Token': 'wrong'}).status_code, 403)

    def test_boards_and_tasks_survive_store_restart(self):
        self.login('alice')
        board = self.client.post('/boards', json={'name': 'Saved'}).json()
        task = self.client.post(f"/boards/{board['id']}/tasks", json={'title': 'Remember me'}).json()
        store.configure(self.db.name)
        self.client.cookies.clear(); self.client.headers.pop('X-CSRF-Token', None); self.login('alice')
        loaded = self.client.get(f"/boards/{board['id']}").json()
        self.assertEqual(loaded['name'], 'Saved')
        self.assertEqual(loaded['tasks'][0]['id'], task['id'])

    def test_competing_writes_accept_only_one_matching_version(self):
        self.login('alice')
        board = self.client.post('/boards', json={'name': 'Concurrent'}).json()
        task = self.client.post(f"/boards/{board['id']}/tasks", json={'title': 'Original'}).json()
        cookies = dict(self.client.cookies); headers = {'X-CSRF-Token': cookies[CSRF_COOKIE]}

        def write(title):
            client = TestClient(app); client.cookies.update(cookies); client.headers.update(headers)
            return client.patch(f"/boards/{board['id']}/tasks/{task['id']}", json={'title': title, 'description': '', 'status': 'todo', 'version': 1}).status_code

        with ThreadPoolExecutor(max_workers=2) as pool:
            statuses = sorted(pool.map(write, ('First', 'Second')))
        self.assertEqual(statuses, [200, 409])


if __name__ == '__main__':
    unittest.main()
