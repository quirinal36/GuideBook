# Graph Report - GuideBook  (2026-09-28)

## Corpus Check
- Corpus is ~14,297 words - fits in a single context window. You may not need a graph.

## Summary
- 140 nodes · 167 edges · 17 communities (12 shown, 5 thin omitted)
- Extraction: 77% EXTRACTED · 23% INFERRED · 1% AMBIGUOUS · INFERRED: 38 edges (avg confidence: 0.89)
- Token cost: unavailable — this session did not expose agent token usage; numeric zeros in cache/cost metadata are placeholders, not a measured zero cost.

## Community Hubs (Navigation)
- 바이브코딩 준비·학원 적용
- 문의 폼·게임 레시피
- 그림 등록·참조 검사
- Quarto 출판 설정
- 작품 공유·라운지 활용
- QR 생성·주소 관리
- 개인정보·게임 마무리
- qrlink 포맷별 출력
- 홈페이지 설계·제작
- 배포·오류 해결
- 플레이스홀더 이미지 생성
- PowerShell 빌드 명령
- 책 표지 플레이스홀더
- 5장 QR SVG
- 6장 QR SVG
- 10장 QR SVG
- 12장 QR SVG

## God Nodes (most connected - your core abstractions)
1. `과목별 미니게임 레시피` - 9 edges
2. `AI가 코드를 써주는 시대, 학원은 무엇을 파는가` - 6 edges
3. `30분 준비물` - 6 edges
4. `다듬기와 배포` - 6 edges
5. `고정 주소·QR·리다이렉트 흐름` - 6 edges
6. `cmd_stale()` - 5 edges
7. `main()` - 5 edges
8. `배포: 세상에 URL 만들기` - 5 edges
9. `문의 폼 붙이기` - 5 edges
10. `코딩학원 원장님께` - 5 edges

## Surprising Connections (you probably didn't know these)
- `AI가 코드를 써주는 시대, 학원은 무엇을 파는가` --references--> `Grey placeholder image labeled ch01-01`  [EXTRACTED]
  chapters/ch01-ai-era.qmd → figures/ch01-01-placeholder.png
- `30분 준비물` --references--> `ch02-01 — grey bordered placeholder image`  [EXTRACTED]
  chapters/ch02-prep.qmd → figures/ch02-01-placeholder.png
- `배포: 세상에 URL 만들기` --references--> `QR code 05-1`  [EXTRACTED]
  chapters/ch05-deploy.qmd → assets/qr/05-1.png
- `배포: 세상에 URL 만들기` --references--> `Gray bordered placeholder image with centered dark-gray label ch05-01`  [EXTRACTED]
  chapters/ch05-deploy.qmd → figures/ch05-01-placeholder.png
- `문의 폼 붙이기` --references--> `QR code (06-1)`  [EXTRACTED]
  chapters/ch06-contact-form.qmd → assets/qr/06-1.png

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **다섯 게임에 공통인 프롬프트·완성 예시·변형 아이디어 구성** — chapters_ch09_game_recipes_english_vocabulary_game, chapters_ch09_game_recipes_multiplication_speed_game, chapters_ch09_game_recipes_hanja_matching_game, chapters_ch09_game_recipes_science_ox_quiz, chapters_ch09_game_recipes_jump_game, chapters_ch09_game_recipes_recipe_structure [EXTRACTED 1.00]
- **폼 공개·정보 최소화·익명 순위표에 걸친 개인정보 보호 설계** — chapters_appendix_c_privacy_checklist_prepublication_privacy_checklist, chapters_ch06_contact_form_external_contact_form, chapters_ch07_privacy_data_minimization_consent, chapters_ch10_polish_deploy_anonymous_leaderboard [INFERRED 0.85]
- **One Korean manuscript published as HTML, EPUB and PDF** — prd_four_week_curriculum, readme_build_workflow, _quarto_book_configuration, _quarto_output_formats [INFERRED 0.95]
- **Mutable destinations behind permanent printed short URLs** — prd_link_pipeline, _variables_short_domain, _extensions_letscoding_qrlink__extension_qrlink, style_mutable_commercial_details [INFERRED 0.95]

## Communities (17 total, 5 thin omitted)

### Community 0 - "바이브코딩 준비·학원 적용"
Cohesion: 0.13
Nodes (18): 원장 코호트 4주 진행표, 가나다순 용어 사전, 용어 사전, AI가 코드를 써주는 시대, 학원은 무엇을 파는가, 네이버 블로그·카카오채널·전단지, 바이브코딩, 30분 준비물, 원장의 첫 프롬프트 (+10 more)

### Community 1 - "문의 폼·게임 레시피"
Cohesion: 0.13
Nodes (15): QR code (06-1), 홈페이지·폼·게임용 복붙 프롬프트, 복붙용 프롬프트 모음, 문의 폼 붙이기, 외부 문의 폼 서비스, 이메일·카카오 문의 알림, 과목별 미니게임 레시피, 영어단어 맞추기 (+7 more)

### Community 2 - "그림 등록·참조 검사"
Cohesion: 0.24
Nodes (14): 그림 대장과 상태 점검, 캡처·그림 등록·검사 절차, cmd_check(), cmd_stale(), cmd_todo(), collect_refs(), load_rows(), main() (+6 more)

### Community 3 - "Quarto 출판 설정"
Cohesion: 0.18
Nodes (14): Quarto 목차·책 기본 설정, HTML·EPUB·A5 PDF 출력 설정, Pretendard SIL OFL 라이선스, 4주 결과물: 홈페이지·폼·게임, 들어가며 원고 개요, 학원 원장 4주 과정, 개요·플레이스홀더 중심 초기 범위, Quarto HTML·EPUB·PDF 통합 빌드 (+6 more)

### Community 4 - "작품 공유·라운지 활용"
Cohesion: 0.15
Nodes (14): QR code, 왜 게임인가, 실제 학생 작품 전시, 코호트 발표회와 피드백 규칙, 만든 것을 보여주는 용기, 라운지에 올리기 (실습), 업로드 → 반응 확인 → 수정 → 다시 올리기, 렛츠코딩 라운지가 하는 일과 하지 않는 일 (+6 more)

### Community 5 - "QR 생성·주소 관리"
Cohesion: 0.21
Nodes (12): qrlink 숏코드 확장 등록, 공유 짧은 주소 도메인, 외주 견적과 작업 시간 비교, 고정 주소·QR·리다이렉트 흐름, main(), make_qr(), links/links.csv 로부터 QR 이미지, links.json, 리다이렉트 파일을 만든다. 생성물: assets/qr/<id>.png,…, _variables.yml 의 short-domain 값을 읽는다 (PyYAML 없이 한 줄 파싱). (+4 more)

### Community 6 - "개인정보·게임 마무리"
Cohesion: 0.17
Nodes (12): Black-and-white QR code, 개인정보 체크리스트, 홈페이지·폼 공개 전 개인정보 점검, 수집 최소화와 동의 문구, 개인정보, 원장이 알아야 할 최소한, 학생 정보를 내 서버에 저장하지 않는 원칙, 이름 없는 순위표, 다듬기와 배포 (+4 more)

### Community 7 - "qrlink 포맷별 출력"
Cohesion: 0.33
Nodes (7): esc(), missing(), project_relative(), render_html(), render_print(), render_typst(), typst_esc()

### Community 8 - "홈페이지 설계·제작"
Cohesion: 0.25
Nodes (8): 학원 한 줄 소개, 학부모가 5초 안에 보는 것 — 페이지 설계, 첫 화면의 위치·대상·과목·연락처, 대화로 첫 화면 생성·수정·사진 삽입, 대화로 페이지 만들기 (따라하기), 모바일 화면 확인, Grey placeholder image labeled ch03-01, ch04-01 — grey bordered placeholder image

### Community 9 - "배포·오류 해결"
Cohesion: 0.29
Nodes (7): QR code 05-1, 오류 해결 사전, 증상별 오류 찾아보기, 배포: 세상에 URL 만들기, 카카오톡 링크 열기 확인, 무료 배포와 공개 URL, Gray bordered placeholder image with centered dark-gray label ch05-01

### Community 10 - "플레이스홀더 이미지 생성"
Cohesion: 0.47
Nodes (5): Path, draw_placeholder(), load_font(), main(), figures/figures.csv 에 등록됐지만 디스크에 없는 그림을 회색 플레이스홀더 PNG로 만든다. 사용법: python…

### Community 11 - "PowerShell 빌드 명령"
Cohesion: 0.83
Nodes (3): Check(), Invoke-Step(), Qr()

## Ambiguous Edges - Review These
- `변동 요금·계약은 웹에 게시` → `외주 견적과 작업 시간 비교`  [AMBIGUOUS]
  index.qmd · relation: conceptually_related_to

## Knowledge Gaps
- **37 isolated node(s):** `가나다순 용어 사전`, `네이버 블로그·카카오채널·전단지`, `학원 한 줄 소개`, `카카오톡 링크 열기 확인`, `이메일·카카오 문의 알림` (+32 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 52 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **5 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **What is the exact relationship between `변동 요금·계약은 웹에 게시` and `외주 견적과 작업 시간 비교`?**
  _Edge tagged AMBIGUOUS (relation: conceptually_related_to) - confidence is low._
- **Why does `복붙용 프롬프트 모음` connect `문의 폼·게임 레시피` to `홈페이지 설계·제작`?**
  _High betweenness centrality (0.098) - this node is a cross-community bridge._
- **Are the 2 inferred relationships involving `과목별 미니게임 레시피` (e.g. with `복붙용 프롬프트 모음` and `다듬기와 배포`) actually correct?**
  _`과목별 미니게임 레시피` has 2 INFERRED edges - model-reasoned connections that need verification._
- **Are the 3 inferred relationships involving `AI가 코드를 써주는 시대, 학원은 무엇을 파는가` (e.g. with `용어 사전` and `코딩학원 원장님께`) actually correct?**
  _`AI가 코드를 써주는 시대, 학원은 무엇을 파는가` has 3 INFERRED edges - model-reasoned connections that need verification._
- **Are the 2 inferred relationships involving `30분 준비물` (e.g. with `코딩학원 원장님께` and `일반학원 원장님께 — 강사 없이 부설 코딩반 여는 법`) actually correct?**
  _`30분 준비물` has 2 INFERRED edges - model-reasoned connections that need verification._
- **Are the 3 inferred relationships involving `고정 주소·QR·리다이렉트 흐름` (e.g. with `qrlink 숏코드 확장 등록` and `공유 짧은 주소 도메인`) actually correct?**
  _`고정 주소·QR·리다이렉트 흐름` has 3 INFERRED edges - model-reasoned connections that need verification._
- **What connects `가나다순 용어 사전`, `네이버 블로그·카카오채널·전단지`, `학원 한 줄 소개` to the rest of the system?**
  _37 weakly-connected nodes found - possible documentation gaps or missing edges._
## Build Notes / 빌드 범위와 한계

- 60개 감지 파일: 코드 7개, 문서 29개, 이미지 24개. 문서·이미지 53개를 모두 분석했습니다.
- 장 원고는 개요·집필 메모 단계이며, 그림 15개와 표지는 플레이스홀더입니다.
- Graph health warning: 외부 import 대상 노드가 없는 참조 18건은 graphify가 최종 그래프에서 제외했습니다: argparse, csv, json, pathlib, pil, qrcode, qrcode_constants, qrcode_image_svg, re, sys.
- Graph health warning: 같은 두 노드 사이의 references / semantically_similar_to 관계 1건은 기본 무방향 단순 그래프에서 병합되었습니다. 대상: style_mutable_commercial_details → prd_link_pipeline. 상세 진단은 graph-health.json에 있습니다.
- Makefile, CSV, CSS, Typst 템플릿과 폰트 바이너리는 자동 감지 대상 밖입니다. 관련 흐름은 README·PRD·Quarto 설정에서 추출했으며 파일 자체의 전체 분석을 뜻하지 않습니다.
- python3 scripts/check_figures.py 통과: 등록·참조 15개, 누락·미등록·미사용 0건; 15개 모두 todo 상태입니다.
- Quarto 실행 파일이 없어 책 HTML·EPUB·PDF 렌더링은 실행하지 않았습니다. 이번 결과물은 graphify 지식 그래프입니다.
