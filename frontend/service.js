export const STATUSES = ['todo', 'doing', 'done'];
export const STATUS_LABELS = { todo: 'To Do', doing: 'In Progress', done: 'Done' };

export class ServiceError extends Error {
  constructor(code, message, details = {}) { super(message); this.code = code; Object.assign(this, details); }
}

const copy = value => structuredClone(value);
const clean = value => String(value ?? '').trim();
const validText = (value, label, max) => {
  const result = clean(value);
  if (!result || result.length > max) throw new ServiceError('validation', `${label} must be 1-${max} characters.`);
  return result;
};

export class MockKanbanService {
  constructor(seed = true) {
    this.session = null; this.failures = new Map(); this.nextBoard = 3; this.nextTask = 4;
    this.boards = seed ? [
      { id: 'b1', name: 'Personal', archived: false, openedAt: 3, tasks: [
        { id: 't1', title: 'Plan the week', description: 'Write down the next small steps.', status: 'todo', createdAt: 1, version: 1 },
        { id: 't2', title: 'Ship first draft', description: 'Keep the scope small.', status: 'doing', createdAt: 2, version: 1 }
      ] },
      { id: 'b2', name: 'Archive example', archived: true, openedAt: 1, tasks: [
        { id: 't3', title: 'Old notes', description: 'Search should include archived boards.', status: 'done', createdAt: 3, version: 1 }
      ] }
    ] : [];
  }
  async _run(name, action) {
    await new Promise(resolve => setTimeout(resolve, 15));
    const failure = this.failures.get(name); if (failure) { this.failures.delete(name); throw failure; }
    if (!this.session) throw new ServiceError('expired', 'Your mock session has expired. Sign in again.');
    return copy(action());
  }
  setFailure(name, error = new ServiceError('network', 'The mock network request failed.')) { this.failures.set(name, error); }
  async signIn() { await new Promise(resolve => setTimeout(resolve, 15)); this.session = { name: 'Demo user', email: 'demo@example.test' }; return copy(this.session); }
  async signOut() { this.session = null; }
  async currentSession() { return this.session ? copy(this.session) : null; }
  async listBoards() { return this._run('listBoards', () => this.boards.slice().sort((a, b) => b.openedAt - a.openedAt || a.id.localeCompare(b.id)).map(({ tasks, ...board }) => ({ ...board, taskCount: tasks.length }))); }
  async getBoard(id) { return this._run('getBoard', () => { const board = this.boards.find(item => item.id === id); if (!board) throw new ServiceError('unavailable', 'Board is unavailable.'); return board; }); }
  async createBoard(name) { return this._run('createBoard', () => { const board = { id: `b${this.nextBoard++}`, name: validText(name, 'Board name', 120), archived: false, openedAt: Date.now(), tasks: [] }; this.boards.push(board); return board; }); }
  async renameBoard(id, name) { return this._run('renameBoard', () => { const board = this._board(id); board.name = validText(name, 'Board name', 120); return board; }); }
  async openBoard(id) { return this._run('openBoard', () => { const board = this._board(id); board.openedAt = Date.now(); return board; }); }
  async archiveBoard(id) { return this._run('archiveBoard', () => { const board = this._board(id); board.archived = true; return board; }); }
  async restoreBoard(id) { return this._run('restoreBoard', () => { const board = this._board(id); board.archived = false; board.openedAt = Date.now(); return board; }); }
  async listTasks(boardId) { return this._run('listTasks', () => this._board(boardId).tasks.slice().sort((a, b) => a.createdAt - b.createdAt || a.id.localeCompare(b.id))); }
  async createTask(boardId, title, description = '') { return this._run('createTask', () => { const task = { id: `t${this.nextTask++}`, title: validText(title, 'Task title', 120), description: String(description ?? '').slice(0, 5000), status: 'todo', createdAt: Date.now(), version: 1 }; this._board(boardId).tasks.push(task); return task; }); }
  async updateTask(boardId, taskId, input, version) { return this._run('updateTask', () => { const task = this._task(boardId, taskId); this._checkVersion(task, version); task.title = validText(input.title, 'Task title', 120); task.description = String(input.description ?? ''); if (task.description.length > 5000) throw new ServiceError('validation', 'Description must be at most 5000 characters.'); task.status = this._status(input.status); task.version++; return task; }); }
  async moveTask(boardId, taskId, status, version) { return this._run('moveTask', () => { const task = this._task(boardId, taskId); this._checkVersion(task, version); task.status = this._status(status); task.version++; return task; }); }
  async deleteTask(boardId, taskId, version) { return this._run('deleteTask', () => { const board = this._board(boardId); const task = this._task(boardId, taskId); this._checkVersion(task, version); board.tasks = board.tasks.filter(item => item.id !== taskId); return { id: taskId }; }); }
  async search(query) { return this._run('search', () => { const needle = clean(query).toLocaleLowerCase(); if (!needle) return []; return this.boards.flatMap(board => board.tasks.filter(task => `${task.title} ${task.description}`.toLocaleLowerCase().includes(needle)).map(task => ({ ...task, boardId: board.id, boardName: board.name, archived: board.archived }))).sort((a, b) => b.createdAt - a.createdAt || a.id.localeCompare(b.id)); }); }
  _board(id) { const board = this.boards.find(item => item.id === id); if (!board) throw new ServiceError('unavailable', 'Board is unavailable.'); return board; }
  _task(boardId, id) { const task = this._board(boardId).tasks.find(item => item.id === id); if (!task) throw new ServiceError('unavailable', 'Task is unavailable.'); return task; }
  _checkVersion(task, version) { if (version !== task.version) throw new ServiceError('conflict', 'This task changed. Review the latest saved version.', { latest: task }); }
  _status(status) { if (!STATUSES.includes(status)) throw new ServiceError('validation', 'Choose a valid status.'); return status; }
}
