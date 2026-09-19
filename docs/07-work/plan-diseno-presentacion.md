# Plan de diseño — presentación "Nuestro harness de desarrollo con IA"

**Skill:** frontend-design (del profesor, usada sin modificar)
**Salida:** `docs/presentacion-harness.html` · 11 diapositivas + 1 de respaldo · ~9 min
**Aprobado:** 19 de septiembre de 2026

## Metáfora rectora

El harness es una *línea de control*: cada etapa es una estación que exige su documento antes de avanzar y tres banderas marcan dónde interviene una persona. El deck es el *expediente* de esa línea y viste los mismos verdes de los artefactos reales que muestra en pantalla.

## Paleta (5 colores y su rol)

| Nombre | Hex | Rol |
|---|---|---|
| Papel | `#F3F4EE` | Fondo, verde-gris neutro, emparentado con los docs del repo. |
| Tinta | `#1C2333` | Texto principal, azul-negro fresco. |
| Verde pizarra | `#245C43` | Estructura: títulos, cinta de estaciones, reglas. Es el verde de spec y producto. |
| Ámbar decisión | `#9C5B0E` | Solo en los 3 puntos de intervención humana (banderas). Oscurecido desde `#C77E1E` para cumplir contraste ≥4.5:1 sobre el papel (4.85:1). |
| Plomo | `#D9D5C6` | Hairlines entre estaciones y bordes de tablas. |

## Tipografía (pilas de sistema, sin descargas)

- **Rótulo** (títulos y cifras de evidencia): `ui-monospace, "Cascadia Mono", "SF Mono", Consolas`, peso heavy. Aire de tablero de control; unifica las cifras del manifiesto (20 puestos, 7 franjas, 140 celdas, `1 h`, `Sí/No`).
- **Texto** (párrafos y tablas): `system-ui`, peso normal, interlineado ~1.5, tamaños grandes de proyección (título 48–72 px, cuerpo 24–28 px, tablas 20–22 px).

## Layout (16:9, alineación izquierda)

- Cinta de estaciones superior: la cadena como secuencia numerada (es un proceso real, no decoración); muestra la estación actual de cada diapositiva.
- Riel transversal de `auditar-contexto` debajo de la cadena.
- Chips de evidencia: rutas reales monoespaciadas (`docs/PLAN.md`, `producto/reservas-laboratorio.html`, `docs/07-work/…`).
- Pie: contador `04 / 11` y etiqueta breve. Sin eyebrows, sin viñetas "·", sin flechas decorativas.
- Portada y cierre centradas (tesis); el resto alineado a la izquierda, nada justificado.

```
Portada                          Flujo
┌────────────────────────┐      ┌────────────────────────┐
│                        │      │ REQUISITO→SPEC→PLAN→…   │
│ NUESTRO HARNESS       │      │ [caja][caja][…]          │
│ DE DESARROLLO CON IA   │      │ ══ auditar-contexto ══  │
│ ■ Breiner Martínez    │      │ ◆ ◆ ◆ (3 banderas)       │
│ (tesis, una línea)     │      │ leyenda                 │
└─────────── 01/11 ─────┘      └─────────── 04/11 ──────┘
```

## Principios

- Un solo alarde: títulos monoespaciados + banderas ámbar. Todo lo demás, sobrio.
- Movimiento solo en un momento orquestado en portada; `prefers-reduced-motion` respetado y foco visible.
- Cada cifra sale de las fuentes reales; sin gradientes, sin sombras acolchadas, sin tarjetas SaaS.

## Revisión contra el brief (barrrido de la skill)

Evitado ("default" que se descarta → elección real): crema+serif+terracota → papel verde-gris y rótulo monoespaciado; negro+ácido → tinta azul-negro y verde pizarra; tarjetas SaaS → estaciones unidas por la cinta, sin sombras; eyebrows/viñetas → cinta de estaciones estructural; acento decorativo → ámbar reservado a los 3 momentos humanos.

## Contenido (12 diapositivas)

1. Portada · 2. El problema y la tesis · 3. Mapa del harness (3 capas) · 4. El flujo (SVG) · 5. Las 6 skills · 6. Por dentro de una skill · 7. Entregable: la especificación (7 secciones) · 8. Entregable: el plan y el informe de validación · 9. El producto y la prueba · 10. Nuestro proceso · 11. Cierre · 12. Respaldo (Plan B, no numerada).

## Datos decididos con el equipo

- `auditar-contexto`: se describe como "ya adaptada a este repositorio".
- Informe de `validar-resultado`: se genera hoy con Chrome real en `docs/informe-validacion-reservas-laboratorio.md` (veredicto: Sirve, 5/5).
- Portada: Breiner Martinez · 19 de septiembre de 2026.
- Diapositiva 8: sin agri/dominio anterior; la fila de la prueba de crear-especificacion sin el ejemplo agrícola original.