-- qrlink 숏코드: {{< qrlink 05-1 >}}
-- links/links.json (scripts/gen_qr.py 가 생성)에서 id 를 찾아
--   HTML      : video → 유튜브 반응형 임베드 + 제목·짧은 주소 / page → 카드형 링크
--   EPUB·PDF  : QR 이미지(약 2.5cm) + 제목 + 짧은 주소(고정폭, 클릭 가능)

local links_cache = nil

local function load_links()
  if links_cache then return links_cache end
  local path = pandoc.path.join({ quarto.project.directory, "links", "links.json" })
  local f = io.open(path, "r")
  if not f then
    quarto.log.warning("[qrlink] links/links.json 이 없습니다. python scripts/gen_qr.py 를 먼저 실행하세요.")
    links_cache = {}
    return links_cache
  end
  local data = quarto.json.decode(f:read("a"))
  f:close()
  links_cache = data.links or {}
  return links_cache
end

local function esc(s)
  return (tostring(s or ""):gsub("&", "&amp;"):gsub("<", "&lt;"):gsub(">", "&gt;"):gsub('"', "&quot;"))
end

-- 현재 문서 위치 기준으로 프로젝트 루트의 파일 경로를 만든다 (chapters/ 하위 문서 대응)
local function project_relative(rel)
  local abs = pandoc.path.join({ quarto.project.directory, rel })
  local doc_dir = pandoc.path.directory(quarto.doc.input_file)
  return pandoc.path.make_relative(abs, doc_dir)
end

local function missing(id)
  quarto.log.warning("[qrlink] links.json 에 없는 id: " .. tostring(id))
  if quarto.doc.is_format("html:js") then
    return pandoc.RawBlock("html",
      '<div class="qrlink qrlink-missing">⚠ qrlink: 알 수 없는 링크 ID “' .. esc(id) .. '” — links/links.csv 확인</div>')
  end
  return pandoc.Para({ pandoc.Strong({ pandoc.Str("⚠ [qrlink: 알 수 없는 링크 ID “" .. tostring(id) .. "”]") }) })
end

local function render_html(link)
  quarto.doc.add_html_dependency({
    name = "qrlink",
    version = "0.1.0",
    stylesheets = { "qrlink.css" },
  })
  local meta = '<span class="qrlink-title">' .. esc(link.title) .. '</span>'
    .. '<a href="' .. esc(link.short_url) .. '"><code>' .. esc(link.short_label) .. '</code></a>'
  if link.kind == "video" and link.youtube_id and link.youtube_id ~= pandoc.null then
    return pandoc.RawBlock("html",
      '<div class="qrlink">'
      .. '<div class="qrlink-video"><iframe src="https://www.youtube-nocookie.com/embed/' .. esc(link.youtube_id)
      .. '" title="' .. esc(link.title) .. '" loading="lazy" allowfullscreen '
      .. 'allow="accelerometer; clipboard-write; encrypted-media; gyroscope; picture-in-picture"></iframe></div>'
      .. '<div class="qrlink-meta">▶ ' .. meta .. '</div></div>')
  end
  local label = (link.kind == "video") and "▶ 영상 (준비 중)" or "🔗 바로가기"
  return pandoc.RawBlock("html",
    '<div class="qrlink"><a class="qrlink-card" href="' .. esc(link.short_url) .. '">'
    .. '<span class="qrlink-title">' .. esc(link.title) .. '</span>'
    .. label .. ' · <code>' .. esc(link.short_label) .. '</code></a></div>')
end

-- typst 마크업 특수문자 이스케이프
local function typst_esc(s)
  return (tostring(s or ""):gsub("([\\%*_#%[%]%$<>@`~=%-/])", "\\%1"))
end

-- PDF: QR 과 제목·짧은 주소를 좌우로 나란히 (페이지 사이에서 쪼개지지 않게)
-- typst book 은 프로젝트 루트의 index.typ 로 합쳐 컴파일되므로 이미지 경로는 루트 기준
local function render_typst(link)
  local prefix = (link.kind == "video") and "▶ 영상: " or "🔗 "
  return pandoc.RawBlock("typst",
    '#block(breakable: false, above: 1.2em, below: 1.2em, grid(columns: (2.5cm, 1fr), column-gutter: 1em, align: horizon,\n'
    .. '  image("' .. link.qr_png .. '", width: 2.5cm, alt: "QR 코드: ' .. link.short_label .. '"),\n'
    .. '  [*' .. typst_esc(prefix .. link.title) .. '* \\\n'
    .. '   #link("' .. link.short_url .. '")[#raw("' .. link.short_label .. '")]]\n'
    .. '))')
end

local function render_print(link)
  local img = pandoc.Image({ pandoc.Str("QR 코드: " .. link.short_label) }, project_relative(link.qr_png), "",
    { width = "2.5cm" })
  local prefix = (link.kind == "video") and "▶ 영상: " or "🔗 "
  return pandoc.Div({
    pandoc.Plain({ img }),
    pandoc.Para({ pandoc.Strong({ pandoc.Str(prefix .. link.title) }) }),
    pandoc.Para({ pandoc.Link({ pandoc.Code(link.short_label) }, link.short_url) }),
  }, pandoc.Attr("", { "qrlink" }))
end

return {
  ["qrlink"] = function(args, kwargs, meta)
    local id = args[1] and pandoc.utils.stringify(args[1]) or ""
    local link = load_links()[id]
    if not link then return missing(id) end
    if quarto.doc.is_format("html:js") then
      return render_html(link)
    end
    if quarto.doc.is_format("typst") then
      return render_typst(link)
    end
    return render_print(link)
  end
}
