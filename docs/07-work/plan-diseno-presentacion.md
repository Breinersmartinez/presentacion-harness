# Plan de diseño — presentación "Nuestro harness de desarrollo con IA"

**Skill:** frontend-design (del profesor, usada sin modificar)
**Salida:** `docs/index.html` · 7 diapositivas · sin minutaje fijo en el deck
**Aprobado:** 19 de septiembre de 2026 · **Reformulado:** 3 de octubre de 2026

> **Qué cambió y por qué.** El deck se aprobó con 11 diapositivas y una de respaldo. Después se rearmó a 7, una por cada skill del harness, que es la forma en que se presenta el reto. El archivo además se renombró de `docs/presentacion-harness.html` a `docs/index.html`. Todo lo de abajo está contrastado contra el archivo actual; lo que quedó fuera se dice en "Del plan original".

## Metáfora rectora

El harness es una *línea de control*: cada etapa es una estación que exige su documento antes de avanzar. El deck es el *expediente* de esa línea y viste los mismos verdes de los artefactos reales que muestra en pantalla.

## Paleta (5 colores y su rol)

Definidos como variables CSS en `docs/index.html`.

| Nombre | Hex | Rol |
|---|---|---|
| Papel | `#F3F4EE` | Fondo, verde-gris neutro, emparentado con los docs del repo. |
| Tinta | `#1C2333` | Texto principal, azul-negro fresco. |
| Verde pizarra | `#245C43` | Estructura: títulos, cinta de estaciones, iconos. Es el verde de spec y producto. |
| Ámbar decisión | `#9C5B0E` | Solo en los momentos de intervención humana y en el detalle de los iconos. Oscurecido desde `#C77E1E` para cumplir contraste ≥4.5:1 sobre el papel (4.85:1). |
| Plomo | `#D9D5C6` | Hairlines entre estaciones y bordes de tablas. |

Dos variables de apoyo: `--verde-claro` `#E7EBE3` para superficies y `--tinta-suave` `#5A6577` para texto secundario.

## Tipografía (pilas de sistema, sin descargas)

- **Rótulo** (`--mono`): `ui-monospace, "Cascadia Mono", "SF Mono", Menlo, Consolas, "Liberation Mono", monospace`. Títulos, cifras de evidencia y el nombre de cada skill en el `<h2>`.
- **Texto** (`--sans`): `system-ui, -apple-system, "Segoe UI", Roboto, Ubuntu, Cantarell, "Noto Sans", sans-serif`. Párrafos y tablas.

## Layout (16:9, alineado a la izquierda)

- **Cinta de estaciones** en el borde superior de cada diapositiva: `Requisito → Especificación → Plan → Ejecución → Validación`, con la estación actual resaltada en cada diapositiva. La cinta es la estructura, no decoración.
- **Riel transversal**: el slot `rail` bajo la cinta lleva `auditar-contexto` en las diapositivas 1 y 6, que es donde explica su papel transversal. La 7 sale de la cadena —su cinta pasa a `Contexto → Skills → Evidencia`— y usa el mismo slot para `frontend-design · la skill del profesor, usada tal cual`.
- **Icono por skill**: SVG inline de 72×72 a la derecha del título, trazo verde pizarra con un detalle ámbar. Es el único elemento gráfico repetido y le da a las seis diapositivas la misma firma visual.
- **Regla dura y mensaje**: cada diapositiva de skill lleva su `kicker` numerado (`Skill 03 de 6`), el nombre de la skill como `<h2>`, un párrafo de qué hace y una regla dura en las notas.
- **Pie**: contador `01 / 07` derivado de la cantidad real de diapositivas, más los botones y la ayuda de teclas.
- Todo alineado a la izquierda, nada justificado. La portada también a la izquierda, solo centrada en el eje vertical.

```
Portada                          Skill 03 de 6
┌────────────────────────┐      ┌────────────────────────┐
│ NUESTRO HARNESS       │      │ [cinta: ▸Ejecución]      │
│ DE DESARROLLO CON IA   │      │ ejecutar-plan      [svg] │
│ (tesis, una línea)     │      │ Regla dura + mensaje     │
│ Requisito→…→Validación  │      └─────────── 04 / 07 ─────┘
└─────────── 01 / 07 ────┘
```

## Principios

- Un solo alarde: títulos monoespaciados + iconos de trazo con detalle ámbar. Todo lo demás, sobrio.
- Movimiento solo en la portada: la cinta se dibuja con la animación `trazar` (0.7 s). `prefers-reduced-motion` respetado y foco visible en los botones.
- Cada afirmación sale de las fuentes reales; sin gradientes, sin sombras acolchadas, sin tarjetas SaaS.

## Revisión contra el brief (barrido de la skill)

Evitado ("default" que se descarta → elección real): crema+serif+terracota → papel verde-gris y rótulo monoespaciado; negro+ácido → tinta azul-negro y verde pizarra; tarjetas SaaS → estaciones unidas por la cinta, sin sombras; eyebrows/viñetas → cinta de estaciones estructural; acento decorativo → ámbar reservado a los momentos humanos y al detalle de cada icono.

## Contenido (7 diapositivas)

1. Portada · tesis, cinta de la cadena, autor y fecha.
2. `crear-especificacion` · de requisito a especificación.
3. `escribir-plan` · de especificación a plan.
4. `ejecutar-plan` · del plan a la ejecución.
5. `validar-resultado` · de la ejecución a la validación.
6. `auditar-contexto` · transversal a todo el contexto.
7. `frontend-design` · la skill del profesor, usada tal cual.

Cada diapositiva de skill lleva en sus notas la regla dura de esa skill y el detalle de la demo. Las notas se togglean con la tecla `N`.

## Datos decididos con el equipo

- `auditar-contexto`: se describe como la skill que se adaptó a este repositorio durante el reto.
- Informe de `validar-resultado`: `docs/informe-validacion-reservas-laboratorio.md`, veredicto "Sirve", 6 de 6 criterios con evidencia, ejecutado en Chrome real.
- Portada: Breiner Martinez · 19 de septiembre de 2026.
- La 7 lleva una cinta distinta porque `frontend-design` no pertenece a la cadena: es la skill de diseño, no una estación.

## Del plan original

Lo que el plan aprobado describía y ya no existe en el deck:

- **11 diapositivas + 1 de respaldo.** No hay Plan B; si se quiere, se agrega como diapositiva 8 y el contador se ajusta solo.
- **Diapositivas de cierre y de mapa de tres capas.** El cierre se eliminó: la tesis está en la portada y la última diapositiva es `frontend-design`.
- **Chips de evidencia con rutas reales** (`docs/PLAN.md`, `producto/reservas-laboratorio.html`, `docs/07-work/…`). Los chips de la portada llevan autor y fecha; las rutas viven en las notas de cada diapositiva.
- **Minutaje de ~9 min.** El deck no fija tiempos. Los tiempos de la demo en vivo están en `docs/decisiones/semana04.md`, no aquí.
- **Riel de `auditar-contexto` en todas las diapositivas.** Solo va en la 1 y la 6; la 7 usa el slot para su propia nota.
