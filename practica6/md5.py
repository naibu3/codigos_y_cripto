import struct
import math

# Padding del mensaje
def pad_message(message):
    message_length = len(message) * 8
    message += b'\x80'
    while (len(message) * 8) % 512 != 448:
        message += b'\x00'
    message += struct.pack('<Q', message_length)
    return message

# Funciones auxiliares
def F(x, y, z):
    return (x & y) | (~x & z)

def G(x, y, z):
    return (x & z) | (y & ~z)

def H(x, y, z):
    return x ^ y ^ z

def I(x, y, z):
    return y ^ (x | ~z)

def Function(x, y, z, i):
    if 0 <= i <= 15: return F(x, y, z)
    elif 16 <= i <= 31: return G(x, y, z)
    elif 32 <= i <= 47: return H(x, y, z)
    elif 48 <= i <= 63: return I(x, y, z)

def rotate_left(x, n):
    return ((x << n) | (x >> (32 - n))) & 0xFFFFFFFF

def rot(i):
    if 0 <= i <= 15: return [ 7, 12, 17, 22 ]       # Ronda 1
    elif 16 <= i <= 31: return [ 5, 9, 14, 20 ]     # Ronda 2
    elif 32 <= i <= 47: return [ 4, 11, 16, 23 ]    # Ronda 3
    elif 48 <= i <= 63: return [ 6, 10, 15, 21 ]    # Ronda 4       

# Constantes de seno
def T(i):
    return int(abs(math.sin(i + 1)) * (2**32)) & 0xFFFFFFFF

def sel(i):
    if 0 <= i <= 15: return (i - 1) % 16
    elif 16 <= i <= 31: return (5 * (i - 1) + 1) % 16
    elif 32 <= i <= 47: return (3 * (i - 1) + 5) % 16
    elif 48 <= i <= 63: return (7 * (i - 1)) % 16

# Algoritmo principal MD5
def md5(message):

    # Convierte el string en bytes y añade el padding
    message = str.encode(message)
    message = pad_message(message)

    # Inicialización
    A0, B0, C0, D0 = 0x67452301, 0xEFCDAB89, 0x98BADCFE, 0x10325476
    
    ti = [T(i) for i in range(64)]   # Evita tener que hacer gran cantidad de operaciones complejas
    
    # Procesamiento de bloques de 512 bits de 4 en 4 palabras
    for chunk_start in range(0, len(message), 64):
        chunk = message[chunk_start:chunk_start + 64]
        M = list(struct.unpack('<16I', chunk))
        A, B, C, D = A0, B0, C0, D0

        for i in range(64):

            f = Function(B, C, D, i)
            g = sel(i)

            f = (f + A + ti[i] + M[g]) & 0xFFFFFFFF
            A, D, C, B = D, C, B, (B + rotate_left(f, rot(i)[i % 4])) & 0xFFFFFFFF

        # Suma al resultado anterior
        A0 = (A0 + A) & 0xFFFFFFFF
        B0 = (B0 + B) & 0xFFFFFFFF
        C0 = (C0 + C) & 0xFFFFFFFF
        D0 = (D0 + D) & 0xFFFFFFFF

    # Resultado final
    return ''.join(f'{x:02x}' for x in struct.unpack('<4I', struct.pack('<IIII', A0, B0, C0, D0)))


if __name__ == "__main__":
    message = "Hola"
    print(f"El hash para el mensaje {message} es: {md5(message)}")
