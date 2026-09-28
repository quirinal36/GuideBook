"""links/links.csv 로부터 QR 이미지, links.json, 리다이렉트 파일을 만든다.

생성물:
    assets/qr/<id>.png, assets/qr/<id>.svg   — 짧은 주소를 담은 QR (오류정정 H, 여백 4모듈)
    links/links.json                         — qrlink 숏코드가 읽는 데이터
    links/_redirects                         — Cloudflare Pages 리다이렉트 (/b/05-1  https://…  302)
    links/redirects.json                     — 다른 호스팅용 같은 내용의 JSON

QR 에는 항상 짧은 주소(short-domain + short_path)가 들어간다. 목적지가 바뀌어도 QR·인쇄물은 그대로.
"""
import csv
import json
import re
import sys
from pathlib import Path

import qrcode
import qrcode.image.svg
from qrcode.constants import ERROR_CORRECT_H

ROOT = Path(__file__).resolve().parent.parent
CSV_PATH = ROOT / "links" / "links.csv"
QR_DIR = ROOT / "assets" / "qr"
KINDS = {"video", "page"}
# 300dpi 에서 2cm ≈ 236px. 여유 있게 한 변 600px 이상이 되도록 모듈 크기를 정한다.
MIN_PNG_PX = 600

try:
    sys.stdout.reconfigure(encoding="utf-8")
except AttributeError:
    pass


def read_short_domain():
    """_variables.yml 의 short-domain 값을 읽는다 (PyYAML 없이 한 줄 파싱)."""
    text = (ROOT / "_variables.yml").read_text(encoding="utf-8")
    m = re.search(r'^short-domain:\s*"?([^"\n#]+?)"?\s*(?:#.*)?$', text, re.MULTILINE)
    if not m:
        sys.exit("_variables.yml 에 short-domain 이 없습니다")
    return m.group(1).rstrip("/")


def make_qr(data):
    qr = qrcode.QRCode(error_correction=ERROR_CORRECT_H, border=4, box_size=1)
    qr.add_data(data)
    qr.make(fit=True)
    modules = qr.modules_count + 2 * qr.border
    qr.box_size = max(10, -(-MIN_PNG_PX // modules))  # 올림 나눗셈
    return qr


def youtube_id(url):
    m = re.search(r"(?:youtu\.be/|[?&]v=|/embed/|/shorts/)([A-Za-z0-9_-]{11})", url or "")
    return m.group(1) if m else None


def main():
    domain = read_short_domain()
    QR_DIR.mkdir(parents=True, exist_ok=True)
    links, redirects, warnings, errors = {}, [], [], []

    with open(CSV_PATH, encoding="utf-8", newline="") as f:
        for row in csv.DictReader(f):
            lid, path, target, kind = row["id"].strip(), row["short_path"].strip(), row["target_url"].strip(), row["kind"].strip()
            if not lid or not path.startswith("/"):
                errors.append(f"{lid or '(빈 id)'}: short_path 는 '/' 로 시작해야 합니다 ({path!r})")
                continue
            if kind not in KINDS:
                errors.append(f"{lid}: kind 는 video|page 중 하나여야 합니다 ({kind!r})")
                continue
            if lid in links:
                errors.append(f"{lid}: id 중복")
                continue

            short_url = domain + path
            todo = target in ("", "TODO")
            if todo:
                warnings.append(f"{lid}: target_url 이 TODO — QR 은 짧은 주소로 생성, 리다이렉트는 제외")
            elif kind == "video" and not youtube_id(target):
                warnings.append(f"{lid}: video 인데 유튜브 영상 ID를 찾지 못함 — HTML에서 링크 카드로 표시")

            qr = make_qr(short_url)
            qr.make_image(fill_color="black", back_color="white").save(QR_DIR / f"{lid}.png")
            qr_svg = make_qr(short_url)
            qr_svg.make_image(image_factory=qrcode.image.svg.SvgPathImage).save(str(QR_DIR / f"{lid}.svg"))

            links[lid] = {
                "id": lid,
                "short_path": path,
                "short_url": short_url,
                "short_label": short_url.split("://", 1)[-1],
                "target_url": None if todo else target,
                "youtube_id": None if todo else youtube_id(target),
                "kind": kind,
                "chapter": row["chapter"].strip(),
                "title": row["title"].strip(),
                "qr_png": f"assets/qr/{lid}.png",
                "qr_svg": f"assets/qr/{lid}.svg",
            }
            if not todo:
                redirects.append({"from": path, "to": target, "status": 302})

    (ROOT / "links" / "links.json").write_text(
        json.dumps({"short_domain": domain, "links": links}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    lines = ["# gen_qr.py 가 생성 — 직접 고치지 말고 links/links.csv 를 고친 뒤 다시 실행"]
    lines += [f"{r['from']}  {r['to']}  {r['status']}" for r in redirects]
    (ROOT / "links" / "_redirects").write_text("\n".join(lines) + "\n", encoding="utf-8")
    (ROOT / "links" / "redirects.json").write_text(
        json.dumps(redirects, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    for w in warnings:
        print(f"경고: {w}")
    for e in errors:
        print(f"오류: {e}")
    print(f"QR {len(links)}개 생성 → assets/qr/ · 리다이렉트 {len(redirects)}개 · links/links.json 갱신")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
