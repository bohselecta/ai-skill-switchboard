/** Minimal ZIP-store writer: deterministic UTF-8 paths, no compression/dependencies. */
export function zipStored(entries) {
 const table=Array.from({length:256},(_,n)=>{for(let i=0;i<8;i++)n=n&1?0xedb88320^(n>>>1):n>>>1;return n>>>0;});
 const crc=b=>{let c=0xffffffff;for(const n of b)c=table[(c^n)&255]^(c>>>8);return (c^0xffffffff)>>>0;};
 const chunks=[],central=[];let offset=0;
 for(const [name,value] of entries){
  if(name.startsWith('/')||name.split('/').some(p=>p==='..'||p==='')||name.includes('\\'))throw new Error('Unsafe archive path.');
  const path=Buffer.from(name),data=Buffer.isBuffer(value)?value:Buffer.from(value),sum=crc(data);
  if(data.length>0xffffffff||path.length>65535)throw new Error('Archive entry too large.');
  const h=Buffer.alloc(30);h.writeUInt32LE(0x04034b50);h.writeUInt16LE(20,4);h.writeUInt16LE(0x800,6);h.writeUInt16LE(0x21,12);h.writeUInt32LE(sum,14);h.writeUInt32LE(data.length,18);h.writeUInt32LE(data.length,22);h.writeUInt16LE(path.length,26);
  chunks.push(h,path,data);
  const c=Buffer.alloc(46);c.writeUInt32LE(0x02014b50);c.writeUInt16LE(20,4);c.writeUInt16LE(20,6);c.writeUInt16LE(0x800,8);c.writeUInt16LE(0x21,14);c.writeUInt32LE(sum,16);c.writeUInt32LE(data.length,20);c.writeUInt32LE(data.length,24);c.writeUInt16LE(path.length,28);c.writeUInt32LE(offset,42);central.push(c,path);offset+=h.length+path.length+data.length;
 }
 if(entries.length>65535)throw new Error('Too many archive entries.');
 const directory=Buffer.concat(central),end=Buffer.alloc(22);end.writeUInt32LE(0x06054b50);end.writeUInt16LE(entries.length,8);end.writeUInt16LE(entries.length,10);end.writeUInt32LE(directory.length,12);end.writeUInt32LE(offset,16);
 return Buffer.concat([...chunks,directory,end]);
}
