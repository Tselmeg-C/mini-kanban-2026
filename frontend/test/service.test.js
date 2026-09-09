import test from 'node:test';
import assert from 'node:assert/strict';
import { MockKanbanService } from '../service.js';

async function loggedIn(seed = true) { const service = new MockKanbanService(seed); await service.signIn(); return service; }
test('mock service creates, validates, edits, moves, searches, archives, and deletes', async () => {
  const service = await loggedIn(); const board = await service.createBoard('Work');
  await assert.rejects(() => service.createTask(board.id, '   '), { code: 'validation' });
  const task = await service.createTask(board.id, 'Write tests', 'Important notes');
  assert.equal(task.status, 'todo'); assert.equal((await service.search('IMPORTANT'))[0].id, task.id);
  const moved = await service.moveTask(board.id, task.id, 'done', task.version); assert.equal(moved.status, 'done');
  await service.archiveBoard(board.id); assert.equal((await service.listBoards()).find(item => item.id === board.id).archived, true);
  await service.restoreBoard(board.id); const edited = await service.updateTask(board.id, task.id, { ...moved, title: 'Updated' }, moved.version); assert.equal(edited.title, 'Updated');
  await service.deleteTask(board.id, task.id, edited.version); assert.equal((await service.search('Updated')).length, 0);
});
test('stale edits are rejected without overwriting saved data', async () => {
  const service = await loggedIn(); const board = await service.createBoard('Conflict'); const task = await service.createTask(board.id, 'Draft');
  const saved = await service.updateTask(board.id, task.id, { ...task, title: 'Newer' }, task.version);
  await assert.rejects(() => service.updateTask(board.id, task.id, { ...task, title: 'Stale' }, task.version), error => error.code === 'conflict' && error.latest.title === saved.title);
});
test('failed requests leave saved data unchanged and can be retried', async () => {
  const service = await loggedIn(); const board = await service.createBoard('Retry');
  service.setFailure('createTask'); await assert.rejects(() => service.createTask(board.id, 'Keep draft'), { code: 'network' });
  const task = await service.createTask(board.id, 'Keep draft'); assert.equal(task.title, 'Keep draft');
  service.setFailure('moveTask'); await assert.rejects(() => service.moveTask(board.id, task.id, 'done', task.version), { code: 'network' });
  assert.equal((await service.listTasks(board.id))[0].status, 'todo');
});
