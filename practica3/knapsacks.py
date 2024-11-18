#!/bin/python3
# -*- coding: utf-8 -*-

"""Practica 3 - Mochilas

En esta práctica se implementan varias funciones relacionadas con el cifrado mediante mochilas,
así como una pequeña interfaz de pruebas a modo de demostración.

Example:

    $ python knapsacks.py.py

Paquetes necesarios para generar la documentación:

    $pip install sphinx sphinxcontrib-napoleon
    $sphinx-quickstart

En `conf.py` añade:

    $extensions = ['sphinx.ext.autodoc', 'sphinxcontrib.napoleon']

Para generar la propia documentación:

    $make html

Todo:
    * Terminar de comentar codigo correctamente.
    * Implementar menu.
    * Implementar criptoanalisis.
"""

import math
import random
import time
from sympy import mod_inverse, gcd

#========================================================================
#   FUNCIONES AUXILIARES
#========================================================================

def letter2ascii(letter):
    """
    Convierte una letra en su representación ASCII binaria de 8 bits.
    
    Args:
        letter: Carácter a convertir.

    Returns:
        Devuelve la representación ASCII binaria.
    """
    return format(ord(letter), '08b')

def ascii2letter(binary_str):
    """
    Convierte una cadena binaria de 8 bits en la letra ASCII correspondiente.
    
    Args:
        binary_str: Cadena binaria a convertir.

    Returns:
        Devuelve un carácter.
    """
    return chr(int(binary_str, 2))

# Determina si es una mochila supercreciente
def knapsack(s):
    """
    Determina si una mochila es supercreciente.

    Args:
        s: Mochila.

    Returns:
      1 si la mochila es supercreciente,
      0 si es una mochila no supercreciente,
     -1 si no es una mochila.
    """
    if len(s) == 0:
        return -1

    # Verificar si es supercreciente
    suma = 0
    for elem in s:
        if elem <= suma:
            return 0
        suma += elem
    return 1

# Determine si v es valor objetivo de una mochila
def knapsacksol(s, v):
    """
    Determina si el valor v puede ser alcanzado por una combinación de elementos de la mochila (supercreciente o no) s.

    Args:
        s: Mochila (supercreciente o no).
        v: Valor.
    """
    # Se asume que s es una mochila supercreciente
    result = []
    for elem in reversed(s):
        if v >= elem:
            result.append(1)
            v -= elem
        else:
            result.append(0)
    return list(reversed(result)) if v == 0 else None

# Comprueba si un valor tiene factores primos en comun con algún elemento de una mochila
def commonfactors(w, s):
    """
    Comprueba si `w` tiene factores primos comunes con alguno de los elementos de `s`.

    Args:
        w: Valor.
        s: Mochila.
    
    Return:
        True si no tiene factores comunes con ninguno, False si los hay.
    """
    for value in s:
        if math.gcd(w, value) != 1:
            return False
    return True

#========================================================================
#   CIFRADO/DESCIFRADO CON MOCHILAS NORMALES
#========================================================================

def knapsackcipher(text, knapsack):
    """
    Cifra un mensaje utilizando una mochila `knapsack`.

    Args:
        text: Mensaje a cifrar.
        knapsack: Mochila.

    Return:
        Un vector numérico con el mensaje cifrado.
    """
    # Convertir cada letra del texto en binario de 8 bits
    binary_text = ''.join(letter2ascii(char) for char in text)
    
    # Dividir en bloques del tamaño de la mochila
    n = len(knapsack)
    blocks = [binary_text[i:i + n] for i in range(0, len(binary_text), n)]
    
    # Añadir 1s si es necesario para completar el último bloque
    if len(blocks[-1]) < n:
        blocks[-1] = blocks[-1].ljust(n, '1')
    
    # Cifrar cada bloque
    encrypted = []
    for block in blocks:
        encrypted.append(sum(int(block[i]) * knapsack[i] for i in range(n)))

    return encrypted

def knapsackdecipher(encrypted_text, s):
    """
    Descifra un vector numérico `encrypted_text` utilizando una mochila supercreciente `s`.

    Args:
        encrypted_text: Texto encriptado.
        s: Mochila supercreciente.
    
    Return:
        El texto en claro.
    """
    decrypted_binary = ''
    for value in encrypted_text:
        solution = knapsacksol(s, value)
        if solution is None:
            raise ValueError("[!] No se puede descifrar el texto con la mochila proporcionada.")
        decrypted_binary += ''.join(map(str, solution))
    
    # Convertir el binario de vuelta a texto ASCII de 8 bits
    text = ''.join(ascii2letter(decrypted_binary[i:i+8]) for i in range(0, len(decrypted_binary), 8))
    return text

#========================================================================
#   CIFRADO/DESCIFRADO CON MOCHILAS TRAMPA
#========================================================================

def knapsackpublicandprivate(super_knapsack, m=None, w=None):
    """
    Genera una pareja de claves pública (mochila con trampa) y privada (w y m) a partir de una mochila supercreciente.
    
    Args:
        super_knapsack: Mochila supercreciente.
        m: Valor m.
        w: Valor w.

    Solicita al usuario valores adecuados para `m` y `w` si no son proporcionados.
    
    Return:
        Un diccionario con las claves pública y privada.
    """
    
    # Solicitar el valor de m si no es proporcionado
    if m is None:
        m = int(input("[*] Ingrese un valor para m que sea mayor que la suma de todos los elementos de la mochila: "))
        while m <= sum(super_knapsack):
            m = int(input("[*] El valor de m debe ser mayor que la suma de los elementos de la mochila. Ingrese un nuevo valor: "))
    
    # Determinar w si no se proporciona, buscando un valor coprimo con m y con todos los elementos de la mochila
    if w is None:
        random_search = input("[*] ¿Desea una búsqueda aleatoria para w? (s/n): ").lower() == 's'
        while True:
            if random_search:
                w = random.randint(2, m - 1)
            else:
                w = int(input("[*] Ingrese un valor para w (debe ser coprimo con m y con los elementos de la mochila): "))

            # Verificar que w y m son coprimos y que w no tiene factores comunes con los elementos de la mochila
            if math.gcd(w, m) == 1 and commonfactors(w, super_knapsack):
                break
            else:
                print("[!] El valor de w no es adecuado. Intente de nuevo.")
    
    # Generar la mochila con trampa
    public_knapsack = [(w * ai) % m for ai in super_knapsack]
    
    # Devolver las claves
    return {
        "public_key": public_knapsack,
        "private_key": {"super_knapsack": super_knapsack, "m": m, "w": w}
    }

def knapsackdeciphermh(super_knapsack, m, w, encrypted_text):
    """
    Descifra un mensaje cifrado con una mochila trampa utilizando el inverso modular de `w` módulo `m`.

    Args:
        super_knapsack: La mochila supercreciente original.
        m: El valor módulo de la clave privada.
        w: El multiplicador de la clave privada.
        encrypted_text: El mensaje cifrado (lista de valores).

    Return:
        El mensaje descifrado como texto en claro.
    """
    # Calcular el inverso modular de w módulo m usando sympy
    w_inverse = mod_inverse(w, m)
    
    # Decodificar cada número cifrado en el mensaje
    decrypted_binary = ''
    for value in encrypted_text:
        # Multiplicar el valor cifrado por el inverso modular de w y reducir módulo m
        modified_value = (value * w_inverse) % m
        
        # Resolver la mochila supercreciente para encontrar la combinación de bits
        solution = knapsacksol(super_knapsack, modified_value)
        if solution is None:
            raise ValueError("[!] No se puede descifrar el mensaje con la mochila proporcionada.")
        
        # Convertir la solución a una cadena binaria y añadirla al mensaje descifrado
        decrypted_binary += ''.join(map(str, solution))
    
    # Convertir el binario en bloques de 8 bits y transformarlo en caracteres ASCII
    text = ''.join(ascii2letter(decrypted_binary[i:i+8]) for i in range(0, len(decrypted_binary), 8))
    return text

#========================================================================
#   CRIPTOANÁLISIS DE SHAMIR Y ZIPPEL
#========================================================================

def shamir_zippel_attack(public_knapsack, m, max_range=100):
    """
    Ataque de Shamir y Zippel para recuperar una mochila supercreciente a partir de una mochila con trampa.

    Args:
        public_knapsack: Mochila pública.
        m: Módulo utilizado para construir la mochila pública.
        max_range: Rango máximo para probar valores de múltiplos modulares.

    Returns:
        Mochila supercreciente recuperada o None si no se encuentra.
    """
    n = len(public_knapsack)

    for range_start in range(1, max_range, 10):  # Probar en bloques de 10
        range_end = min(range_start + 10, max_range)
        print(f"\nBuscando en el rango {range_start} a {range_end}...")
        
        # Iniciar el cronómetro para medir el tiempo en este rango
        start_time = time.time()

        for i in range(n - 1):  # Probar pares consecutivos S1, S2
            S1, S2 = public_knapsack[i], public_knapsack[i + 1]
            if gcd(S2, m) != 1:
                continue  # Ignorar si no cumplen mcd(S2, m) = 1

            # Paso 1: Calcular q
            q = (S1 * mod_inverse(S2, m)) % m

            # Paso 2: Generar múltiplos modulares de q
            multiples = [(k * q) % m for k in range(range_start, range_end + 1)]
            multiples = sorted(set(multiples))  # Evitar duplicados y ordenar

            # Paso 3-6: Iterar sobre posibles valores de S1'
            for candidate in multiples:
                if gcd(candidate, m) != 1:
                    continue  # Ignorar si mcd(S1', m) ≠ 1

                # Paso 4: Calcular w
                w = (S1 * mod_inverse(candidate, m)) % m

                # Paso 5: Construir mochila supercreciente
                w_inv = mod_inverse(w, m)
                super_knapsack = [(si * w_inv) % m for si in public_knapsack]

                # Verificar si es supercreciente
                if knapsack(super_knapsack) == 1:
                    elapsed_time = time.time() - start_time
                    print(f"Tiempo en rango {range_start}-{range_end}: {elapsed_time:.2f} segundos")
                    print(f"Mochila supercreciente encontrada: {super_knapsack}")
                    return super_knapsack

        # Medir el tiempo que tomó analizar el rango actual
        elapsed_time = time.time() - start_time
        print(f"Tiempo en rango {range_start}-{range_end}: {elapsed_time:.2f} segundos")

        # Preguntar al usuario si desea continuar con el siguiente rango
        continue_search = input("¿Desea continuar con el siguiente rango? (s/n): ").strip().lower()
        if continue_search != 's':
            print("Búsqueda de criptoanálisis finalizada.")
            break

    print("No se encontró una mochila supercreciente para descifrar el mensaje.")
    return None

#========================================================================
#   MENU
#========================================================================

def main_menu():
    """
    Menú principal para interactuar con las funciones de cifrado, descifrado y criptoanálisis.
    """
    while True:
        print("\n==== Menú Principal ====")
        print("[1] Cifrar un mensaje")
        print("[2] Descifrar un mensaje")
        print("[3] Generar una mochila publica y privada")
        print("[4] Realizar criptoanálisis (Shamir y Zippel)")
        print("[5] Salir")
        
        choice = input("[*] Elige una opción (1/2/3/4): ").strip()
        
        if choice == "1":
            cipher_message()
        elif choice == "2":
            decipher_message()
        elif choice == "3":
            generate_public_private_key()
        elif choice == "4":
            perform_cryptoanalysis()
        elif choice == "5":
            print("[+] ¡Hasta luego!")
            break
        else:
            print("[!] Opción no válida. Intenta de nuevo.")

def parse_knapsack_input(input_str):
    """
    Procesa la entrada del usuario para convertirla en una lista de enteros.
    
    Args:
        input_str: Cadena de entrada del usuario que representa una lista en formato Python.
    
    Returns:
        Una lista de enteros si la entrada es válida.
    """
    try:
        # Quitar corchetes y dividir por comas
        input_str = input_str.strip().strip('[]')
        knapsack = [int(x.strip()) for x in input_str.split(',')]
        return knapsack
    except ValueError:
        raise ValueError("[!] Entrada inválida. Asegúrate de usar el formato [1, 2, 3, ...] con números enteros.")

def cipher_message():
    """
    Opción del menu que permite cifrar un mensaje utilizando una mochila.
    """
    print("\n==== Cifrar un mensaje ====")
    message = input("[*] Introduce el mensaje a cifrar: ").strip()
    
    # Opción para elegir mochila
    choice = input("[*] ¿Deseas usar una mochila específica o generar una aleatoria? (elegir/generar): ").strip().lower()
    if choice == "elegir":
        knapsack = input("[*] Introduce la mochila  (ejemplo: [2, 3, 7, 14]): ").strip()
        knapsack = parse_knapsack_input(knapsack)
    else:
        knapsack = generate_random_knapsack()
        print(f"[+] Se generó una mochila aleatoria: {knapsack}")
    
    # Cifrar el mensaje
    encrypted = knapsackcipher(message, knapsack)
    print(f"[+] Mensaje cifrado: {encrypted}")

def decipher_message(): #TODO - Permitir descifrar con mochila trampa
    """
    Permite descifrar un mensaje cifrado utilizando una mochila supercreciente.
    """
    print("\n==== Descifrar un mensaje ====")
    encrypted_message = input("[*] Introduce el mensaje cifrado (ejemplo: [82, 123, 39]): ").strip()
    encrypted_message = parse_knapsack_input(encrypted_message)
    
    knapsack = input("[*] Introduce la mochila (ejemplo: [2, 3, 7, 14]): ").strip()
    knapsack = parse_knapsack_input(knapsack)
    
    try:
        decrypted = knapsackdecipher(encrypted_message, knapsack)
        print(f"[+] Mensaje descifrado: {decrypted}")
    except ValueError as e:
        print(f"[!] Error al descifrar: {e}")

def perform_cryptoanalysis():
    """
    Permite realizar el ataque de criptoanálisis de Shamir y Zippel.
    """
    print("\n==== Criptoanálisis (Shamir y Zippel) ====")

    # Opción para elegir mochila
    choice = input("[*] ¿Deseas realizar un criptoanálisis de ejemplo o indicar una mochila? (default/custom): ").strip().lower()
    if choice == "default":
        public_knapsack = [35, 137, 41, 149, 65, 197]
        m=300
        w=67
        print(f"\n\n[+] Probando para la mochila {public_knapsack}, (m={m}, w={w})")
    else:
        public_knapsack = input("[*] Introduce la mochila pública separada por comas (ejemplo: 82,123,39): ").strip()
        public_knapsack = [int(x) for x in public_knapsack.split(",")]
    
        m = int(input("[*] Introduce el valor del módulo m: ").strip())
        #max_range = int(input("Introduce el rango máximo para el ataque: ").strip())
    
    recovered_knapsack = shamir_zippel_attack(public_knapsack, m)

    if recovered_knapsack:
        print(f"[+] Mochila supercreciente recuperada: {recovered_knapsack}")
    else:
        print("[!]No se pudo recuperar una mochila supercreciente.")

def generate_random_knapsack(size=7, start=2, step=2):
    """
    Genera una mochila aleatoria para el cifrado.

    Args:
        size: Tamaño de la mochila.
        start: Valor inicial.
        step: Incremento mínimo para garantizar supercrecimiento.

    Return:
        Devuelve la mochila generada.
    """
    knapsack = [start]
    for _ in range(1, size):
        knapsack.append(knapsack[-1] + random.randint(step, step * 2))
    return knapsack

def generate_public_private_key():
    """
    Genera una clave pública y privada a partir de una mochila supercreciente ingresada.
    """
    print("\n==== Generar Clave Pública y Privada ====")
    super_knapsack = generate_random_knapsack()

    try:

        # Pedir valores de m y w o generarlos automáticamente
        m = input("[*] Introduce un valor para m (debe ser mayor que la suma de la mochila) o presiona Enter para generarlo automáticamente: ").strip()
        if m:
            m = int(m)
        else:
            m = sum(super_knapsack) + random.randint(1, 100)

        w = input("[*] Introduce un valor para w (coprimo con m y los elementos de la mochila) o presiona Enter para generarlo automáticamente: ").strip()
        if w:
            w = int(w)
            if gcd(w, m) != 1 or not commonfactors(w, super_knapsack):
                raise ValueError("[!] El valor de w no es adecuado. Debe ser coprimo con m y los elementos de la mochila.")
        else:
            # Generar automáticamente w
            w = random.randint(2, m - 1)
            while gcd(w, m) != 1 or not commonfactors(w, super_knapsack):
                w = random.randint(2, m - 1)

        # Generar las claves
        keys = knapsackpublicandprivate(super_knapsack, m, w)
        print(f"[+] Clave pública (mochila trampa): {keys['public_key']}")
        print(f"[+] Clave privada: (m = {keys['private_key']['m']}, w = {keys['private_key']['w']})")
        print(f"[+] Mochila supercreciente original (clave privada): {keys['private_key']['super_knapsack']}")
    except ValueError as e:
        print(e)
    except Exception as e:
        print(f"[!] Error al generar las claves: {e}")

#========================================================================
#   FLUJO DE EJECUCIÓN PRINCIPAL
#========================================================================

if __name__ == "__main__":
    
    main_menu()

    ## DEBUG CODE

    # # Mochila supercreciente para pruebas
    # mochila = (1, 2, 5, 10)

    # # Prueba de la función knapsack
    # if knapsack(mochila):
    #     print(f"{mochila} es supercreciente")

    # # Prueba de la función knapsacksol
    # if knapsacksol(mochila, 7):
    #     print(f"{7} es valor de la mochila")
    # if knapsacksol(mochila, 9):
    #     print(f"{9} es valor de la mochila")

    # # Prueba de cifrado y descifrado con la función knapsackcipher y knapsackdecipher
    # message = "Hola A TODOS"
    # ciphered = knapsackcipher(message, mochila)
    # print(f"Mensaje cifrado: {ciphered}")
    # print(f"Mensaje descifrado: {knapsackdecipher(ciphered, mochila)}")

    # # Parámetros para generar la mochila trampa
    # m = 20  # Un número mayor que la suma de los elementos de la mochila
    # w = 3   # Un número coprimo con m y con todos los elementos de la mochila

    # # Generar la clave pública y privada
    # keys = knapsackpublicandprivate(mochila, m, w)
    # public_key = keys["public_key"]
    # private_key = keys["private_key"]

    # print(f"Clave pública: {public_key}")
    # print(f"Clave privada (m, w): ({private_key['m']}, {private_key['w']})")

    # # Cifrado con la mochila trampa (clave pública)
    # trap_message = "TEST"
    # trap_ciphered = knapsackcipher(trap_message, public_key)
    # print(f"Mensaje cifrado con mochila trampa: {trap_ciphered}")

    # # Descifrado con mochila trampa usando la clave privada
    # decrypted_message = knapsackdeciphermh(private_key["super_knapsack"], private_key["m"], private_key["w"], trap_ciphered)
    # print(f"Mensaje descifrado con mochila trampa: {decrypted_message}")

    # #===================================================================
    # #   CRIPTOANALISIS
    # #===================================================================

    # print("\n\n[+] Probando método de criptoanálisis de Shamir y Zippel.")

    # # PRUEBA 1__________________________________________________________
    # public_knapsack = [82, 123, 39, 78, 238, 105, 208]
    # m=248
    # w=41
    # print(f"\n\n[+] Probando para la mochila {public_knapsack}, (m={m}, w={w})")

    # # Ataque de Shamir y Zippel
    # recovered_knapsack = shamir_zippel_attack(public_knapsack, m)

    # # Verificar si coincide con la mochila privada original
    # if recovered_knapsack == None:
    #     print("[!] No se ha podido recuperar la mochila.")
    # else:
    #     print(f"[*] La mochila es {recovered_knapsack}")

    # # PRUEBA 2__________________________________________________________
    # public_knapsack = [35, 137, 41, 149, 65, 197]
    # m=300
    # w=67
    # print(f"\n\n[+] Probando para la mochila {public_knapsack}, (m={m}, w={w})")

    # # Ataque de Shamir y Zippel
    # recovered_knapsack = shamir_zippel_attack(public_knapsack, m)

    # if recovered_knapsack == None:
    #     print("[!] No se ha podido recuperar la mochila.")
    # else:
    #     print(f"[*] La mochila es {recovered_knapsack}")
