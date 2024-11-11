#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random
import time
import sympy
from math import gcd

# Cálculo del símbolo de Jacobi - necesario para el test de Solovay-Strassen
def jacobi(a, n):
    """
    Calcula el simbolo de Jacobi. Es necesario para el test de Solovay-Strassen.

    Args:
        a: Valor a.
        n: Valor n.

    Returns:
        El valor (a sobre n).
    """
    if n <= 0 or n % 2 == 0:
        return 0
    
    result = 1
    while a != 0:
        while a % 2 == 0:
            a //= 2
            if n % 8 in [3, 5]:
                result = -result
        a, n = n, a
        if a % 4 == 3 and n % 4 == 3:
            result = -result
        a %= n
    return result if n == 1 else 0

# primosolostra
# Tests de Solovay-Strassen
def primosolostra(n, a, b, k):
    """
    Tests de Solovay-Strassen para buscar pseudoprimos.

    Args:
        n: Nuemro a comprobar.
        a: Limite inferior del rango.
        b: Limite superior del rango.
        k: Numero de iteraciones a considerar.

    Returns:
        En caso de obtener un numero que pase los test, indica la probabilidad de que dicho supuesto primo sea un pseudo-primo.
        Tambien da como respuesta el tiempo requerido para realizar el test.
        En caso de no superar los test o dar error, responde con False.
    """

    start_time = time.time()
    if b <= a:
        print("[x] El rango [{a}, {b}] no es válido.")
        return False
    
    if n > b or n < a:
        print("[x] El {n} no está en el rango [{a}, {b}]")
        return False
        
    for _ in range(k):
        base = random.randint(a, b)
        x = jacobi(base, n)
        if x == 0 or pow(base, (n - 1) // 2, n) != x % n:
            print("[x] El test para {n} con base {base} ha fallado.")
            return False
    
    prob = 1 - 1 / (2 ** k)
    print(f"[!] La probabilidad de que en contrar un primo en el rango [{a},{b}] en {k} iteraciones es {prob}")
    end_time = time.time()
    print(f"[!] Tiempo en completar el test: {end_time - start_time}")
    return True

# primoMillerRabin 
# Busqueda de primos mediante los Tests de Miller-Rabin
def primoMillerRabin(n, a, b, k):
    """
    Busca primos mediante los Tests de Miller-Rabin

    Args:
        n: Nuemro a comprobar.
        a: Limite inferior del rango.
        b: Limite superior del rango.
        k: Numero de iteraciones a considerar.

    Returns:
        En caso de obtener un numero que pase los test, indica la probabilidad de que dicho supuesto primo sea un pseudo-primo.
        Tambien da como respuesta el tiempo requerido para realizar el test.
        En caso de no superar los test o dar error, responde con False.
    """
    start_time = time.time()
    if n <= 1 or n == 4:
        print("[x] El test para {n} con base {base} ha fallado.")
        return False
    if n <= 3:
        print(f"[!] La probabilidad de que en contrar un primo en el rango [{a},{b}] en {k} iteraciones es {prob}")
        end_time = time.time()
        print(f"[!] Tiempo en completar el test: {end_time - start_time}")
        return True
    
    if b <= a:
        print("[x] El rango [{a}, {b}] no es válido.")
        return False
    
    if n > b or n < a:
        print("[x] El {n} no está en el rango [{a}, {b}]")
        return False

    base = n - 1
    while base % 2 == 0:
        base //= 2
    
    for _ in range(k):
        if not miller_rabin_test(base, n):
            print("[x] El test para {n} con base {base} ha fallado.")
            return False
    
    prob = 1 - 1 / (4 ** k)

    print(f"[!] La probabilidad de que en contrar un primo en el rango [{a},{b}] en {k} iteraciones es {prob}")
    end_time = time.time()
    print(f"[!] Tiempo en completar el test: {end_time - start_time}")
    return True

# Función de Miller-Rabin
def miller_rabin_test(base, n):
    """
    Aplica el Test de Miller-Rabin a un número y una base.

    Args:
        base: Base a comprobar.
        n: Número a comprobar.

    Returns:
        En caso de pasar el test, devuelve True.
        En caso de no superar los test o dar error, responde con False.
    """
    a = random.randint(2, n - 2)
    x = pow(a, base, n)
    if x == 1 or x == n - 1:
        return True
    while base != n - 1:
        x = (x * x) % n
        base *= 2
        if x == 1:
            return False
        if x == n - 1:
            return True
    return False

def keygeneration(p=None, q=None, e_option=None):
    """
    Genera claves públicas y privadas.

    Args:
        p: Número primo 1.
        q: Número primo 2.
        e_option: Parámetro para seleccionar el valor de e: 'Fermat' (e = 65537), 'random' (aleatorio) o 'user' (dado por el usuario).

    Returns:
        Devuelve dos listas con dos elementos, la primera con la clave pública y la segunda con la clave privada.
    """

    if p is None or q is None:  # Si no se proporcionan p y q, sugerir algunos primos pequeños

        print("[*] Sugerencia de primos para p y q: [101, 103, 65551, 65579, 109, 113]")
        p = int(input("> Ingrese el valor de p (debe ser un número primo): "))
        q = int(input("> Ingrese el valor de q (debe ser un número primo): "))

    if not sympy.isprime(p) or not sympy.isprime(q):    # Verificar que p y q sean primos

        raise ValueError("[!] p y q deben ser números primos.")

    # Calcular n y phi(n)
    n = p * q
    phi_n = (p - 1) * (q - 1)

    print(f"[DEBUG] p = {p}; q = {q}") # DEBUG
    print(f"[DEBUG] n = {n}; phi_n = {phi_n}") # DEBUG

    # Selección de e
    if e_option is None:
        e_option = input("> Elija la opción para 'e' (fermat, random, user): ").strip().lower()
        #print(f"[DEBUG] e_option = '{e_option}'") # DEBUG

    if e_option == "fermat" or e_option == "":  # Solo recomendado para n>65537
        if n < 65537:
            raise ValueError("[!] El valor de n es muy pequeño ({n}), debe ser mayor de 65537.")
        e = 65537

    elif e_option == "random":
        e = random.randint(2, phi_n - 1)
        while sympy.gcd(e, phi_n) != 1:
            e = random.randint(2, phi_n - 1)

    elif e_option == "user":
        e = int(input("> Ingrese un valor de e que sea coprimo con φ(n): "))
        if sympy.gcd(e, phi_n) != 1:
            raise ValueError("[!] El valor de e debe ser coprimo con φ(n).")
        
    else:
        raise ValueError("[!] Opción de e no válida. Use 'Fermat', 'random' o 'user'.")

    print(f"[DEBUG] e = {e}") # DEBUG

    # Calcular d, el inverso modular de e módulo phi(n)
    d = sympy.mod_inverse(e, phi_n)

    print(f"[DEBUG] d = {d}") # DEBUG

    # Claves pública y privada
    public_key = (e, n)
    private_key = (d, n)

    return public_key, private_key

# Convierte un string en una cadena numerica (a->01, b->02...)
def letters2num(a):
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
            num = ord(char) - ord('a') + 1
            # Asegúrate de que cada número tenga dos dígitos, agregando un cero si es necesario
            result.append(f"{num:02}")
    return ''.join(result)

# Convierte una cadena numerica (a->01, b->02...) en un string legible
def nums2letter(a):
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
        num = int(a[i:i+2])  # Convierte el bloque a un número
        # Convierte el número a letra (0 -> 'a', 1 -> 'b', etc.)
        if 1 <= num <= 26:
            result.append(chr(num - 1 + ord('a')))
    return ''.join(result)


# Toma una cadena numerica (un texto transformado a su equivalente numerico) y lo divide en bloques
# de tamaño fijado por n. El programa debera incluir 30s o 0 para rellenar los bloques incompletos.
def preparenumcipher(text, n):
    """
    Toma una cadena numerica (un texto transformado a su equivalente numérico) y lo divide en bloques de tamaño fijado por n.

    Args:
        text: Texto a dividir.
        n: Tamaño de bloque.

    Returns:
        Devuelve una lista de bloques. Incluye 30 seguido de 0 para rellenar los bloques incompletos.
    """

    #Convierte el texto en numeros
    text = letters2num(text)
    
    # Divide el texto en bloques de tamaño n
    blocks = [text[i:i + n] for i in range(0, len(text), n)]
    
    # Rellena el último bloque si es necesario
    if len(blocks[-1]) < n:
        remaining_length = n - len(blocks[-1])
        padding = '30' * (remaining_length // 2) + '0' * (remaining_length % 2)
        blocks[-1] += padding[:remaining_length] #Añade el padding generado al ultimo bloque
    
    return blocks

# Toma un vector numerico, y devuelva una cadena numerica lista para ser traducida a texto.
def preparetextdecipher(nums):
    """
    Toma un vector numerico, y devuelva una cadena numérica lista para ser traducida a texto.

    Args:
        nums: Cadena a traducir.

    Returns:
        Devuelve un texto.
    """
    # Une todos los bloques en una sola cadena
    text = ''.join(str(num) for num in nums)
    
    # Elimina los posibles caracteres de relleno (0 y 30 al final)
    while text.endswith("30") or text.endswith("0"):
        if text.endswith("30"):
            text = text[:-2]
        elif text.endswith("0"):
            text = text[:-1]
    
    return text

def rsacipher(block, public_key):
    """
    Cifra un bloque utilizando RSA.

    Args:
        block: Bloque.
        public_key: Lista de dos elementos con la clave pública (n,e)

    Returns:
        Devuelve el bloque cifrado.
    """
    n, e = public_key
    # Cifra el bloque: c = (block^e) mod n
    cipher_block = pow(block, e, n)
    return cipher_block

def rsadecipher(cipher_block, private_key):
    """
    Descifra un bloque utilizando RSA.

    Args:
        cipher_block: Bloque cifrado.
        private_key: Lista de dos elementos con la clave privada (n,d)

    Returns:
        Devuelve el bloque descifrado.
    """
    n, d = private_key
    # Descifra el bloque: m = (cipher_block^d) mod n
    deciphered_block = pow(cipher_block, d, n)
    return deciphered_block

# Cifra un texto con una clave publica con un tamaño de bloque dado
def rsaciphertext(text, public_key, block_size):
    """
    Cifra un texto utilizando RSA.

    Args:
        text: Texto.
        public_key: Lista de dos elementos con la clave pública (n,e)
        block_size: Tamaño de bloque.

    Returns:
        Devuelve una lista de bloques cifrados.
    """
    # Convierte el texto en bloques numéricos
    blocks = preparenumcipher(text, block_size)

    print(f"[DEBUG] Bloques RAW {blocks}.") # DEBUG
    
    # Cifra cada bloque con la clave pública
    cipher_blocks = [rsacipher(int(block), public_key) for block in blocks]
    
    return cipher_blocks

# Descifra una serie de bloques con una clave privada y un tamaño de bloque dado 
def rsadeciphertext(cipher_blocks, private_key, block_size):
    """
    Descifra una lista de bloques cifrados utilizando RSA.

    Args:
        cipher_blocks: Lista de bloques cifrados.
        private_key: Lista de dos elementos con la clave privada (n,d)
        block_size: Tamaño de bloque.

    Returns:
        Devuelve el texto descifrado.
    """
    # Descifra cada bloque con la clave privada
    decrypted_blocks = [rsadecipher(cipher_block, private_key) for cipher_block in cipher_blocks]

    print(f"[DEBUG] Bloques descifrados RAW {decrypted_blocks}.") # DEBUG
    
    # Convierte los bloques de vuelta a texto
    decrypted_text = preparetextdecipher(decrypted_blocks)
    
    return nums2letter(decrypted_text)

# Función para mostrar el menú
def menu():
    """
    Muestra el menú por terminal.
    """
    print("\n--------------------------")
    print("  Menú de la suite RSA")
    print("--------------------------")
    print("1. Generar claves")
    print("2. Cifrar mensaje")
    print("3. Descifrar mensaje")
    print("4. Salir")
    print("--------------------------")

# Logica del menu
def main():
    """
    Lógica del menu.
    """
    public_key = private_key = None
    
    while True:
        menu()
        choice = input("[*] Inserta una opcion (1-4): ")

        if choice == '1': # Generar claves

            public_key, private_key = keygeneration(101, 65557, "fermat")
            print("\n[*] Generando claves RSA...")
            print(f"[+] Clave pública: {public_key}")
            print(f"[+] Clave privada: {private_key}")
        
        elif choice == '2': # Cifrar mensaje

            if public_key is None:  #Si no se han generado las claves, volvemos
                print("[!] Primero, genera las claves.")
                continue

            message = input("\n[*] Introduce el mensaje que quieres cifrar: ")
            block_size = int(input("[*] Introduce el tamaño de bloque para cifrado: "))
            cipher_blocks = rsaciphertext(message, public_key, block_size)
            print("\n[+] Mensaje cifrado:")
            print(cipher_blocks)
        
        elif choice == '3': # Descifrar mensaje

            if private_key is None: # Si no hemos generado las claves, volvemos
                print("[!] Primero, genera las claves.")
                continue

            cipher_text = input("\n[*] Introduce el mensaje cifrado (como una lista de bloques, ej. [a, b, c]): ")
            cipher_blocks = eval(cipher_text)  # Convierte la cadena de texto en una lista de bloques
            block_size = int(input("[*] Introduce el tamaño de bloque para descifrado: "))
            decrypted_message = rsadeciphertext(cipher_blocks, private_key, block_size)
            print("\n[+] Mensaje descifrado:")
            print(decrypted_message)
        
        elif choice == '4': #Salir
            print("\n[!] Saliendo...")
            break
        
        else:
            print("[!] Opción no válida. Por favor, elige una opción válida (1-4).")

if __name__ == "__main__":
    main()