#!/usr/bin/env python3

import json
import urllib.request
import platform

# cmd.exe con la fuente por defecto (Raster Fonts) no puede mostrar €
if platform.system() == "Windows":
    EUR = "EUR"
else:
    EUR = "€"


def estado_sorteo():
    url_elpais = "https://api.elpais.com/ws/LoteriaNavidadPremiados?s=1"
    respuesta = urllib.request.urlopen(url_elpais)
    contenido = respuesta.read()
    datos = json.loads(contenido.decode("utf8").replace("info=", ""))
    status = datos["status"]
    estado = None
    if status == 0:
        estado = "El sorteo no ha comenzado."
    elif status == 1:
        estado = "El sorteo ha empezado. Lista de premios parcial."
    elif status == 2:
        estado = "Sorteo terminado. Lista de premios provisional."
    elif status == 3:
        estado = "Sorteo terminado. Lista de premios semioficial."
    elif status == 4:
        estado = "Sorteo terminado. Lista de premios oficial."
    print("\n=====>", estado, "\n\n")


def consultar(n):
    url_elpais = "https://api.elpais.com/ws/LoteriaNavidadPremiados?n=" + n
    respuesta = urllib.request.urlopen(url_elpais)
    contenido = respuesta.read()
    datos = json.loads(contenido.decode("utf8").replace("busqueda=", ""))
    premio = float(datos["premio"])
    return premio


estado_sorteo()

fichero_jugados = open("mis_numeros.txt", "r")

total_ganado = 0.0
total_jugado = 0.0
for linea in fichero_jugados:
    linea_limpia = (
        linea.rstrip("\n").replace(" ", "").replace(",", ".").replace("=", ":")
    )
    if linea_limpia == "":
        continue
    numero, jugado = (
        linea.rstrip("\n")
        .replace(" ", "")
        .replace(",", ".")
        .replace("=", ":")
        .split(":")
    )
    ganado_decimo = consultar(str(int(numero)))
    he_ganado = max(float(jugado) * ganado_decimo / 20, 0)
    total_ganado += he_ganado
    total_jugado += float(jugado)
    print(
        "Número: " + "{0:05d}".format(int(numero)),
        "Jugado: " + "{0:6.2f}".format(float(jugado)) + " " + EUR,
        "Ganado: " + "{0:10.2f}".format(he_ganado) + " " + EUR,
        sep="\t|\t",
    )

print("\n=============================")
print("Total Jugado = " + "{0:10.2f}".format(total_jugado), EUR)
print("Total Ganado = " + "{0:10.2f}".format(total_ganado), EUR)
print("Saldo        = " + "{0:10.2f}".format(total_ganado - total_jugado), EUR)

if platform.system() == "Windows":
    input()
