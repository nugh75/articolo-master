-- Lua filter to promote headings by one level.
-- Converts level 2 (##) headings to level 1, etc.,
-- leaving level 1 headings untouched.

function Header(el)
  if el.level > 1 then
    el.level = el.level - 1
  end
  return el
end
