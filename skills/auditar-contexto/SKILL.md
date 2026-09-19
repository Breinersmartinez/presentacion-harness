---
name: auditar-contexto
description: Audita si el contexto versionado de presentacion-harness (AGENTS.md, docs y skills) sigue siendo coherente entre sí y con el repositorio. Se usa al cambiar reglas, documentación o skills; informa hallazgos sin editar.
---

# Auditar contexto

Verifica que un agente pueda confiar en el contexto del repositorio antes de tomar decisiones. Es una auditoría de coherencia entre instrucciones, documentación y estado observable; no es una revisión de estilo ni una implementación.

## Fuentes y precedencia

1. `AGENTS.md`: reglas operativas, convenciones, restricciones y harness. Máxima precedencia.
2. `.opencode/skills/<skill>/SKILL.md`: fuentes canónicas de las skills.
3. `docs/07-work/especificacion-<skill>.html`: contrato de cada skill.
4. `docs/SPEC.md`, `docs/PLAN.md`, `docs/decisiones/`, `docs/especificacion-reserva-puestos-laboratorio.html` y `producto/`: caso de demostración y evidencia.
5. `skills/<skill>/SKILL.md`: espejo versionado para revisión del reto; debe coincidir con el canónico.

Si dos fuentes difieren, no elige una en silencio: reporta el conflicto, indica la fuente de mayor precedencia y pide decidir o actualizar la fuente inferior.

## Procedimiento

1. Determina el alcance: cambio de reglas, de skill, de spec, de documentación o general. Si no se indicó, audita `AGENTS.md` contra el resto de fuentes.
2. Lee `AGENTS.md` y contrástalo con la estructura observable del repo:
   - Cada spec anunciada en `docs/07-work/especificacion-<skill>.html` existe y su contrato describe la skill real.
   - Cada skill en `.opencode/skills/` tiene su espejo en `skills/` y ambos `SKILL.md` coinciden.
   - El caso de demostración está presente: `docs/SPEC.md`, `docs/PLAN.md`, `docs/decisiones/semana04.md`, `producto/reservas-laboratorio.html`.
   - Los estados especiales declarados en `AGENTS.md` (p. ej. la skill canónica externa de `frontend-design` y su spec/plan descartados) se respetan en el árbol.
   - HTMLs autocontenidos: sin `src`, `href` ni `url()` remotas; diagramas SVG inline, nunca raster.
3. Registra cada afirmación comprobada en una tabla con fuente, evidencia y estado: **coherente**, **desactualizada**, **contradictoria** o **no verificable**.
4. Clasifica hallazgos como bloqueantes, advertencias o informativos. Propone una corrección precisa, pero no modifica archivos.
5. Declara los límites de la auditoría: archivos no inspeccionados, espejos externos al repo y decisiones que requieren al dueño.

## Formato de salida

```markdown
## Alcance y fuentes revisadas

## Matriz de coherencia
| Afirmación | Fuente | Evidencia observada | Estado |

## Hallazgos
| Severidad | Conflicto o desactualización | Corrección propuesta |

## Límites y decisiones pendientes
```

## Reglas duras

- Cada hallazgo cita una ruta y una evidencia observable; no usa impresiones ni suposiciones.
- No audita ni reporta como defecto `.git/` ni archivos temporales o de respaldo fuera de las fuentes de verdad.
- Los espejos globales (`~/.config/opencode/skills`, `~/.agents/skills`) son externos a este repo: si se inspeccionan se cita la ruta; caso contrario se declaran no verificables.
- No cambia contexto, documentación, configuración ni código. Para aplicar una corrección se solicita una tarea posterior.
- No inventa el estado de decisiones abiertas del dueño (p. ej. el `PENDIENTE` de AGENTS.md sobre replicar a los espejos globales): lo declara como decisión pendiente.

## Ejemplo de activación

"Audita si AGENTS.md sigue alineado con las skills y sus specs" activa esta skill.