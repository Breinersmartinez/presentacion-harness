# AGENTS.md — presentacion-harness

## Que es esto
- Harness de skills de OpenCode para el reto de la clase: cadena `crear-especificacion` → `escribir-plan` → `ejecutar-plan`, reforzada por `validar-resultado` y `auditar-contexto`, más la skill de diseño `frontend-design`.
- Caso de demostración cerrado: reserva de puestos del laboratorio (`docs/SPEC.md`, `docs/PLAN.md`, `docs/especificacion-reserva-puestos-laboratorio.html`, `producto/reservas-laboratorio.html`).
- Todo en español, autocontenido, sin build ni servidor: la salida son HTMLs que abren con doble clic.

## Como se corre
- Skills: `cd ~/Development/IdeaProjects/presentacion-harness && opencode` (las carga desde `.opencode/skills/`).
- Producto: abrir `producto/reservas-laboratorio.html` con doble clic (usa `localStorage`, sin backend).
- No hay comandos de build, test ni instalación en este repo.

## Convenciones
- Skills en `.opencode/skills/<skill>/SKILL.md`; espejo versionado para revisión en `skills/<skill>/SKILL.md`.
- Spec de cada skill en `docs/07-work/especificacion-<skill>.html` (contrato §1–§7, HTML autocontenido sin recursos remotos). Planes de skill en `docs/07-work/PLAN-<tema>.md`. La skill canónica de `frontend-design` es el SKILL.md del profesor (diseño web distintivo); la spec de decks (`especificacion-frontend-design.html`) y su plan quedan descartados hasta nueva decisión.
- Caso de demostración: `docs/SPEC.md` (entrada), `docs/PLAN.md`, `docs/decisiones/semana04.md` (evidencia y guion de demo).
- Documentos en español, filenames kebab-case, HTMLs sin recursos remotos; los diagramas son SVG inline, nunca raster.

## Que NO hacer
- No inventar decisiones de producto: las skills preguntan antes de escribir una spec o un plan.
- No marcar como "cumplido" un criterio que no pudo verificarse: es "No verificable".
- No usar recursos remotos en los HTMLs generados.
- PENDIENTE: definir si editar una skill aquí exige replicarla a los espejos globales (`~/.config/opencode/skills`, `~/.agents/skills`).