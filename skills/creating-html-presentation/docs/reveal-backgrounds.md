# Reveal.js Backgrounds Reference

## Color Backgrounds

All CSS color formats supported: hex, keywords, `rgba()`, `hsl()`.

```html
<section data-background-color="aquamarine">
  <h2>🍦</h2>
</section>
<section data-background-color="rgb(70, 70, 255)">
  <h2>🍰</h2>
</section>
```

---

## Gradient Backgrounds

All CSS gradient formats supported: `linear-gradient`, `radial-gradient`, `conic-gradient`.

```html
<section data-background-gradient="linear-gradient(to bottom, #283b95, #17b2c3)">
  <h2>🐟</h2>
</section>
<section data-background-gradient="radial-gradient(#283b95, #17b2c3)">
  <h2>🐳</h2>
</section>
```

---

## Image Backgrounds

**⚠️ NOT RECOMMENDED FOR THIS PROJECT** (violates "Abstract Continuity" design philosophy).

```html
<section data-background-image="http://example.com/image.png">
  <h2>Image</h2>
</section>
<section 
  data-background-image="http://example.com/image.png"
  data-background-size="100px"
  data-background-repeat="repeat">
  <h2>Tiled Background</h2>
</section>
```

**Available Options**:
- `data-background-size`: CSS background-size
- `data-background-position`: CSS background-position
- `data-background-repeat`: CSS background-repeat

---

## Video Backgrounds

Automatically plays full-size video behind slide.

```html
<section 
  data-background-video="https://example.com/video.mp4"
  data-background-video-loop
  data-background-video-muted>
  <h2>Video</h2>
</section>
```

**Sizing**:
- `cover` (default): Fill entire slide
- `contain`: Fit within slide bounds

---

## Iframe Backgrounds

Embeds a web page as slide background (100% width/height).

```html
<section 
  data-background-iframe="https://slides.com"
  data-background-interactive>
  <h2>Iframe</h2>
</section>
```

**⚠️ Performance**: Use `data-preload` attribute or `preloadIframes` config option for ahead-of-time loading.

---

## Background Transitions

Default: Cross-fade between backgrounds.

**Config Option**: `backgroundTransition`

```javascript
Reveal.initialize({
  backgroundTransition: 'slide' // or 'fade', 'none', 'zoom', 'convex', 'concave'
});
```
