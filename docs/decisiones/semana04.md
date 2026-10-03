# Decisiones — Semana 4

**Equipo:** AgroCortex
**Caso elegido:** A — aplicación HTML autónoma de reserva de puestos.

## Las tres decisiones más difíciles de la spec

1. **Identificación:** se eligió pedir un nombre visible antes de reservar, sin autenticar usuarios. Se descartó el inicio de sesión porque el reto prohíbe servidor y no lo exige.
2. **Límite de reservas:** se eligió **una sola reserva activa por estudiante**, en cualquier franja. Se descartaron los límites por franja, los límites diarios y las sanciones. La primera versión de la spec decía "una por nombre y franja", lo que permitía hasta siete puestos por estudiante; se corrigió al unificarlo con la regla que el agente de la semana 6 dice heredar de esta spec.
3. **Cancelación:** se dejó fuera de este ciclo. Se descartó implementarla antes de la demo para priorizar reserva y verificación completa.

## Los skills y dónde quedaron

**Hay dos copias, y esta es la respuesta a la pregunta del enunciado.**

| Copia | Ruta | Rol |
|---|---|---|
| Canónica en el repo | `.opencode/skills/<skill>/SKILL.md` | La que se revisa en el repositorio del equipo |
| Espejo versionado | `skills/<skill>/SKILL.md` | Copia idéntica, la que exige el enunciado |
| Espejos locales | `~/.opencode/skills/`, `~/.config/opencode/skills/`, `~/.agents/skills/` | Donde las carga la herramienta al ejecutar |

- **La herramienta sí lee skills del repositorio**: OpenCode lee `.opencode/skills/` del proyecto. Sin embargo, cuando existe un homónimo en `~/.opencode/skills/`, **prevalece el global**. Por eso la copia que realmente ejecuta el agente es `~/.opencode/skills/`, y por eso existe el espejo en `skills/`: para que el profesor vea el contenido sin acceso a la máquina del equipo.
- Las cuatro copias se verificaron **idénticas** con `diff` antes de esta entrega.
- Verificación de que la herramienta las carga: `opencode debug skill`.

### El skill del taller fue renombrado

El enunciado pide entregar "los tres skills, **incluido el del taller**". El skill que llegó del taller se llamaba `escribir-spec`; aquí se llama **`crear-especificacion`**. Se renombró para que su descripción no se solapara con la de `escribir-plan` —que es justamente el riesgo de la prueba 2— y se reescribió su cuerpo. **El archivo original del taller no está en el repositorio**: no hay copia de `escribir-spec` que entregar. Se declara aquí en lugar de dejar que el profesor lo descubra.

| Lo que el enunciado pide | Lo que hay en `skills/` |
|---|---|
| Skill del taller (`escribir-spec`) | `crear-especificacion` — renombrado y ajustado |
| `escribir-plan` | `escribir-plan` |
| `ejecutar-plan` | `ejecutar-plan` |

## Medir el skill del taller

La columna de hoy **no se puede llenar** y eso es un resultado, no un papel que se quedaron sin hacer. No existe el archivo original del taller en el repositorio y no quedó registrada ninguna corrida con su descripción antes de ajustarlo, así que cualquier dato en esa columna sería inventado. Se marca **No verificable** tal como manda la regla del harness.

| Pregunta | Hoy, con la descripción del taller | Al final, con las tres ajustadas |
|---|---|---|
| ¿Se cargó solo, sin nombrarlo? | **No verificable.** El skill del taller no está en el repositorio y no hay corrida registrada. | **Sí.** Con el requerimiento "registrar un sembradío", sin nombrar la skill, `crear-especificacion` se activó sola. |
| ¿Cuántas preguntas hizo antes de escribir? | **No verificable**, por la misma razón. | **Seis** decisiones pendientes, y no redactó nada antes de las respuestas. |
| ¿Qué le faltó? | **No verificable**, por la misma razón. | Lo que sí quedó escrito después, en las reglas duras de las tres skills: criterio de aceptación respondible con sí o no, tareas de un máximo de cuatro horas, responsable siempre, confirmation antes de tocar un artefacto, y prohibición explícita de declarar cumplido lo que no se verificó. |

## Reglas duras agregadas

Las tres del enunciado van literales en cada skill. Estas son las del equipo, por encima de ellas:

- `crear-especificacion` no avanza si hay decisiones de producto relevantes sin respuesta.
- `escribir-plan` no permite una tarea mayor a cuatro horas ni sin responsable, y devuelve el trabajo a la spec si un criterio de aceptación no es verificable.
- `ejecutar-plan` espera confirmación antes de tocar un artefacto y no marca una tarea como cumplida si no puede verificarla.
- `ejecutar-plan` tiene que describir "artefactos" y no presuponer un lenguaje o un proyecto, para servir igual al caso A que al caso B.
- `crear-especificacion` no acepta "maneja errores" ni "rápido" como criterio: los sustituye por un comportamiento comprobable.

## Pruebas de la cadena

| Skill | Prueba | Resultado | Ajuste o evidencia |
|---|---|---|---|
| Instalación | Ejecutar `opencode debug skill`. | Pasó. | OpenCode reconoció las skills canónicas desde los espejos sincronizados. |
| Renderizado mínimo | Abrir el producto con Chrome headless y contar los puestos dibujados. | Pasó. | El DOM generado contiene 20 filas, 7 franjas y 140 celdas. |
| crear-especificacion | Pedir una spec sin nombrar la skill. | Pasó. | Con "registrar un sembradío" la skill se activó sola, preguntó seis decisiones pendientes y no redactó la spec antes de las respuestas. |
| escribir-plan | Pedir un plan a partir de la spec sin nombrar la skill. | Pasó. | Con la spec de reservas ya cerrada la skill se activó sola, revalidó su cobertura y señaló la tarea 1 como primera ejecutable. |
| escribir-plan | Pedir una spec sin nombrar la skill: debe cargar la otra. | Pasó. | La activación es por condición previa (no hay spec), no por el verbo "escribir". |
| ejecutar-plan | Criterio de persistencia no comprobable en este entorno. | Pasó. | Verdictó **No verificable** (9/9 escenarios simulados) en lugar de declarar éxito sin comprobar el `localStorage` real del navegador. |
| Verificación manual | Reservar, bloquear y recargar en Chrome real. | Pasó. | Sin nombre no reserva; "Ana" deja la celda reservada y bloqueada (segundo clic inmuta); al recargar la celda continúa reservada. |

### Por tarea ejecutada

| Tarea del plan | ¿Avisó antes de tocar? | ¿Verificó? | ¿Se detuvo al terminar? | ¿Tuvieron que intervenir? |
|---|---|---|---|---|
| 1 · Estructura visual de 20 puestos y 7 franjas | No registrado | Sí | No registrado | No registrado |
| 2 · Reserva de un puesto libre | No registrado | Sí | No registrado | No registrado |
| 3 · Persistencia local | No registrado | Sí | No registrado | No registrado |
| 4 · Verificación manual de los criterios | No registrado | Sí | No registrado | No registrado |

**(columns honestas y su relleno pendiente)** Las tres columnas de conducta —avisar, detenerse, intervención— no quedaron registradas durante la ejecución original de estas cuatro tareas, así que se marcan como no registradas en vez de rellenarse con una suposición. La columna de verificación sí tiene evidencia: los cinco criterios de la spec están comprobados en navegador real en [`../informe-validacion-reservas-laboratorio.md`](../informe-validacion-reservas-laboratorio.md), más el sexto criterio que se añadió al unificar la regla de reservas. Para llenar las otras tres hay que volver a pasar las tareas por `ejecutar-plan` y anotar la traza.

## Guion de la demo

**Seis minutos.** Cuatro puntos, en el orden del enunciado, empezando por el producto.

| # | Punto | Tiempo | Qué se muestra | Qué se dice |
|---:|---|---:|---|---|
| 1 | Las dos decisiones más difíciles | 1 min | `SPEC.md` §7 | Identificación: nombre propio, se descartó login. Límite de reservas: una sola reserva activa por estudiante; se descartaron límites por franja y sanciones. Se corrigió durante el trabajo: la primera spec decía "una por franja" y eso contradecía al agente de la semana 6. |
| 2 | El producto funcionando | 2 min | `reservas-laboratorio.html` abierto | Reservar "Ana", clic en celda reservada inmuta, recarga y la reserva sigue. Intentar una segunda reserva con el mismo nombre y ver el aviso que cita la reserva previa. Mínimo: 20 puestos, 7 franjas, sin backend. |
| 3 | La cadena y cuál falló | 2 min | `skills/` y la tabla de pruebas | Las tres skills y qué las distingue: la condición previa, no el verbo. **El fallo que mostramos es el nuestro**: la spec decía "una reserva por nombre y franja" y el agente de la semana 6 aplicaba "una por estudiante". Lo detectamos al auditar los dos artefactos del mismo caso, y la corrección fue en la spec. También el `ejecutar-plan` que dictaminó **No verificable** en vez de declarar cumplido un criterio que no podía comprobar. |
| 4 | Una decisión que defender | 1 min | `PLAN.md`, sección "Fuera de este ciclo" | Cancelación fuera del ciclo. Tres tareas verificadas valen más que ocho con palomita, y el enunciado lo dice: cancelar no está en el mínimo a propósito. |

**Plan B:** si OpenCode falla, mostrar los `SKILL.md` versionados en `skills/`, la spec, el plan y la evidencia guardada, sin intentar repararlo en vivo. Si el navegador falla, abrir `reservas-laboratorio.html` en un segundo navegador. Si la red falla, el agente de la semana 6 arranca en MODO SIMULADO sin `API_KEY` y las cuatro trazas ya están en `docs/decisiones/semana06.md`: se lee la evidencia guardada. Un video o captura sirve de respaldo, no sustituye la demostración.

## Lo que no se alcanzó a hacer, y por qué

- **La cancelación.** Está intencionalmente fuera del ciclo, declarado en la spec y en `PLAN.md`. No es un descuido: el enunciado la excluye del mínimo a propósito.
- **Las dos columnas de la medición del skill del taller.** La columna de "hoy" no es reproducible porque el archivo original del taller no está en el repositorio y no se registró ninguna corrida con él. Está declarado arriba en vez de inventado.
- **Las tres columnas de conducta por tarea.** No quedaron registradas durante la ejecución original. Ver la tabla anterior.
- **Las trazas del agente con un modelo real.** Las cuatro de la semana 6 son de MODO SIMULADO; se declara en `semana06.md` y ahí está el procedimiento para repetirlas con `API_KEY`.
