"""Check the generated ZIPs using an independent standard-library ZIP reader."""
import hashlib,json,pathlib,zipfile
root=pathlib.Path(__file__).resolve().parents[1]
manifest=json.loads((root/'dist/build-manifest.json').read_text())
for output in manifest['outputs']:
 data=(root/'dist'/output['file']).read_bytes()
 assert hashlib.sha256(data).hexdigest()==output['sha256'] and len(data)==output['bytes']
for edition in ['chatgpt','claude','gemini']:
 name='skill-switchboard-'+edition
 with zipfile.ZipFile(root/'dist'/f'{name}.zip') as z:
  assert z.testzip() is None
  assert len(z.namelist())==5
  assert all(p.startswith(name+'/') and '..' not in p.split('/') for p in z.namelist())
  assert z.read(name+'/references/companion.html')==(root/'dist'/f'{name}.html').read_bytes()
  assert f'name: {name}'.encode() in z.read(name+'/SKILL.md')
  assert b'MIT License' in z.read(name+'/LICENSE')
 print('Verified',name,'ZIP, packaged HTML, skill name, license and build hashes.')
