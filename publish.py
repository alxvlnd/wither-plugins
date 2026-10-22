from pathlib import Path
import zipfile,hashlib,json
root=Path(__file__).resolve().parent
entries=[]
for jar in sorted((root/'jars').glob('*.jar')):
    with zipfile.ZipFile(jar) as z:
        lines=z.read('plugin.yml').decode().splitlines()
    data={k:v.strip().strip("\"'") for l in lines if ':' in l and not l.startswith(' ') for k,v in [l.split(':',1)]}
    entries.append(dict(name=data['name'],version=data['version'],file='jars/'+jar.name,sha256=hashlib.sha256(jar.read_bytes()).hexdigest()))
names=[e['name'].lower() for e in entries]
if len(names)!=len(set(names)): raise SystemExit('Keep only ONE JAR per plugin in jars!')
(root/'plugins.json').write_text(json.dumps(dict(schema=1,plugins=entries),indent=2)+'\n')
print('plugins.json updated:',len(entries),'plugins')
