import { ServiceError } from './service.js';

export class ApiService {
  constructor(base = 'http://localhost:8000') { this.base = base.replace(/\/$/, ''); }
  async request(path, options = {}) {
    const response = await fetch(`${this.base}${path}`, { credentials: 'include', ...options, headers: { 'Content-Type': 'application/json', ...this.csrf(), ...options.headers } });
    if (response.status === 204) return null;
    const body = await response.json().catch(() => ({}));
    if (!response.ok) throw new ServiceError(body.code || 'network', body.message || 'The API request failed.', { latest: body.latest });
    return body;
  }
  csrf() { const match = document.cookie.match(/(?:^|; )tidyboard_csrf=([^;]*)/); return match ? { 'X-CSRF-Token': decodeURIComponent(match[1]) } : {}; }
  signIn() { return this.request('/dev/session', { method: 'POST' }); }
  signOut() { return this.request('/session', { method: 'DELETE' }); }
  currentSession() { return this.request('/session').catch(error => error.code === 'unauthenticated' ? null : Promise.reject(error)); }
  listBoards() { return this.request('/boards?includeArchived=true'); }
  getBoard(id) { return this.request(`/boards/${id}`); }
  createBoard(name) { return this.request('/boards', { method: 'POST', body: JSON.stringify({ name }) }); }
  renameBoard(id, name) { return this.request(`/boards/${id}`, { method: 'PATCH', body: JSON.stringify({ name }) }); }
  openBoard(id) { return this.request(`/boards/${id}/open`, { method: 'POST' }); }
  archiveBoard(id) { return this.request(`/boards/${id}/archive`, { method: 'POST' }); }
  restoreBoard(id) { return this.request(`/boards/${id}/restore`, { method: 'POST' }); }
  listTasks(boardId) { return this.request(`/boards/${boardId}/tasks`); }
  createTask(boardId, title, description = '') { return this.request(`/boards/${boardId}/tasks`, { method: 'POST', body: JSON.stringify({ title, description }) }); }
  updateTask(boardId, taskId, input, version) { return this.request(`/boards/${boardId}/tasks/${taskId}`, { method: 'PATCH', body: JSON.stringify({ ...input, version }) }); }
  moveTask(boardId, taskId, status, version) { return this.request(`/boards/${boardId}/tasks/${taskId}/status`, { method: 'PATCH', body: JSON.stringify({ status, version }) }); }
  deleteTask(boardId, taskId, version) { return this.request(`/boards/${boardId}/tasks/${taskId}?version=${version}`, { method: 'DELETE' }); }
  search(query) { return this.request(`/search/tasks?q=${encodeURIComponent(query)}&pageSize=100`); }
}
