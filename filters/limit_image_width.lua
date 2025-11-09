--[[
Limit image sizing for LaTeX/PDF outputs.

Pandoc turns percentage-based widths (e.g. width=100%) into
\includegraphics options that reserve the whole \textheight, which
creates oversized floats that hide the following text.  This filter
strips percentage-based width/height attributes so LaTeX can apply the
template defaults (\linewidth-constrained width with keepaspectratio).
]]

local function strip_percent_dimension(value)
  if not value then
    return nil
  end

  if value:match('%%%s*$') then
    return nil
  end

  return value
end

function Image(img)
  img.attributes.width = strip_percent_dimension(img.attributes.width)
  img.attributes.height = strip_percent_dimension(img.attributes.height)
  return img
end

return {
  { Image = Image }
}
