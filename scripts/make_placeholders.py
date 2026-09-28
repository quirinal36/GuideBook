"""figures/figures.csv 에 등록됐지만 디스크에 없는 그림을 회색 플레이스홀더 PNG로 만든다.

사용법:
    python scripts/make_placeholders.py          # 없는 파일만 생성
    python scripts/make_placeholders.py --force  # 플레이스홀더를 모두 다시 생성
"""
import argparse
import csv
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
CSV_PATH = ROOT / "figures" / "figures.csv"
SIZE = (1280, 800)

try:
    sys.stdout.reconfigure(encoding="utf-8")
except AttributeError:
    pass


def load_font(size):
    # 저장소 폰트 → 시스템 폰트 → 기본 폰트 순으로 시도
    for cand in [ROOT / "fonts" / "Pretendard-Bold.otf", "malgunbd.ttf", "NotoSansKR-VF.ttf", "DejaVuSans.ttf"]:
        try:
            return ImageFont.truetype(str(cand), size)
        except OSError:
            continue
    return ImageFont.load_default()


def draw_placeholder(path: Path, label: str):
    img = Image.new("RGB", SIZE, (200, 200, 200))
    d = ImageDraw.Draw(img)
    d.rectangle([8, 8, SIZE[0] - 9, SIZE[1] - 9], outline=(150, 150, 150), width=6)
    font = load_font(96)
    box = d.textbbox((0, 0), label, font=font)
    w, h = box[2] - box[0], box[3] - box[1]
    d.text(((SIZE[0] - w) / 2 - box[0], (SIZE[1] - h) / 2 - box[1]), label, fill=(90, 90, 90), font=font)
    path.parent.mkdir(parents=True, exist_ok=True)
    img.save(path)


def main():
    ap = argparse.ArgumentParser(description="플레이스홀더 그림 생성")
    ap.add_argument("--force", action="store_true", help="이미 있는 플레이스홀더도 다시 생성")
    args = ap.parse_args()

    made = 0
    with open(CSV_PATH, encoding="utf-8", newline="") as f:
        for row in csv.DictReader(f):
            path = ROOT / row["file"]
            if path.suffix.lower() != ".png":
                continue
            is_placeholder = "placeholder" in path.name
            if path.exists() and not (args.force and is_placeholder):
                continue
            draw_placeholder(path, row["id"])
            print(f"생성: {row['file']}")
            made += 1
    print(f"플레이스홀더 {made}개 생성")
    return 0


if __name__ == "__main__":
    sys.exit(main())
