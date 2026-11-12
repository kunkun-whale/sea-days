// 把一页 HTML 渲染成一张长图。用法：node 长图.mjs 输入.html 输出.png [宽度]
import { chromium } from 'playwright-core';

const [src, out, widthArg] = process.argv.slice(2);
if (!src || !out) { console.log('用法: node 长图.mjs 输入.html 输出.png [宽度]'); process.exit(2); }
const width = Number(widthArg) || 1000;

const browser = await chromium.launch({
  executablePath: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
});
const page = await browser.newPage({ viewport: { width, height: 900 }, deviceScaleFactor: 2 });
await page.goto('file://' + (src.startsWith('/') ? src : process.cwd() + '/' + src), { waitUntil: 'load' });
await page.waitForTimeout(800);
const h = await page.evaluate(() => document.body.scrollHeight);
await page.setViewportSize({ width, height: Math.min(h, 20000) });
await page.waitForTimeout(400);
await page.screenshot({ path: out, fullPage: true });
console.log(`${out}  宽 ${width}，高 ${h}`);
await browser.close();
