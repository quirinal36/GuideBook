"""원고의 그림 참조와 figures/figures.csv 를 대조한다.

사용법:
    python scripts/check_figures.py                                  # 누락·미등록·미사용 점검
    python scripts/check_figures.py --todo                           # status=todo 목록(챕터 순)
    python scripts/check_figures.py --stale --tool Lovable --before 2.0
        # 해당 도구의 2.0 이전 버전으로 찍은 그림을 stale 로 표시

종료 코드: 문제가 있으면 1, 없으면 0.
"""
import argparse
import csv
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CSV_PATH = ROOT / "figures" / "figures.csv"
FIELDS = ["id", "chapter", "file", "tool", "tool_version", "os", "captured_at",
          "window_size", "caption", "status", "notes"]
STATUSES = {"todo", "current", "stale"}
# ![..](figures/x.png) · ](/figures/x.png) · ](../figures/x.png) 모두 잡는다
REF_RE = re.compile(r"(?:\.\./|/)?(figures/[^\s)\"'}]+?\.(?:png|jpg|jpeg|svg))", re.IGNORECASE)

# Windows 콘솔에서도 한글이 깨지지 않게
try:
    sys.stdout.reconfigure(encoding="utf-8")
except AttributeError:
    pass


def load_rows():
    with open(CSV_PATH, encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def save_rows(rows):
    with open(CSV_PATH, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        w.writeheader()
        w.writerows(rows)


def collect_refs():
    """{그림경로: [참조한 qmd 파일들]}"""
    refs = {}
    for qmd in sorted(ROOT.rglob("*.qmd")):
        if any(p.startswith((".", "_")) for p in qmd.relative_to(ROOT).parts):
            continue
        text = qmd.read_text(encoding="utf-8")
        for m in REF_RE.finditer(text):
            refs.setdefault(m.group(1), []).append(qmd.relative_to(ROOT).as_posix())
    return refs


def print_table(title, headers, rows):
    print(f"\n■ {title} ({len(rows)}건)")
    if not rows:
        return
    widths = [max(len(str(h)), *(len(str(r[i])) for r in rows)) for i, h in enumerate(headers)]
    line = "  ".join(str(h).ljust(widths[i]) for i, h in enumerate(headers))
    print(line)
    print("-" * len(line))
    for r in rows:
        print("  ".join(str(c).ljust(widths[i]) for i, c in enumerate(r)))


def version_tuple(v):
    return tuple(int(x) for x in re.findall(r"\d+", v or ""))


def cmd_check(rows):
    refs = collect_refs()
    by_file = {r["file"]: r for r in rows}
    problems = 0

    unregistered = [(f, ", ".join(srcs)) for f, srcs in refs.items() if f not in by_file]
    missing = [(f, ", ".join(refs.get(f, ["(CSV)"]))) for f in sorted(set(refs) | set(by_file))
               if not (ROOT / f).exists()]
    unused = [(r["id"], r["file"]) for r in rows if r["file"] not in refs]
    bad_status = [(r["id"], r["status"]) for r in rows if r["status"] not in STATUSES]

    print_table("(a) CSV에 없는 참조", ["그림", "참조 위치"], unregistered)
    print_table("(b) 디스크에 없는 파일", ["그림", "참조 위치"], missing)
    print_table("(c) CSV에만 있고 아무도 참조하지 않는 그림", ["id", "그림"], unused)
    if bad_status:
        print_table("status 값 오류 (todo|current|stale 만 허용)", ["id", "status"], bad_status)

    problems = len(unregistered) + len(missing) + len(unused) + len(bad_status)
    counts = {s: sum(1 for r in rows if r["status"] == s) for s in sorted(STATUSES)}
    print(f"\n등록 {len(rows)}개 · 참조 {len(refs)}개 · 상태 {counts}")
    print("문제 없음" if problems == 0 else f"문제 {problems}건")
    return 1 if problems else 0


def cmd_todo(rows):
    todo = sorted((r for r in rows if r["status"] == "todo"), key=lambda r: (r["chapter"], r["id"]))
    print_table("캡처할 그림 (status=todo)", ["chapter", "id", "file", "caption"],
                [(r["chapter"], r["id"], r["file"], r["caption"]) for r in todo])
    return 0


def cmd_stale(rows, tool, before):
    limit = version_tuple(before)
    hit = []
    for r in rows:
        if r["tool"].strip().lower() != tool.strip().lower():
            continue
        v = version_tuple(r["tool_version"])
        if v and v < limit:
            r["status"] = "stale"
            hit.append(r)
    if hit:
        save_rows(rows)
    print_table(f"{tool} {before} 이전 버전 캡처 → stale 표시", ["chapter", "id", "tool_version", "file"],
                [(r["chapter"], r["id"], r["tool_version"], r["file"]) for r in hit])
    return 0


def main():
    ap = argparse.ArgumentParser(description="그림 참조·등록 상태 점검")
    ap.add_argument("--todo", action="store_true", help="status=todo 그림 목록")
    ap.add_argument("--stale", action="store_true", help="특정 도구 구버전 캡처를 stale 로 표시")
    ap.add_argument("--tool", help="--stale 과 함께: 도구 이름 (CSV의 tool 컬럼)")
    ap.add_argument("--before", help="--stale 과 함께: 이 버전 미만을 stale 로")
    args = ap.parse_args()

    rows = load_rows()
    if args.stale:
        if not (args.tool and args.before):
            ap.error("--stale 에는 --tool 과 --before 가 필요합니다")
        return cmd_stale(rows, args.tool, args.before)
    if args.todo:
        return cmd_todo(rows)
    return cmd_check(rows)


if __name__ == "__main__":
    sys.exit(main())
