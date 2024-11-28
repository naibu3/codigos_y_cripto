#!/usr/bin/python3
# -*- coding: utf-8 -*-

from rsa import *
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

        if opcion == "1": # Generacion de claves

            q = int(input("[*] Introduce el valor de q (0 para valor aleatorio): "))
            g = int(input("[*] Introduce el valor de g (0 para valor aleatorio): "))
            a = int(input("[*] Introduce el valor de a (0 para valor aleatorio): "))

            public_key, private_key = generate_keys_elgamal(q, g, a)

            print("[+] Clave pública:", public_key)
            print("[+] Clave privada:", private_key)

        elif opcion == "2":
            
            mensaje = input("[*] Introduce el mensaje a cifrar: ")
            gk, criptograma = elgamal_encrypt(public_key, mensaje)
            print("[+] Criptograma:", criptograma)
            print(f"[+] gk: {gk}")

        elif opcion == "3":
            
            cipher_text = input("\n[*] Introduce el mensaje cifrado (como una lista de bloques, ej. [a, b, c]): ")
            gk = int(input("\n[*] Introduce gk: "))

            cipher_blocks = eval(cipher_text)  # Convierte la cadena de texto en una lista de bloques

            descifrado = elgamal_decrypt(private_key, public_key, (gk, cipher_blocks) )
            print(f"[+] Mensaje descifrado: {descifrado}")

        elif opcion == "4":
            print("[!] Saliendo del programa.")
            break
        else:
            print("[!] Opción no válida. Inténtalo de nuevo.")


# Ejemplo de uso
if __name__ == "__main__":
    main()
