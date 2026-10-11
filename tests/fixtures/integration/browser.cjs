// Optional viewer test; source is retained, dependencies are supplied explicitly.
const fs = require('fs').promises;
const path = require('path');
const http = require('http');
const {pathToFileURL} = require('url');
const options = {};
for (let i = 2; i < process.argv.length; i += 2) options[process.argv[i]] = process.argv[i + 1];
const root = path.resolve(options['--root']);
const modules = path.resolve(options['--modules']);
const output = path.resolve(options['--output']);
const {chromium} = require(path.join(modules, 'playwright'));
const mermaidURL = 'https://cdn.jsdelivr.net/npm/mermaid@12.1.0/dist/mermaid.esm.min.mjs';

(async () => {
  await fs.mkdir(output, {recursive: true});
  const {marked} = await import(pathToFileURL(path.join(modules, 'marked/lib/marked.esm.js')).href);
  const server = http.createServer(async (req, res) => {
    try {
      const relative = decodeURIComponent(new URL(req.url, 'http://127.0.0.1').pathname).replace(/^\/+/, '');
      const target = path.resolve(root, relative);
      if (!target.startsWith(root + path.sep)) {res.writeHead(403); res.end(); return;}
      const bytes = await fs.readFile(target);
      const extension = path.extname(target);
      if (extension === '.md') {
        res.writeHead(200, {'Content-Type': 'text/html; charset=utf-8'});
        res.end(`<!doctype html><html lang="en"><meta charset="utf-8"><title>Vault integration viewer</title>
          <style>body{max-width:1180px;margin:30px auto;padding:0 24px;font:17px/1.5 Arial}img,svg{max-width:100%;height:auto}.mermaid{padding:12px 0}</style>
          <main>${marked.parse(bytes.toString('utf8'))}</main><script type="module">
          try{for(const code of document.querySelectorAll('pre > code.language-mermaid')){
            const pre=code.parentElement;pre.className='mermaid';pre.textContent=code.textContent;}
            const {default:mermaid}=await import(${JSON.stringify(mermaidURL)});
            mermaid.initialize({startOnLoad:false,securityLevel:'strict',fontFamily:'Arial'});
            await document.fonts.ready;await mermaid.run({querySelector:'.mermaid'});
            window.proof={status:'rendered'};
          }catch(error){window.proof={status:'failed',message:String(error)};}</script></html>`);
      } else {
        res.writeHead(200, {'Content-Type': extension === '.svg' ? 'image/svg+xml' : 'text/plain; charset=utf-8'});
        res.end(bytes);
      }
    } catch (_) {res.writeHead(404); res.end('Missing fixture file');}
  });
  await new Promise(resolve => server.listen(0, '127.0.0.1', resolve));
  let browser;
  try {
    browser = await chromium.launch({executablePath: options['--browser'], headless: true});
    const page = await browser.newPage({viewport: {width: 1280, height: 1000}});
    const pageErrors = [];
    page.on('pageerror', error => pageErrors.push(String(error)));
    const origin = `http://127.0.0.1:${server.address().port}`;
    await page.goto(origin + '/media/workflow.md', {waitUntil: 'networkidle', timeout: 60000});
    await page.waitForFunction(() => window.proof, {timeout: 60000});
    const state = await page.evaluate(() => window.proof);
    if (state.status !== 'rendered') throw Error(state.message);
    const metrics = await page.evaluate(() => ({
      nodes: document.querySelectorAll('.mermaid svg g.node').length,
      edges: document.querySelectorAll('.mermaid svg path.flowchart-link').length,
      image: [...document.images].map(image => ({complete:image.complete,width:image.naturalWidth,height:image.naturalHeight})),
      links: [...document.querySelectorAll('a[href]')].map(a => a.getAttribute('href')),
      clipped: document.documentElement.scrollWidth > window.innerWidth
    }));
    if (metrics.nodes !== 7 || metrics.edges !== 7 || metrics.image.length !== 1 ||
        !metrics.image[0].complete || metrics.image[0].width !== 1100 || metrics.clipped || pageErrors.length) {
      throw Error('Diagram, fallback or clipping check failed: ' + JSON.stringify({metrics,pageErrors}));
    }
    for (const href of metrics.links) {
      const response = await page.request.get(new URL(href, page.url()).href);
      if (!response.ok()) throw Error('Relocated local link failed: ' + href);
    }
    await page.locator('main').screenshot({path:path.join(output,'workflow.png')});
    const result = {status:'passed',viewer:{node:process.version,browser:await browser.version(),
      playwright:require(path.join(modules,'playwright/package.json')).version,
      marked:require(path.join(modules,'marked/package.json')).version,mermaid:'12.1.0'},
      metrics,scope:'custom local Markdown viewer; Codex and GitHub rendering remain unchecked',
      dependency:'Mermaid loaded from pinned jsDelivr URL; network required',screenshot:'workflow.png'};
    await fs.writeFile(path.join(output,'result.json'),JSON.stringify(result,null,2)+'\n');
    console.log(JSON.stringify(result));
  } finally {
    if (browser) await browser.close();
    await new Promise(resolve => server.close(resolve));
  }
})().catch(error => {console.error(String(error));process.exitCode=1;});
