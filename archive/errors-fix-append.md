
---

## 2025-12-30 (Evening) | Worksheet Generation - Bell Header Confusion

### Bell Header Parameter Misunderstanding
- **Issue**: Agent initially removed "Bell Language Centre" strap line thinking it was duplicate
- **Cause**: Misunderstood the header structure - user passed "Bell Language Centre|Useful Language" but template already has "Bell Language Centre" as a hardcoded strap line
- **Root Problem**: Skill documentation wasn't clear that `--header-title` should ONLY contain the topic/title, NOT "Bell Language Centre"
- **Fix**: 
  1. Restored "Bell Language Centre" as hardcoded top strap line in template
  2. Updated skill documentation with clear section explaining Bell header structure
  3. Added examples showing correct vs incorrect usage
- **Lesson**: Template has TWO lines in Bell header: (1) "Bell Language Centre" strap (hardcoded), (2) Custom title from `--header-title` parameter. Users should only pass the topic name.

### Quote Parameter Showing "None"
- **Issue**: When `--quote` parameter was omitted, template displayed "None" instead of hiding the section
- **Cause**: Template used `{{ quote | default('Topic Quote Here') }}` which shows "None" for Python None values
- **Fix**: Wrapped quote section in `{% if quote %}` conditional to completely hide when omitted
- **Additional**: Added automatic padding (margin-top: 8mm) when quote is absent to maintain spacing

### Thanking Section Too Long
- **Issue**: Worksheet spilled to 5 pages due to verbose bullet lists
- **Cause**: "Thanking Your Audience" used 4 bullet points with spacing
- **Fix**: Changed to pipe-separated format: "Thank you for listening | Thanks for your attention | ..."
- **Result**: Compressed section vertically while maintaining all content

### Missing PDF Link in Completion Message
- **Issue**: User couldn't easily access the generated PDF
- **Fix**: Added reminder to skill documentation: "IMPORTANT: Always provide the file link to the generated PDF after completion"
- **Workflow**: Always include markdown link after PDF generation

