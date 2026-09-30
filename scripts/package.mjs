/** Refresh the small downloadable bundles committed beside each edition. */
import {copyFile} from 'node:fs/promises';
import {resolve,dirname} from 'node:path';
import {fileURLToPath} from 'node:url';
const root=resolve(dirname(fileURLToPath(import.meta.url)),'..');
for(const edition of ['chatgpt','claude','gemini']){
 const file=`skill-switchboard-${edition}.zip`;
 await copyFile(resolve(root,'dist',file),resolve(root,edition,file));
 console.log(`Refreshed ${edition}/${file}`);
}
