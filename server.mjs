/** Local-only, dependency-free drafting bridge. Never deploy this process on a public interface. */
import http from 'node:http';
import { readFile, realpath } from 'node:fs/promises';
import { randomBytes, timingSafeEqual } from 'node:crypto';
import { dirname, resolve, extname, sep } from 'node:path';
import { fileURLToPath } from 'node:url';
import { validateSkill, text, safeUrl, normalizeResult, makeHandoff, SYSTEM_PROMPT } from './shared/core.mjs';
const ROOT=dirname(fileURLToPath(import.meta.url));
const PROVIDER_ENV={chatgpt:['OPENAI_API_KEY','OPENAI_MODEL'],claude:['ANTHROPIC_API_KEY','ANTHROPIC_MODEL'],gemini:['GEMINI_API_KEY','GEMINI_MODEL']};
const MIME={'.html':'text/html; charset=utf-8','.mjs':'text/javascript; charset=utf-8','.css':'text/css; charset=utf-8','.svg':'image/svg+xml','.webp':'image/webp','.png':'image/png','.json':'application/json','.md':'text/plain; charset=utf-8'};
const allowedFile=/^(index\.html|shared\/(app\.mjs|core\.mjs|styles\.css|landing\.css|favicon\.svg)|(?:chatgpt|claude|gemini)\/(index\.html|SKILL\.md|assets\/(hero\.webp|board\.png)))$/;
class HttpError extends Error { constructor(status,message){super(message);this.status=status;} }
export function configuration(env=process.env){return Object.fromEntries(Object.entries(PROVIDER_ENV).map(([id,[key,model]])=>[id,{configured:!!(env[key]?.trim()&&env[model]?.trim()),model:env[model]?.trim()||''}]));}
function tokenMatches(a,b){return typeof a==='string'&&Buffer.byteLength(a)===Buffer.byteLength(b)&&timingSafeEqual(Buffer.from(a),Buffer.from(b));}
async function limitedJSON(stream,max){const chunks=[];let size=0;for await(const chunk of stream){size+=chunk.byteLength;if(size>max)throw new HttpError(413,'Request or response is too large.');chunks.push(Buffer.from(chunk));}try{return JSON.parse(Buffer.concat(chunks).toString('utf8'));}catch{throw new HttpError(400,'Expected complete, valid JSON.');}}
export function validateRequest(raw){
 if(!raw||!Object.hasOwn(PROVIDER_ENV,raw.edition))throw new HttpError(400,'Choose ChatGPT, Claude, or Gemini.');
 const skill=validateSkill(raw.skill), t=raw.task;
 if(!t||t.sensitivity!=='shareable')throw new HttpError(403,'Only a source you marked shareable can be sent.');
 if(t.skillId!==skill.id||!['ready','awaiting','blocked'].includes(t.status))throw new HttpError(400,'Task must be routed and ready for preparation.');
 const task={id:text(t.id,'Task ID',100,true),title:text(t.title,'Title',140,true),body:text(t.body,'Source',12000,true),source:text(t.source,'Source label',120,true),sourceUrl:safeUrl(t.sourceUrl),skillId:skill.id,steering:text(t.steering??'','Steering',2000)};
 return {edition:raw.edition,skill,task};
}
/** An injected fetch lets tests verify all three wire contracts without provider charges. */
export async function draftWithProvider(raw,{env=process.env,fetchImpl=fetch,signal}={}){
 const {edition,task,skill}=validateRequest(raw),[keyName,modelName]=PROVIDER_ENV[edition],key=env[keyName]?.trim(),model=env[modelName]?.trim();
 if(!key||!model)throw new HttpError(503,'This provider is not configured. Set its server API key and model, or use companion mode.');
 if(!/^[a-zA-Z0-9._:/-]{1,160}$/.test(model))throw new HttpError(503,'The configured model identifier is invalid.');
 const prompt=makeHandoff(task,skill),headers={'Content-Type':'application/json'};let url,body;
 if(edition==='chatgpt'){url='https://api.openai.com/v1/responses';headers.Authorization=`Bearer ${key}`;body={model,instructions:SYSTEM_PROMPT,input:prompt,max_output_tokens:4096,store:false,tools:[]};}
 else if(edition==='claude'){url='https://api.anthropic.com/v1/messages';headers.Authorization=`Bearer ${key}`;headers['anthropic-version']='2023-06-01';if(env.ANTHROPIC_WORKSPACE_ID)headers['anthropic-workspace-id']=env.ANTHROPIC_WORKSPACE_ID;body={model,max_tokens:4096,system:SYSTEM_PROMPT,messages:[{role:'user',content:prompt}]};}
 else {url=`https://generativelanguage.googleapis.com/v1beta/models/${encodeURIComponent(model.replace(/^models\//,''))}:generateContent`;headers['x-goog-api-key']=key;body={systemInstruction:{parts:[{text:SYSTEM_PROMPT}]},contents:[{role:'user',parts:[{text:prompt}]}],generationConfig:{maxOutputTokens:4096,responseMimeType:'application/json'}};}
 let response;
 try{response=await fetchImpl(url,{method:'POST',headers,body:JSON.stringify(body),signal,redirect:'error'});}catch(e){if(signal?.aborted)throw new HttpError(504,'Request cancelled or timed out. A request already received may still be billed.');throw new HttpError(502,'Could not reach the provider. Check your connection and server configuration. No automatic retry was made.');}
 if(!response.ok){await response.body?.cancel();const status=response.status;throw new HttpError(status===429?429:502,status===429?'Provider rate limit reached. Wait before making a new request.':status===401||status===403?'Provider authorization failed. Check the server key, workspace, and model access.':`Provider returned HTTP ${status}. No automatic retry was made.`);}
 let data;try{data=await limitedJSON(response.body,1000000);}catch{throw new HttpError(502,'Provider returned an invalid or oversized response. No draft was saved.');}
 let output='';
 if(edition==='chatgpt'){
  if(data.status!=='completed'||data.error)throw new HttpError(502,'Provider did not finish the draft. Try a shorter source or a different configured model.');
  output=(data.output??[]).filter(x=>x.type==='message').flatMap(x=>x.content??[]).filter(x=>x.type==='output_text').map(x=>x.text).join('\n');
 }else if(edition==='claude'){
  if(data.stop_reason!=='end_turn'&&data.stop_reason!=='stop_sequence')throw new HttpError(502,'Provider stopped before a complete draft. No partial result was approved.');
  output=(data.content??[]).filter(x=>x.type==='text').map(x=>x.text).join('\n');
 }else{
  const candidate=data.candidates?.[0];if(!candidate||candidate.finishReason!=='STOP')throw new HttpError(502,'Provider blocked or did not finish this draft. Review the source before retrying.');
  output=(candidate.content?.parts??[]).filter(x=>!x.thought&&typeof x.text==='string').map(x=>x.text).join('\n');
 }
 try{return {result:normalizeResult(output),model};}catch{throw new HttpError(502,'The provider response did not contain a usable complete draft. No result was saved.');}
}
export function createServer({root=ROOT,env=process.env,fetchImpl=fetch,deadlineMs=40000}={}){
 const csrf=randomBytes(32).toString('hex');let inFlight=false;
 const server=http.createServer(async(req,res)=>{
  const json=(status,body)=>{if(!res.destroyed){res.writeHead(status,{'Content-Type':'application/json; charset=utf-8','Cache-Control':'no-store'});res.end(JSON.stringify(body));}};
  res.setHeader('X-Content-Type-Options','nosniff');res.setHeader('Referrer-Policy','no-referrer');res.setHeader('Cross-Origin-Resource-Policy','same-origin');
  res.setHeader('Content-Security-Policy',"default-src 'self'; script-src 'self'; style-src 'self'; img-src 'self' data:; connect-src 'self'; frame-ancestors 'none'; base-uri 'none'; form-action 'self'");
  try{
   const port=server.address()?.port,hosts=[`127.0.0.1:${port}`,`localhost:${port}`],host=req.headers.host;
   if(!hosts.includes(host))throw new HttpError(403,'Local host required. This server must not be exposed publicly.');
   if(req.headers.origin && ![`http://127.0.0.1:${port}`,`http://localhost:${port}`].includes(req.headers.origin))throw new HttpError(403,'Cross-origin access is not allowed.');
   const path=new URL(req.url,`http://${host}`).pathname;
   if(path.startsWith('/api/')){
    if(req.headers['sec-fetch-site']==='cross-site')throw new HttpError(403,'Cross-site API access denied.');
    if(path==='/api/status'&&req.method==='GET'){json(200,{csrf,providers:configuration(env),mode:'local-only'});return;}
    if(path!=='/api/generate')throw new HttpError(404,'API route not found.');
    if(req.method!=='POST')throw new HttpError(405,'Use an explicit POST request.');
    if(!tokenMatches(req.headers['x-switchboard-csrf'],csrf))throw new HttpError(403,'Refresh this local page before making an API request.');
    if(!/^application\/json(?:;|$)/i.test(req.headers['content-type']??''))throw new HttpError(415,'JSON content type required.');
    if(inFlight)throw new HttpError(409,'A request is already active. Wait or cancel it first.');
    const raw=await limitedJSON(req,100000);validateRequest(raw);
    if(inFlight)throw new HttpError(409,'A request is already active.');
    inFlight=true;const controller=new AbortController(),timer=setTimeout(()=>controller.abort(),deadlineMs);
    const cancel=()=>{if(!res.writableEnded)controller.abort();};res.once('close',cancel);
    try{const result=await draftWithProvider(raw,{env,fetchImpl,signal:controller.signal});json(200,result);}
    finally{clearTimeout(timer);res.off('close',cancel);inFlight=false;}return;
   }
   if(!['GET','HEAD'].includes(req.method))throw new HttpError(405,'Read-only static files.');
   let relative;try{relative=decodeURIComponent(path).replace(/^\//,'');}catch{throw new HttpError(400,'Invalid path.');}
   if(!relative||relative.endsWith('/'))relative+='index.html';
   if(!allowedFile.test(relative))throw new HttpError(404,'File not found.');
   const file=resolve(root,relative),realRoot=await realpath(root);let real;try{real=await realpath(file);}catch{throw new HttpError(404,'File not found.');}
   if(!real.startsWith(realRoot+sep))throw new HttpError(403,'Path not allowed.');
   const data=await readFile(real);res.writeHead(200,{'Content-Type':MIME[extname(file)]||'application/octet-stream','Cache-Control':'no-cache','Content-Length':data.length});res.end(req.method==='HEAD'?undefined:data);
  }catch(e){json(e.status||400,{error:e.status?e.message:'The request could not be accepted. Check its fields and try again.'});}
 });
 server.requestTimeout=15000;server.headersTimeout=10000;return server;
}
if(process.argv[1]&&resolve(process.argv[1])===fileURLToPath(import.meta.url)){
 try{process.loadEnvFile(resolve(ROOT,'.env'));}catch(e){if(e.code!=='ENOENT'){console.error('Could not read .env. Correct the file before starting.');process.exit(1);}}
 const port=Number(process.env.PORT||4173);if(!Number.isInteger(port)||port<1024||port>65535){console.error('PORT must be an integer from 1024 to 65535.');process.exit(1);}
 const server=createServer();server.on('error',e=>{console.error(e.code==='EADDRINUSE'?`Port ${port} is already in use. Set PORT to another local port.`:'Could not start the local server.');process.exitCode=1;});
 server.listen(port,'127.0.0.1',()=>console.log(`Skill Switchboard: http://127.0.0.1:${port}\nLocal companion mode is ready. No provider request has been made.`));
}
