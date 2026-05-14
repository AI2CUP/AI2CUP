# Skill: Premium UI & UX Design

**Objective**: Maintain the high-end "Premium Dark" aesthetic of AI2CUP.

## 🎨 Design System

### 1. Color Palette (HSL)
Always use these CSS variables for consistency:
```css
:root {
  --bg-primary: hsl(220, 15%, 7%);    /* Rich, dark background */
  --bg-surface: hsla(220, 15%, 15%, 0.7); /* Translucent surface */
  --accent: hsl(30, 50%, 45%);        /* Bronze/Coffee accent */
  --text-main: hsl(0, 0%, 95%);       /* Off-white for readability */
  --glass-border: hsla(0, 0%, 100%, 0.1);
  --glass-blur: blur(12px);
}
```

### 2. Glassmorphism Patterns
Apply to cards, modals, and navigation bars:
- **Background**: `var(--bg-surface)`
- **Blur**: `backdrop-filter: var(--glass-blur)`
- **Border**: `1px solid var(--glass-border)`
- **Shadow**: `box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37)`

## ✨ Micro-Animations
- **Hover Transitions**: Use `transition: all 0.3s ease`.
- **Accent Glow**: On hover, add a subtle glow using the accent color:
  ```css
  .button:hover {
    box-shadow: 0 0 15px hsla(30, 50%, 45%, 0.3);
    transform: translateY(-2px);
  }
  ```

## 🏗 Typography
- Use `Inter`, `Outfit`, or `Roboto`.
- Letter spacing: `-0.02em` for headings to give a modern look.
