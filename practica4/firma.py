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

        if debug: print(f"[{self.name}] Cifrando firma. ")

        # 1er Cifrado
        ciphered = rsaciphertext(self.firma, self.private_key, self.block_size)

        if debug: print(f"[{self.name}] Ciphered: {ciphered} ")

        # Convierte la cadena de bloques resultante en texto que pueda volver a cifrarse
        ciphered_str = preparetextdecipher(ciphered, block_size)

        if debug: print(f"[{self.name}] Ciphered num string: {ciphered_str} ")

        ciphered_letters = nums2letter(ciphered_str)

        if debug: print(f"[{self.name}] Ciphered num letters: {ciphered_letters} ")

        # 2o Cifrado
        ciphered_2 = rsaciphertext(ciphered_letters, public_key, block_size)

        return ciphered_2

    def descifrar_mensaje(self, ciphered):

        if debug: print(f"[{self.name}] Descifrando mensaje. ")

        deciphered = rsadeciphertext(ciphered, self.private_key, self.block_size)

        if debug: print(f"[{self.name}] Mensaje descifrado => {deciphered}")

        return deciphered

    def descifrar_firma(self, ciphered, public_key, block_size):

        if debug: print(f"[{self.name}] Descifrando firma. ")

        deciphered_str = rsadeciphertext(ciphered, self.private_key, self.block_size)

        # Convertir texto a bloques para volver a descifrar
        deciphered_blocks = preparenumcipher(deciphered_str, block_size)

        deciphered = rsadeciphertext(deciphered_blocks, public_key, block_size)

        print(f"[{self.name}] Firma descifrada => {deciphered}")

        return deciphered

    def rsaciphertextsign(self, mensaje, public_key, block_size):

        
        mensajeFirma = self.cifrar_mensaje(public_key, mensaje, block_size)
        firma = self.cifrar_firma(public_key, block_size)

        print(f"[{self.name}] Mensaje + firma cifrado => {mensajeFirma}")
        print(f"[{self.name}] Firma cifrada => {firma}")

        return mensajeFirma, firma

    # La parte de descifrar la firma no funciona correctamente
    def rsadeciphertextsign(self, criptograma1, criptograma2, public_key, block_size):

        if len(criptograma1) > len(criptograma2):
            
            mensajeFirma = self.descifrar_mensaje(criptograma1)
            print(f"[{self.name}] Mensaje + firma descifrado => {mensajeFirma}")
            firma = self.descifrar_firma(criptograma2, public_key, block_size)

        else:
            mensajeFirma = self.descifrar_mensaje(criptograma2)
            firma = self.descifrar_firma(criptograma1, public_key, block_size)

        if debug: 
            print(f"[{self.name}] Mensaje + firma descifrado => {mensajeFirma}")
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