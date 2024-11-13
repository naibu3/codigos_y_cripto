import math
import random
import time
from sympy import mod_inverse

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

#Toma un vector fila y determine si es una mochila supercreciente (devolviendo 1),
# una mochila no supercreciente (devolviendo 0) o no es una mochila (devolviendo -1)
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

# Toma una mochila (supercreciente o no) s, un valor v, y determine usando el algoritmo de
# mochilas supercrecientes si v es valor objetivo de s
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


#TODO - DEBUG
def shamir_zippel_attack(encrypted_text, max_range=100):
    """
    Implementa el ataque de criptoanálisis de Shamir y Zippel.
    Explora en un rango de valores para encontrar una mochila supercreciente que permita descifrar `encrypted_text`.
       
    Args:
        encrypted_text: El vector cifrado a analizar.
        max_range: Rango máximo de valores a probar en la búsqueda de una mochila supercreciente.
       
    Return:
        La mochila supercreciente encontrada, si existe. Mensaje informativo si no encuentra solución.
    """
    for range_start in range(1, max_range, 10):  # Probar en bloques de 10
        range_end = min(range_start + 10, max_range)
        print(f"Buscando en el rango {range_start} a {range_end}...")

        # Iniciar el cronómetro para medir el tiempo en cada rango
        start_time = time.time()
        
        # Generar una mochila supercreciente en el rango actual y probarla
        for trial_value in range(range_start, range_end):
            # Construir una posible mochila supercreciente
            super_knapsack = [trial_value * i for i in range(1, len(encrypted_text) + 1)]
            
            # Intentar descifrar con la mochila generada
            try:
                decrypted_message = knapsackdeciphermh(super_knapsack, max(super_knapsack) + 1, trial_value, encrypted_text)
                print(f"Solución encontrada con mochila supercreciente: {super_knapsack}")
                print(f"Mensaje descifrado: {decrypted_message}")
                return super_knapsack
            except ValueError:
                # Ignorar mochilas no válidas o fallos en descifrado
                pass

        # Medir el tiempo que tomó el análisis en el rango actual
        elapsed_time = time.time() - start_time
        print(f"Tiempo en rango {range_start}-{range_end}: {elapsed_time:.2f} segundos")

        # Preguntar al usuario si desea continuar en el siguiente rango
        continue_search = input("¿Desea continuar con el siguiente rango? (s/n): ").strip().lower()
        if continue_search != 's':
            print("Búsqueda de criptoanálisis finalizada.")
            break

    print("No se encontró una mochila supercreciente para descifrar el mensaje.")
    return None



if __name__ == "__main__":
    # Mochila supercreciente para pruebas
    mochila = (1, 2, 5, 10)

    # Prueba de la función knapsack
    if knapsack(mochila):
        print(f"{mochila} es supercreciente")

    # Prueba de la función knapsacksol
    if knapsacksol(mochila, 7):
        print(f"{7} es valor de la mochila")
    if knapsacksol(mochila, 9):
        print(f"{9} es valor de la mochila")

    # Prueba de cifrado y descifrado con la función knapsackcipher y knapsackdecipher
    message = "Hola A TODOS"
    ciphered = knapsackcipher(message, mochila)
    print(f"Mensaje cifrado: {ciphered}")
    print(f"Mensaje descifrado: {knapsackdecipher(ciphered, mochila)}")

    # Parámetros para generar la mochila trampa
    m = 20  # Un número mayor que la suma de los elementos de la mochila
    w = 3   # Un número coprimo con m y con todos los elementos de la mochila

    # Generar la clave pública y privada
    keys = knapsackpublicandprivate(mochila, m, w)
    public_key = keys["public_key"]
    private_key = keys["private_key"]

    print(f"Clave pública: {public_key}")
    print(f"Clave privada (m, w): ({private_key['m']}, {private_key['w']})")

    # Cifrado con la mochila trampa (clave pública)
    trap_message = "TEST"
    trap_ciphered = knapsackcipher(trap_message, public_key)
    print(f"Mensaje cifrado con mochila trampa: {trap_ciphered}")

    # Descifrado con mochila trampa usando la clave privada
    decrypted_message = knapsackdeciphermh(private_key["super_knapsack"], private_key["m"], private_key["w"], trap_ciphered)
    print(f"Mensaje descifrado con mochila trampa: {decrypted_message}")

    # Ejecutar el ataque de criptoanálisis - NO FUNCIONA
    print("Iniciando criptoanálisis de Shamir y Zippel...")
    super_knapsack_found = shamir_zippel_attack(trap_ciphered)
    if super_knapsack_found:
        print(f"Mochila supercreciente encontrada: {super_knapsack_found}")
    else:
        print("No se encontró una mochila supercreciente adecuada.")