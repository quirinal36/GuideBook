# 원장님, 오늘 밤에 홈페이지 하나 만드세요

학원 원장이 AI와 대화하며 홈페이지·문의 폼·과목별 미니게임을 만드는 4주 과정을 담은 책의 원고 저장소입니다.
**마크다운 원고 하나**에서 웹판(HTML), 전자책(EPUB), PDF(전자책·인쇄)를 모두 빌드합니다.

- 도구: [Quarto](https://quarto.org) book 프로젝트
- PDF 엔진: **typst** (Quarto 1.10.18 내장 typst 0.15.1, `orange-book` 템플릿). LaTeX는 쓰지 않습니다.
- 원고 규칙은 [STYLE.md](STYLE.md) 참고

## 설치

1. **Quarto** 1.10 이상 — <https://quarto.org/docs/get-started/>
   Windows: `winget install --id Posit.Quarto -e`
   typst가 Quarto에 들어 있으므로 따로 설치할 것이 없습니다 (`quarto typst --version` 으로 확인).
2. **Python** 3.10 이상 + 패키지
   ```
   python -m pip install -r requirements.txt
   ```
3. **폰트** — `fonts/` 에 이미 들어 있습니다 (둘 다 SIL OFL 라이선스).
   | 용도 | 폰트 | 파일 |
   |---|---|---|
   | 본문 | Pretendard 1.3.9 (Regular·Medium·SemiBold·Bold) | `fonts/Pretendard-*.otf` |
   | 코드 | D2Coding 1.3.2 (Regular·Bold) | `fonts/D2Coding-*.ttf` |

   PDF(typst)는 `fonts/` 를 직접 읽으므로 시스템 설치가 필요 없습니다.
   웹판은 방문자 기기의 폰트를 쓰며, 없으면 Noto Sans KR → 기본 고딕 순으로 대체됩니다.
   폰트 파일이 없어졌다면 아래에서 받아 `fonts/` 에 넣으세요.
   - Pretendard: <https://github.com/orioncactus/pretendard/releases> → `public/static/Pretendard-*.otf`
   - D2Coding: <https://github.com/naver/d2codingfont/releases>
   - 다른 폰트로 바꾸려면 `assets/typst/fonts.typ` 의 폰트 이름을 고칩니다 (예: `"Noto Sans KR"`, `"Noto Sans Mono CJK KR"`).
4. (선택) `make` — Windows에서 없으면 같은 기능의 `build.ps1` 을 씁니다.

## 빌드

| 하는 일 | make | PowerShell |
|---|---|---|
| 세 포맷 모두 | `make all` | `.\build.ps1 all` |
| 웹판 | `make html` | `.\build.ps1 html` |
| EPUB | `make epub` | `.\build.ps1 epub` |
| PDF | `make pdf` | `.\build.ps1 pdf` |
| QR·링크 재생성 | `make qr` | `.\build.ps1 qr` |
| 그림 점검 | `make check` | `.\build.ps1 check` |
| 캡처할 그림 목록 | `make todo` | `.\build.ps1 todo` |
| 미리보기(자동 새로고침) | `make serve` | `.\build.ps1 serve` |

결과물은 `_book/` 에 생깁니다 — `index.html`, `guidebook.epub`, `guidebook.pdf`.

> 포맷 하나만 렌더(`--to epub` 등)하면 `_book/` 을 비우고 그 포맷만 남깁니다. 세 개를 한꺼번에 얻으려면 `make all`.

## 폴더 구조

```
_quarto.yml              책 설정 (제목·부제·저자는 맨 위 book: 블록)
_variables.yml           짧은 주소 도메인(short-domain) 등 공용 변수
index.qmd                들어가며
chapters/                1~15장(chNN-*.qmd), 부록(appendix-*.qmd)
figures/                 본문 그림 + figures.csv(그림 대장)
links/                   links.csv(링크 대장) → links.json, _redirects, redirects.json (자동 생성)
assets/cover.png         표지 (현재 700×1000 플레이스홀더)
assets/qr/               QR 이미지 (자동 생성)
assets/typst/            PDF용 폰트 설정(fonts.typ), 판형 전달용 템플릿 조각(typst-show.typ)
_extensions/letscoding/qrlink/   qrlink 숏코드 (Lua)
fonts/                   Pretendard, D2Coding
scripts/                 gen_qr.py, check_figures.py, make_placeholders.py
STYLE.md                 원고 규칙
```

## 집필 워크플로 — 그림

1. **캡처** — 아래 캡처 규칙대로 찍어 `figures/` 에 저장.
2. **CSV 등록** — `figures/figures.csv` 에 한 줄 추가.
   `id, chapter, file, tool, tool_version, os, captured_at, window_size, caption, status, notes`
   - `status`: `todo`(아직 안 찍음) · `current`(최신) · `stale`(도구 UI가 바뀌어 다시 찍어야 함)
   - `tool`, `tool_version` 은 반드시 채운다 — 나중에 일괄 `stale` 처리의 기준.
3. **본문 삽입**
   ```
   ![캡션](/figures/ch05-02-deploy-button.png){#fig-ch05-02}
   ```
   경로 앞의 `/` 는 “프로젝트 루트 기준”이라는 뜻입니다 (`chapters/` 안에서도 그대로 동작).
   본문에서 참조는 `@fig-ch05-02`.
4. **점검** — `make check`. 미등록 참조, 없는 파일, 안 쓰는 그림이 표로 나오고 문제가 있으면 종료 코드 1.
5. **빌드** — `make all`.

도구가 업데이트되면:
```
python scripts/check_figures.py --stale --tool Lovable --before 2.0
```
→ 해당 도구 2.0 미만 버전으로 찍은 그림을 모두 `stale` 로 바꾸고 목록을 보여줍니다.

아직 캡처 안 한 그림 자리는 `python scripts/make_placeholders.py` 가 CSV를 보고 회색 플레이스홀더(1280×800)를 만들어 줍니다.

### 캡처 규칙

- 브라우저/앱 창 크기 **1280×800**, 디스플레이 배율 **200%(2배)** 로 캡처 → 실제 파일 2560×1600
- **밝은 테마**, **한국어 UI**
- 파일명 `chNN-MM-설명.png` (예: `ch05-02-deploy-button.png`) — 소문자·하이픈, 설명은 영문
- 개인정보(이메일, 전화번호, 학생 이름 등)가 보이면 찍기 전에 테스트 계정으로 바꾸거나 가린다
- 캡처는 “어디를 누르는지” 보여줄 때만. 결과는 글로 쓴다 ([STYLE.md](STYLE.md))

## 집필 워크플로 — 영상·QR 링크

책에는 항상 **짧은 주소**(`https://letscoding.kr/b/05-1`)만 실립니다. 실제 목적지(유튜브, 웹판 페이지)는 리다이렉트로 연결하므로, 목적지가 바뀌어도 인쇄된 QR은 그대로 쓸 수 있습니다.

1. `links/links.csv` 에 한 줄 추가
   `id, short_path, target_url, kind, chapter, title, notes`
   - `id`: `05-1` 처럼 `장-순번`
   - `short_path`: `/b/05-1` (한 번 인쇄되면 **절대 바꾸지 않는다**)
   - `target_url`: 유튜브·웹판 URL. 아직 없으면 `TODO`
   - `kind`: `video`(유튜브 임베드) 또는 `page`(링크 카드)
2. 본문에 숏코드 삽입 (단독 줄)
   ```
   {{< qrlink 05-1 >}}
   ```
3. `make qr` → `assets/qr/05-1.png·svg`, `links/links.json`, `links/_redirects` 생성
   - `TODO` 행은 경고만 나오고 QR은 짧은 주소로 만들어집니다. 리다이렉트에서는 빠집니다.
4. `links/_redirects` 를 letscoding.kr(Cloudflare Pages)에 배포.

숏코드 출력:
- **웹판**: `video` 는 유튜브 반응형 임베드 + 제목·짧은 주소, `page` 는 카드형 링크
- **EPUB·PDF**: QR(약 2.5cm) + 제목 + 짧은 주소(고정폭, 클릭 가능)
- 없는 id 를 쓰면 빌드 경고 + 본문에 빨간 경고 블록

짧은 주소 도메인은 `_variables.yml` 의 `short-domain` 에서 바꿉니다.

## 알아둘 점 (PDF / typst)

- Quarto의 typst **book**은 `orange-book` 템플릿을 쓰는데, 이 템플릿은 `mainfont`·`papersize` 같은 옵션을 넘기지 않습니다. 그래서
  - 폰트는 `assets/typst/fonts.typ` 에서 직접 지정하고,
  - 판형·여백·글자 크기는 `assets/typst/typst-show.typ`(Quarto 원본을 복사해 고친 것)로 넘깁니다.
  - **Quarto를 올린 뒤에는** 원본 `…/share/extension-subtrees/orange-book/_extensions/orange-book/typst-show.typ` 와 비교해 달라진 부분을 반영하세요.
- 현재 판형 A5, 여백 좌우 2cm·위아래 2.2cm, 본문 10pt (`_quarto.yml` 의 `format.typst`).
- 머리글의 장 표기가 “장 5.” 처럼 나옵니다 (orange-book이 접두어를 번호 앞에 붙임). 인쇄 전 조판 다듬기 때 손볼 항목입니다.
- 장 번호는 Quarto가 자동으로 붙이므로 원고 H1에 “1장.”을 쓰지 않습니다. 부록은 A, B, C… 로 붙습니다.
