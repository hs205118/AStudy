from __future__ import annotations
import argparse,datetime,hashlib,html,json,os,platform,shutil,socket,subprocess,sys,time,traceback,urllib.request,uuid,zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
def iso(): return datetime.datetime.now(datetime.timezone.utc).isoformat()
def free_port():
 s=socket.socket();s.bind(('127.0.0.1',0));p=s.getsockname()[1];s.close();return p
def req(base,path,method='GET',body=None):
 data=json.dumps(body).encode() if body else None;r=urllib.request.Request(base+path,data=data,method=method)
 if data:r.add_header('content-type','application/json')
 with urllib.request.urlopen(r,timeout=15) as x:return x.status,json.loads(x.read().decode())
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--suite',default='smoke');ap.add_argument('--case-id');a=ap.parse_args()
 rid='AVF-'+datetime.datetime.now().strftime('%Y%m%dT%H%M%S')+'-'+uuid.uuid4().hex[:6].upper();out=ROOT/'.avf'/'reports'/rid
 raw=out/'raw-results';logs=out/'runtime-logs';human=out/'human-report';runtime=out/'runtime'
 for p in(raw,logs,human,runtime):p.mkdir(parents=True,exist_ok=True)
 os.environ.update(TRD_ENVIRONMENT='self-test',TRD_DATABASE_URL='sqlite:///'+(runtime/'test.db').as_posix(),TRD_ARTIFACT_ROOT=str(runtime/'artifacts'),TRD_MODULE_ROOT=str(ROOT/'modules'),TRD_REQUIRE_API_KEY='false')
 cases=json.loads((ROOT/'validation/registry/cases.json').read_text())['cases']; selected=[c for c in cases if not a.case_id or c['id']==a.case_id]
 results=[]
 def run(cid,fn):
  c=next(x for x in selected if x['id']==cid);start=time.perf_counter()
  try:d=fn() or {};st='PASSED';msg='Check passed';err=''
  except Exception as e:d={};st='FAILED';msg=str(e);err=traceback.format_exc()
  results.append({**c,'status':st,'duration_ms':int((time.perf_counter()-start)*1000),'message':msg,'details':d,'stacktrace':err});print(f'[{st}] {cid} {c["title"]}')
 port=free_port();base=f'http://127.0.0.1:{port}';proc=None;fh=None;state={}
 try:
  if any(c['id']=='ENV-001' for c in selected):run('ENV-001',lambda:(_ for _ in ()).throw(AssertionError(sys.version)) if sys.version_info<(3,11) else {'python':sys.version,'os':platform.platform()})
  if any(c['id']=='ENV-002' for c in selected):
   def packages():
    for m in ['fastapi','uvicorn','sqlalchemy','jsonschema','yaml']:__import__(m)
    return {'packages':'ok'}
   run('ENV-002',packages)
  if any(c['id']=='APP-001' for c in selected):run('APP-001',lambda:{'app':__import__('app').__file__})
  if any(c['id']=='APP-002' for c in selected):
   def db():
    from app.infrastructure.database import init_db;init_db();assert (runtime/'test.db').exists();return {'database':str(runtime/'test.db')}
   run('APP-002',db)
  if any(c['id']=='APP-003' for c in selected):
   def service():
    nonlocal proc,fh;fh=(logs/'uvicorn.log').open('w');proc=subprocess.Popen([sys.executable,'-m','uvicorn','app.main:app','--host','127.0.0.1','--port',str(port)],cwd=ROOT,stdout=fh,stderr=subprocess.STDOUT,text=True,env=os.environ.copy())
    for _ in range(60):
     try:
      s,p=req(base,'/health');
      if s==200:return {'pid':proc.pid,'base_url':base}
     except:time.sleep(.5)
    raise RuntimeError('service readiness timeout')
   run('APP-003',service)
  if any(c['id']=='API-001' for c in selected):run('API-001',lambda:{'response':req(base,'/health')[1]})
  if any(c['id']=='API-002' for c in selected):run('API-002',lambda:{'paths':len(req(base,'/openapi.json')[1]['paths'])})
  if any(c['id']=='MOD-001' for c in selected):run('MOD-001',lambda:{'modules':[x['id'] for x in req(base,'/api/v1/modules')[1]]})
  if any(c['id']=='WF-001' for c in selected):
   def wf1():
    s,r=req(base,'/api/v1/runs','POST',{'module_id':'storage-wizard','module_version':'1.0.0','parameters':{'product':'avf'},'input_text':'Storage requires RAID 1 and 4 NVMe drives.'});assert s==201
    rid2=r['id'];s,e=req(base,f'/api/v1/runs/{rid2}/execute','POST');assert e['status']=='WAITING_FOR_USER_REVIEW';state['rid']=rid2;return {'run_id':rid2,'status':e['status']}
   run('WF-001',wf1)
  if any(c['id']=='WF-002' for c in selected):
   def wf2():
    s,g=req(base,f'/api/v1/runs/{state["rid"]}/generate','POST');assert g['status']=='COMPLETED';arts=req(base,f'/api/v1/runs/{state["rid"]}/artifacts')[1];assert any(x['kind']=='final' for x in arts);return {'status':g['status'],'artifacts':[x['kind'] for x in arts]}
   run('WF-002',wf2)
  if any(c['id']=='UI-001' for c in selected):
   def ui():
    npm=shutil.which('npm');assert npm,'npm not installed';env=os.environ.copy();env['AVF_BASE_URL']=base;r=subprocess.run([npm,'test'],cwd=ROOT/'validation',env=env,capture_output=True,text=True,timeout=180);(logs/'playwright.log').write_text(r.stdout+'\n'+r.stderr);assert r.returncode==0,'Playwright failed';return {'log':'runtime-logs/playwright.log'}
   run('UI-001',ui)
 finally:
  if proc and proc.poll() is None:proc.terminate();proc.wait(timeout=8)
  if fh:fh.close()
 status='PASSED' if all(x['status']=='PASSED' for x in results) else 'FAILED';code=0 if status=='PASSED' else 30
 summary={'project':'AStudy','run_id':rid,'status':status,'suite':a.suite,'repository':'https://github.com/hs205118/AStudy.git','environment':{'os':platform.platform(),'python':sys.version},'counts':{'total':len(results),'passed':sum(x['status']=='PASSED' for x in results),'failed':sum(x['status']!='PASSED' for x in results)},'exit_code':code}
 for n,v in [('summary.json',summary),('cases.json',results),('failures.json',[x for x in results if x['status']!='PASSED'])]:(raw/n).write_text(json.dumps(v,indent=2,ensure_ascii=False))
 mods=sorted(set(x['module'] for x in results));nav=''.join(f'<button onclick="f(\'{m}\')">{m}</button>' for m in mods);rows=''.join(f'<article data-m="{x["module"]}" class="{x["status"]}"><h3>{x["id"]} {html.escape(x["title"])}</h3><b>{x["status"]}</b><p>{html.escape(x["message"])}</p><details><pre>{html.escape(json.dumps(x,indent=2,ensure_ascii=False))}</pre></details></article>' for x in results)
 page=f'''<!doctype html><meta charset="utf-8"><title>AStudy AVF</title><style>body{{margin:0;font:14px Segoe UI;background:#f5f7fb}}aside{{position:fixed;width:220px;height:100%;background:#172033;color:white;padding:20px}}aside button{{display:block;width:100%;margin:6px 0;padding:10px}}main{{margin-left:250px;padding:25px}}article{{background:white;margin:10px;padding:15px;border-left:5px solid #d33;border-radius:9px}}article.PASSED{{border-color:#198754}}pre{{white-space:pre-wrap}}</style><aside><h2>AStudy AVF</h2><button onclick="f('ALL')">All</button>{nav}</aside><main><h1>{status}</h1><p>{rid}</p>{rows}</main><script>function f(m){{document.querySelectorAll('article').forEach(x=>x.style.display=m==='ALL'||x.dataset.m===m?'block':'none')}}</script>''';(human/'index.html').write_text(page)
 ai=out/'ai-report';ai.mkdir();
 for n in ['summary.json','cases.json','failures.json']:shutil.copy2(raw/n,ai/n)
 (ai/'README_FOR_AI.md').write_text('Read summary.json then failures.json and cases.json. Repository: https://github.com/hs205118/AStudy.git')
 zpath=out/f'AStudy_AVF_{rid}_{status}.zip'
 with zipfile.ZipFile(zpath,'w',zipfile.ZIP_DEFLATED) as z:
  for p in ai.rglob('*'):
   if p.is_file():z.write(p,Path('ai-report')/p.relative_to(ai))
 print('Human report:',human/'index.html');print('AI package:',zpath);return code
if __name__=='__main__':raise SystemExit(main())
