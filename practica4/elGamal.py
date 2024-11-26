#!/usr/bin/python3
# -*- coding: utf-8 -*-

from rsa import *
import random
from sympy import mod_inverse, isprime

def generate_keys_elgamal(q=None, g=None, a=None):
    """
    Genera las claves para ElGamal.

    Args:
        q: Primo grande (opcional). Si no se da, se genera automáticamente.

    Returns:
        public_key: Clave pública (p, g, h).
        private_key: Clave privada a.
    """
    if not q:
        q = random.randint(2**10, 2**12)  # Generar un primo grande.
        while not isprime(q):
            q = random.randint(2**10, 2**12)
    
    if not g:
        g = random.randint(2, q - 1)  # Generador.
    
    if not a:
        a = random.randint(2, q - 2)  # Clave privada.
    h = pow(g, a, q)  # Clave pública.

    public_key = (q, g, h)
    private_key = a

    if debug:
        print(f"[DEBUG] Clave publica: {public_key}")
        print(f"[DEBUG] Clave privada: {private_key}")

    return public_key, private_key

def elgamal_encrypt(public_key, message):
    """
    Cifra un mensaje usando ElGamal.
    Args:
        public_key: Clave pública (q, g, h).
        message: Mensaje a cifrar.

    Returns:
        Criptograma (C1, C2).
    """
    q, g, h = public_key
    k = random.randint(2, q - 2)
    
    block_size = len(str(abs(q))) - 1

    if debug: print(f"[DEBUG] Tamaño de bloque: {block_size}")

    blocks = preparenumcipher(message, block_size)

    if debug: print(f"[DEBUG] Mensaje en bloques: {blocks}")
    
    gk = pow(g, k, q)
    gak = pow(h, k, q)
    
    if debug: 
        print(f"[DEBUG] gk: {gk}")
        print(f"[DEBUG] gak: {gak}")
    
    encrypted_blocks = [(block * gak) % q for block in blocks]
    
    if debug: print(f"[DEBUG] Mensaje cifrado: {encrypted_blocks}")

    return gk, encrypted_blocks

def elgamal_decrypt(private_key, public_key, ciphertext):
    """
    Descifra un mensaje cifrado con ElGamal.
    Args:
        private_key: Clave privada a.
        public_key: Clave pública (q, g, h).
        ciphertext: Criptograma (gk, blocks).

    Returns:
        Mensaje descifrado.
    """
    q, _, _ = public_key
    gk, blocks = ciphertext
    a = private_key

    block_size = len(str(abs(q))) - 1

    gak = pow(gk, a, q)  # gak = gk^a mod p
    inv = mod_inverse(gak, q)  # Inverso modular de s

    decrypted_blocks = [(block * inv) % q for block in blocks]

    # Convertir bloques a cadena numerica
    num_text = ""
    for block in decrypted_blocks:
        num_text += str(block).zfill(block_size)

    return nums2letter(num_text)

def main():
    """
    Lógica del menú.
    """

    while True:
        print("\n--- CIFRADO ElGamal ---")
        print("1. Generar claves")
        print("2. Cifrar mensaje")
        print("3. Descifrar mensaje")
        print("4. Salir")

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


# Ejemplo de uso
if __name__ == "__main__":
    # Generar claves
    public_key, private_key = generate_keys_elgamal()
    print("Clave pública:", public_key)
    print("Clave privada:", private_key)

    # Mensaje original
    mensaje = "Esto es una prueba"  # Un número que represente un bloque del mensaje
    print("Mensaje original:", mensaje)

    # Cifrar mensaje
    criptograma = elgamal_encrypt(public_key, mensaje)
    print("Criptograma:", criptograma)

    # Descifrar mensaje
    mensaje_descifrado = elgamal_decrypt(private_key, public_key, criptograma)
    print("Mensaje descifrado:", mensaje_descifrado)
