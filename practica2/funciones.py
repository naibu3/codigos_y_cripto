#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Practica 1.1 - Funciones útiles

Estas son funciones necesarias para la implementación de cifrado afín y Hill, 

Example:

    import funciones
"""

import random

MODULO = 27

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

# Genera un valor k que sea coprimo con el modulo m
def generar_k(m):
    invertibles = eulerfun(27)
    return random.choice(invertibles)

# Genera un valor d que sea coprimo con el modulo  m
def generar_d(m):
    while True:
        d = random.randint(0, 25)
        if algeucl(d, m) == 1:  # d es coprimo con m
            return d

# Devuelve la dimension si es cuadrada ó 0 si no lo es
def cuadrada(matriz):   
    if matriz is None or len(matriz) == 0:  # Comprobar si la matriz no está vacía
        return 0
    
    num_filas = len(matriz)

    for fila in matriz:
        if len(fila) != num_filas:
            return 0
   
    return num_filas

# Calcula el determinante modulo n de una matriz
def determinante_modular(matriz, n):
    if len(matriz) == 1:
        return matriz[0][0] % n
    det = 0
    for j in range(len(matriz)):
        menor = matriz_menor(matriz, 0, j)
        signo = (-1) ** j
        det += signo * matriz[0][j] * determinante_modular(menor, n)
    return det % n


# Devuelve la matriz resultado de eliminar la fila i y la columna j
def matriz_menor(matriz, i, j):
    return [fila[:j] + fila[j + 1:] for fila in (matriz[:i] + matriz[i + 1:])]

def matriz_adjunta(matriz, m):
    """
    Busca la adjunta de una matriz.

    Args:
        matriz: Matriz a buscar la adjunta.
        m: Modulo m.

    Return:
        Devuelve la matriz adjunta.
    """

    n = len(matriz)
    adjunta = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            menor = matriz_menor(matriz, i, j)
            cofactor = (-1) ** (i + j) * determinante_modular(menor, m)
            adjunta[j][i] = cofactor
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

    if matriz is None or len(matriz) == 0:
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
    adjunta = matriz_adjunta(matriz, n)

    inversa_mod = []
    # Iteramos por cada fila de la matriz adjunta
    for i in range(len(adjunta)):
        fila_inversa = []  # Creamos una lista para almacenar la fila actual de la matriz inversa
        for j in range(len(adjunta[i])):
            # Calculamos el valor modular para el elemento actual
            elemento_mod = (det_inv * adjunta[i][j]) % n
            fila_inversa.append(elemento_mod)  # Añadimos el elemento calculado a la fila
        inversa_mod.append(fila_inversa)

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
        else: result.append('27')
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
        
        if a[i:i+2] == '##': num = 27
        else: num = int(a[i:i+2])  # Convierte el bloque a un número

        # Convierte el número a letra (00 -> 'a', 01 -> 'b', etc.)
        if 0 <= num <= 26:
            result.append(chr(num + ord('a')))
        else: result.append('#')
    return ''.join(result)