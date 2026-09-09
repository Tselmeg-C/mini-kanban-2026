import test, { before, after } from 'node:test';
import assert from 'node:assert/strict';
import { chromium } from 'playwright';
import { spawn } from 'node:child_process';

let server, browser, page;
const waitFor = async check => { for (let i = 0; i < 20; i++) { if (await check()) return; await new Promise(resolve => setTimeout(resolve, 100)); } assert.fail('Timed out waiting for browser state'); };
before(async () => { server = spawn('python3', ['-m', 'http.server', '4173'], { stdio: 'ignore' }); await new Promise(resolve => setTimeout(resolve, 300)); browser = await chromium.launch({ headless: true }); page = await browser.newPage(); page.on('pageerror', error => console.error('PAGEERROR', error.message)); await page.goto('http://127.0.0.1:4173/'); });
after(async () => { await browser?.close(); server?.kill(); });

test('core mock journey works in Chromium', { concurrency: false }, async () => {
  await page.getByRole('button', { name: /Continue with local session/ }).click(); await page.getByRole('button', { name: 'Personal' }).click();
  await page.getByLabel('Task title').fill('Browser QA task'); await page.getByRole('button', { name: 'Create in To Do' }).click(); await waitFor(() => page.getByText('Browser QA task').count().then(Boolean));
  await page.locator('.task-open[data-task="t4"]').click(); assert.equal(await page.locator('#panel').evaluate(element => element.open), true); await page.getByLabel('Title', { exact: true }).fill('Browser QA edited'); await page.getByRole('button', { name: 'Save' }).click(); await waitFor(() => page.getByText('Browser QA edited').count().then(Boolean));
  await page.getByLabel('Search tasks').fill('edited'); await page.getByRole('button', { name: 'Search' }).click(); await waitFor(() => page.getByText(/Browser QA edited — Personal/).count().then(Boolean));
  await page.locator('.task-open[data-task="t4"]').click(); await page.getByLabel('Title', { exact: true }).fill('Unsaved draft'); page.once('dialog', dialog => dialog.dismiss()); await page.getByRole('button', { name: 'Cancel' }).click(); assert.equal(await page.locator('#panel').evaluate(element => element.open), true); page.once('dialog', dialog => dialog.accept()); await page.getByRole('button', { name: 'Cancel' }).click(); await waitFor(() => page.locator('#panel').evaluate(element => !element.open));
  await page.locator('.task-open[data-task="t4"]').click(); await page.getByLabel('Status').selectOption('done'); await page.getByRole('button', { name: 'Save' }).click(); await waitFor(() => page.locator('.column[data-status="done"] [data-task="t4"]').count().then(Boolean));
  await page.locator('.task-open[data-task="t4"]').click(); page.once('dialog', dialog => dialog.accept()); await page.getByRole('button', { name: 'Delete permanently' }).click(); await waitFor(() => page.locator('.task-open[data-task="t4"]').count().then(count => count === 0));
});

test('archive and restore remain visible', { concurrency: false }, async () => {
  await page.locator('[data-archive="b1"]').click(); await waitFor(() => page.locator('[data-board="b1"]').count().then(count => count === 0)); await page.getByRole('button', { name: 'Archived' }).click(); await waitFor(() => page.locator('[data-board="b1"]').count().then(Boolean)); assert.equal(await page.locator('[data-board="b1"]').count(), 1);
  await page.locator('[data-archive="b1"]').click(); await waitFor(() => page.getByRole('button', { name: 'Active' }).count().then(Boolean)); await page.getByRole('button', { name: 'Active' }).click(); await waitFor(() => page.locator('[data-board="b1"]').count().then(Boolean)); assert.equal(await page.locator('[data-board="b1"]').count(), 1);
});

test('keyboard controls and long content remain reachable', { concurrency: false }, async () => {
  await page.locator('[data-board="b1"]').click();
  const title = 'L'.repeat(120); const description = 'Long content '.repeat(350);
  await page.getByLabel('Task title').fill(title); await page.getByLabel('Description (optional)').fill(description);
  await page.getByRole('button', { name: 'Create in To Do' }).click(); await waitFor(() => page.getByText(title).count().then(Boolean));
  const task = page.locator('.task-open').filter({ hasText: title }); await task.focus(); await task.press('Enter');
  assert.equal(await page.locator('#panel').evaluate(element => element.open), true);
  await page.getByLabel('Status').selectOption('doing'); await page.getByRole('button', { name: 'Save' }).click();
  await waitFor(() => page.locator('.column[data-status="doing"] .task-open').filter({ hasText: title }).count().then(Boolean));
  assert.equal(await page.locator('body').evaluate(element => element.scrollWidth <= document.documentElement.clientWidth), true);
});
