#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Practica 1.1 - Cifrado Afín

En esta práctica se implementan varias funciones relacionadas con el cifrado Afín,
así como una pequeña interfaz de pruebas a modo de demostración.

Example:

    $ python afin.py

Paquetes necesarios para generar la documentación:

    $pip install sphinx sphinxcontrib-napoleon
    $sphinx-quickstart

En `conf.py` añade:

    $extensions = ['sphinx.ext.autodoc', 'sphinxcontrib.napoleon']

Para generar la propia documentación:

    $make html

Todo:
    * Terminar de comentar codigo correctamente.
    * Criptoanálisis.
"""

import argparse
from funciones import *

parser = argparse.ArgumentParser()
parser.add_argument("-v", "--verbose", help="Mostrar información de depuración", action="store_true")
#parser.add_argument("-f", "--file", help="Nombre de archivo a procesar")
args = parser.parse_args()

#FLAGS
debug=0

if args.verbose:
    print("[Debug Mode]")
    debug=1

def Afincypher(text, k, d):
    """
    Cifra utilizando cifrado afín.

    Args:
        text: Texto a cifrar.
        k: Valor k.
        d: Varlor d.

    Return:
        Devuelve la cadena numérica correspondiente al texto cifrado.
    """
    tocipher = TexttoNumber(text)

    ciphered = ""
    # Procesa la cadena en bloques de 2 caracteres
    for i in range(0, len(tocipher), 2):
        
        num = int(tocipher[i:i+2])  # Convierte el bloque a un número

        if 0 <= num <= 26:
            if debug: print(f"[DEBUG] Cifrando -> {num} => {(num*k + d)%MODULO}") #DEBUG
            
            num = (num*k + d) % MODULO
            ciphered += str(num).zfill(2) # Aplica el cifrado afin f(x)=kx+d mod MODULO

        else: ciphered += '##'

    return ciphered

def Afindecypher(text, k, d):
    """
    Descifra un texto cifrado con cifrado afín.

    Args:
        text: Texto a descifrar.
        k: Valor k.
        d: Varlor d.

    Return:
        Devuelve la cadena numérica correspondiente al texto cifrado.
    """

    inv_k = invmod(k, MODULO)

    deciphered = ""
    # Procesa la cadena en bloques de 2 caracteres
    for i in range(0, len(text), 2):

        if text[i:i+2] == '##': num = 27
        else: num = int(text[i:i+2])  # Convierte el bloque a un número

        if 0 <= num <= 26:
            if debug: print(f"[DEBUG] Descifrando -> {num} => {((num - d) * inv_k) % MODULO}") #DEBUG
            
            num = ((num - d) * inv_k) % MODULO
            deciphered += str(num).zfill(2) # Aplica el descifrado afin f(x)=kx+d mod MODULO

        else: deciphered += '##'

    return deciphered

def main():
    """
    Lógica del menú.
    """

    while True:
        print("\n--- CIFRADO AFIN ---")
        print("1. Ingresar k y d")
        print("2. Generar k y d aleatorios")
        print("3. Cifrar mensaje")
        print("4. Descifrar mensaje")
        print("5. Salir")

        opcion = input("Elige una opción: ")

        if opcion == "1":
            k = int(input("Introduce el valor de k (0 <= k < 26) y asegúrate de que tiene inverso: "))
            d = int(input("Introduce el valor de d (0 <= d < 26) y asegúrate de que es coprimo con 26: "))
        elif opcion == "2":
            k = generar_k(MODULO)
            d = generar_d(MODULO)
            print(f"Valores generados: k = {k}, d = {d}")
        elif opcion == "3":
            mensaje = input("Introduce el mensaje a cifrar: ")
            cifrado = Afincypher(mensaje, k, d)
            print(f"Mensaje cifrado: {cifrado}")
        elif opcion == "4":
            mensaje_cifrado = input("Introduce el mensaje cifrado a descifrar: ")
            descifrado = Afindecypher(mensaje_cifrado, k, d)
            print(f"Mensaje descifrado: {NumberstoText(descifrado)}")
        elif opcion == "5":
            print("Saliendo del programa.")
            break
        else:
            print("Opción no válida. Inténtalo de nuevo.")

if __name__ == "__main__":

    main()