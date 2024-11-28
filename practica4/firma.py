#!/usr/bin/python3
# -*- coding: utf-8 -*-

from rsa import *

class Agente:

    firma=""

    block_size = 7

    # Constructor (opcional, se ejecuta al crear una instancia)
    def __init__(self, name, p=101, q=65557):

        self.name = name

        self.p = p
        self.q = q
        self.n = p*q

         # Generamos las claves del agente con parámetros de prueba
        self.public_key, self.private_key = keygeneration(self.p, self.q, "fermat")

    def set_firma(self, firma):
        self.firma = firma

    def get_firma(self):
        print(f"[{self.name}] La firma es: {self.firma}")
        print(f"[{self.name}] La firma como numeros es: {letters2num(self.firma)}")

    def get_public(self):
        print(f"[{self.name}] La clave pública es: {self.public_key}")
        return self.public_key
    
    def get_private(self):
        print(f"[{self.name}] La clave privada es: {self.private_key}")
        return self.private_key

    def get_block_size(self):
        return self.block_size

    def cifrar_mensaje(self, public_key, mensaje, block_size):
        if self.firma == "":
            print(f"[{self.name}] Debes asignar una firma a este agente!")

        if debug: print(f"[{self.name}] Cifrando mensaje. ")

        mensajeFirma = mensaje+self.firma

        print(f"[{self.name}] Mensaje + firma => {mensajeFirma}")

        ciphered = rsaciphertext(mensajeFirma, public_key, block_size)

        return ciphered
    
    def cifrar_firma(self, public_key, block_size):
    
        if self.firma == "":
            print(f"[{self.name}] Debes asignar una firma a este agente!")

        if debug: print(f"\n[{self.name}] Cifrando firma. ") #DEBUG

        # 1er Cifrado
        ciphered = rsaciphertext(self.firma, self.private_key, self.block_size)

        if debug: print(f"[{self.name}] 1st ciphered ({self.name} priv key): {ciphered} ") #DEBUG

        '''
        # Convertimos los bloques a cadena numerica
        ciphered_str = preparetextdecipher(ciphered, self.block_size)

        # De cadena numerica volvemos a convertir en bloques pero de la longitud de bloque del receptor
        blocks = [ciphered_str[i:i + block_size] for i in range(0, len(ciphered_str), block_size)] # Divide el texto en bloques de tamaño n
        
        # Rellena el último bloque si es necesario
        if len(blocks[-1]) < block_size:
            remaining_length = block_size - len(blocks[-1])
            padding = '30' * (remaining_length // 2) + '0' * (remaining_length % 2)
            blocks[-1] += padding[:remaining_length] #Añade el padding generado al ultimo bloque
        
        blocks = [int(block) for block in blocks]
        '''

        # Convertimos los bloques a cadena numerica
        ciphered_str = ''.join([f"{block:0{self.block_size}}" for block in ciphered])

        # De cadena numerica volvemos a convertir en bloques pero del tamaño del receptor
        blocks = [ciphered_str[i:i + block_size] for i in range(0, len(ciphered_str), block_size)]

        # Rellenamos si el último bloque no tiene el tamaño esperado
        if len(blocks[-1]) < block_size:
            remaining_length = block_size - len(blocks[-1])
            blocks[-1] += '0' * remaining_length
        blocks = [int(block) for block in blocks]


        if debug: print(f"[{self.name}] Conversion para el segundo cifrado: {blocks} ") #DEBUG

        # 2o Cifrado
        ciphered_2 = [rsacipher(int(block), public_key) for block in blocks]

        return ciphered_2

    def descifrar_mensaje(self, ciphered):

        if debug: print(f"[{self.name}] Descifrando mensaje. ")

        deciphered = rsadeciphertext(ciphered, self.private_key, self.block_size)

        if debug: print(f"[{self.name}] Mensaje descifrado => {deciphered}")

        return deciphered

    def descifrar_firma(self, ciphered, public_key, block_size):

        if debug: print(f"\n[{self.name}] Descifrando firma. ({ciphered})")

        # 1er descifrado -> No utilizo la función de rsa
        # Realizamos el primer descifrado con la clave privada
        decrypted_blocks = [rsadecipher(block, self.private_key) for block in ciphered]

        if debug: print(f"[{self.name}] 1er descifrado: {decrypted_blocks}")

        '''# Convertimos la lista a cadena para dividir con el tamaño de bloque correcto
        deciphered_str = preparetextdecipher(ciphered, self.block_size)

        if debug: print(f"[{self.name}] A cadena: {deciphered_str}")

        # De cadena numerica volvemos a convertir en bloques pero de la longitud de bloque correcta
        blocks = [deciphered_str[i:i + block_size] for i in range(0, len(deciphered_str), block_size)] # Divide el texto en bloques de tamaño n

        # Rellena el último bloque si es necesario
        if len(blocks[-1]) < block_size:
            remaining_length = block_size - len(blocks[-1])
            padding = '30' * (remaining_length // 2) + '0' * (remaining_length % 2)
            blocks[-1] += padding[:remaining_length] #Añade el padding generado al ultimo bloque
        
        blocks = [int(block) for block in blocks]'''

        if debug: print(f"[{self.name}] bloq_size: {self.block_size}")
        # Convertimos la lista descifrada a cadena
        deciphered_str = ''.join([f"{block:0{self.block_size}}" for block in decrypted_blocks])

        # Convertimos a bloques para el descifrado final
        blocks = [deciphered_str[i:i + block_size] for i in range(0, len(deciphered_str), block_size)]

        # Rellenamos si necesario
        if len(blocks[-1]) < block_size:
            remaining_length = block_size - len(blocks[-1])
            blocks[-1] += '0' * remaining_length
        blocks = [int(block) for block in blocks]

        # Segundo descifrado con la clave pública
        deciphered = rsadeciphertext(blocks, public_key, block_size)


        if debug: print(f"[{self.name}] A bloques: {blocks}")

        deciphered = rsadeciphertext(blocks, public_key, block_size)

        return deciphered

    def rsaciphertextsign(self, mensaje, public_key, block_size):

        
        mensajeFirma = self.cifrar_mensaje(public_key, mensaje, block_size)
        print(f"[{self.name}] Mensaje + firma cifrado => {mensajeFirma}")

        firma = self.cifrar_firma(public_key, block_size)
        print(f"[{self.name}] Firma cifrada => {firma}")

        return mensajeFirma, firma

    # La parte de descifrar la firma no funciona correctamente
    def rsadeciphertextsign(self, criptograma1, criptograma2, public_key, block_size):

        if len(criptograma1) > len(criptograma2):
            
            mensajeFirma = self.descifrar_mensaje(criptograma1)
            print(f"[{self.name}] Mensaje + firma descifrado => {mensajeFirma}")

            firma = self.descifrar_firma(criptograma2, public_key, block_size)
            print(f"[{self.name}] Firma descifrada => {firma}")

        else:
            mensajeFirma = self.descifrar_mensaje(criptograma2)
            print(f"[{self.name}] Mensaje + firma descifrado => {mensajeFirma}")

            firma = self.descifrar_firma(criptograma1, public_key, block_size)
            print(f"[{self.name}] Firma descifrada => {firma}")            

        return mensajeFirma, firma


if __name__ == "__main__":

    # DEFINICION DE ALICE

    alice = Agente("A")

    alice.set_firma("Alice")
    alice.get_firma()

    alice_public = alice.get_public()
    alice_private = alice.get_private()
    alice_block_size = alice.get_block_size()

    print("\n")
    # DEFINICION DE BOB

    bob = Agente("B", 47)

    bob.set_firma("Bob")
    bob.get_firma()

    bob_public = bob.get_public()
    bob_private = bob.get_private()
    bob_block_size = bob.get_block_size()

    print("\n")
    # CIFRADO DE MENSAJE Y FIRMA

    mensajeFirma, firma = alice.rsaciphertextsign("Hola BOB", bob_public, bob_block_size)

    print(f"[Alice] Aquí tienes Bob {mensajeFirma}")
    print(f"[Alice] Aquí tienes Bob {firma}")

    print("\n")
    # DESCIFRADO

    bob.rsadeciphertextsign(mensajeFirma, firma, alice_public, alice_block_size)