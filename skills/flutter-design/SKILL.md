---
name: flutter-design
description: Create distinctive, production-grade Flutter interfaces with high design quality. Use when building Flutter screens, widgets, components, or apps (e.g., dashboards, onboarding flows, profile screens, or styling/beautifying any Flutter UI). Generates creative, polished Dart code and UI design that avoids generic AI aesthetics.
---

This skill guides creation of distinctive, production-grade Flutter interfaces that avoid generic "AI slop" aesthetics. Implement real working Dart/Flutter code with exceptional attention to aesthetic details and creative choices.

The user provides Flutter UI requirements: a screen, widget, component, or app to build. They may include context about purpose, audience, or technical constraints.

## Design Thinking

Before coding, understand the context and commit to a BOLD aesthetic direction:
- **Purpose**: What problem does this interface solve? Who uses it?
- **Tone**: Pick an extreme: brutally minimal, maximalist chaos, retro-futuristic, organic/natural, luxury/refined, playful/toy-like, editorial/magazine, brutalist/raw, art deco/geometric, soft/pastel, industrial/utilitarian, etc. Use these for inspiration but design one that is true to the aesthetic direction.
- **Constraints**: Technical requirements (Material 2/3, Cupertino, performance, accessibility).
- **Differentiation**: What makes this UNFORGETTABLE? What's the one thing someone will remember?

**CRITICAL**: Choose a clear conceptual direction and execute it with precision. Bold maximalism and refined minimalism both work - the key is intentionality, not intensity.

Then implement working Flutter code that is:
- Production-grade and functional
- Visually striking and memorable
- Cohesive with a clear aesthetic point-of-view
- Meticulously refined in every detail

## Flutter Aesthetics Guidelines

Focus on:

### Typography
Choose fonts that are beautiful, unique, and interesting. Avoid generic fonts like Roboto, Arial, and system defaults. Use `GoogleFonts` for distinctive choices:
- Pair a distinctive display font with a refined body font
- Use `TextTheme` and `ThemeData.textTheme` for consistency
- Consider `fontFamily`, `fontWeight`, `letterSpacing`, and `height` for character

```dart
// Example: Custom typography in ThemeData
final base = ThemeData(useMaterial3: true);
ThemeData(
  textTheme: GoogleFonts.playfairDisplayTextTheme(
    base.textTheme.copyWith(
      bodyLarge: GoogleFonts.sourceSans3(),
    ),
  ),
)
```

### Color & Theme
Commit to a cohesive aesthetic. Use `ThemeData`, `ColorScheme`, and `Color` consistently:
- Define `ColorScheme.fromSeed()` or custom `ColorScheme` with dominant colors and sharp accents
- Use `Theme.of(context).colorScheme` and `Theme.of(context).textTheme` throughout
- Dominant colors with sharp accents outperform timid, evenly-distributed palettes
- Support both light and dark via `brightness: Brightness.light/dark`

### Motion
Use Flutter animations for effects and micro-interactions:
- **Implicit**: `AnimatedContainer`, `AnimatedOpacity`, `AnimatedSwitcher` for simple transitions
- **Explicit**: `AnimationController`, `Tween`, `AnimatedBuilder` for orchestrated sequences
- **Staggered**: Use `Interval` curves for page-load reveals and staggered entrances
- Focus on high-impact moments: one well-orchestrated screen transition creates more delight than scattered micro-interactions
- Consider `Hero` for shared-element transitions between routes

### Spatial Composition
Unexpected layouts. Asymmetry. Overlap. Diagonal flow. Grid-breaking elements:
- Use `Stack` with `Positioned` or `Align` for overlap and layering
- Use `CustomScrollView` with `SliverList`, `SliverGrid` for custom scroll effects
- Use `LayoutBuilder` for responsive, constraint-aware layouts
- Generous negative space OR controlled density - be intentional
- Break the grid: offset children, use `Transform.rotate`, asymmetric padding

### Backgrounds & Visual Details
Create atmosphere and depth rather than defaulting to solid colors:
- `BoxDecoration`: `gradient`, `boxShadow`, `border`, `borderRadius`
- `LinearGradient`, `RadialGradient`, `SweepGradient` for gradient meshes
- `ShaderMask` with `ImageShader` or custom shaders for textures
- `BackdropFilter` with `ImageFilter.blur` for glassmorphism
- `DecoratedBox` with `Decoration` for layered effects
- Add noise/grain via `CustomPaint` or overlay images when needed

## Anti-Patterns to Avoid

NEVER use generic AI-generated aesthetics:
- Overused font families (Roboto, Arial, system fonts, Inter)
- Cliched color schemes (purple gradients on white, default Material seed colors without customization)
- Predictable layouts (centered card stacks, uniform grids)
- Cookie-cutter design that lacks context-specific character

Interpret creatively and make unexpected choices that feel genuinely designed for the context. No design should be the same. Vary between light and dark themes, different fonts, different aesthetics. NEVER converge on common choices (Space Grotesk, Poppins, etc.) across generations.

## Implementation Notes

- **Match complexity to vision**: Maximalist designs need elaborate code with extensive animations and effects. Minimalist or refined designs need restraint, precision, and careful attention to spacing, typography, and subtle details. Elegance comes from executing the vision well.
- **Material 3**: Prefer `useMaterial3: true` (default in recent Flutter). Use `ColorScheme` and component theming consistently.
- **Cross-reference**: For layout mechanics, see `flutter-layout`. For animation implementation details, see `flutter-animation`.

Remember: Commit fully to a distinctive vision. Don't hold back - show what can truly be created when thinking outside the box.
