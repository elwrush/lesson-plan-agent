# Code Reference (Copy-Paste Snippets)

> **Purpose**: Raw code for copying into presentations.  
> **NOT for documentation**: See `COMPONENTS.md` for usage guidelines.  
> **NOT for decisions**: See `DECISION_TREE.md` for "which to use when" logic.

---

/* TYPOGRAPHY: PRESENTATION SCALING */
.reveal h1 { font-size: 80pt !important; }
.reveal h2 { font-size: 45pt !important; }
.reveal h3 { font-size: 35pt !important; }
.text-body { font-size: 30pt; line-height: 1.2; }
.text-small { font-size: 24pt; color: #cbd5e1; }

/* INTERACTIVE TIMER PILL */
.timer-pill {
    display: flex;
    align-items: center;
    gap: 15px;
    background: rgba(0, 0, 0, 0.8);
    border: 2px solid var(--gold);
    padding: 10px 25px;
    border-radius: 50px;
    margin-top: 30px;
}
.timer-display {
    font-family: 'Courier Prime', monospace;
    font-size: 40pt;
    font-weight: 800;
    color: var(--gold);
}
.start-btn {
    background: var(--gold);
    color: var(--navy);
    border: none;
    padding: 8px 15px;
    font-weight: 900;
    cursor: pointer;
    border-radius: 5px;
}
.start-btn.pause { background: var(--maroon); color: white; }

/* TABLES */
.slide-table {
    width: 100%;
    border-collapse: separate;
    border-spacing: 5px;
    font-size: 28px;
}
.slide-table th { background: var(--maroon); color: white; padding: 15px; font-weight: 800; }
.slide-table td { background: var(--glass); border: 1px solid var(--gold); padding: 15px; }

/* MASTER FRAME ARCHITECTURAL BACKER */
/* Move this to the .reveal container in style block */
/*
background: 
    radial-gradient(circle at center, transparent 30%, rgba(0,0,0,0.5) 100%),
    linear-gradient(rgba(255, 215, 0, 0.15) 1px, transparent 1px),
    linear-gradient(90deg, rgba(255, 215, 0, 0.15) 1px, transparent 1px),
    linear-gradient(45deg, rgba(166, 45, 38, 0.1) 25%, transparent 25%, transparent 50%, rgba(166, 45, 38, 0.1) 50%, rgba(166, 45, 38, 0.1) 75%, transparent 75%, transparent),
    radial-gradient(circle at 20% 30%, #1a2a45 0%, #0a192f 100%);
*/

/* NATIVE WEB COMPONENT: <timer-pill> */
/* Drop this into your script block once */
/*
class TimerPill extends HTMLElement {
    constructor() {
        super();
        this.duration = parseInt(this.getAttribute('duration')) || 5;
        this.timeLeft = this.duration * 60;
        this.timer = null;
    }
    connectedCallback() {
        this.render();
        this.updateDisplay();
        this.querySelector('.start-btn').onclick = () => this.toggle();
    }
    render() {
        this.innerHTML = `
            <div class="timer-pill">
                <div class="timer-display">00:00</div>
                <button class="start-btn">START</button>
            </div>
        `;
    }
    updateDisplay() {
        const m = Math.floor(this.timeLeft / 60).toString().padStart(2, '0');
        const s = (this.timeLeft % 60).toString().padStart(2, '0');
        this.querySelector('.timer-display').textContent = `${m}:${s}`;
    }
    toggle() {
        const btn = this.querySelector('.start-btn');
        const pill = this.querySelector('.timer-pill');
        if (this.timer) {
            clearInterval(this.timer);
            this.timer = null;
            btn.textContent = 'START';
        } else {
            btn.textContent = 'PAUSE';
            this.timer = setInterval(() => {
                if (this.timeLeft > 0) {
                    this.timeLeft--;
                    this.updateDisplay();
                    if (this.timeLeft === 30) warningSfx.play();
                    blipSfx.currentTime = 0; blipSfx.play();
                } else {
                    clearInterval(this.timer);
                    this.timer = null;
                    btn.textContent = 'DONE';
                    bellSfx.play();
                }
            }, 1000);
        }
    }
}
customElements.define('timer-pill', TimerPill);
*/

/* USAGE:
<timer-pill duration="5"></timer-pill>
*/

---

## Content Checklist Template

Use this format for Step 0.6 (Source Content Extraction):

```markdown
## Source Content Extraction Checklist

### From Lesson Plan:
- [ ] Stage 1: [name] - [key activity]
- [ ] Stage 2: [name] - [key activity]
...

### From Worksheet:
#### Task 1: [exact title]
- [ ] Question 1: "[exact wording]"
  - Answer: "[exact answer from key]"
- [ ] Question 2: "[exact wording]"
  - Answer: "[exact answer from key]"
...

### Total Counts:
- Tasks: X
- Questions: Y
- Answers to create: Y (1 slide per answer)
```

---

## Auto-Animate Patterns

### Before/After Sentence Transformation
```html
<!-- Before -->
<section data-auto-animate 
         data-auto-animate-duration="1.5" 
         data-auto-animate-easing="ease-in-out"
         data-background-color="var(--bg-dark)">
    <h2>Sentence Reduction</h2>
    <p data-id="sentence" style="font-size: 36px;">
        Michelangelo, <span data-id="remove" style="color: #ef4444; text-decoration: underline;">who was</span> a brilliant sculptor, carved...
    </p>
    <p style="font-size: 24px; color: #ef4444;">⬇ Watch the underlined words disappear ⬇</p>
</section>

<!-- After -->
<section data-auto-animate 
         data-auto-animate-duration="1.5" 
         data-auto-animate-easing="ease-in-out"
         data-background-color="var(--bg-dark)">
    <h2>Sentence Reduction</h2>
    <p data-id="sentence" style="font-size: 36px; color: var(--text-accent);">
        Michelangelo, a brilliant sculptor, carved...
    </p>
    <p style="font-size: 32px; color: var(--text-accent);">✓ We removed: <strong>who was</strong></p>
</section>
```

### Reusable Grammar Transform Component
```html
<grammar-transform 
    title="From Relative Clause to Appositive"
    before="Michelangelo, who was a brilliant sculptor, carved the statue of David."
    after="Michelangelo, a brilliant sculptor, carved the statue of David."
    highlight="who was">
</grammar-transform>
```

---

## Horizontal Layout Patterns

### ❌ BANNED: Narrow Centered Stacking
```html
<section>
    <h2>Title</h2>
    <div class="glass-box" style="width: 500px; margin: 0 auto;">
        <p>Content 1</p>
        <p>Content 2</p>
        <p>Content 3</p>
        <p>Content 4</p>  <!-- HIDDEN! -->
        <timer-pill></timer-pill>  <!-- HIDDEN! -->
    </div>
</section>
```

### ✅ CORRECT: Horizontal Split (Task Slide)
```html
<section>
    <div class="row-container">
        <div class="col-50">
            <img src="images/task.jpg" class="inset-media">
        </div>
        <div class="col-50">
            <div class="glass-box">
                <h3>Task Title</h3>
                <p>Instructions...</p>
                <timer-pill duration="5"></timer-pill>
            </div>
        </div>
    </div>
</section>
```

### ✅ CORRECT: Wide Glass Box (Multi-Content)
```html
<section>
    <h2>B2 Mission</h2>
    <div class="glass-box" style="width: 800px; margin: 0 auto;">
        <div style="display: flex; gap: 20px;">
            <div style="flex: 1;">Content A</div>
            <div style="flex: 1;">Content B</div>
        </div>
        <timer-pill duration="2"></timer-pill>
    </div>
</section>
```
