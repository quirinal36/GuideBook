// PDF(typst) 폰트 설정
// Quarto 의 typst book(orange-book 템플릿)은 mainfont/codefont 옵션을 반영하지 않아 여기서 직접 지정한다.
// 목록 앞쪽 폰트가 없으면 다음 폰트로 넘어간다. 폰트 파일은 fonts/ (_quarto.yml 의 font-paths).
#set text(font: ("Pretendard", "Noto Sans KR"))
#show raw: set text(font: "D2Coding")   // 없으면 "Noto Sans Mono CJK KR" 등으로 교체
