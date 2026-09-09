import test, { before, after } from 'node:test';
import assert from 'node:assert/strict';
import { chromium } from 'playwright';
import { spawn } from 'node:child_process';

let server, browser, page;
before(async () => { server = spawn('python3', ['-m', 'http.server', '4173'], { stdio: 'ignore' }); await new Promise(resolve => setTimeout(resolve, 300)); browser = await chromium.launch({ headless: true }); page = await browser.newPage({ viewport: { width: 1440, height: 1000 } }); await page.goto('http://127.0.0.1:4173/'); });
after(async () => { await browser?.close(); server?.kill(); });

test('rendered layout remains reachable at the 20-board by 200-task target', { concurrency: false }, async () => {
  await page.getByRole('button', { name: /Continue with local session/ }).click();
  await page.evaluate(() => {
    const boards = document.querySelector('#boards');
    boards.innerHTML = Array.from({ length: 20 }, (_, index) => `<li><button class="board-link">Scale board ${index}</button></li>`).join('');
    const long = 'Long task content '.repeat(30);
    document.querySelector('#board').hidden = false;
    document.querySelector('#board-title').textContent = 'Scale board 19';
    document.querySelector('#columns').innerHTML = ['todo', 'doing', 'done'].map(status => `<section class="column" data-status="${status}"><h3>${status}</h3>${Array.from({ length: status === 'todo' ? 200 : 0 }, (_, index) => `<article class="task"><button class="task-open"><strong>Scale task ${index}</strong><span>${long}</span></button></article>`).join('')}</section>`).join('');
  });
  assert.equal(await page.locator('[data-status="todo"] .task-open').count(), 200);
  assert.equal(await page.locator('.board-link').count(), 20);
  assert.equal(await page.locator('body').evaluate(element => element.scrollWidth <= document.documentElement.clientWidth), true);
  assert.ok(await page.getByText('Scale task 199').count());
});
