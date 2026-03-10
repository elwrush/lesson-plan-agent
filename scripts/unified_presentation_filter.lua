-- Pandoc Lua Filter for Unified Presentation Pipeline
-- Handles ESL-specific directives and layouts for Reveal.js and PPTX

function Span(el)
  -- 1. [text]{.highlight} -> Gold highlight
  if el.classes:includes('highlight') then
    if FORMAT == 'revealjs' or FORMAT == 'html' then
      return pandoc.RawInline('html', '<span class="text-gold">' .. pandoc.utils.stringify(el) .. '</span>')
    elseif FORMAT == 'pptx' then
      -- PPTX doesn't have native highlight well supported via pandoc, 
      -- but we can use Strong or Emph.
      return pandoc.Strong(el.content)
    end
  end

  -- 2. [text]{.reveal} -> Reveal.js Fragment
  if el.classes:includes('reveal') then
    if FORMAT == 'revealjs' or FORMAT == 'html' then
      return pandoc.RawInline('html', '<span class="fragment">' .. pandoc.utils.stringify(el) .. '</span>')
    elseif FORMAT == 'pptx' then
      -- Strip it out for PPTX
      return el.content
    end
  end

  return el
end

function Div(el)
  -- 3. ::: mission-badge
  if el.classes:includes('mission-badge') then
    if FORMAT == 'revealjs' or FORMAT == 'html' then
      local icon = el.attributes['icon'] or 'fa-star'
      local inner_html = pandoc.write(pandoc.Pandoc(el.content), 'html')
      inner_html = inner_html:gsub("^<p>", ""):gsub("</p>$", "")
      
      return pandoc.RawBlock('html', 
        '<div class="mission-badge"><i class="fas ' .. icon .. '"></i>' ..
        '<div style="color: white; font-size: 1.1em; line-height: 1.3; margin-top: 10px; text-align: center;">' ..
        inner_html .. '</div></div>'
      )
    elseif FORMAT == 'pptx' then
      -- For PPTX, render it as a simple list item or block
      local icon = el.attributes['icon'] or 'badge'
      return pandoc.Para({pandoc.Strong(icon .. ": "), table.unpack(pandoc.utils.blocks_to_inlines(el.content))})
    end
  end

  -- 4. Handle Layout Containers (Mission Badges)
  if el.classes:includes('mission-badges') then
    if FORMAT == 'revealjs' or FORMAT == 'html' then
      local inner_html = pandoc.write(pandoc.Pandoc(el.content), 'html')
      return pandoc.RawBlock('html', 
        '<div style="display: flex; flex-direction: row; justify-content: center; flex-wrap: wrap; gap: 20px; margin-top: 20px; width: 100%;">' ..
        inner_html .. '</div>'
      )
    elseif FORMAT == 'pptx' then
        return el.content
    end
  end

  return el
end

-- 6. Filter Background Attributes for PPTX (Remove Video, preserve images if possible)
function Header(el)
    if FORMAT == 'pptx' and el.level == 2 then
        -- Pandoc PPTX writer doesn't support data-background-video.
        -- We remove these to avoid corruption.
        el.attributes['data-background-video'] = nil
        el.attributes['data-background-video-loop'] = nil
        el.attributes['data-background-video-muted'] = nil
        
        -- If it's a mission slide, we'll give it a different marker or class
        -- and use the reference-doc's layouts if possible.
    end
    return el
end
