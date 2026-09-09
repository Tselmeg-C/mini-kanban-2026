import unittest
from datetime import timedelta

from fastapi.testclient import TestClient

from app.main import CSRF_COOKIE, SESSION_COOKIE, app, now, store


class ApiTests(unittest.TestCase):
    def setUp(self):
        store.boards.clear(); store.sessions.clear(); store.next_board = 1; store.next_task = 1
        self.client = TestClient(app)

    def login(self, subject):
        token, csrf = store.create_session(subject, subject, f"{subject}@example.test")
        self.client.cookies.set(SESSION_COOKIE, token)
        self.client.cookies.set(CSRF_COOKIE, csrf)
        self.client.headers.update({"X-CSRF-Token": csrf})

    def test_auth_required_and_callback_rejected_without_credentials(self):
        self.assertEqual(self.client.get('/boards').status_code, 401)
        response = self.client.get('/auth/google/callback?code=x&state=y')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['code'], 'validation')

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


if __name__ == '__main__':
    unittest.main()
