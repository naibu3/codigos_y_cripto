#!/usr/bin/python3
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

def leer_matriz():
    """
    Permite al usuario introducir una matriz en formato Python.
    Ejemplo: [[17, 22], [22, 7]]

    Returns:
        list: La matriz introducida como una lista de listas.
    """
    try:
        entrada = input("Introduce la matriz en formato [[a, b], [c, d]]: ")
        matriz = eval(entrada)
        if not all(isinstance(fila, list) for fila in matriz):
            raise ValueError("La entrada no es una matriz válida.")
        return matriz
    except Exception as e:
        print(f"Error: {e}")
        print("Asegúrate de introducir la matriz en el formato correcto.")
        return leer_matriz()  # Reintentar

# Cifrado Hill
def hillcipher(text, key_matrix):

    n = cuadrada(key_matrix)
    
    if n == 0:
        raise ValueError("La clave debe ser una matriz cuadrada.")
    
    text_numbers = TexttoNumber(text)
    
    #NO ES NECESARIO
    #while len(text_numbers) % n != 0:
    #    text_numbers.append(27)  # Padding con '#'

    if debug: print(f"[DEBUG] TexttoNumber={text_numbers} ({type(text_numbers)})")

    # Creamos una lista con los numeros
    bloques = [int(text_numbers[i:i + 2]) for i in range(0, len(text_numbers), 2)]

    if debug: print(f"[DEBUG] Bloques={bloques} ({type(bloques)})")

    encrypted = []
    for i in range(0, len(bloques), n):
        
        block = bloques[i:i + n]

        if debug: print(f"[DEBUG] Bloque a cifrar => {block} ({type(block)})")

        # Inicializamos el bloque cifrado como una lista vacía
        result = []
        # Iteramos por cada fila de la matriz clave
        for k in range(n):
            suma = 0  # Inicializamos la suma para la columna actual
            for j in range(n):  # Iteramos por cada columna de la clave/elemento del bloque
                suma += block[j] * key_matrix[k][j]  # Multiplicamos y acumulamos
            suma_mod = suma % MODULO  # Reducimos el resultado módulo MODULO

            # Añadimos el valor cifrado al bloque (asegurando que tenga 2 cifras)
            result.append(str(suma_mod).zfill(2))  
        
        encrypted.extend(result)
    
    if debug: print(f"[DEBUG] encrypted={encrypted}")
    if debug: print(f"[DEBUG] returned={NumberstoText(''.join(encrypted))}")

    return NumberstoText("".join(encrypted))

# Descifrado Hill
def hilldecipher(encrypted_text, key_matrix):

    inverse_key = InvModMatrix(key_matrix, MODULO)

    n = len(inverse_key)

    # Tratamiento de la entrada
    encrypted_numbers = TexttoNumber(encrypted_text)

    if debug: print(f"[DEBUG] Encripted numbers={encrypted_numbers} ({type(encrypted_numbers)})")

    # Creamos una lista con los numeros
    bloques = [int(encrypted_numbers[i:i + 2]) for i in range(0, len(encrypted_numbers), 2)]

    if debug: print(f"[DEBUG] Bloques={bloques} ({type(bloques)})")

    decrypted = []
    for i in range(0, len(bloques), n):

        block = bloques[i:i + n]

        if debug: print(f"[DEBUG] Bloque a descifrar => {block} ({type(block)})")

        # Inicializamos el bloque cifrado como una lista vacía
        result = []
        # Iteramos por cada columna de la matriz clave
        for k in range(n):
            # Calculamos la suma de productos para la fila actual
            suma = 0
            for j in range(n):
                suma += block[j] * inverse_key[k][j]
            
            suma_mod = suma % MODULO  # Reducimos el resultado módulo MODULO

            # Lo añadimos al mensaje descifrado asegurando que tenga 2 cifras
            result.append(str(suma_mod).zfill(2))

        if debug: print(f"[DEBUG] decrypted block={result}")

        decrypted.extend(result)
    
    if debug: print(f"[DEBUG] decrypted={decrypted}")
    if debug: print(f"[DEBUG] returned={NumberstoText(''.join(decrypted))}")

    return NumberstoText("".join(decrypted))

# Generar clave aleatoria para Hill
def generar_clave_hill(n):
    while True:
        clave = [[random.randint(0, 25) for _ in range(n)] for _ in range(n)]
        if determinante_modular(clave, MODULO) != 0 and algeucl(determinante_modular(clave, MODULO), MODULO) == 1:
            return clave

def generar_clave_menu():

    while True:
        print("\n===== Cifrado Hill - Generar Clave ======")
        print("1. Aleatoria")
        print("2. Introducir manualmente")
        print("3. Volver")

        opcion = input("[*] Elige una opción: ")

        if opcion == "1":
            n = input("[*] Elige el tamaño de la matriz: ")
            n = int(n)
            return generar_clave_hill(n)
        
        elif opcion == "2":
            return leer_matriz()
        
        elif opcion == "3":
            print("[!] No se ha generado ninguna clave.")
            break
        else:
            print("Opción no válida. Inténtalo de nuevo.")

# Pruebas
def main_menu():
    """
    Lógica del menú.
    """

    key = []

    while True:
        print("\n===== Cifrado Hill ======")
        print("1. Establecer clave")
        print("2. Cifrar mensaje")
        print("3. Descifrar mensaje")
        print("4. Salir")

        opcion = input("Elige una opción: ")

        if opcion == "1":
            key =  generar_clave_menu()
            print(f"[+] Clave: {key}")
        elif opcion == "2":
            mensaje = input("Introduce el mensaje a cifrar: ")
            mensaje_cifrado = hillcipher(mensaje, key)
            print(f"[+] Mensaje cifrado: {mensaje_cifrado}")
        elif opcion == "3":
            mensaje_cifrado = input("[*] Introduce el mensaje cifrado a descifrar: ")
            descifrado = hilldecipher(mensaje_cifrado, key)
            print(f"[+] Mensaje descifrado: {descifrado}")
        elif opcion == "4":
            print("[+] Saliendo del programa.")
            break
        else:
            print("[!] Opción no válida. Inténtalo de nuevo.")

if __name__ == "__main__":
    main_menu()
