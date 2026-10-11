"""Colour an image, then animate its selected PNG in separate owned ComfyUI processes."""
from pathlib import Path
from datetime import datetime
import argparse,json,sys
import run_example as engine
KIT=Path(__file__).resolve().parent
def save(p,d):p.write_text(json.dumps(d,indent=2)+'\n',encoding='utf-8')
def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--comfyui',type=Path,required=True);parser.add_argument('--python',type=Path,default=Path(sys.executable));parser.add_argument('--output',type=Path,default=Path('my-colour-and-motion'));parser.add_argument('--input',type=Path,default=KIT/'example/GRAYSCALE.png');parser.add_argument('--port',type=int,default=18189);parser.add_argument('--timeout',type=int,default=1200);parser.add_argument('--clip-reserve-vram',type=float,default=16);parser.add_argument('--colour-only',action='store_true');parser.add_argument('--check',action='store_true');args=parser.parse_args()
    args.comfyui=args.comfyui.resolve();args.python=args.python.resolve();args.input=args.input.resolve();root=args.output.resolve()
    if not (args.comfyui/'main.py').is_file() or not args.python.is_file() or not args.input.is_file():parser.error('Supply existing ComfyUI, its Python, and an input image')
    models=engine.read(KIT/'MODELS.json')['models'];models=models[:3] if args.colour_only else models
    verified=[]
    for model in models:
        p=args.comfyui/'models'/model['path'];assert p.is_file() and p.stat().st_size==model['bytes'],'Missing or wrong-size model: '+str(p)
        digest=engine.sha(p);assert digest==model['sha256'],'Model SHA differs: '+str(p);verified.append(dict(path=model['path'],sha256=digest,bytes=p.stat().st_size));print('MODEL OK',model['path'],flush=True)
    for name in ['01-COLOUR.api.json','02-ANIMATE.api.json']:
        graph=engine.read(KIT/'workflows'/name)
        for node in graph.values():
            for value in node['inputs'].values():
                if isinstance(value,list) and len(value)==2 and isinstance(value[0],str):assert value[0] in graph,'Broken link in '+name
    for row in engine.read(KIT/'CONDITIONING.json')['files']:assert engine.sha(KIT/'embeddings'/row['file'])==row['sha256']
    if args.check:print('Selected weights, graphs and motion conditioning verified; no inference');return
    if root.exists():parser.error('Choose a new output directory')
    if engine.occupied(args.port):parser.error('Port occupied; existing server is preserved')
    for name in ['input','output','user','embeddings','results']:(root/name).mkdir(parents=True)
    (root/'input/START.png').write_bytes(args.input.read_bytes())
    for row in engine.read(KIT/'CONDITIONING.json')['files']:(root/'embeddings'/row['file']).write_bytes((KIT/'embeddings'/row['file']).read_bytes())
    (root/'extra-model-paths.yaml').write_text('colour_example:\n  base_path: '+root.as_posix()+'\n  is_default: true\n  embeddings: embeddings\n',encoding='utf-8');save(root/'MODELS-VERIFIED.json',verified)
    graph=engine.read(KIT/'workflows/01-COLOUR.api.json');graph['10']['inputs']['image']='START.png'
    files=engine.stage(args,root,'01-colour',graph,[]);source=next(Path(r['path']) for r in files if Path(r['path']).suffix.lower()=='.png');target=root/'results/COLORIZED.png';target.write_bytes(source.read_bytes())
    result=dict(status='completed',colour=str(target),colour_sha256=engine.sha(target),source_image_sha256=engine.sha(args.input),colour_only=args.colour_only)
    if not args.colour_only:
        (root/'input/COLORIZED.png').write_bytes(target.read_bytes());graph=engine.read(KIT/'workflows/02-ANIMATE.api.json')
        files=engine.stage(args,root,'02-motion',graph,['--reserve-vram',str(args.clip_reserve_vram)]);source=next(Path(r['path']) for r in files if Path(r['path']).suffix.lower()=='.mp4');target=root/'results/ANIMATED.mp4';target.write_bytes(source.read_bytes());result.update(clip=str(target),clip_sha256=engine.sha(target))
    result['completed_at']=datetime.now().astimezone().isoformat();save(root/'RESULT.json',result);print(json.dumps(result,indent=2))
if __name__=='__main__':main()
