import test from 'node:test';
import assert from 'node:assert/strict';
import { ApiService } from '../api-service.js';

test('API service uses the contract paths and maps API errors', async () => {
  const calls = [];
  globalThis.document = { cookie: 'tidyboard_csrf=token' };
  globalThis.fetch = async (url, options) => { calls.push([url, options]); return { ok: false, status: 409, json: async () => ({ code: 'conflict', message: 'Changed', latest: { id: 't1' } }) }; };
  await assert.rejects(() => new ApiService('http://api').updateTask('b1', 't1', { title: 'x', description: '', status: 'todo' }, 1), error => error.code === 'conflict' && error.latest.id === 't1');
  assert.equal(calls[0][0], 'http://api/boards/b1/tasks/t1'); assert.equal(calls[0][1].headers['X-CSRF-Token'], 'token');
});
