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

import random
import argparse
import numpy as np

parser = argparse.ArgumentParser()
parser.add_argument("-v", "--verbose", help="Mostrar información de depuración", action="store_true")
#parser.add_argument("-f", "--file", help="Nombre de archivo a procesar")
args = parser.parse_args()

#FLAGS
debug=0

if args.verbose:
    print("[Debug Mode]")
    debug=1

 
# MCD mediante algoritmo de euclides, se comprueba que ambos números sean apropiados
def algeucl(a, b):
    if(a<0 or b<0):
        print("[ERROR] Debes introducir números positivos")
        exit(-1)

    if(b==0): return a
    return algeucl(b, a%b)

# Calcula el inverso de p en Zn, avisa en caso de no existir
def invmod(p, n):
    r = [n, p]
    s = [0, 1]
    
    count = 0
    while r[-1] != 0 and r[-1] != 1:
        q = r[count] // r[count + 1]
        r.append(r[count] % r[count + 1])
        s.append(s[count] - q * s[count + 1])
        count += 1

    if r[-1] == 0:  # No existe inverso
        print(f"[INFO] No existe inverso para {p} en Z{n}")
        return None
    else:  # Existe inverso
        inv = s[-1] % n
        print(f"[INFO] El inverso para {p} en Z{n} es {inv}")
        return inv


# Devuelve una lista con los elementos invertibles en Zn
def eulerfun(n):
    invertibles = []
    for i in range(0, n):
        if invmod(i, n): invertibles.append(i)

    print(f"[INFO] Existen los inversos en Z{n} para: {invertibles}")


    return invertibles

# Genera un valor k que sea coprimo con 26
def generar_k():
    invertibles = eulerfun(26)
    return random.choice(invertibles)

# Genera un valor d que sea coprimo con 26
def generar_d():
    while True:
        d = random.randint(0, 25)
        if algeucl(d, 26) == 1:  # d es coprimo con 26
            return d

# Devuelve la dimension si es cuadrada ó 0 si no lo es
def cuadrada(matriz):   
    if matriz is None or matriz.size == 0:  # Comprobar si la matriz no está vacía
        return 0
    
    num_filas = len(matriz)

    for fila in matriz:
        if len(fila) != num_filas:
            return 0
   
    return num_filas

# Calcula el determinante modulo n de una matriz
def determinante_modular(matriz, n):

    det = int(np.linalg.det(matriz))

    return det % n


# Devuelve la matriz resultado de eliminar la fila i y la columna j
def matriz_menor(matriz, i, j):
    menor = np.delete(matriz, i, axis=0)  # Elimina la fila i
    menor = np.delete(menor, j, axis=1)  # Elimina la columna j
    return menor

def matriz_adjunta(matriz):
    """
    Busca la adjunta de una matriz.

    Args:
        matriz: Matriz a buscar la adjunta. Debe ser en formato numpy.

    Return:
        Devuelve la matriz adjunta.
    """
    n = matriz.shape[0]  # Tamaño de la matriz
    adjunta = np.zeros((n, n))

    for i in range(n):
        for j in range(n):
            # Calcular el cofactor: (-1)^(i+j) * determinante de la matriz menor
            menor = matriz_menor(matriz, i, j)
            cofactor = (-1) ** (i + j) * np.linalg.det(menor)
            adjunta[j, i] = cofactor

    return adjunta

def InvModMatrix(matriz, n):
    """
    Calcula la inversa modular de una matriz.

    Args:
        matriz: Matriz a la que buscar inversa. Debe estar en formato numpy.
        n: Módulo.

    Return:
        Devuelve la inversa de la matriz.
    """

    if matriz is None or matriz.size == 0:
        print(f"[ERROR] La matriz no está definida")
        exit(-1)
    
    if cuadrada(matriz) == 0:
        print(f"[ERROR] La matriz no es invertible (No cuadrada)")
        exit(-1)

    det = determinante_modular(matriz, n)

    if det == 0:
        print(f"[ERROR] La matriz no es invertible (Det=0)")
        exit(-1)
    
    if algeucl(det, n)!=1:
        print(f"[ERROR] La matriz no es invertible (GCD(det,n)!=1)")
        exit(-1)

    det_inv = invmod(det, n)
    adjunta = matriz_adjunta(matriz)

    inversa_mod = (det_inv * adjunta) % n

    # Redondear los valores y aplicar el módulo n para obtener enteros en Zn
    inversa_mod = np.round(inversa_mod).astype(int) % n

    return inversa_mod

def TexttoNumber(a):
    """
    Convierte un string en una cadena numerica.

    Args:
        a: String a convertir.

    Returns:
        Devuelve una cadena numérica (a->01, b->02...).
    """

    result = []
    for char in a.lower():
        if 'a' <= char <= 'z':
            num = ord(char) - ord('a')
            # Asegúrate de que cada número tenga dos dígitos, agregando un cero si es necesario
            result.append(f"{num:02}")
        else: result.append('30')
    return ''.join(result)

def NumberstoText(a):
    """
    Convierte una cadena numerica en un string.

    Args:
        a: Cadena numérica a convertir.

    Returns:
        Devuelve un string legible.
    """

    result = []
    # Procesa la cadena en bloques de 2 caracteres
    for i in range(0, len(a), 2):
        
        if a[i:i+2] == '##': num = 30
        else: num = int(a[i:i+2])  # Convierte el bloque a un número

        # Convierte el número a letra (00 -> 'a', 01 -> 'b', etc.)
        if 0 <= num <= 26:
            result.append(chr(num + ord('a')))
        else: result.append('#')
    return ''.join(result)

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
            if debug: print(f"[DEBUG] Cifrando -> {num} => {(num*k + d)%26}") #DEBUG
            
            num = (num*k + d)%26
            ciphered += str(num).zfill(2) # Aplica el cifrado afin f(x)=kx+d mod 26

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

    inv_k = invmod(k, 26)

    deciphered = ""
    # Procesa la cadena en bloques de 2 caracteres
    for i in range(0, len(text), 2):

        if text[i:i+2] == '##': num = 30
        else: num = int(text[i:i+2])  # Convierte el bloque a un número

        if 0 <= num <= 26:
            if debug: print(f"[DEBUG] Descifrando -> {num} => {((num - d) * inv_k) % 26}") #DEBUG
            
            num = ((num - d) * inv_k) % 26
            deciphered += str(num).zfill(2) # Aplica el descifrado afin f(x)=kx+d mod 26

        else: deciphered += '##'

    return deciphered

def main():
    """
    Lógica del menú.
    """

    while True:
        print("\n--- Menú ---")
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
            k = generar_k()
            d = generar_d()
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