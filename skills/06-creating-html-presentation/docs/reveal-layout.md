# Reveal.js Layout Reference

## Core Layout Helpers

### `.r-stack`
**Purpose**: Center and stack multiple elements on top of each other.
**Use Case**: Incremental reveals with fragments.

```html
<div class="r-stack">
  <img class="fragment" src="image1.jpg" width="450" height="300" />
  <img class="fragment" src="image2.jpg" width="300" height="450" />
  <img class="fragment" src="image3.jpg" width="400" height="400" />
</div>
```

### `.r-fit-text`
**Purpose**: Makes text as large as possible without overflowing the slide.
**Use Case**: BIG headlines without manual font sizing.

```html
<h2 class="r-fit-text">BIG HEADLINE</h2>
```

**⚠️ Limitation**: Use ONLY for long text (> 40 chars). For short titles, use fixed 80pt sizing.

### `.r-stretch`
**Purpose**: Resize an element to cover remaining vertical space.
**Use Case**: Full-height images/videos with title + byline.

```html
<h2>Stretch Example</h2>
<img class="r-stretch" src="image.png" />
<p>Image byline</p>
```

**⚠️ Limitations**:
- Only direct descendants of `<section>` can be stretched
- Only ONE descendant per slide can be stretched

### `.r-frame`
**Purpose**: Decorative border around images/elements.
**Use Case**: Make focal images stand out.

```html
<a href="#">
  <img class="r-frame" src="logo.svg" width="200" />
</a>
```

---

## Viewport & Slide Structure

### Required Hierarchy
```
.reveal > .slides > section
```

- `.reveal`: Main container (viewport)
- `.slides`: Slide wrapper
- `section`: Individual slide

### Vertical Slides
Nest `<section>` elements to create vertical navigation:

```html
<section>Horizontal Slide</section>
<section>
  <section>Vertical Slide 1</section>
  <section>Vertical Slide 2</section>
</section>
```

---

## Slide States

### `data-state` Attribute
Apply custom CSS classes to the viewport based on active slide:

```html
<section data-state="make-it-pop"></section>
```

```css
/* CSS */
.make-it-pop {
  filter: drop-shadow(0 0 10px purple);
}
```

**JavaScript Hook**:
```javascript
Reveal.on('make-it-pop', () => {
  console.log('✨');
});
```
