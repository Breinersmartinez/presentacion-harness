# Decisiones de arquitectura: agente del laboratorio de cómputo

**Equipo:** AgroCortex
**Ubicación del script:** `producto/agente-consola/agente.py`, con un enlace simbólico en `scripts/agente_laboratorio.py` para la ruta que pide el enunciado. Es el mismo archivo, no una segunda copia.
**Modo de evidencia:** simulado, sin `API_KEY` y sin red.
**Especificación del dominio:** [`../SPEC.md`](../SPEC.md) §7.

## 1. Forma del sistema

- **Elección:** agente autónomo con bucle ReAct.
- **Justificación técnica:** el camino depende de la información que encuentre el agente. Una consulta compuesta requiere primero obtener disponibilidad y luego sintetizarla con la regla de horario. Para cancelar, primero debe consultar la reserva del estudiante para conocer el identificador y solo después solicitar la cancelación. Una solicitud fuera de horario se resuelve directamente, sin herramienta. Por ello no se usa un flujo determinista fijo ni un chat sin herramientas.

### La regla que se hereda de la semana 4

El enunciado da por hecho que la spec de la semana 4 fijó un máximo de una reserva por estudiante. Al revisar la spec entregada, la decisión decía "una por nombre y franja", lo que permitía hasta siete puestos por estudiante y contradecía al agente. **Se corrigió la spec, no el agente**: [`../SPEC.md`](../SPEC.md) §7 ahora dice una sola reserva activa por estudiante, el HTML lo hace cumplir y el `RESERVAS` del agente —indexado por estudiante— lo cumple por construcción. Los tres artefactos del mismo caso dicen ahora lo mismo.

## 2. El contexto y las instrucciones

Texto efectivo de `SYSTEM_PROMPT` en `agente.py`:

```text
Eres el agente de operaciones del laboratorio de computacion de la universidad.
Ayudas a consultar disponibilidad, consultar reservas activas y cancelar reservas.

Reglas duras del laboratorio:
- Hay 20 puestos, de P-01 a P-20.
- El laboratorio atiende solo de 06:00 a 20:00, en estas franjas fijas de dos
  horas: 06:00-08:00, 08:00-10:00, 10:00-12:00, 12:00-14:00, 14:00-16:00, 16:00-18:00, 18:00-20:00. Fuera de ellas esta cerrado.
- Cada estudiante tiene como maximo una reserva activa.
- Nunca confirmes una cancelacion sin llamar a cancelar_reserva: la herramienta
  pide autorizacion explicita al operador humano antes de modificar el estado.

Herramientas disponibles (esta es la lista completa; no inventes otras):
- ACCION: consultar_disponibilidad:FRANJA
- ACCION: consultar_reserva:CODIGO_ESTUDIANTE
- ACCION: cancelar_reserva:ID_RESERVA

Reglas de formato (obligatorias, responde con una sola linea):
- Para usar una herramienta: ACCION: NOMBRE_HERRAMIENTA:PARAMETRO
- Para responder al usuario: FINAL: respuesta
- Si la solicitud es fuera de horario o no permitida, responde FINAL: sin llamar
  una herramienta ficticia.
- No declares una reserva cancelada si la observacion no confirma la cancelacion.
- Responde en espanol, texto plano y breve.
```

El prompt fija el rol, el horario, el límite de una reserva activa y el protocolo `ACCION:`/`FINAL:`. El inventario es taxativo para impedir que el modelo invente operaciones de creación, modificación o consulta no disponibles.

## 3. Herramientas y mapa de autonomía

| Herramienta | Parámetro y retorno | Nivel de autonomía | Peor escenario si alucina sin supervisión |
|---|---|---|---|
| `consultar_disponibilidad` | `franja: str` → puestos libres o aviso de cerrado | Ejecuta y reporta | Entregar disponibilidad incorrecta; es lectura y no altera el estado. |
| `consultar_reserva` | `codigo_estudiante: str` → puesto, franja e ID o ausencia de reserva | Ejecuta y reporta | Exponer o interpretar mal una reserva; es lectura y reversible. |
| `cancelar_reserva` | `id_reserva: str` → cancelación o ausencia de reserva | Ejecuta con aprobación | Liberar indebidamente un puesto y afectar la reserva de un estudiante. |

`consultar_disponibilidad` no consulta un diccionario `DISPONIBILIDAD` como en el ejemplo del enunciado: **deriva los puestos libres de `RESERVAS`**, restando los ocupados de la franja a los 20 puestos. Es una decisión deliberada. Un diccionario de disponibilidad paralelo tendría que actualizarse en cada alta y en cada cancelación, y un forgetting en esa actualización mostraría un puesto como libre estando ocupado. Con una sola fuente de verdad no hay estado que pueda quedar desincronizado. La diferencia observable: en `10:00-12:00` el agente devuelve los 19 puestos libres (solo `P-04` está ocupado por `E-101`), donde el ejemplo del enunciado muestra cinco.

`ejecutar_herramienta` intercepta `cancelar_reserva` con `input()`. Solo la respuesta exacta `s` invoca la función que elimina la reserva del diccionario en memoria. Cualquier otro valor, EOF incluido, informa rechazo y conserva el estado.

## 4. Criterio de parada y seguridad

- **Límite máximo:** `MAX_VUELTAS=5` por defecto, sobrescribible por variable de entorno.
- **Éxito:** al detectar `FINAL:`, el bucle imprime la respuesta y termina la misión.
- **Tope:** al no recibir `FINAL:` tras el máximo, imprime `[PARADA] Tope alcanzado` y termina ordenadamente.
- **Antirrepetición:** una misma herramienta con los mismos parámetros recibe una observación de repetición en vez de ejecutarse otra vez.
- **Formato inválido:** una respuesta que no sea `FINAL:` ni `ACCION:` no se toma como respuesta final; se devuelve al modelo como observación de formato inválido con otra oportunidad.
- **Timeout:** la llamada HTTP con `urllib.request.urlopen` usa 10 segundos para evitar que una API degradada bloquee la consola.
- **Estado:** las reservas viven en el diccionario `RESERVAS` y se reinician al terminar el proceso; no hay archivo, base de datos ni sincronización.

**Diferencia con el taller, declarada.** El agente del taller comprueba `if vuelta >= MAX_VUELTAS` *antes* de llamar al modelo, de modo que con `MAX_VUELTAS = 5` da cuatro vueltas efectivas y el tope salta en la quinta iteración sin llegar a preguntar nada. Aquí el bucle itera cinco vueltas y el freno corta al terminar la quinta. El enunciado dice "si el agente llega a la vuelta 5 sin emitir `FINAL:`, interrumpe", que es la lectura del taller; se eligió dar cinco vueltas completas porque es el criterio menos ambiguo de contar y el que coincide con el número que se lee en la consola.

## 5. Evidencia de ejecución

Cada ejecución siguiente se realizó en un proceso nuevo con `API_KEY` vacía. Por eso Misión 2A y Misión 2B parten de la misma reserva inicial `RES-402`.

### Misión 1: consulta compuesta

**Consulta enviada:** `¿Qué puestos hay libres para la franja de 10:00 a 12:00 y hasta qué hora abre el laboratorio?`

```text
--- Vuelta 1/5 ---
[Modelo] ACCION: consultar_disponibilidad:10:00-12:00
[Herramienta -> consultar_disponibilidad] Puestos libres en 10:00-12:00: P-01, P-02, P-03, P-05, P-06, P-07, P-08, P-09, P-10, P-11, P-12, P-13, P-14, P-15, P-16, P-17, P-18, P-19, P-20.

--- Vuelta 2/5 ---
[Modelo] FINAL: Puestos libres en 10:00-12:00: P-01, P-02, P-03, P-05, P-06, P-07, P-08, P-09, P-10, P-11, P-12, P-13, P-14, P-15, P-16, P-17, P-18, P-19, P-20. El laboratorio atiende hasta las 20:00.

[RESPUESTA FINAL] Puestos libres en 10:00-12:00: P-01, P-02, P-03, P-05, P-06, P-07, P-08, P-09, P-10, P-11, P-12, P-13, P-14, P-15, P-16, P-17, P-18, P-19, P-20. El laboratorio atiende hasta las 20:00.
```

### Misión 2A: cancelación con rechazo humano

**Consulta enviada:** `El estudiante E-101 necesita cancelar su reserva activa.`
**Respuesta del operador:** `n`

```text
--- Vuelta 1/5 ---
[Modelo] ACCION: consultar_reserva:E-101
[Herramienta -> consultar_reserva] Estudiante E-101 tiene reservado el puesto P-04, franja 10:00-12:00, id de reserva RES-402.

--- Vuelta 2/5 ---
[Modelo] ACCION: cancelar_reserva:RES-402
[CONTROL-HUMANO] ¿Autorizas cancelar la reserva RES-402? (s/n): [Herramienta -> cancelar_reserva] Cancelación de reserva rechazada por el operador humano.

--- Vuelta 3/5 ---
[Modelo] FINAL: La reserva sigue activa porque el operador humano rechazó la cancelación.

[RESPUESTA FINAL] La reserva sigue activa porque el operador humano rechazó la cancelación.
```

### Misión 2B: cancelación con aprobación humana

**Consulta enviada:** `El estudiante E-101 necesita cancelar su reserva activa.`
**Respuesta del operador:** `s`

```text
--- Vuelta 1/5 ---
[Modelo] ACCION: consultar_reserva:E-101
[Herramienta -> consultar_reserva] Estudiante E-101 tiene reservado el puesto P-04, franja 10:00-12:00, id de reserva RES-402.

--- Vuelta 2/5 ---
[Modelo] ACCION: cancelar_reserva:RES-402
[CONTROL-HUMANO] ¿Autorizas cancelar la reserva RES-402? (s/n): [Herramienta -> cancelar_reserva] Reserva RES-402 cancelada exitosamente y puesto liberado.

--- Vuelta 3/5 ---
[Modelo] FINAL: La cancelación fue autorizada y la reserva se liberó correctamente.

[RESPUESTA FINAL] La cancelación fue autorizada y la reserva se liberó correctamente.
```

### Misión 3: solicitud fuera de horario

**Consulta enviada:** `Quiero reservar un puesto para hoy a las 10 de la noche (22:00).`

```text
--- Vuelta 1/5 ---
[Modelo] FINAL: No es posible atender esa solicitud: el laboratorio opera solo de 06:00 a 20:00.

[RESPUESTA FINAL] No es posible atender esa solicitud: el laboratorio opera solo de 06:00 a 20:00.
```

### Experimento 2 del taller: la no-convergencia y el freno

No es una de las tres misiones, pero es la única forma de evidenciar el tope de vueltas sin una `API_KEY`: en MODO SIMULADO el simulador siempre converge en dos vueltas. La consulta dispara el escenario de no-convergencia, que devuelve siempre la misma acción.

**Consulta enviada:** `Investiga de manera infinita sin parar`

```text
--- Vuelta 1/5 ---
[Modelo] ACCION: consultar_disponibilidad:06:00-08:00
[Herramienta -> consultar_disponibilidad] Puestos libres en 06:00-08:00: P-01, P-02, P-03, P-04, P-05, P-06, P-07, P-08, P-09, P-10, P-11, P-12, P-13, P-14, P-15, P-16, P-17, P-18, P-19, P-20.

--- Vuelta 2/5 ---
[Modelo] ACCION: consultar_disponibilidad:06:00-08:00
[Herramienta -> consultar_disponibilidad] ya pediste 'consultar_disponibilidad' con esos parametros y la respuesta fue la misma. No lo repitas: cambia de herramienta o responde FINAL: con lo que ya sabes.

--- Vuelta 3/5 ---
[Modelo] ACCION: consultar_disponibilidad:06:00-08:00
[Herramienta -> consultar_disponibilidad] ya pediste 'consultar_disponibilidad' con esos parametros y la respuesta fue la misma. No lo repitas: cambia de herramienta o responde FINAL: con lo que ya sabes.

--- Vuelta 4/5 ---
[Modelo] ACCION: consultar_disponibilidad:06:00-08:00
[Herramienta -> consultar_disponibilidad] ya pediste 'consultar_disponibilidad' con esos parametros y la respuesta fue la misma. No lo repitas: cambia de herramienta o responde FINAL: con lo que ya sabes.

--- Vuelta 5/5 ---
[Modelo] ACCION: consultar_disponibilidad:06:00-08:00
[Herramienta -> consultar_disponibilidad] ya pediste 'consultar_disponibilidad' con esos parametros y la respuesta fue la misma. No lo repitas: cambia de herramienta o responde FINAL: con lo que ya sabes.

[PARADA] Tope alcanzado tras 5 vueltas sin respuesta final.
El agente no convergio: revisa si la petición era indefinida o imposible.
```

La traza muestra los dos frenos por separado: el aviso de repetición evita el gasto de la llamada repetida, y el tope corta cuando el aviso solo no basta. Sin el tope, este mismo bucle seguiría llamando al proveedor indefinidamente.

## 6. Lo que no se pudo verificar

- **Con un modelo real.** Las cinco trazas son de MODO SIMULADO. No se ejecutó ninguna misión con `API_KEY` real, así que no hay evidencia de cómo responden `gemini-2.5-flash-lite` o `qwen/qwen3-32b` a este `SYSTEM_PROMPT`. En particular, la Misión 3 depende de que el modelo se niegue a inventar herramientas: el simulador lo garantiza por construcción, un modelo real no. Con red y cuota, la comprobación es `export PROVEEDOR=gemini API_KEY=...` y repetir las tres misiones.
- **Resistencia del bucle ante un modelo que ignora el protocolo.** El parser tolerante y la observación de formato inválido están implementados y probados con entradas mal formadas, pero no se observaron en una corrida real.
