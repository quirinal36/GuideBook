# 빌드 명령 모음. Windows 에서 make 가 없으면 같은 기능의 build.ps1 을 쓴다.
PYTHON ?= python
QUARTO ?= quarto

.PHONY: all html epub pdf qr check todo placeholders serve clean

# 세 포맷 한꺼번에 (한 번에 렌더해야 _book/ 에 모두 남는다)
all: qr check
	$(QUARTO) render

html: qr
	$(QUARTO) render --to html

epub: qr
	$(QUARTO) render --to epub

pdf: qr
	$(QUARTO) render --to typst

qr:
	$(PYTHON) scripts/gen_qr.py

check:
	$(PYTHON) scripts/check_figures.py

todo:
	$(PYTHON) scripts/check_figures.py --todo

placeholders:
	$(PYTHON) scripts/make_placeholders.py

serve: qr
	$(QUARTO) preview

clean:
	rm -rf _book .quarto
