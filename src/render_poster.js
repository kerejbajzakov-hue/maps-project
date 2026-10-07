// Рендер постера в PNG высокого разрешения (нужен Playwright: npm i playwright)
const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1587, height: 1123 }, deviceScaleFactor: 4 });
  await p.goto('file://' + process.cwd() + '/poster_clay.html');
  await p.waitForTimeout(1000);
  await p.screenshot({ path: 'poster_hi.png' });
  await b.close();
})();
