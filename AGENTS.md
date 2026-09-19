# AGENTS.md — presentacion-harness

## Que es esto
- Harness de skills de OpenCode para el reto de la clase: cadena `crear-especificacion` → `escribir-plan` → `ejecutar-plan`, reforzada por `validar-resultado` y `auditar-contexto`, más la skill de diseño `frontend-design`.
- Caso de demostración cerrado: reserva de puestos del laboratorio (`docs/SPEC.md`, `docs/PLAN.md`, `docs/especificacion-reserva-puestos-laboratorio.html`, `producto/reservas-laboratorio.html`).
- Todo en español, autocontenido, sin build ni servidor: la salida son HTMLs que abren con doble clic.

## Como se corre
- Skills: `cd ~/Development/IdeaProjects/presentacion-harness && opencode`. OpenCode ejecuta la cadena canónica desde el espejo global `~/.opencode/skills/`, que prevalece sobre el `.opencode/skills/` del proyecto para el mismo nombre; el `.opencode/` del proyecto solo aporta las skills sin homónimo global (p. ej. `frontend-design`).
- Producto: abrir `producto/reservas-laboratorio.html` con doble clic (usa `localStorage`, sin backend).
- No hay comandos de build, test ni instalación en este repo.

## Convenciones
- Skills en `.opencode/skills/<skill>/SKILL.md` (canónica en el repo); espejo versionado para revisión en `skills/<skill>/SKILL.md`. La copia que ejecuta opencode vive en `~/.opencode/skills/<skill>/SKILL.md` y debe replicarse en cada edición (ver "Como se corre").
- Spec de cada skill en `docs/07-work/especificacion-<skill>.html` (contrato §1–§7, HTML autocontenido sin recursos remotos). Planes de skill en `docs/07-work/PLAN-<tema>.md`. La skill canónica de `frontend-design` es el SKILL.md del profesor (diseño web distintivo); la spec de decks (`especificacion-frontend-design.html`) y su plan quedan descartados hasta nueva decisión.
- Caso de demostración: `docs/SPEC.md` (entrada), `docs/PLAN.md`, `docs/decisiones/semana04.md` (evidencia y guion de demo).
- Documentos en español, filenames kebab-case, HTMLs sin recursos remotos; los diagramas son SVG inline, nunca raster.

## Que NO hacer
- No inventar decisiones de producto: las skills preguntan antes de escribir una spec o un plan.
- No marcar como "cumplido" un criterio que no pudo verificarse: es "No verificable".
- No usar recursos remotos en los HTMLs generados.
- Editar una skill aquí exige replicarla a `~/.opencode/skills/` (fuente de ejecución), verificado con `opencode debug skill`. `~/.config/opencode/skills/` sí la usa opencode pero solo para skills externas del bucle (encargo/plan/ejecución/validación); `~/.agents/skills/` no aparece en el runtime. PENDIENTE: decidir si `~/.config/opencode/skills` y `~/.agents/skills` se siguen manteniendo como espejos.