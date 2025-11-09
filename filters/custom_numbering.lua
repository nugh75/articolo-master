--[[
Custom section numbering filter.

Responsibilities:
  * Prefix headers with hierarchical numbers (e.g., "1.2 Title").
  * Skip numbering for headings containing "Introduction/Introduzione" or
    "Conclusion/Conclusioni" (case-insensitive).
  * Respect `.unnumbered` class if manually set.
  * Reset numbering whenever we enter a Div that carries the attribute `lang`
    (used to separate English and Italian sections in bilingual builds).
]]

local counters = {0, 0, 0, 0, 0, 0}
local secnumdepth = 3

local in_appendix = false

local function reset_from(level)
  for i = level or 1, #counters do
    counters[i] = 0
  end
end

local function normalize(text)
  text = text:lower()
  text = text:gsub("%b()", "")  -- remove parenthetical content
  text = text:gsub("[%c%p]", "")
  text = text:gsub("%s+", " ")
  text = text:gsub("^%s+", "")
  return text
end

local function is_intro_or_conclusion(text)
  local normalized = normalize(text)
  return normalized:match("^introduction") or
         normalized:match("^conclusion") or
         normalized:match("^introduzione") or
         normalized:match("^conclusione") or
         normalized:match("^conclusioni")
end

local function is_bibliography(text)
  local normalized = normalize(text)
  return normalized:match("^bibliography") or
         normalized:match("^references") or
         normalized:match("^bibliografia") or
         normalized:match("^riferimenti")
end

local function is_appendix_header(text)
  local normalized = normalize(text)
  return normalized:match("^appendix") or
         normalized:match("^appendice") or
         normalized:match("^appendici") or
         normalized:match("^appendices")
end

local function should_number(header)
  if header.classes:includes("unnumbered") then
    return false
  end
  if header.attributes["unnumbered"] == "true" then
    return false
  end
  local text = pandoc.utils.stringify(header.content)
  if in_appendix then
    return false
  end
  if is_intro_or_conclusion(text) then
    return false
  end
  if is_bibliography(text) then
    return false
  end
  return header.level <= secnumdepth
end

local function number_header(header)
  local text = pandoc.utils.stringify(header.content)
  if is_appendix_header(text) then
    in_appendix = true
  end

  if not should_number(header) then
    return header
  end

  counters[header.level] = counters[header.level] + 1
  for lvl = header.level + 1, #counters do
    counters[lvl] = 0
  end

  local parts = {}
  for lvl = 1, header.level do
    if counters[lvl] > 0 then
      table.insert(parts, tostring(counters[lvl]))
    end
  end
  local label = table.concat(parts, ".") .. " "
  table.insert(header.content, 1, pandoc.Str(label))
  return header
end

local function deep_copy_counters()
  local copy = {}
  for i = 1, #counters do
    copy[i] = counters[i]
  end
  return copy
end

function Pandoc(doc)
  if doc.meta.secnumdepth then
    local value = pandoc.utils.stringify(doc.meta.secnumdepth)
    local numeric = tonumber(value)
    if numeric then
      secnumdepth = numeric
    end
  end

  reset_from(1)
  in_appendix = false
  -- Process blocks with manual stack handling for language Divs.
  local function walk(blocks)
    local result = {}
    for _, block in ipairs(blocks) do
      if block.t == "Div" and block.attributes and block.attributes.lang then
        local snapshot = deep_copy_counters()
        local appendix_snapshot = in_appendix
        reset_from(1)
        in_appendix = false
        block.content = walk(block.content)
        table.insert(result, block)
        counters = snapshot
        in_appendix = appendix_snapshot
      elseif block.t == "Header" then
        table.insert(result, number_header(block))
      elseif block.t == "Div" then
        block.content = walk(block.content)
        table.insert(result, block)
      else
        table.insert(result, block)
      end
    end
    return result
  end

  doc.blocks = walk(doc.blocks)
  return doc
end
