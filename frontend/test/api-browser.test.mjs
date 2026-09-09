import test, { before, after } from 'node:test';
import assert from 'node:assert/strict';
import { chromium } from 'playwright';
import { spawn } from 'node:child_process';

let backend, frontend, browser, page;
const waitFor = async check => { for (let i = 0; i < 40; i++) { if (await check()) return; await new Promise(resolve => setTimeout(resolve, 100)); } assert.fail('Timed out waiting for integration state'); };
before(async () => {
  backend = spawn('uv', ['run', 'uvicorn', 'app.main:app', '--host', '127.0.0.1', '--port', '8000'], { cwd: '../backend', env: { ...process.env, AUTH_DISABLED: '1' }, stdio: 'ignore' });
  frontend = spawn('python3', ['-m', 'http.server', '4173'], { cwd: '.', stdio: 'ignore' });
  for (let i = 0; i < 40; i++) { try { if ((await fetch('http://127.0.0.1:8000/openapi.json')).ok) break; } catch {} await new Promise(resolve => setTimeout(resolve, 100)); }
  browser = await chromium.launch({ headless: true }); page = await browser.newPage(); await page.goto('http://localhost:4173/?api=1');
});
after(async () => { await browser?.close(); frontend?.kill(); backend?.kill(); });

test('real API client completes a local board and task flow', { concurrency: false }, async () => {
  await page.getByRole('button', { name: /Continue with Google/ }).click(); page.once('dialog', dialog => dialog.accept('API Board')); await page.getByRole('button', { name: 'New board' }).click(); await waitFor(() => page.locator('[data-board]').count().then(Boolean));
  await page.locator('[data-board]').click(); await page.getByLabel('Task title').fill('API task'); await page.getByRole('button', { name: 'Create in To Do' }).click(); await waitFor(() => page.getByText('API task').count().then(Boolean));
  await page.getByLabel('Search tasks').fill('API task'); await page.getByRole('button', { name: 'Search' }).click(); await waitFor(() => page.getByText(/API task — API Board/).count().then(Boolean));
  const second = await browser.newPage(); await second.goto('http://localhost:4173/?api=1'); await second.getByRole('button', { name: /Continue with Google/ }).click(); await waitFor(() => second.locator('[data-board]').count().then(Boolean)); await second.locator('[data-board]').click(); await second.getByLabel('Task title').fill('Second session task'); await second.getByRole('button', { name: 'Create in To Do' }).click(); await waitFor(() => second.getByText('Second session task').count().then(Boolean)); await waitFor(() => page.getByText('Second session task').count().then(Boolean)); await second.close();
});
