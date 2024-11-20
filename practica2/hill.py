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
    * No funciona
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

# Cifrado Hill
def hillcipher(text, key_matrix):

    n = len(key_matrix)
    
    if not cuadrada(key_matrix):
        raise ValueError("La clave debe ser una matriz cuadrada.")
    
    text_numbers = TexttoNumber(text)

    while len(text_numbers) % n != 0:
        text_numbers.append(0)  # Padding con 'a'

    encrypted = []
    for i in range(0, len(text_numbers), n):

        block = text_numbers[i:i + n]
        
        # Inicializamos el bloque cifrado como una lista vacía
        result = []
        # Iteramos por cada columna de la matriz clave
        for k in range(n):
            suma = 0  # Inicializamos la suma para la columna actual
            for j in range(n):  # Iteramos por cada elemento del bloque
                suma += int(block[j]) * key_matrix[j][k]  # Multiplicamos y acumulamos
            suma_mod = suma % 26  # Reducimos el resultado módulo 26
            result.append(str(suma_mod))  # Añadimos el valor cifrado al bloque
        encrypted.extend(result)
    return NumberstoText("".join(encrypted))

# Descifrado Hill
def hilldecipher(encrypted_text, key_matrix):

    inverse_key = InvModMatrix(key_matrix, 26)

    encrypted_numbers = TexttoNumber(encrypted_text)

    n = len(inverse_key)

    decrypted = []
    for i in range(0, len(encrypted_numbers), n):

        block = encrypted_numbers[i:i + n]

        # Inicializamos el bloque cifrado como una lista vacía
        result = []
        # Iteramos por cada columna de la matriz clave
        for k in range(n):
            # Calculamos la suma de productos para la columna actual
            suma = 0
            for j in range(n):
                suma += int(block[j]) * key_matrix[j][k]
            
            # Reducimos el resultado módulo 26 y lo añadimos al bloque cifrado
            result.append(str(suma % 26))
        
        decrypted.extend(result)
    return NumberstoText("".join(decrypted))

# Generar clave aleatoria para Hill
def generar_clave_hill(n):
    while True:
        clave = [[random.randint(0, 25) for _ in range(n)] for _ in range(n)]
        if determinante_modular(clave, 26) != 0 and algeucl(determinante_modular(clave, 26), 26) == 1:
            return clave

# Pruebas
def main():
    print("Cifrado Hill")
    key = generar_clave_hill(2)  # Matriz 2x2 como clave
    print("Clave generada:", key)
    mensaje = input("Introduce el mensaje a cifrar: ")
    cifrado = hillcipher(mensaje, key)
    print("Texto cifrado:", cifrado)
    descifrado = hilldecipher(cifrado, key)
    print("Texto descifrado:", descifrado)

if __name__ == "__main__":
    main()