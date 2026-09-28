# 작업: 학원 원장용 전자책 Quarto 프로젝트 뼈대 만들기

## 배경
학원 원장(코딩학원 + 일반학원)이 AI와 대화하며 학원 홈페이지·문의 폼·과목별 미니게임을 직접 만드는 4주 과정을 담은 책이다. 전자책(EPUB, PDF)과 종이책(PDF 인쇄), 그리고 웹판(HTML)을 **하나의 마크다운 원고**에서 빌드한다. 캡처 화면이 많고 도구 UI가 자주 바뀌므로, 그림 관리와 QR 링크 관리를 스크립트로 처리한다.

이 작업에서는 **본문을 쓰지 않는다.** 챕터 파일 뼈대, 설정, 스크립트, 규칙 문서까지만 만든다. 모든 텍스트와 주석은 한국어로 작성한다.

## 만들 것

### 1. Quarto book 프로젝트
- 프로젝트 루트에 `_quarto.yml` — `project: type: book`
- 가제: 『원장님, 오늘 밤에 홈페이지 하나 만드세요』 (부제: AI와 대화로 만드는 우리 학원 사이트와 게임). 쉽게 바꿀 수 있게 yml 상단 변수로.
- 저자: 주식회사 렛츠코딩 (임시)
- 언어: `lang: ko`
- 출력 포맷 3종:
  - `html` — 웹판. 출력 폴더 `_book/`. 나중에 `letscoding.kr` 하위 경로에 올릴 것을 가정하고 `site-url`은 플레이스홀더로.
  - `epub` — 서점 유통용. 표지 이미지는 `assets/cover.png` 플레이스홀더(700×1000).
  - PDF — **typst 엔진** 우선. Quarto book이 typst를 지원하는 버전이면 typst로, 아니면 LaTeX(xelatex)로 대체하고 README에 어느 쪽을 썼는지 기록. 한국어 본문 폰트는 Pretendard(없으면 Noto Sans KR), 코드 폰트는 D2Coding 또는 Noto Sans Mono CJK KR. 폰트 파일은 `fonts/`에 두고, 다운로드가 안 되면 README에 수동 설치 안내를 남기고 시스템 폰트명으로 설정.
- `.gitignore`에 `_book/`, `.quarto/`, `*.pyc`, `.venv/` 포함. `git init` 후 초기 커밋.

### 2. 챕터 파일
아래 목차 그대로 `chapters/` 폴더에 `.qmd` 파일을 만들고 `_quarto.yml`의 `book.chapters`에 `part`로 묶어 순서대로 등록한다.

각 챕터 파일 규칙:
- 첫 줄은 H1 제목. 목차의 하위 항목은 H2 소제목으로.
- 각 H2 아래에는 본문 대신 `<!-- 집필 메모: ... -->` HTML 주석으로 "이 절에 들어갈 내용" 한두 문장을 목차 설명에서 옮겨 적는다.
- 그림 예시 한 개: 챕터마다 첫 H2 아래에 아래 형식의 플레이스홀더 그림을 하나 넣는다. 파일은 `figures/` 아래에 실제로 존재하는 회색 플레이스홀더 PNG(1280×800, 가운데에 그림 ID 텍스트)를 생성해 둔다.
  `![캡션](figures/ch05-01-placeholder.png){#fig-ch05-01}`
- 영상 링크 예시: 5장, 6장, 10장, 12장에는 `{{< qrlink ID >}}` 숏코드 플레이스홀더를 하나씩 넣는다 (아래 4번 참고).
- 트랙 표시: 13장은 `::: {.callout-tip title="코딩학원 원장 트랙"}`, 14장은 `::: {.callout-tip title="일반학원 원장 트랙"}` 콜아웃으로 챕터 첫머리를 감싼다. 1장과 2장에도 두 트랙 콜아웃 예시를 하나씩 넣어 형식을 보여준다.

**목차** (파일명 → 제목 → 소제목):

들어가며 — `index.qmd`
- 외주 견적서 300만원 vs 오늘 밤 한 시간
- 4주 뒤 원장님 손에 남는 세 가지: 홈페이지 URL, 문의 폼, 우리 과목 게임
- 저자의 고백: 6개월 만에 커리큘럼이 끊겼던 날
- 이 책 읽는 법 — 코딩학원 원장 트랙 / 일반학원 원장 트랙

1부. 준비 (읽기만 해도 되는 부분)
- `ch01-ai-era.qmd` — 1장. AI가 코드를 써주는 시대, 학원은 무엇을 파는가
  - 네이버 블로그·카카오채널·전단지의 한계
  - "만들 수 있는 사람"과 "시킬 수 있는 사람"
  - 바이브코딩: 대화로 만들기
- `ch02-prep.qmd` — 2장. 30분 준비물
  - 계정 세 개 (AI 도구, 배포 서비스, 도메인)
  - 원장의 첫 프롬프트 — 잘 시키는 법 다섯 가지
  - 망쳐도 되돌릴 수 있다는 것

2부. 1주차 — 오늘 밤에 링크 하나 만들기
- `ch03-page-design.qmd` — 3장. 학부모가 5초 안에 보는 것 — 페이지 설계
  - 위치, 대상, 과목, 연락처
  - 우리 학원 한 줄 소개 쓰기
- `ch04-build-page.qmd` — 4장. 대화로 페이지 만들기 (따라하기)
  - 첫 화면 만들기
  - 수정 요청하기
  - 사진 넣기
  - 모바일에서 확인하기
- `ch05-deploy.qmd` — 5장. 배포: 세상에 URL 만들기
  - 무료 배포 서비스로 올리기
  - 카카오톡으로 링크 보내보기
  - 흔한 오류 다섯 가지

3부. 2주차 — 상담 문의 받기
- `ch06-contact-form.qmd` — 6장. 문의 폼 붙이기
  - 폼 서비스 연결
  - 이메일·카카오 알림으로 받기
- `ch07-privacy.qmd` — 7장. 개인정보, 원장이 알아야 할 최소한
  - "저장하지 않는다"는 원칙 — 학생 정보를 내 서버에 두지 않는 이유
  - 수집 최소화와 동의 문구
  - 절대 하지 말 것 목록

4부. 3주차 — 우리 과목으로 게임 만들기
- `ch08-why-games.qmd` — 8장. 왜 게임인가
  - 학생들이 실제로 만든 것들 (주장 없이 작품만 보여준다)
- `ch09-game-recipes.qmd` — 9장. 과목별 미니게임 레시피
  - 영어단어 맞추기
  - 구구단 스피드
  - 한자 짝맞추기
  - 과학 OX 퀴즈
  - 코딩학원용: 점프 게임
  - (각 레시피는 프롬프트 / 완성 예시 / 변형 아이디어 세 소절로 구성)
- `ch10-polish-deploy.qmd` — 10장. 다듬기와 배포
  - 점수와 타이머
  - 이름 없는 순위표
  - 홈페이지에 게임 붙이기

5부. 4주차 — 보여주고, 듣고, 고치기
- `ch11-share.qmd` — 11장. 만든 것을 보여주는 용기
  - 발표회
  - 피드백 주고받는 규칙
- `ch12-lounge-upload.qmd` — 12장. 라운지에 올리기 (실습)
  - 업로드 → 반응 확인 → 수정 → 다시 올리기
  - 원장이 겪은 그대로 학생이 겪는다

6부. 그 다음 — 학원에 적용하기
- `ch13-for-coding-academy.qmd` — 13장. 코딩학원 원장님께
  - 학생에게 이 과정을 어떻게 시킬 것인가
  - 강의식이 아니라 자기주도로 — 과제 공급과 코칭이라는 문제
- `ch14-for-general-academy.qmd` — 14장. 일반학원 원장님께 — 강사 없이 부설 코딩반 여는 법
  - 원장이 감독자가 되는 구조
  - 실패하는 부설반의 공통점
- `ch15-lounge.qmd` — 15장. 렛츠코딩 라운지가 하는 일과 하지 않는 일
  - "가맹비 없는 프랜차이즈"라는 말의 뜻
  - 솔직한 한계

부록 (`appendices`로 등록)
- `appendix-a-prompts.qmd` — A. 복붙용 프롬프트 모음 (홈페이지 / 폼 / 게임별 H2)
- `appendix-b-troubleshooting.qmd` — B. 오류 해결 사전
- `appendix-c-privacy-checklist.qmd` — C. 개인정보 체크리스트
- `appendix-d-cohort-schedule.qmd` — D. 원장 코호트 4주 진행표
- `appendix-e-glossary.qmd` — E. 용어 사전

### 3. 그림 관리 — `figures/figures.csv` + `scripts/check_figures.py`
CSV 컬럼: `id, chapter, file, tool, tool_version, os, captured_at, window_size, caption, status, notes`
- `status`는 `todo | current | stale` 중 하나.
- 위에서 만든 플레이스홀더 그림들을 `status=todo`로 미리 등록.

`scripts/check_figures.py`:
- 모든 `.qmd`에서 `figures/…png|jpg|svg` 참조를 긁어 (a) CSV에 없는 참조, (b) 디스크에 없는 파일, (c) CSV에는 있는데 어느 챕터도 참조하지 않는 그림을 표로 출력.
- 옵션 `--stale --tool <이름> --before <버전>`: 해당 도구의 지정 버전 이전에 찍은 그림을 일괄 `stale`로 표시하고 목록 출력.
- 옵션 `--todo`: `status=todo`인 그림 목록만 챕터 순으로 출력.
- 종료 코드: 문제가 있으면 1.

### 4. QR·링크 관리 — `links/links.csv` + `scripts/gen_qr.py` + `qrlink` 숏코드
`links/links.csv` 컬럼: `id, short_path, target_url, kind, chapter, title, notes`
- `kind`는 `video | page`.
- `short_path`는 `/b/05-1` 형식. 실제 목적지(`target_url`)는 유튜브나 웹판 페이지. 책에는 항상 `https://letscoding.kr` + `short_path`만 실린다 (도메인은 `_quarto.yml`이나 별도 설정 파일의 변수로).
- 예시 행 4개(5장, 6장, 10장, 12장)를 `target_url`은 `TODO`로 채워 넣는다.

`scripts/gen_qr.py` (Python, `qrcode[pil]` 사용):
- 각 행에 대해 `assets/qr/<id>.png`와 `.svg` 생성. 오류 정정 H, 조용한 영역 4모듈, PNG는 300dpi 인쇄 시 최소 2cm가 되도록 충분히 크게(한 변 600px 이상).
- `links/links.json` 생성 (숏코드가 읽음).
- `links/_redirects` 생성 — Cloudflare Pages 리다이렉트 형식(`/b/05-1  https://…  302`). 필요하면 `links/redirects.json`도.
- `target_url`이 `TODO`인 행은 경고만 출력하고 QR은 짧은 주소로 만든다(짧은 주소는 이미 확정이므로).

`qrlink` 숏코드 — `_extensions/letscoding/qrlink/` 에 Quarto 확장(Lua)으로 구현. `{{< qrlink 05-1 >}}` 사용법:
- `links/links.json`에서 id를 찾는다. 없으면 빌드 경고 + 눈에 띄는 플레이스홀더 출력.
- HTML 출력: `kind=video`면 유튜브 URL에서 영상 ID를 뽑아 반응형 iframe으로 임베드하고, 아래에 제목과 짧은 주소를 표시. `kind=page`면 제목·짧은 주소를 카드형 링크로.
- EPUB·PDF 출력: `assets/qr/<id>.png` 이미지(너비 약 2.5cm) + 제목 + 짧은 주소(고정폭 글꼴)를 한 블록으로. 전자책 독자를 위해 짧은 주소는 클릭 가능한 링크로도 넣는다.

### 5. 편의 파일
- `Makefile` (또는 `justfile`): `make html`, `make epub`, `make pdf`, `make all`, `make qr`, `make check`, `make serve`(quarto preview).
- `requirements.txt`: qrcode[pil] 등.
- `README.md` (한국어): 설치(Quarto, Python, 폰트), 폴더 구조, 집필 워크플로(그림 추가 → CSV 등록 → 체크 → 빌드), 캡처 규칙(창 1280×800·2배율 캡처, 밝은 테마, 한국어 UI, 파일명 `chNN-MM-설명.png`), 링크 추가 규칙, 빌드 명령, 어느 PDF 엔진을 썼는지.
- `STYLE.md` (한국어): 원고 규칙 — 존댓말 "~해요"체, 캡처는 클릭 위치를 보여줄 때만 쓰고 결과는 텍스트로, 성과 주장 대신 실제 작품만 보여주기, **가격·계약 조건은 책에 넣지 않고 웹판 링크로**, 라운지 상품 언급은 12장·15장에서만, 학생·학부모 실명 및 개인정보 사용 금지.

## 하지 말 것
- 본문 문장을 지어내지 않는다. 집필 메모 주석과 플레이스홀더만.
- 가격, 요금제, 계약 조건을 어디에도 쓰지 않는다.
- 실제 학원·학생·학부모 이름을 쓰지 않는다.

## 검증
1. `quarto render --to html`, `--to epub`, PDF 순으로 빌드해 오류 없이 통과할 것. Quarto가 없으면 설치한다.
2. `python scripts/gen_qr.py` 실행 → QR 파일과 links.json, _redirects가 생기고 숏코드가 세 포맷에서 모두 렌더링되는지 확인.
3. `python scripts/check_figures.py` 실행 → 플레이스홀더 그림이 전부 `todo`로 잡히고 참조 누락이 0인지 확인.
4. 끝나면 폴더 트리, 빌드 명령, 내가 다음에 채워야 할 것(표지, 폰트, links.csv의 TODO, 본문) 목록을 짧게 정리해서 보고.