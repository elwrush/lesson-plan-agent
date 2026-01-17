# Color Palettes for Reveal.js Presentations

Pre-defined, coherent color palettes based on [Material Design Color System](https://m2.material.io/design/color/the-color-system.html).

## How to Use

In your presentation's `<style>` block, override the CSS variables:

```html
<style>
    :root {
        --primary: #00F2FF;
        --secondary: #7000ff;
        --bg-dark: #050811;
        --text-accent: #FFD700;
        --glass: rgba(10, 10, 20, 0.95);
    }
</style>
```

---

## Available Palettes

### 1. Cyber-Gamer (Default)
**Theme**: Futuristic, high-energy, gaming aesthetics

| Variable       | Value     | Description        |
|----------------|-----------|--------------------|
| `--primary`    | `#00F2FF` | Cyan               |
| `--secondary`  | `#7000ff` | Purple             |
| `--bg-dark`    | `#050811` | Deep navy          |
| `--text-accent`| `#FFD700` | Gold               |
| `--glass`      | `rgba(10, 10, 20, 0.95)` |

---

### 2. Indigo Nightfall
**Theme**: Professional, calm, trustworthy

| Variable       | Value     | Description        |
|----------------|-----------|--------------------|
| `--primary`    | `#5C6BC0` | Indigo 400         |
| `--secondary`  | `#7986CB` | Indigo 300         |
| `--bg-dark`    | `#1A237E` | Indigo 900         |
| `--text-accent`| `#FFEB3B` | Yellow 500         |
| `--glass`      | `rgba(26, 35, 126, 0.95)` |

---

### 3. Teal Horizon
**Theme**: Fresh, modern, balanced

| Variable       | Value     | Description        |
|----------------|-----------|--------------------|
| `--primary`    | `#26A69A` | Teal 400           |
| `--secondary`  | `#4DB6AC` | Teal 300           |
| `--bg-dark`    | `#004D40` | Teal 900           |
| `--text-accent`| `#FFECB3` | Amber 100          |
| `--glass`      | `rgba(0, 77, 64, 0.95)` |

---

### 4. Deep Purple
**Theme**: Creative, imaginative, premium

| Variable       | Value     | Description        |
|----------------|-----------|--------------------|
| `--primary`    | `#7E57C2` | Deep Purple 400    |
| `--secondary`  | `#9575CD` | Deep Purple 300    |
| `--bg-dark`    | `#311B92` | Deep Purple 900    |
| `--text-accent`| `#B2FF59` | Light Green A200   |
| `--glass`      | `rgba(49, 27, 146, 0.95)` |

---

### 5. Blue Grey Steel
**Theme**: Corporate, neutral, serious

| Variable       | Value     | Description        |
|----------------|-----------|--------------------|
| `--primary`    | `#78909C` | Blue Grey 400      |
| `--secondary`  | `#90A4AE` | Blue Grey 300      |
| `--bg-dark`    | `#263238` | Blue Grey 900      |
| `--text-accent`| `#FFFFFF` | White              |
| `--glass`      | `rgba(38, 50, 56, 0.95)` |

---

### 6. Amber Sunrise
**Theme**: Warm, energetic, optimistic

| Variable       | Value     | Description        |
|----------------|-----------|--------------------|
| `--primary`    | `#FFB300` | Amber 600          |
| `--secondary`  | `#FFC107` | Amber 500          |
| `--bg-dark`    | `#E65100` | Orange 900         |
| `--text-accent`| `#FFFFFF` | White              |
| `--glass`      | `rgba(230, 81, 0, 0.95)` |

---

### 7. Green Forest
**Theme**: Natural, calming, growth

| Variable       | Value     | Description        |
|----------------|-----------|--------------------|
| `--primary`    | `#66BB6A` | Green 400          |
| `--secondary`  | `#81C784` | Green 300          |
| `--bg-dark`    | `#1B5E20` | Green 900          |
| `--text-accent`| `#FFF59D` | Yellow 200         |
| `--glass`      | `rgba(27, 94, 32, 0.95)` |

---

### 8. Red Alert
**Theme**: Urgent, powerful, attention-grabbing

| Variable       | Value     | Description        |
|----------------|-----------|--------------------|
| `--primary`    | `#EF5350` | Red 400            |
| `--secondary`  | `#E57373` | Red 300            |
| `--bg-dark`    | `#B71C1C` | Red 900            |
| `--text-accent`| `#FFEB3B` | Yellow 500         |
| `--glass`      | `rgba(183, 28, 28, 0.95)` |

---

### 9. Light Blue Ocean
**Theme**: Open, refreshing, inviting

| Variable       | Value     | Description        |
|----------------|-----------|--------------------|
| `--primary`    | `#29B6F6` | Light Blue 400     |
| `--secondary`  | `#4FC3F7` | Light Blue 300     |
| `--bg-dark`    | `#01579B` | Light Blue 900     |
| `--text-accent`| `#FFEE58` | Yellow 400         |
| `--glass`      | `rgba(1, 87, 155, 0.95)` |

---

### 10. Pink Blossom
**Theme**: Playful, youthful, creative

| Variable       | Value     | Description        |
|----------------|-----------|--------------------|
| `--primary`    | `#EC407A` | Pink 400           |
| `--secondary`  | `#F48FB1` | Pink 200           |
| `--bg-dark`    | `#880E4F` | Pink 900           |
| `--text-accent`| `#E1F5FE` | Light Blue 50      |
| `--glass`      | `rgba(136, 14, 79, 0.95)` |

---

## Creating Custom Palettes

1. Use [Material Design Color Tool](https://m2.material.io/resources/color/) to generate a palette.
2. Pick a **Primary** color (main brand/theme color).
3. Pick a **Secondary** color (complementary or analogous).
4. Use the **900 shade** for `--bg-dark` (dark backgrounds).
5. Use a contrasting light color for `--text-accent`.
6. Ensure sufficient contrast for accessibility.

---

## Segue Slide Backgrounds

> [!IMPORTANT]
> **Segue slides should ALWAYS use a high-contrast, dark gradient background** regardless of the selected palette. This ensures visual separation and dramatic impact for phase transitions.

**Recommended Pattern:**
```html
<section data-background-gradient="radial-gradient(circle, #1a1a2e 0%, #0f0f1a 100%)">
    <slide-segue title="PHASE 1"></slide-segue>
</section>
```

The gradient should fade from a slightly lighter dark tone (center) to a deeper black (edges). Avoid using `--secondary` for segue backgrounds as it may not provide sufficient contrast with all palettes.

---

## Header Contrast Rule

> [!CAUTION]
> **Slide Headers (H2) must ALWAYS be WHITE** (`#FFFFFF`) with a strong drop shadow.

**Rationale**: Projectors often wash out colors. Using palette colors (like grey or dark blue) for headers can lead to unreadable titles on dark backgrounds. White ensures maximum contrast.

**Implementation**:
```css
.reveal h2 { 
    color: white !important;
    text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.9), 0 0 10px rgba(0, 0, 0, 0.5);
}
```
*Do not override this rule in individual palettes.*
