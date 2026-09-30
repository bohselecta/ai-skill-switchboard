/** Repeatable, dependency-free static and single-file builds. No minifier or network fetches. */
import {readFile,writeFile,mkdir,rm,cp} from 'node:fs/promises';
import {resolve,dirname} from 'node:path';
import {fileURLToPath} from 'node:url';
import {createHash} from 'node:crypto';
import {zipStored} from './zip.mjs';
const root=resolve(dirname(fileURLToPath(import.meta.url)),'..'),out=resolve(root,'dist');
await rm(out,{recursive:true,force:true});await mkdir(out,{recursive:true});
for(const name of ['index.html','shared','chatgpt','claude','gemini'])await cp(resolve(root,name),resolve(out,name),{recursive:true});
const css=await readFile(resolve(root,'shared/styles.css'),'utf8'), core=await readFile(resolve(root,'shared/core.mjs'),'utf8'), app=await readFile(resolve(root,'shared/app.mjs'),'utf8'),favicon=await readFile(resolve(root,'shared/favicon.svg'));
const compiledCore=core.replace(/^export /gm,''),compiledApp=app.replace(/^import .*?;\n/,'');
if(/^import /m.test(compiledApp)||/^export /m.test(compiledCore))throw new Error('Unexpected module syntax; update the explicit bundle transform.');
const outputs=[];
for(const edition of ['chatgpt','claude','gemini']){
 const hero=await readFile(resolve(root,edition,'assets/hero.webp'));
 const art='data:image/webp;base64,'+hero.toString('base64');
 let js=compiledCore+'\n'+compiledApp.replaceAll('./assets/hero.webp',art).replace('href="../index.html"','href="https://github.com/bohselecta/ai-skill-switchboard"');
 let html=await readFile(resolve(root,edition,'index.html'),'utf8');
 html=html.replace('<link rel="stylesheet" href="../shared/styles.css">',`<style>${css}</style>`).replace('href="../shared/favicon.svg"',`href="data:image/svg+xml;base64,${favicon.toString('base64')}"`).replace('<script type="module" src="../shared/app.mjs"></script>',`<script>\n(()=>{\n${js.replace(/<\/script/gi,'<\\/script')}\n})();\n</script>`);
 const filename=`skill-switchboard-${edition}.html`;await writeFile(resolve(out,filename),html);
 outputs.push({file:filename,bytes:Buffer.byteLength(html),sha256:createHash('sha256').update(html).digest('hex')});
 const prefix=`skill-switchboard-${edition}`;
 const zip=zipStored([[`${prefix}/SKILL.md`,await readFile(resolve(root,edition,'SKILL.md'))],[`${prefix}/references/companion.html`,html],[`${prefix}/references/result.schema.json`,await readFile(resolve(root,'contracts/result.schema.json'))],[`${prefix}/LICENSE`,await readFile(resolve(root,edition,'LICENSE'))],[`${prefix}/PERMISSION-GRANT.md`,await readFile(resolve(root,edition,'PERMISSION-GRANT.md'))]]);
 await writeFile(resolve(out,`${prefix}.zip`),zip);
 outputs.push({file:`${prefix}.zip`,bytes:zip.length,sha256:createHash('sha256').update(zip).digest('hex')});
}
await writeFile(resolve(out,'build-manifest.json'),JSON.stringify({version:'1.0.0',outputs},null,2)+'\n');
console.log('Built static site and three self-contained companion files. No credentials or provider calls.');for(const output of outputs)console.log(`${output.file}: ${Math.ceil(output.bytes/1024)} KiB`);
