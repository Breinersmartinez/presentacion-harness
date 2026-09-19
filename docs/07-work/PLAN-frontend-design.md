# Plan — skill frontend-design

> **ESTADO: descartado.** La skill canónica de frontend-design es el SKILL.md del profesor; este plan de decks de presentación queda sin ejecutar hasta nueva decisión.

**Spec fuente:** [especificacion-frontend-design.html](especificacion-frontend-design.html)  
**Responsable:** Breiner Martínez  
**Alcance de este ciclo:** crear el skill `frontend-design` que maqueta presentaciones de slides en un HTML único y autocontenido, con identidad visual fija, a partir del contenido que entrega el usuario, y dejar la skill disponible en los espejos del harness.

## Tareas

| # | Resultado | Responsable | Depende de | Estimación | Criterio de aceptación |
|---|---|---|---|---|---:|---|
| 1 | Esqueleto del skill: `frontmatter` y procedimiento de activación. | Breiner Martínez | — | 1 h | Existe `.opencode/skills/frontend-design/SKILL.md` con `name: frontend-design`; su procedimiento exige pedir el contenido del tema antes de generar y no producir HTML si no lo hay (§6, criterio 7). |
| 2 | Sistema visual fijo y estructura del HTML de salida. | Breiner Martínez | 1 | 2 h | La instrucción del skill fija la paleta `#174326`/`#28613b`/`#f6f8f6`/`#1c2820`, tipografía `system-ui`, portada, encabezado y pie; y exige un HTML sin recursos remotos. Dos temas distintos producen el mismo sistema visual (§6, criterios 3 y 5). |
| 3 | Navegación y degradación sin JavaScript. | Breiner Martínez | 2 | 1 h | Con las flechas o el clic se avanza, se retrocede y se vuelve a la primera slide; con JavaScript desactivado las slides quedan apiladas y el contenido se lee por scroll (§6, criterios 4 y 6). |
| 4 | Reglas de fidelidad del contenido y partición de slides. | Breiner Martínez | 2 | 1 h | El skill reproduce cada punto aportado sin datos inventados y parte una slide larga conservando orden y jerarquía (§6, criterio 2). |
| 5 | Verificación de la cadena contra la spec y evidencia. | Breiner Martínez | 3, 4 | 1 h | Se registran los siete criterios de la spec con estado Sí/No/No verificable y la evidencia correspondiente (apertura, contenido, sistema visual, navegación, sin red, sin JS, sin contenido). |
| 6 | Sincronización de la skill a los espejos. | Breiner Martínez | 5 | 30 min | `.opencode/skills/frontend-design/` se replica en `~/.config/opencode/skills/` y `~/.agents/skills/`, y el `md5sum` del `SKILL.md` coincide en las tres copias. |

## Orden y dependencias

Primero nace la skill con su procedimiento, porque el sistema visual, la navegación y la fidelidad son instrucciones que la completan. La navegación y la fidelidad dependen de que exista el sistema visual (tareas 3 y 4 sobre la tarea 2). La verificación solo empieza cuando el skill completo puede ejecutarse (tareas 3 y 4), y el sync a los espejos es el último paso para que la skill quede operativa en el harness.

## Primera tarea

**Tarea 1.** No tiene dependencias y puede empezar de inmediato: crear el archivo del skill con su `frontmatter` y procedimiento.

## Fuera de este ciclo

- Definir un tema personalizable o identidad del equipo: la spec lo descarta; la identidad es fija.
- Redactar el contenido de las presentaciones: la spec lo descarta; lo aporta el usuario.
- Generar PDF, imágenes o videos: la salida es únicamente el HTML.
- Diseñar pantallas o prototipos de aplicaciones: la spec solo cubre decks de presentación.