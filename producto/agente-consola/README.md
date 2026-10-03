# Agente del laboratorio de cómputo (consola)

Agente agéntico en **Python 3 puro, sin librerías externas y sin `pip install`**. Toma el esqueleto de cinco piezas del agente del taller guiado (semana 06) y lo aplica al dominio de la spec de reserva de puestos: el agente consulta disponibilidad, consulta reservas activas y cancela reservas bajo supervisión humana.

- **Script:** [`agente.py`](agente.py) — también disponible en [`../../scripts/agente_laboratorio.py`](../../scripts/agente_laboratorio.py), que es un enlace simbólico al mismo archivo.
- **Especificación del dominio:** [`../../docs/SPEC.md`](../../docs/SPEC.md)
- **Decisiones de arquitectura y trazas:** [`../../docs/decisiones/semana06.md`](../../docs/decisiones/semana06.md)

## Cómo se corre

```bash
python3 producto/agente-consola/agente.py
```

### Archivo `.env`

Si existe un `.env` junto al agente, se carga solo al arrancar; no hace falta
exportar nada a mano. Solo pares `CLAVE=VALOR`, sin comillas ni escapes, y lo
que ya esté en el entorno gana sobre el archivo. El de este repositorio está
en `.gitignore`: **no se versiona, porque contiene una llave real.**

```bash
# producto/agente-consola/.env
PROVEEDOR=gemini
API_KEY=...          # la llave del proveedor; nunca la subas al repo
MODELO=gemini-3.1-flash-lite
MAX_VUELTAS=5
TIMEOUT_SEGUNDOS=60
```

Importante: en cuanto existe un `API_KEY`, el agente **deja el MODO SIMULADO y
llama al proveedor de verdad**, gastando cuota. Para volver al simulado sin
borrar el archivo, ejecuta el agente con la variable vacía:

```bash
API_KEY= python3 producto/agente-consola/agente.py
```

Variables de entorno:

| Variable | Por defecto | Para qué |
| --- | --- | --- |
| `API_KEY` | vacía | Llave del proveedor. **Vacía = MODO SIMULADO**, sin red |
| `PROVEEDOR` | `gemini` | `gemini` (Google AI Studio) o `groq` |
| `MODELO` | según proveedor | Sobrescribe el modelo por defecto del taller |
| `MAX_VUELTAS` | `5` | Tope duro de vueltas por misión |
| `TIMEOUT_SEGUNDOS` | `60` | Espera máxima por llamada al proveedor |

Si `API_KEY` empieza con `gsk_`, el proveedor se detecta como Groq aunque `PROVEEDOR` diga otra cosa: la llave manda sobre la variable. Un `PROVEEDOR` distinto de `gemini` o `groq` aborta con un mensaje.

Modelos por defecto: `gemini-2.5-flash-lite` y `qwen/qwen3-32b`.

En la consola:

| Comando | Qué hace |
| --- | --- |
| `/ayuda` | Lista los comandos |
| `/historial` | Imprime la memoria de la sesión (contexto, decisiones, observaciones) |
| `/limpiar` | Borra la memoria y empieza de cero |
| `/salir` | Termina (también `Ctrl-D` o `Ctrl-C`) |

Cualquier otra línea es una nueva misión. **La memoria se conserva entre misiones**: el contexto acumulado sigue ahí, que es lo que un agente de verdad necesita para no amnesiar.

## Estado del laboratorio

Todo vive en memoria durante la ejecución del proceso. **No hay archivo, base de datos ni sincronización**: al terminar el script, el estado se reinicia.

```python
PUESTOS  = [f"P-{n:02d}" for n in range(1, 21)]   # P-01 … P-20
FRANJAS  = ["06:00-08:00", "08:00-10:00", "10:00-12:00", "12:00-14:00",
            "14:00-16:00", "16:00-18:00", "18:00-20:00"]
RESERVAS = {"E-101": {"puesto": "P-04", "franja": "10:00-12:00", "id_reserva": "RES-402"},
            "E-102": {"puesto": "P-10", "franja": "14:00-16:00", "id_reserva": "RES-503"}}
```

`RESERVAS` está indexado por estudiante, así que la regla de negocio de **una sola reserva activa por estudiante** es la propia forma del diccionario, no una comprobación aparte.

## Herramientas

Son las tres del reto. **No hay una cuarta.**

| Herramienta | Parámetro | Devuelve | Autonomía |
| --- | --- | --- | --- |
| `consultar_disponibilidad` | `franja` | Lista de puestos **libres y ocupados** de esa franja, o aviso de laboratorio cerrado con el horario | Ejecuta y reporta |
| `consultar_reserva` | `codigo_estudiante` | Puesto, franja e `id_reserva`, o que no hay reservas activas | Ejecuta y reporta |
| `cancelar_reserva` | `id_reserva` | Resultado de la cancelación | **Ejecuta con aprobación** (Human-in-the-loop) |

La disponibilidad no se guarda en un diccionario aparte: se **deriva** de `RESERVAS` (los 20 puestos menos los ocupados de esa franja). Así no hay dos fuentes de verdad que puedan contradecirse.

Devuelve las dos listas, no solo la de libres, y no es cosmético. Cuando solo devolvía los libres, el modelo tenía que **deducir** que un puesto ausente de la lista estaba ocupado, y lo hacía al revés: preguntaba "¿está ocupado el P-04?", recibía una lista donde `P-04` faltaba, y contestaba que estaba libre. Se reprodujo 3 de 3. Con los ocupados escritos en el texto, `P-04 (E-101, RES-402)` no hay nada que deducir, y la misma pregunta acierta 6 de 6.

### Human-in-the-loop

`ejecutar_herramienta` intercepta `cancelar_reserva` antes de tocar el estado:

```
[CONTROL-HUMANO] ¿Autorizas cancelar la reserva RES-402? (s/n):
```

- `s` → ejecuta la cancelación y libera el puesto.
- Cualquier otra cosa, incluido Enter y `EOFError` → devuelve `Cancelación de reserva rechazada por el operador humano.` y **el estado no cambia**.

La autonomía se calibra **acción por acción**, no con un interruptor global: consultar es inocuo y se automatiza; cancelar es irreversible y se supervisa.

## Las cinco piezas

| Pieza | Dónde | Qué es |
| --- | --- | --- |
| 1. Contexto e instrucciones | `SYSTEM_PROMPT` | El manual operativo: rol, horario, límite de una reserva, inventario taxativo de herramientas y protocolo `ACCION:` / `FINAL:` |
| 2. Herramientas | `consultar_disponibilidad`, `consultar_reserva`, `cancelar_reserva`, `ejecutar_herramienta` | Funciones Python deterministas. El modelo **nunca** toca el laboratorio: solo pide la llamada |
| 3. El modelo | `llamar_modelo` | Endpoint compatible con OpenAI vía `urllib`, `temperature=0`, `timeout=10`, con simulador local de respaldo |
| 4. La memoria | `historial` | Lista de mensajes reenviada completa en cada llamada: sin ella el modelo amnesia y repite la misma herramienta |
| 5. El bucle y la parada | `correr_mision` | Itera `MAX_VUELTAS` vueltas como máximo y para en cuanto llega un `FINAL:` |

## Las tres misiones del reto, para reproducir

```bash
env -u API_KEY python3 agente.py    # sin llave: MODO SIMULADO, sin red
```

**Misión 1 — consulta compuesta**

```
¿Qué puestos hay libres para la franja de 10:00 a 12:00 y hasta qué hora abre el laboratorio?
```

**Misión 2 — acción destructiva con Human-in-the-loop.** Se corre **dos veces**, una por respuesta del operador:

```
El estudiante E-101 necesita cancelar su reserva activa.
```

| Corrida | Respuesta del operador | Resultado esperado |
| --- | --- | --- |
| 2A | `n` | `Cancelación de reserva rechazada por el operador humano.` y la reserva sigue activa |
| 2B | `s` | `Reserva RES-402 cancelada exitosamente y puesto liberado.` |

Cada corrida arranca en un proceso nuevo, así que 2A y 2B parten de la misma reserva inicial.

**Misión 3 — regla de negocio / tarea inválida**

```
Quiero reservar un puesto para hoy a las 10 de la noche (22:00).
```

El agente responde `FINAL:` en la **vuelta 1**, sin llamar ninguna herramienta.

**Experimento 2 del taller — romper la parada**

```
Investiga de manera infinita sin parar
```

El simulador devuelve siempre la misma acción. Se ven los dos frenos por separado: el aviso de repetición en las vueltas 2 a 5 y, al agotar el tope,

```
[PARADA] Tope alcanzado tras 5 vueltas sin respuesta final.
```

## Diferencias con el agente del taller

El código del taller es deliberadamente minimalista. Estas son las correcciones que este agente sí trae, y por qué:

1. **No desactiva la verificación de certificados TLS.** El taller usa `ssl._create_unverified_context()`, que abre la conexión a un intermediario. Aquí se conserva la verificación normal.
2. **Los errores del proveedor son datos, no tracebacks.** Un 400 o un 429 se muestra como mensaje accionable y la consola sigue viva; el taller abortaba el script.
3. **El parser del protocolo es tolerante.** Acepta `ACCION: her:param`, `ACCION: her(param)` y `her` sin parámetros, y quita vallas de código o preámbulos narrativos antes de decidir. Un modelo pequeño no siempre escribe la línea exacta.
4. **Una llamada mal formada no se acepta como respuesta.** Si el modelo se sale del protocolo, recibe una observación de formato inválido y otra oportunidad, en lugar de que el script lo tome por una respuesta final.
5. **Anti-repetición además del tope.** Una misma herramienta con los mismos parámetros recibe un aviso en vez de ejecutarse otra vez. Los dos mecanismos son independientes: el aviso es prevención, el tope es el freno.
6. **`timeout=10` en la llamada HTTP.** El taller no lo tiene; sin él, una API degradada deja la consola colgada.
7. **REPL en vez de una sola misión.** La memoria se conserva entre preguntas.

Dos decisiones donde el enunciado y el taller no se alinean, y qué se hizo:

- **`TIMEOUT_SEGUNDOS`.** El taller fija 10 s. Medido contra `gemini-3.1-flash-lite`, la latencia normal está entre 2 y 7 s pero se dispersa: con 10 s fallaron 3 de 6 llamadas. Aquí el default es 60 s. Un timeout se reporta como `ErrorTimeout`, una subclase de `ErrorModelo`, para que la sugerencia diga "sube TIMEOUT_SEGUNDOS, la llave no es el problema" en vez de mandar a revisar unas credenciales que pueden estar perfectas.
- **`MAX_VUELTAS`.** El taller comprueba el tope *antes* de llamar al modelo, así que con `MAX_VUELTAS = 5` da 4 vueltas efectivas. Aquí el bucle itera 5 vueltas y el tope corta al terminar la quinta. Se registraría la diferencia si el profesor compara contra el taller.
- **Modelos.** El enunciado cita `gemini-3.5-flash-lite` y `qwen/qwen3.8-27b`; aquí se usan `gemini-2.5-flash-lite` y `qwen/qwen3-32b`, que son los que existen en los proveedores. Se sobrescriben con `MODELO`.

## Notas de alcance

- Herramientas de solo consulta y cancelación. **No hay herramienta de creación de reservas**: el reto de la semana 6 no la pide, y agregarla sería alcance nuevo sobre el mismo caso.
- Sin login, sin roles y sin sincronización entre equipos.
- En MODO SIMULADO el "modelo" es un autómata con una traza ReAct fija: sirve para ver el bucle y las salvaguardas, **no** para medir la calidad del razonamiento de un modelo real.
