/* One-time extraction of the reviewed prototype's content and original diagrams. */
const fs = require('node:fs');
const vm = require('node:vm');
const source = fs.readFileSync('research/previews/technology-route-discussion-2026-10-04/index.html', 'utf8');
const block = source.slice(source.indexOf('const sources='), source.indexOf("let current='drive'"));
const data = vm.runInNewContext(block + ';({sources,hands,chapters,diagrams})', Object.create(null));
fs.writeFileSync('research/route-preview-content.json', JSON.stringify(data, null, 2) + '\n');
fs.mkdirSync('website/docs/images/knowledge/routes', {recursive: true});
for (const [id, diagram] of Object.entries(data.diagrams)) {
  fs.writeFileSync(`website/docs/images/knowledge/routes/${id}.svg`, diagram.replace('<svg ', '<svg xmlns="http://www.w3.org/2000/svg" '));
}
