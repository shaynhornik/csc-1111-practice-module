const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1300, height: 900 } });
  const errs = []; p.on('pageerror', e => errs.push('PAGEERROR ' + e.message)); p.on('console', m => { if (m.type() === 'error') errs.push('CONSOLE ' + m.text()); });
  await p.goto('file://' + process.argv[2]);
  console.log('loaded', JSON.stringify(await p.evaluate(() => window.__course)));
  const units = await p.$$eval('nav button[data-r="unit"]', bs => bs.map(b => b.getAttribute('data-u')));
  let lessons = 0, wide = 0;
  for (const u of units) {
    await p.click(`nav button[data-u="${u}"]`);
    const ls = await p.$$eval('button[data-l]', bs => bs.map(b => b.getAttribute('data-l')));
    for (const l of ls) { await p.click(`nav button[data-u="${u}"]`); await p.click(`button[data-l="${l}"]`); lessons++;
      const w = await p.evaluate(() => document.documentElement.scrollWidth > window.innerWidth + 2); if (w) { wide++; console.log('page wider than window on lesson', l); } }
  }
  console.log('lessons opened', lessons, 'too wide', wide);
  // run through every question of every unit once, answering first option / typing junk, to catch render errors
  let asked = 0;
  for (const u of units) {
    await p.click(`nav button[data-u="${u}"]`); await p.click('#all');
    for (let guard = 0; guard < 400; guard++) {
      if (await p.$('#cont')) break; // session finished screen
      if (await p.$('.choice')) await p.click('.choice'); else { await p.fill('#inp', 'zz'); await p.click('#chk'); }
      asked++;
      const nxt = await p.$('#next'); if (!nxt) { console.log('NO NEXT in', u); break; }
      // second pass answers: after a miss the question comes back; end the session once every question was shown once
      const doneTxt = await p.textContent('.qmeta'); 
      await p.click('#next');
      if (guard > 120) { await p.click('#quit'); break; }
    }
    if (await p.$('#quit')) await p.click('#quit');
  }
  console.log('question renders', asked);
  await p.click('nav button[data-r="programs"]'); console.log('program cards', await p.$$eval('details', d => d.length));
  await p.click('nav button[data-r="home"]'); await p.screenshot({ path: (process.argv[3] || "dashboard.png"), fullPage: false });
  console.log(errs.length ? errs.slice(0, 8).join('\n') : 'no page errors');
  await b.close();
})().catch(e => { console.log('TEST FAIL', e.message.slice(0, 400)); process.exit(1); });
