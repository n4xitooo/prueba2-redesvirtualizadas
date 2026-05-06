import os
import sys
from datetime import date, datetime

import requests


API_KEY = os.getenv("THESPORTSDB_API_KEY")
PLAYER_NAME = os.getenv("PLAYER_NAME", "Lionel Messi")
BASE_URL = "https://www.thesportsdb.com/api/v1/json"


def calcular_edad(fecha_nacimiento):
    if not fecha_nacimiento or fecha_nacimiento == "N/A":
        return "N/A"

    try:
        nacimiento = datetime.strptime(fecha_nacimiento, "%Y-%m-%d").date()
    except ValueError:
        return "N/A"

    hoy = date.today()
    edad = hoy.year - nacimiento.year

    if (hoy.month, hoy.day) < (nacimiento.month, nacimiento.day):
        edad -= 1

    if edad < 0:
        return "N/A"

    return f"{edad} anios"


def validar_variables_entorno():
    if not API_KEY:
        print("Error: falta la variable de entorno THESPORTSDB_API_KEY.")
        sys.exit(1)


def consultar_api(url):
    try:
        respuesta = requests.get(url, timeout=10)

        if respuesta.status_code in (401, 403):
            print("Error: API key invalida o sin permisos.")
            sys.exit(1)

        if respuesta.status_code == 404:
            print("Error 404: recurso no encontrado en la API.")
            sys.exit(1)

        respuesta.raise_for_status()

        try:
            return respuesta.json()
        except ValueError:
            print("Error: la API respondio con JSON invalido.")
            sys.exit(1)

    except requests.exceptions.Timeout:
        print("Error: timeout al consultar la API.")
        sys.exit(1)
    except requests.exceptions.ConnectionError:
        print("Error: problema de conexion a internet o DNS.")
        sys.exit(1)
    except requests.exceptions.HTTPError as error:
        print(f"Error HTTP: {error}")
        sys.exit(1)
    except requests.exceptions.RequestException as error:
        print(f"Error inesperado de conexion: {error}")
        sys.exit(1)


def buscar_jugador(nombre_jugador):
    jugador_formateado = nombre_jugador.strip().replace(" ", "_")
    url = f"{BASE_URL}/{API_KEY}/searchplayers.php?p={jugador_formateado}"
    datos = consultar_api(url)

    if datos.get("player") is None:
        print(f"No se encontro el jugador: {nombre_jugador}")
        sys.exit(1)

    futbolistas = [
        jugador for jugador in datos["player"]
        if jugador.get("strSport") == "Soccer"
    ]

    if not futbolistas:
        print(f"El nombre '{nombre_jugador}' no corresponde a un futbolista registrado.")
        sys.exit(1)

    return futbolistas[0]


def obtener_detalle_jugador(id_jugador):
    if not id_jugador:
        return {}

    url = f"{BASE_URL}/{API_KEY}/lookupplayer.php?id={id_jugador}"
    datos = consultar_api(url)
    jugadores = datos.get("players")

    if not jugadores:
        return {}

    return jugadores[0]


def valor(campo):
    return campo or "No disponible"


def generar_informe(player, detalle):
    nombre = valor(player.get("strPlayer"))
    equipo = valor(player.get("strTeam"))
    nacionalidad = valor(player.get("strNationality"))
    posicion = valor(player.get("strPosition"))
    edad = calcular_edad(player.get("dateBorn", "N/A"))
    estado = valor(player.get("strStatus"))
    numero = valor(detalle.get("strNumber"))
    fichaje = valor(detalle.get("strSigning"))
    salario = valor(detalle.get("strWage"))
    altura = valor(detalle.get("strHeight"))
    peso = valor(detalle.get("strWeight"))
    pie = valor(detalle.get("strSide"))
    seleccion = valor(detalle.get("strTeam2"))

    print("=" * 60)
    print("SISTEMA DE SCOUTING - FOOTBALL MANAGER")
    print("=" * 60)
    print(f"Jugador consultado : {PLAYER_NAME}")
    print("-" * 60)
    print(f"Jugador            : {nombre}")
    print(f"Equipo actual      : {equipo}")
    print(f"Seleccion          : {seleccion}")
    print(f"Dorsal             : {numero}")
    print(f"Posicion           : {posicion}")
    print(f"Nacionalidad       : {nacionalidad}")
    print(f"Edad               : {edad}")
    print(f"Estado             : {estado}")
    print(f"Altura             : {altura}")
    print(f"Peso               : {peso}")
    print(f"Pie dominante      : {pie}")
    print(f"Costo fichaje      : {fichaje}")
    print(f"Salario            : {salario}")
    print("=" * 60)
    print("Consulta finalizada correctamente.")


def main():
    validar_variables_entorno()
    player = buscar_jugador(PLAYER_NAME)
    detalle = obtener_detalle_jugador(player.get("idPlayer"))
    generar_informe(player, detalle)


if __name__ == "__main__":
    main()
