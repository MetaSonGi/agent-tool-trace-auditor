# AI 에이전트 도구 실행 감사기

에이전트 실행 기록을 정책과 대조해 허용되지 않은 도구, 승인 없는 쓰기, 오래된 상태, 근거 없는 결정을 차단합니다.

## 핵심 기능

읽기·결정·쓰기를 구분하고 write는 정책상 허용 도구·승인 ID·최신 상태 버전을 모두 요구합니다. 기록만 읽으며 실제 도구는 실행하지 않습니다.

## 설치·실행

Python 3.10 이상, 외부 패키지·유료 API·장비 연결이 필요 없습니다.

~~~bash
git clone https://github.com/MetaSonGi/agent-tool-trace-auditor.git
cd agent-tool-trace-auditor
python -m pip install -r requirements.txt
python main.py
python main.py --input sample-input.json --html result.html
python -m unittest -v
~~~

example-report.html 또는 result.html을 브라우저에서 열 수 있습니다. CDN과 서버 없이 동작하며 문자열은 HTML escape됩니다.

## 입출력 예제

[sample-input.json](sample-input.json), [example-output.json](example-output.json), [example-report.html](example-report.html)을 포함합니다.

~~~json
{
  "policy": {
    "allowed_tools": [
      "read_sensor",
      "search_manual",
      "propose_speed"
    ],
    "write_tools": [
      "propose_speed"
    ],
    "citation_required": true
  },
  "state_versions": {
    "robot-1": 7
  },
  "trace": [
    {
      "event_id": "e1",
      "step": 1,
      "tool": "read_sensor",
      "effect": "read",
      "resource": "robot-1"
    },
    {
      "event_id": "e2",
      "step": 2,
      "tool": "search_manual",
      "effect": "decision",
      "resource": "manual",
      "citations": [
        "manual@2#heat"
      ]
    },
    {
      "event_id": "e3",
      "step": 3,
      "tool": "propose_speed",
      "effect": "write",
      "resource": "robot-1",
      "observed_version": 6
    }
  ]
}
~~~

출력 미리보기:

~~~text
{
  "allowed": false,
  "violations": [
    {
      "step": 3,
      "reason": "approval_missing"
    },
    {
      "step": 3,
      "reason": "stale_or_unknown_state"
    }
  ],
  "events_checked": 3,
  "executed_actions": false,
  "mode": "offline_trace_audit"
}

~~~

## 설계 판단

읽기·결정·쓰기를 구분하고 write는 정책상 허용 도구·승인 ID·최신 상태 버전을 모두 요구합니다. 기록만 읽으며 실제 도구는 실행하지 않습니다. JSON 입출력으로 Python 작업 큐, Nest.js 자동화, XR/WebGL 모니터링 앞단에 연결할 수 있습니다. 실제 장비 상태는 변경하지 않습니다.

## 한계

서명·승인자 신원·분산 로그 무결성·실제 MCP 차단은 포함하지 않는 합성 trace 기준선입니다. 가상의 경력, 논문 성능, 모델 재현, 실물 제조 검증을 주장하지 않습니다.

## 검증·근거

정상·경계·오류 테스트 4개를 실행했습니다. [VALIDATION.txt](VALIDATION.txt)와 [TRENDS.md](TRENDS.md)에 결과와 근거를 구분했습니다.

실행 기준일: 2026-10-10 (Asia/Seoul). 기존 저장소를 수정하지 않은 독립 프로그램입니다.
