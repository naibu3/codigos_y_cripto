#!/usr/bin/env python
# -*- coding: utf-8 -*-
 
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

# Devuelve la dimension si es cuadrada ó 0 si no lo es
def cuadrada(matriz):   
    if not matriz:  # Comprobar si la matriz no está vacía
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

    if not matriz:
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

if __name__ == "__main__":

    matiz = [
        [3, 1],
        [2, 3]]

    print(algeucl(3,4))
    print(determinante_modular(matiz, 4))
    print(InvModMatrix(matiz, 4))