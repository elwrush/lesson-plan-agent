# Skill Validation Requirements

This document maps enforceable requirements from each skill to validator checks.

## 1. designing-slides

**Validator**: `skills/designing-slides/scripts/validate_slideshow_outline.py`

**Checks**:
- ✅ Answer key interleaving (CRITICAL ERROR if violated)
- ✅ Bullet point limit (max 7, warning at 7)
- ✅ Vocabulary format: `word /phonemic/: Thai translation`
- ✅ No image placeholders (`[image]`, `🖼️`, etc.)
- ✅ Mechanistic language detection (warnings)

**TODO**:
- Transition slides between major stages
- Font size minimums (24pt+ body, 44pt+ titles) - requires script analysis, not outline

---

## 2. generating-worksheets

**Validator**: `skills/generating-worksheets/scripts/validate_worksheet.py` ⚠️ NOT YET CREATED

**Required Checks**:
1. **Single-column text** (ERROR if 2-column CSS detected)
2. **Mandatory page break before Answer Key** (ERROR if missing `.page-break` div before answer key section)
3. **Orphan prevention CSS** (WARNING if missing)
   - Required rules:
     ```css
     table { break-inside: auto; }
     tr { break-inside: avoid; }
     thead { display: table-header-group; }
     h1, h2, h3 { break-after: avoid; }
     ```
4. **No duplicate headers** (ERROR if fragment contains `<img src=".../intensive-header.jpg">` or `bell-header.jpg`)
5. **Page break usage** (WARNING if page breaks mid-paragraph or mid-table)

**Implementation Priority**: HIGH (prevents layout regressions)

---

## 3. writing-lesson-plans

**Validator**: `skills/writing-lesson-plans/scripts/validate_lesson_plan.py` ⚠️ NOT YET CREATED

**Required Checks**:
1. **Shape compliance** (CRITICAL)
   - Extract selected shape from metadata
   - Compare stage structure against `knowledge_base/shapes/shape-[letter].yaml`
   - Verify stage names match shape requirements
2. **Timing validation**
   - Sum all stage times
   - ERROR if != total duration
   - WARNING if any single stage > 40% of total time
3. **Pre-teach vocabulary (Shape E-H only)**
   - ERROR if Shape E/F/G/H lesson has no "Pre-teach Vocabulary" stage
   - Format check: `/phonemic/: Thai translation` pattern
4. **Answer key presence**
   - If lesson uses exercises/tasks, must have Answer Key section
5. **Thai scaffolding**
   - Vocabulary items must include Thai translations
   - WARNING if Thai script not detected in vocab section

**Implementation Priority**: MEDIUM (prevents shape mismatches)

---

## 4. developing-bespoke-materials

**Validator**: Not required (meta-skill with soft guidelines)

**Notes**: This skill orchestrates other skills. Validation happens at the sub-skill level.

---

## Validation Workflow Pattern (All Skills)

```
1. Generate artifact (HTML/markdown outline)
2. 🔍 RUN VALIDATOR
3. 🚦 USER REVIEW (only proceed if validator passes + user approves)
4. Execute final action (push to API, generate PDF, etc.)
```

---

## Implementation Plan

### Phase 1: Critical Validators ✅
- [x] designing-slides validator (DONE)

### Phase 2: High Priority
- [ ] generating-worksheets validator
  - Check CSS for single-column layout
  - Check for `.page-break` before Answer Key
  - Check for duplicate headers

### Phase 3: Medium Priority  
- [ ] writing-lesson-plans validator
  - Shape compliance check
  - Timing validation
  - Pre-teach vocabulary verification

### Phase 4: Integration
- [ ] Update all SKILL.md files with validator workflow gates
- [ ] Test validators on existing materials
- [ ] Document validator usage in README.md
