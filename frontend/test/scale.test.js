import test from 'node:test';
import assert from 'node:assert/strict';
import { MockKanbanService } from '../service.js';

test('mock workspace remains reachable at the 20 by 200 target', async () => {
  const service = new MockKanbanService(false); await service.signIn();
  const boards = [];
  for (let boardIndex = 0; boardIndex < 20; boardIndex += 1) {
    const board = await service.createBoard(`Scale board ${boardIndex}`); boards.push(board);
    await Promise.all(Array.from({ length: 200 }, (_, taskIndex) => service.createTask(board.id, `Task ${boardIndex}-${taskIndex}`, `Long detail ${'x'.repeat(80)}`)));
  }
  assert.equal((await service.listBoards()).length, 20);
  assert.equal((await service.listTasks(boards[19].id)).length, 200);
  assert.equal((await service.search('Task 19-199')).length, 1);
});
