import math

def letter2ascii(letter):
    """Convierte una letra en su representación ASCII binaria de 8 bits."""
    return format(ord(letter), '08b')

def ascii2letter(binary_str):
    """Convierte una cadena binaria de 8 bits en la letra ASCII correspondiente."""
    return chr(int(binary_str, 2))

#Toma un vector fila y determine si es una mochila supercreciente (devolviendo 1),
# una mochila no supercreciente (devolviendo 0) o no es una mochila (devolviendo -1)
def knapsack(s):
    """
    Determina el tipo de mochila.
    Retorna:
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

# Toma una mochila (supercreciente o no) s, un valor v, y determine usando el algoritmo de
# mochilas supercrecientes si v es valor objetivo de s
def knapsacksol(s, v):
    """
    Determina si el valor v puede ser alcanzado por una combinación de elementos de la mochila supercreciente s.
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

def knapsackcipher(text, knapsack):
    """Cifra un mensaje utilizando una mochila `knapsack`. Retorna un vector numérico con el mensaje cifrado."""
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

def knapsackdecipher(encrypted_text, super_knapsack):
    """Descifra un vector numérico `encrypted_text` utilizando una mochila supercreciente `super_knapsack`.
       Retorna el texto en claro."""
    decrypted_binary = ''
    for value in encrypted_text:
        solution = knapsacksol(super_knapsack, value)
        if solution is None:
            raise ValueError("No se puede descifrar el texto con la mochila proporcionada.")
        decrypted_binary += ''.join(map(str, solution))
    
    # Convertir el binario de vuelta a texto ASCII de 8 bits
    text = ''.join(ascii2letter(decrypted_binary[i:i+8]) for i in range(0, len(decrypted_binary), 8))
    return text

if __name__ == "__main__":

    mochila = (1,2,5,10) 

    if knapsack(mochila): print(f"{mochila} es supercreciente")

    if knapsacksol(mochila, 7): print(f"{7} es valor de la mochila")
    if knapsacksol(mochila, 9): print(f"{9} es valor de la mochila")

    ciphered=knapsackcipher("Hola A TODOS", mochila)
    print(f"Mensaje cifrado: {ciphered}")
    print(f"Mensaje descifrado: {knapsackdecipher(ciphered, mochila)}")