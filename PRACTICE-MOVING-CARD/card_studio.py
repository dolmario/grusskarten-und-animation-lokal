"""Make a greeting-card MP4 from an existing local clip with a fixed text overlay."""
from pathlib import Path
from http.server import BaseHTTPRequestHandler,ThreadingHTTPServer
import argparse,hashlib,json,os,shutil,socket,subprocess,threading,time,urllib.parse
from PIL import Image,ImageDraw,ImageFont
PAGE='''<!doctype html><html lang="en"><meta charset="utf-8"><title>Dolmario / moving greeting card</title><style>*{box-sizing:border-box}body{margin:0;background:#111a24;color:#f3f6f8;font:20px Segoe UI,sans-serif}header{padding:18px 28px;background:#203542;font-size:24px;font-weight:650}main{display:grid;grid-template-columns:350px 1fr;gap:25px;padding:28px}aside{background:#1b2b38;border-radius:12px;padding:24px}label{display:block;margin:0 0 10px}input,select,button{width:100%;padding:13px;font:20px Segoe UI;margin:0 0 24px;border-radius:7px;border:1px solid #648094;background:#101e2a;color:white}button{background:#237d71;border:0;cursor:pointer;font-weight:600}button:disabled{opacity:.5;cursor:wait}video{width:100%;max-height:550px;background:#0b1118;border-radius:9px}.note{font-size:17px;color:#b8cbd7;line-height:1.5}a{color:#8be3d5}#status{margin:0 0 18px;min-height:27px}h1{font-size:24px;margin:0 0 20px}</style><header>Dolmario / moving greeting card</header><main><aside><label for="message">Your message</label><input id="message" maxlength="60" value="Alles Gute!"><label for="position">Text position</label><select id="position"><option value="bottom">Bottom</option><option value="top">Top</option></select><label for="size">Text size</label><select id="size"><option value="64">64</option><option value="80" selected>80</option><option value="96">96</option></select><button id="export">Export MP4</button><div class="note">The message stays fixed over the moving clip. Each export creates a separate file.</div></aside><section><h1>Use the movement, keep the words clear</h1><div id="status">Source clip ready</div><video controls src="/source.mp4"></video><p id="link"></p></section></main><script>const button=document.querySelector('#export');let timer;button.onclick=async()=>{button.disabled=true;document.querySelector('#status').textContent='Rendering your card…';const r=await fetch('/export',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({message:document.querySelector('#message').value,position:document.querySelector('#position').value,size:Number(document.querySelector('#size').value)})});const d=await r.json();if(!r.ok){document.querySelector('#status').textContent=d.error;button.disabled=false;return;}timer=setInterval(async()=>{const r=await fetch('/status?id='+encodeURIComponent(d.id));const job=await r.json();if(job.status==='completed'){clearInterval(timer);document.querySelector('video').src=job.url;document.querySelector('#status').textContent='Your card is ready';document.querySelector('#link').innerHTML='<a download href="'+job.url+'">Download MP4</a>';button.disabled=false;}else if(job.status==='failed'){clearInterval(timer);document.querySelector('#status').textContent=job.error;button.disabled=false;}},300);};</script></html>'''
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def create_overlay(path,message,position,size,fontfile):
    image=Image.new('RGBA',(1280,720),(0,0,0,0));draw=ImageDraw.Draw(image);font=ImageFont.truetype(str(fontfile),size);box=draw.textbbox((0,0),message,font=font);width=box[2]-box[0]
    while width>1120 and size>24:size-=2;font=ImageFont.truetype(str(fontfile),size);box=draw.textbbox((0,0),message,font=font);width=box[2]-box[0]
    y=570 if position=='bottom' else 40;draw.rounded_rectangle((40,y,1240,y+112),radius=18,fill=(15,32,43,232));draw.text(((1280-width)/2,y+18-box[1]),message,font=font,fill=(255,255,255,255));image.save(path);return size
def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--clip',type=Path,default=Path(__file__).parent/'example/SOURCE.mp4');parser.add_argument('--output',type=Path,default=Path('my-moving-cards'));parser.add_argument('--port',type=int,default=18192);parser.add_argument('--font',type=Path,default=Path(os.environ.get('WINDIR','C:/Windows'))/'Fonts/segoeuib.ttf');args=parser.parse_args();args.clip=args.clip.resolve();args.output=args.output.resolve();args.font=args.font.resolve()
    if not args.clip.is_file() or not args.font.is_file():parser.error('Supply an existing clip and TrueType font')
    if not shutil.which('ffmpeg') or not shutil.which('ffprobe'):parser.error('Install FFmpeg and put its bin directory on PATH')
    if args.output.exists():parser.error('Choose a new output directory')
    with socket.socket() as sock:
        if sock.connect_ex(('127.0.0.1',args.port))==0:parser.error('Port already occupied')
    args.output.mkdir(parents=True);jobs={};guard=threading.Lock();source_sha=sha(args.clip)
    def render(job):
        try:
            directory=args.output/job['id'];directory.mkdir();overlay=directory/'TEXT.png';used=create_overlay(overlay,job['message'],job['position'],job['size'],args.font);target=directory/'CARD.mp4'
            command=['ffmpeg','-y','-hide_banner','-loglevel','warning','-i',str(args.clip),'-loop','1','-framerate','24','-i',str(overlay),'-filter_complex','[0:v]scale=1280:720:force_original_aspect_ratio=decrease,pad=1280:720:(ow-iw)/2:(oh-ih)/2,setsar=1,fps=24[base];[base][1:v]overlay=0:0:shortest=1[v]','-map','[v]','-an','-c:v','libx264','-preset','veryfast','-crf','18','-pix_fmt','yuv420p','-threads','2','-movflags','+faststart',str(target)]
            flags=subprocess.CREATE_NO_WINDOW if os.name=='nt' else 0
            with(directory/'FFMPEG.log').open('w',encoding='utf-8') as log:subprocess.run(command,stdout=log,stderr=subprocess.STDOUT,check=True,creationflags=flags)
            probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_format','-show_streams','-of','json',str(target)],creationflags=flags));v=next(s for s in probe['streams'] if s['codec_type']=='video');assert(v['width'],v['height'],v['r_frame_rate'])==(1280,720,'24/1')
            report=dict(source_clip_sha256=source_sha,message=job['message'],position=job['position'],requested_font_size=job['size'],used_font_size=used,font_file=args.font.name,fixed_overlay=True,model_generation_not_repeated=True,video_sha256=sha(target),seconds=float(probe['format']['duration']),format=probe,command=command)
            (directory/'RESULT.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');job.update(status='completed',url='/result/'+job['id']+'/CARD.mp4')
        except Exception as exc:job.update(status='failed',error=str(exc))
        finally:guard.release()
    class Handler(BaseHTTPRequestHandler):
        def log_message(self,*args):pass
        def send_json(self,status,data):
            body=json.dumps(data,ensure_ascii=False).encode();self.send_response(status);self.send_header('Content-Type','application/json; charset=utf-8');self.send_header('Content-Length',str(len(body)));self.end_headers();self.wfile.write(body)
        def do_GET(self):
            parsed=urllib.parse.urlparse(self.path)
            if parsed.path=='/':
                body=PAGE.encode();self.send_response(200);self.send_header('Content-Type','text/html; charset=utf-8');self.send_header('Content-Length',str(len(body)));self.end_headers();self.wfile.write(body);return
            if parsed.path=='/status':self.send_json(200,jobs.get(urllib.parse.parse_qs(parsed.query).get('id',[''])[0],dict(status='unknown')));return
            target=None
            if parsed.path=='/source.mp4':target=args.clip
            elif parsed.path.startswith('/result/'):
                parts=parsed.path.split('/')
                if len(parts)==4 and parts[2] in jobs and parts[3]=='CARD.mp4' and jobs[parts[2]]['status']=='completed':target=args.output/parts[2]/parts[3]
            if target is None:self.send_error(404);return
            data=target.read_bytes();self.send_response(200);self.send_header('Content-Type','video/mp4');self.send_header('Content-Length',str(len(data)));self.end_headers();self.wfile.write(data)
        def do_POST(self):
            if self.path!='/export':self.send_error(404);return
            origin=self.headers.get('Origin')
            if origin not in (None,f'http://127.0.0.1:{args.port}',f'http://localhost:{args.port}'):self.send_json(403,dict(error='Use this local page to export'));return
            try:
                length=int(self.headers.get('Content-Length','0'));assert 0<length<=1024
                data=json.loads(self.rfile.read(length));message=data['message'].strip();position=data['position'];size=int(data['size']);assert 1<=len(message)<=60 and not any(ord(c)<32 for c in message) and position in ['top','bottom'] and size in [64,80,96]
            except Exception:self.send_json(400,dict(error='Use a message of1–60characters and the supplied size/position choices'));return
            if not guard.acquire(blocking=False):self.send_json(409,dict(error='An export is already running'));return
            job=dict(id=str(time.time_ns()),status='rendering',message=message,position=position,size=size);jobs[job['id']]=job;threading.Thread(target=render,args=(job,),daemon=True).start();self.send_json(202,dict(id=job['id']))
    print(f'Open http://127.0.0.1:{args.port}',flush=True);ThreadingHTTPServer(('127.0.0.1',args.port),Handler).serve_forever()
if __name__=='__main__':main()
