"""에이전트 실행 기록을 정책과 대조해 허용되지 않은 도구, 승인 없는 쓰기, 오래된 상태, 근거 없는 결정을 차단합니다."""
import argparse,html,json,math
from pathlib import Path
def finite(v,n,minimum=None):
 if type(v) not in (int,float) or not math.isfinite(v):raise ValueError(n+": finite number required")
 if minimum is not None and v<minimum:raise ValueError(n+": below minimum")
 return v
def report(x,t):
 p=html.escape(json.dumps(x,ensure_ascii=False,indent=2,allow_nan=False))
 return '<!doctype html><meta charset="utf-8"><meta name="viewport" content="width=device-width"><title>'+html.escape(t)+'</title><style>body{font:16px/1.6 system-ui;max-width:1000px;margin:30px auto;padding:20px;background:#101b2b;color:#eef7ff}pre{background:#192b40;padding:22px;border-radius:12px;white-space:pre-wrap}h1{color:#79e3c2}</style><h1>'+html.escape(t)+'</h1><p>오프라인 합성 예제 · 실물 장비 연결 없음</p><pre>'+p+'</pre>'
def cli(fn,title):
 p=argparse.ArgumentParser();p.add_argument("--input",default=str(Path(__file__).with_name("sample-input.json")));p.add_argument("--html");a=p.parse_args()
 try:
  x=fn(json.loads(Path(a.input).read_text(encoding="utf-8")))
  if a.html:Path(a.html).write_text(report(x,title),encoding="utf-8")
  print(json.dumps(x,ensure_ascii=False,indent=2,allow_nan=False))
 except (ValueError,KeyError,TypeError) as e:p.exit(2,"input error: "+str(e)+"\n")

def run(d):
 p=d["policy"];bad=[];seen=set();last=-1
 for e in d["trace"]:
  step=e["step"]
  if type(step) is not int or step<=last:bad.append({"step":step,"reason":"non_monotonic_step"})
  last=step
  if e["event_id"] in seen:bad.append({"step":step,"reason":"duplicate_event_id"})
  seen.add(e["event_id"]);tool=e["tool"]
  if tool not in p["allowed_tools"]:bad.append({"step":step,"reason":"tool_not_allowed","tool":tool})
  if e["effect"]=="write":
   if tool not in p["write_tools"]:bad.append({"step":step,"reason":"write_not_declared"})
   if not e.get("approval_id"):bad.append({"step":step,"reason":"approval_missing"})
   if e.get("observed_version")!=d["state_versions"].get(e["resource"]):bad.append({"step":step,"reason":"stale_or_unknown_state"})
  if e["effect"]=="decision" and p.get("citation_required",True) and not e.get("citations"):bad.append({"step":step,"reason":"citation_missing"})
 return {"allowed":not bad,"violations":bad,"events_checked":len(d["trace"]),"executed_actions":False,"mode":"offline_trace_audit"}

if __name__=="__main__":cli(run,'AI 에이전트 도구 실행 감사기')
