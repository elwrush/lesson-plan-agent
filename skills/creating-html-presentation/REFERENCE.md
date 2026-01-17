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
