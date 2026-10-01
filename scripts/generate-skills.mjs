import {mkdir, readFile, writeFile} from 'node:fs/promises';
import {join} from 'node:path';
import {fileURLToPath} from 'node:url';
import {CATALOG} from '../shared/core.mjs';

const ROOT=fileURLToPath(new URL('..',import.meta.url));
const CHECK=process.argv.includes('--check');
const slug=value=>value.toLowerCase().replace(/[^a-z0-9]+/g,'-').replace(/^-|-$/g,'');
const render=skill=>`---
name: ${slug(skill.name)}
description: ${skill.description}
---

# ${skill.name}

A provider-neutral Skill Switchboard capability. **Tasks move to this skill; the skill stays stable.**

## Use when

${skill.useWhen}

## Do not use when

${skill.doNotUseWhen}

## Helpful inputs

${skill.requiredInputs.length?skill.requiredInputs.map(x=>`- ${x}`).join('\n'):'- The task source supplied by the user.'}

## Output contract

${skill.outputContract}

## Instructions

${skill.instructions}

## Effect boundary

\`${skill.effectClass}\`. ${skill.negativeScope}

This skill prepares work only. It grants no connector, tool, credential, spending, deployment, or external-action permission. Human approval applies to the exact draft revision, not to a future action.
`;

let stale=[];
for(const skill of CATALOG){
  const dir=join(ROOT,'skills',skill.id), path=join(dir,'SKILL.md'), content=render(skill);
  if(CHECK){
    let actual='';try{actual=await readFile(path,'utf8');}catch{}
    if(actual!==content)stale.push(path);
  }else{
    await mkdir(dir,{recursive:true});await writeFile(path,content);
  }
}
if(CHECK&&stale.length){
  console.error('Canonical skill library is stale:\n'+stale.join('\n'));
  process.exit(1);
}
if(!CHECK)console.log(`Generated ${CATALOG.length} canonical skills.`);
