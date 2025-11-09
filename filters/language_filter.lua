--[[
Language Filter and Reordering for Pandoc
-----------------------------------------

Supports HTML-style language markers:
  <!-- lang:en --> ... <!-- /lang:en -->
  <!-- lang:it --> ... <!-- /lang:it -->

Usage:
  pandoc input.md -L language_filter.lua -M lang=en   # English only
  pandoc input.md -L language_filter.lua -M lang=it   # Italian only
  pandoc input.md -L language_filter.lua -M lang=both # English first, then Italian

Rules:
  * Content without markers is treated as English-only.
  * When building bilingual outputs (lang=both), English content is emitted first,
    followed by Italian content. A page break separates the two sections.
  * Each language block is wrapped in a Div with attribute {lang="en|it"} so that
    downstream filters (e.g., custom numbering) can reset counters per language.
]]

local target_lang = "both"
local lang_stack = {}

local function meta_to_string(value)
  if not value then
    return nil
  end
  local str = pandoc.utils.stringify(value)
  if str == "" then
    return nil
  end
  return str
end

local function string_to_inlines(str)
  local doc = pandoc.read(str, "markdown")
  if #doc.blocks > 0 then
    local block = doc.blocks[1]
    if block.t == "Plain" or block.t == "Para" then
      return block.c
    end
  end
  return { pandoc.Str(str) }
end

local function build_title_inlines(lines)
  local combined = {}
  for idx, line in ipairs(lines) do
    if idx > 1 then
      -- Add a blank line between localized titles for visual separation
      table.insert(combined, pandoc.LineBreak())
      table.insert(combined, pandoc.LineBreak())
    end
    local inlines = string_to_inlines(line)
    for _, inline in ipairs(inlines) do
      table.insert(combined, inline)
    end
  end
  return combined
end

local function set_meta_title(meta, lines)
  if not lines or #lines == 0 then
    return
  end
  meta.title = pandoc.MetaInlines(build_title_inlines(lines))
end

local function current_lang()
  if #lang_stack == 0 then
    return "en" -- default fallback
  end
  return lang_stack[#lang_stack]
end

local function push_lang(value)
  table.insert(lang_stack, value)
end

local function pop_lang(value)
  if #lang_stack == 0 then
    return
  end
  local top = lang_stack[#lang_stack]
  if top == value then
    table.remove(lang_stack)
  else
    -- Unbalanced markers: remove anyway to avoid corrupting following content
    table.remove(lang_stack)
  end
end

local function is_lang_start(block)
  if block.t ~= "RawBlock" or block.format ~= "html" then
    return nil
  end
  return block.text:match("^<!%-%-%s*lang:(%w+)%s*%-%->%s*$")
end

local function is_lang_end(block)
  if block.t ~= "RawBlock" or block.format ~= "html" then
    return nil
  end
  return block.text:match("^<!%-%-%s*/lang:(%w+)%s*%-%->%s*$")
end

local function add_block(dest, block)
  table.insert(dest, block)
end

local function clone_block(block)
  return pandoc.utils.deepcopy(block)
end

local function assign_block(block, english_blocks, italian_blocks)
  local lang = current_lang()
  if lang == "it" then
    add_block(italian_blocks, block)
  elseif lang == "both" then
    add_block(english_blocks, clone_block(block))
    add_block(italian_blocks, block)
  else
    add_block(english_blocks, block)
  end
end

local function wrap_language_block(lang, blocks)
  local classes = { "lang-section", lang .. "-section" }
  local attr = pandoc.Attr(lang .. "-section", classes, { lang = lang })
  return pandoc.Div(blocks, attr)
end

local function page_break_blocks()
  return {
    pandoc.RawBlock("latex", "\\clearpage"),
    pandoc.RawBlock("openxml", "<w:p><w:r><w:br w:type=\"page\"/></w:r></w:p>"),
    pandoc.RawBlock("html", "<div style=\"page-break-after: always;\"></div>")
  }
end

local function update_titles(meta)
  local title_en = meta_to_string(meta.title)
  local title_it = meta_to_string(meta["title-it"])

  if target_lang == "en" then
    if title_en then
      set_meta_title(meta, { title_en })
    end
  elseif target_lang == "it" then
    if title_it then
      set_meta_title(meta, { title_it })
    elseif title_en then
      set_meta_title(meta, { title_en })
    end
  else
    if title_en and title_it then
      set_meta_title(meta, { title_en, title_it })
    elseif title_en then
      set_meta_title(meta, { title_en })
    elseif title_it then
      set_meta_title(meta, { title_it })
    end
  end
end

function Meta(meta)
  if meta.lang then
    target_lang = pandoc.utils.stringify(meta.lang)
  else
    target_lang = "both"
  end
  update_titles(meta)
  return meta
end

local function split_blocks(blocks)
  local english_blocks, italian_blocks = {}, {}
  lang_stack = {}

  for _, block in ipairs(blocks) do
    local start_lang = is_lang_start(block)
    if start_lang then
      push_lang(start_lang)
    else
      local end_lang = is_lang_end(block)
      if end_lang then
        pop_lang(end_lang)
      else
        assign_block(block, english_blocks, italian_blocks)
      end
    end
  end

  return english_blocks, italian_blocks
end

function Pandoc(doc)
  local english_blocks, italian_blocks = split_blocks(doc.blocks)
  local new_blocks = {}

  if target_lang == "en" then
    new_blocks = english_blocks
  elseif target_lang == "it" then
    new_blocks = italian_blocks
  else
    if #english_blocks > 0 then
      add_block(new_blocks, wrap_language_block("en", english_blocks))
    end

    if #english_blocks > 0 and #italian_blocks > 0 then
      for _, blk in ipairs(page_break_blocks()) do
        add_block(new_blocks, blk)
      end
    end

    if #italian_blocks > 0 then
      add_block(new_blocks, wrap_language_block("it", italian_blocks))
    end
  end

  doc.blocks = new_blocks
  return doc
end
