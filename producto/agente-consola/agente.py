#!/usr/bin/env python3
"""Agente de consola para reservar puestos de laboratorio.

Esqueleto de cinco piezas (contexto, herramientas, modelo, memoria, bucle)
tomado del agente del taller guiado, extendido con:
  - un REPL multi-turno que conserva la memoria entre misiones;
  - herramientas del dominio de la spec de reserva de puestos;
  - un human-in-the-loop real sobre la unica operacion mutante.

Sin dependencias externas: solo la biblioteca estandar de Python 3.
Si API_KEY esta vacia, arranca en MODO SIMULADO y opera sin red.
"""

import json
import os
import re
import ssl
import urllib.error
import urllib.request

# ---------------------------------------------------------------------------
# PIEZA 1 - Configuracion (proveedor, endpoint y credenciales)
# ---------------------------------------------------------------------------

PROVEEDOR = os.environ.get("PROVEEDOR", "gemini").strip().lower()
API_KEY = os.environ.get("API_KEY", "").strip()
MAX_VUELTAS = int(os.environ.get("MAX_VUELTAS", "5"))

ENDPOINTS = {
    "gemini": "https://generativelanguage.googleapis.com/v1beta/openai/chat/completions",
    "groq": "https://api.groq.com/openai/v1/chat/completions",
}
MODELOS = {
    "gemini": "gemini-2.5-flash-lite",
    "groq": "qwen/qwen3-32b",
}

# La llave manda sobre la variable: una gsk_ siempre es de Groq.
if API_KEY.startswith("gsk_"):
    PROVEEDOR = "groq"
if PROVEEDOR not in ENDPOINTS:
    raise SystemExit(
        f"PROVEEDOR='{PROVEEDOR}' no soportado. Usa 'gemini' o 'groq'."
    )

URL = ENDPOINTS[PROVEEDOR]
MODELO = os.environ.get("MODELO", MODELOS[PROVEEDOR]).strip()
ES_SIMULADO = not API_KEY

# Dominio fijo del reto: estado efímero en memoria durante la ejecución.
PUESTOS = [f"P-{n:02d}" for n in range(1, 21)]
FRANJAS = [
    "06:00-08:00", "08:00-10:00", "10:00-12:00", "12:00-14:00",
    "14:00-16:00", "16:00-18:00", "18:00-20:00",
]
RESERVAS = {
    "E-101": {"puesto": "P-04", "franja": "10:00-12:00", "id_reserva": "RES-402"},
    "E-102": {"puesto": "P-10", "franja": "14:00-16:00", "id_reserva": "RES-503"},
}

# ---------------------------------------------------------------------------
# PIEZA 2 - Herramientas (codigo Python normal; el modelo solo las solicita)
# ---------------------------------------------------------------------------

def consultar_disponibilidad(franja):
    """Consulta los puestos libres de una franja oficial."""
    franja = franja.strip()
    if franja not in FRANJAS:
        return (
            f"El laboratorio esta cerrado en la franja '{franja}'. "
            "Atiende de 06:00 a 20:00 en bloques de 2 horas."
        )
    ocupadas = {reserva["puesto"] for reserva in RESERVAS.values() if reserva["franja"] == franja}
    libres = [p for p in PUESTOS if p not in ocupadas]
    if not libres:
        return f"La franja {franja} esta completa: 20 de 20 puestos reservados."
    return f"Puestos libres en {franja}: {', '.join(libres)}."


def consultar_reserva(codigo_estudiante):
    """Consulta la única reserva activa de un estudiante."""
    codigo = codigo_estudiante.strip().upper()
    reserva = RESERVAS.get(codigo)
    if reserva is None:
        return f"El estudiante {codigo} no tiene reservas activas."
    return (
        f"Estudiante {codigo} tiene reservado el puesto {reserva['puesto']}, "
        f"franja {reserva['franja']}, id de reserva {reserva['id_reserva']}."
    )


def cancelar_reserva(id_reserva):
    """Cancela una reserva identificada y libera su puesto en memoria."""
    identificador = id_reserva.strip().upper()
    codigo = next(
        (codigo for codigo, reserva in RESERVAS.items() if reserva["id_reserva"] == identificador),
        None,
    )
    if codigo is None:
        return f"La reserva {identificador} no existe o ya fue cancelada."
    del RESERVAS[codigo]
    return f"Reserva {identificador} cancelada exitosamente y puesto liberado."


def ejecutar_herramienta(nombre, argumentos):
    """Despachador. Nadie mas que esta funcion toca el estado del laboratorio."""
    nombre = nombre.strip().lower()
    argumento = argumentos.strip()
    if nombre == "consultar_disponibilidad":
        return consultar_disponibilidad(argumento)
    if nombre == "consultar_reserva":
        return consultar_reserva(argumento)
    if nombre == "cancelar_reserva":
        try:
            confirmacion = input(f"[CONTROL-HUMANO] ¿Autorizas cancelar la reserva {argumento}? (s/n): ")
        except EOFError:
            return "Cancelación de reserva rechazada por el operador humano."
        if confirmacion.strip().lower() != "s":
            return "Cancelación de reserva rechazada por el operador humano."
        return cancelar_reserva(argumento)
    return f"Herramienta '{nombre}' no reconocida. Solo puedes usar: consultar_disponibilidad, consultar_reserva, cancelar_reserva."

# ---------------------------------------------------------------------------
# PIEZA 3 - El modelo (cerebro). Endpoint compatible con OpenAI via urllib.
# ---------------------------------------------------------------------------

SYSTEM_PROMPT = f"""Eres el agente de operaciones del laboratorio de computacion de la universidad.
Ayudas a consultar disponibilidad, consultar reservas activas y cancelar reservas.

Reglas duras del laboratorio:
- Hay {len(PUESTOS)} puestos, de P-01 a P-20.
- El laboratorio atiende solo de 06:00 a 20:00, en estas franjas fijas de dos
  horas: {", ".join(FRANJAS)}. Fuera de ellas esta cerrado.
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
- Responde en espanol, texto plano y breve."""


class ErrorModelo(RuntimeError):
    """Fallo de transporte o de credenciales al hablar con el proveedor."""


def limpiar_respuesta(texto):
    """Quita vallas de codigo y prefijos narrativos que rompen el protocolo."""
    limpio = texto.strip()
    limpio = re.sub(r"^```[a-zA-Z]*\s*|\s*```$", "", limpio).strip()
    etiqueta = re.search(r"(ACCION|FINAL)\s*:", limpio, re.IGNORECASE)
    if etiqueta and limpio[: etiqueta.start()].strip():
        limpio = limpio[etiqueta.start() :]
    return limpio.strip()


# Acepta las tres formas que los modelos usan para la misma llamada:
# "ACCION: herramienta" (sin parametros), "ACCION: herramienta:param" y
# "ACCION: herramienta(param)".
PATRON_ACCION = re.compile(
    r"^ACCION\s*:\s*([a-z_]+)\s*(?::|\()?\s*(.*?)\)?\s*$", re.IGNORECASE
)


def llamar_modelo(mensajes):
    """Una llamada al LLM. Sin API_KEY cae al simulador local."""
    if ES_SIMULADO:
        return simular_respuesta(mensajes)

    carga = {"model": MODELO, "messages": mensajes, "temperature": 0}
    peticion = urllib.request.Request(
        URL,
        data=json.dumps(carga).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json",
            "User-Agent": "agente-consola-laboratorio/1.0",
        },
    )
    try:
        with urllib.request.urlopen(peticion, timeout=10) as respuesta:
            cuerpo = json.loads(respuesta.read().decode("utf-8"))
    except urllib.error.HTTPError as error:
        raise ErrorModelo(f"HTTP {error.code} del proveedor: {_detalle_error(error)}") from error
    except (urllib.error.URLError, TimeoutError, ssl.SSLError) as error:
        raise ErrorModelo(f"No se pudo contactar al proveedor: {error}") from error

    try:
        contenido = cuerpo["choices"][0]["message"]["content"] or ""
    except (KeyError, IndexError, TypeError) as error:
        raise ErrorModelo(f"Respuesta inesperada del proveedor: {cuerpo}") from error
    return limpiar_respuesta(contenido)


def _detalle_error(error):
    """Saca el mensaje util del JSON de error, sin volcar la respuesta entera."""
    crudo = error.read().decode("utf-8", "replace")
    try:
        cuerpo = json.loads(crudo)
    except ValueError:
        return crudo[:200]
    detalle = cuerpo.get("error", cuerpo) if isinstance(cuerpo, dict) else cuerpo
    if isinstance(detalle, dict):
        return str(detalle.get("message") or detalle.get("status") or detalle)[:200]
    return str(detalle)[:200]


def simular_respuesta(mensajes):
    """Simulador determinista de las misiones del reto, sin red ni cuota."""
    inicio = max(
        indice
        for indice, mensaje in enumerate(mensajes)
        if mensaje["role"] == "user" and not mensaje["content"].startswith("OBSERVACION")
    )
    pregunta = mensajes[inicio]["content"].lower()
    acciones = [
        mensaje for mensaje in mensajes[inicio:]
        if mensaje["role"] == AGENTE and mensaje["content"].startswith("ACCION:")
    ]
    observaciones = [
        mensaje["content"].removeprefix("OBSERVACION: ") for mensaje in mensajes[inicio:]
        if mensaje["role"] == "user" and mensaje["content"].startswith("OBSERVACION:")
    ]
    ultima_observacion = observaciones[-1] if observaciones else ""

    if re.search(r"\b22(?::00)?\b", pregunta):
        return "FINAL: No es posible atender esa solicitud: el laboratorio opera solo de 06:00 a 20:00."

    # Taller guiado, experimento 2: una peticion sin criterio de terminacion
    # devuelve siempre la misma accion, para poder evidenciar en consola los dos
    # frenos por separado (aviso de repeticion y tope de vueltas).
    if re.search(r"indefinid|sin parar|infinit", pregunta):
        return "ACCION: consultar_disponibilidad:06:00-08:00"

    codigo = (re.search(r"\be-\d+\b", pregunta) or ["e-101"])[0].upper()
    if "cancel" in pregunta:
        if not acciones:
            return f"ACCION: consultar_reserva:{codigo}"
        if len(acciones) == 1:
            identificador = (re.search(r"RES-\d+", ultima_observacion) or ["RES-402"])[0]
            return f"ACCION: cancelar_reserva:{identificador}"
        if "rechazada" in ultima_observacion.lower():
            return "FINAL: La reserva sigue activa porque el operador humano rechazó la cancelación."
        return "FINAL: La cancelación fue autorizada y la reserva se liberó correctamente."

    coincidencia = re.search(r"\b(\d{1,2})(?::00)?\s*(?:-|a)\s*(\d{1,2})(?::00)?\b", pregunta)
    franja = (
        f"{int(coincidencia.group(1)):02d}:00-{int(coincidencia.group(2)):02d}:00"
        if coincidencia else "10:00-12:00"
    )
    if not acciones:
        return f"ACCION: consultar_disponibilidad:{franja}"
    return f"FINAL: {ultima_observacion} El laboratorio atiende hasta las 20:00."

# ---------------------------------------------------------------------------
# PIEZA 4 y 5 - Memoria (historial) y bucle ReAct con criterio de parada.
# ---------------------------------------------------------------------------

AGENTE = "assistant"


def correr_mision(pregunta, historial):
    """Un bucle ReAct completo: razonar, actuar, observar, parar."""
    historial.append({"role": "user", "content": pregunta})
    repeticiones = {}

    for vuelta in range(1, MAX_VUELTAS + 1):
        print(f"\n--- Vuelta {vuelta}/{MAX_VUELTAS} ---")
        try:
            respuesta = llamar_modelo(historial)
        except ErrorModelo as error:
            print(f"[MODELO] {error}")
            print(
                "Sugerencia: revisa API_KEY y la cuota del proveedor, o corre "
                "sin API_KEY para entrar en MODO SIMULADO."
            )
            return None

        print(f"[Modelo] {respuesta}")

        if re.match(r"^FINAL\s*:", respuesta, re.IGNORECASE):
            final = respuesta.split(":", 1)[1].strip()
            historial.append({"role": AGENTE, "content": respuesta})
            print(f"\n[RESPUESTA FINAL] {final}")
            return final

        accion = PATRON_ACCION.match(respuesta)
        if not accion:
            # El modelo fallo el protocolo: no lo trates como respuesta final.
            historial.extend([
                {"role": AGENTE, "content": respuesta},
                {
                    "role": "user",
                    "content": (
                        "OBSERVACION: formato invalido. Responde solo con "
                        "'ACCION: herramienta:parametros' o 'FINAL: respuesta'."
                    ),
                },
            ])
            continue

        nombre, argumentos = accion.group(1), accion.group(2)
        clave = f"{nombre}:{argumentos.strip()}"
        if repeticiones.get(clave):
            observacion = (
                f"OBSERVACION: ya pediste '{nombre}' con esos parametros y la "
                "respuesta fue la misma. No lo repitas: cambia de herramienta o "
                "responde FINAL: con lo que ya sabes."
            )
            repeticiones[clave] += 1
        else:
            repeticiones[clave] = 1
            observacion = ejecutar_herramienta(nombre, argumentos)

        etiqueta = observacion.removeprefix("OBSERVACION: ")
        print(f"[Herramienta -> {nombre}] {etiqueta}")
        historial.extend([
            {"role": AGENTE, "content": respuesta},
            {"role": "user", "content": f"OBSERVACION: {etiqueta}"},
        ])

    total = f"{MAX_VUELTAS} vueltas" if MAX_VUELTAS > 1 else "1 vuelta"
    print(f"\n[PARADA] Tope alcanzado tras {total} sin respuesta final.")
    print("El agente no convergio: revisa si la petición era indefinida o imposible.")
    return None


def imprimir_ayuda():
    print(
        "\nComandos de consola:\n"
        "  /ayuda      esta ayuda\n"
        "  /historial  imprime la memoria de la sesion\n"
        "  /limpiar    borra la memoria y empieza de cero\n"
        "  /salir      termina (Ctrl-D o Ctrl-C tambien)\n"
        "\nCualquier otra linea es la nueva mision del agente."
    )


def main():
    modo = "MODO SIMULADO (sin API_KEY, sin red)" if ES_SIMULADO else f"API {PROVEEDOR}/{MODELO}"
    print("=" * 68)
    print(f"  AGENTE DE RESERVAS DEL LABORATORIO - {modo}")
    print("  Estado de reservas: memoria local de esta ejecución")
    print(f"  {len(PUESTOS)} puestos, {len(FRANJAS)} franjas ({FRANJAS[0]} a {FRANJAS[-1]})")
    print("=" * 68)
    imprimir_ayuda()

    historial = [{"role": "system", "content": SYSTEM_PROMPT}]
    while True:
        try:
            pregunta = input("\nTú> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nHasta luego.")
            return

        if not pregunta:
            continue
        if pregunta.lower() in ("/salir", "salir", "exit", "quit"):
            print("Hasta luego.")
            return
        if pregunta.lower() in ("/ayuda", "ayuda", "help", "?"):
            imprimir_ayuda()
            continue
        if pregunta.lower() == "/historial":
            for mensaje in historial:
                who = "Sistema" if mensaje["role"] == "system" else "Tú" if mensaje["role"] == "user" else "Agente"
                print(f"  [{who}] {mensaje['content']}")
            continue
        if pregunta.lower() in ("/limpiar", "limpiar", "reset"):
            historial = [{"role": "system", "content": SYSTEM_PROMPT}]
            print("Memoria borrada.")
            continue

        correr_mision(pregunta, historial)


if __name__ == "__main__":
    main()
