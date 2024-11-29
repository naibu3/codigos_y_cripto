import numpy as np
from PIL import Image
import os

def is_invertible(matrix, n):
    """Verifica si una matriz 2x2 es invertible en Z_n."""
    det = int(round(np.linalg.det(matrix)))  # Determinante de la matriz
    det_mod = det % n  # Determinante en Z_n
    # Verificar si el determinante es coprimo con n
    return np.gcd(det_mod, n) == 1

def mod_inverse(a, n):
    """Calcula el inverso modular de un número a en Z_n usando el algoritmo extendido de Euclides."""
    t, new_t = 0, 1
    r, new_r = n, a
    while new_r != 0:
        quotient = r // new_r
        t, new_t = new_t, t - quotient * new_t
        r, new_r = new_r, r - quotient * new_r
    if r > 1:
        raise ValueError(f"{a} no tiene inverso modular en Z_{n}")
    if t < 0:
        t += n
    return t

def matrix_mod_inverse(matrix, n):
    """Calcula la matriz inversa en Z_n."""
    det = int(round(np.linalg.det(matrix)))  # Determinante de la matriz
    det_mod = det % n
    det_inv = mod_inverse(det_mod, n)  # Inverso del determinante en Z_n
    
    # Matriz adjunta (cofactores transpuestos)
    adj = np.array([[matrix[1, 1], -matrix[0, 1]],
                    [-matrix[1, 0], matrix[0, 0]]]) % n
    return (det_inv * adj) % n

def mod_matrix_mult(A, B, n):
    """Multiplica dos matrices A y B en Z_n."""
    return np.dot(A, B) % n

def mod_matrix_power(A, p, n):
    """Eleva la matriz A a la potencia p en Z_n."""
    result = np.eye(A.shape[0], dtype=int)  # Matriz identidad
    base = A.copy()
    
    while p > 0:
        if p % 2 == 1:
            result = mod_matrix_mult(result, base, n)
        base = mod_matrix_mult(base, base, n)
        p //= 2
    return result

def powinverse(A, n):
    """Calcula el menor p tal que A^p ≡ I (mod n) en Z_n."""
    identity = np.eye(A.shape[0], dtype=int)  # Matriz identidad
    power = A.copy()
    p = 1
    
    while not np.array_equal(power % n, identity):
        power = mod_matrix_mult(power, A, n)
        p += 1
        if p > n ** 2:  # Evita bucles infinitos
            raise ValueError("No se encontró un p tal que A^p ≡ I en Z_n.")
    
    return p

def crop_to_square(image_path, output_path):
    """Recorta una imagen para que sea cuadrada, centrando el área de recorte."""
    img = Image.open(image_path)
    width, height = img.size

    if width == height: return 0 # Si ya es cuadrada vuelve
    
    # Determinar el tamaño del lado cuadrado (mínimo entre ancho y altura)
    side = min(width, height)
    
    # Calcular las coordenadas para el recorte
    left = (width - side) // 2
    top = (height - side) // 2
    right = left + side
    bottom = top + side
    
    # Recortar la imagen
    cropped_img = img.crop((left, top, right, bottom))
    
    # Guardar la imagen recortada
    cropped_img.save(output_path)
    print(f"Imagen recortada guardada en {output_path}")
    return 1

def delete_image(image_path):
    """Elimina un archivo de imagen dado."""
    try:
        os.remove(image_path)
        print(f"Imagen '{image_path}' eliminada con éxito.")
    except FileNotFoundError:
        print(f"El archivo '{image_path}' no existe.")
    except PermissionError:
        print(f"No tienes permisos para eliminar el archivo '{image_path}'.")
    except Exception as e:
        print(f"Ocurrió un error al intentar eliminar '{image_path}': {e}")

def desordenaimagen(matrix, image_path, output_path, n):
    """Desordena una imagen utilizando una matriz 2x2 en Z_n."""
    if not is_invertible(matrix, n):
        raise ValueError("La matriz no es invertible en Z_n.")
    
    # Cargar la imagen
    img = Image.open(image_path).convert('RGB')  # Convertir a RGB
    pixels = np.array(img)
    h, w, _ = pixels.shape
    
    # Crear una nueva matriz de píxeles
    shuffled = np.zeros_like(pixels)
    
    for x in range(h):
        for y in range(w):
            new_pos =  mod_matrix_mult(matrix, [x, y], n)
            shuffled[new_pos[0] % h, new_pos[1] % w] = pixels[x, y]
    
    # Guardar la imagen desordenada
    shuffled_img = Image.fromarray(shuffled)
    shuffled_img.save(output_path)
    print(f"Imagen desordenada guardada en {output_path}")

def ordenaimagen(matrix, image_path, output_path, n):
    """Ordena una imagen utilizando la matriz inversa en Z_n."""
    inverse_matrix = matrix_mod_inverse(matrix, n)
    desordenaimagen(inverse_matrix, image_path, output_path, n)
    print(f"Imagen ordenada guardada en {output_path}")

def find_suitable_k(A, n):
    """
    Encuentra los valores de k adecuados para calcular A^k en Z_n.
    Devuelve los valores de k hasta que A^k ≡ I (mod n).
    """
    identity = np.eye(A.shape[0], dtype=int)  # Matriz identidad
    Ak = A.copy()
    k = 1
    
    while True:
        #print(f"Probando: K={k}, Ak={Ak}") # DEBUG
        if np.array_equal(Ak % n, identity):
            break  # Detener el ciclo si regresamos a la identidad
        Ak = mod_matrix_mult(Ak, A, n)  # Multiplicar iterativamente
        k += 1
    
    # print(f"Valores de k adecuados: (0, {k})") # DEBUG
    return k


def desordenaimagenite(A, image_path, output_path, n):
    """
    Desordena una imagen utilizando la matriz A elevada a una potencia k en Z_n.
    Solicita al usuario el valor de k.
    """

    # Verificar si la matriz A es invertible en Z_n
    if not is_invertible(A, n):
        raise ValueError("La matriz A no es invertible en Z_n.")
    
    suitable_k = find_suitable_k(A, n)
    print(f"Puedes usar los siguientes valores de k: {suitable_k}")

    # Solicitar el valor de k al usuario
    k = int(input(f"Ingrese un valor k para desordenar la imagen (1 <= k): "))
    
    # Calcular A^k en Z_n
    Ak = mod_matrix_power(A, k, n)
    
    # Cargar la imagen
    img = Image.open(image_path).convert('RGB')
    pixels = np.array(img)
    h, w, _ = pixels.shape
    
    if h != w:
        raise ValueError("La imagen debe ser cuadrada para este método.")
    
    # Crear una nueva matriz de píxeles desordenados
    shuffled = np.zeros_like(pixels)
    
    for x in range(h):
        for y in range(w):
            new_pos = np.dot(Ak, [x, y]) % n
            shuffled[new_pos[0] % h, new_pos[1] % w] = pixels[x, y]
    
    # Guardar la imagen desordenada
    shuffled_img = Image.fromarray(shuffled)
    shuffled_img.save(output_path)
    print(f"Imagen desordenada con k={k} guardada en {output_path}")

def ordenaimagenite(A, image_path, output_path, n):
    """
    Ordena una imagen utilizando la matriz inversa de A^k en Z_n.
    Solicita al usuario el valor de k.
    """
    # Solicitar el valor de k al usuario
    k = int(input(f"Ingrese el mismo valor k utilizado para desordenar la imagen: "))
    
    # Calcular A^k y su inversa en Z_n
    Ak = mod_matrix_power(A, k, n)
    Ak_inverse = matrix_mod_inverse(Ak, n)
    
    # Usar la función de desordenamiento con la matriz inversa para reordenar
    desordenaimagenite(Ak_inverse, image_path, output_path, n)
    print(f"Imagen ordenada con k={k} guardada en {output_path}")

def desordenaimagenproceso(A, image_path, output_dir, n, max_k):
    """
    Aplica el desordenamiento iterativo para observar la evolución con diferentes valores de k.
    Guarda las imágenes generadas en el directorio especificado.
    """

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Verificar si la matriz A es invertible en Z_n
    if not is_invertible(A, n):
        raise ValueError("La matriz A no es invertible en Z_n.")
    
    # Cargar la imagen
    img = Image.open(image_path).convert('RGB')
    pixels = np.array(img)
    h, w, _ = pixels.shape
    
    if h != w:
        raise ValueError("La imagen debe ser cuadrada para este método.")
    
    # Iterar sobre valores de k y guardar la evolución
    for k in range(1, max_k + 1):
        # Calcular A^k en Z_n
        Ak = mod_matrix_power(A, k, n)
        
        # Crear una nueva matriz de píxeles desordenados
        shuffled = np.zeros_like(pixels)
        
        for x in range(h):
            for y in range(w):
                new_pos = np.dot(Ak, [x, y]) % n
                shuffled[new_pos[0] % h, new_pos[1] % w] = pixels[x, y]
        
        # Guardar la imagen desordenada
        output_path = os.path.join(output_dir, f"imagen_desordenada_k{k}.png")
        shuffled_img = Image.fromarray(shuffled)
        shuffled_img.save(output_path)
        print(f"Imagen desordenada con k={k} guardada en {output_path}")


if __name__=="__main__":

    A = np.array([[1, 5], [2, 3]])
    print(f"¿Es {A} invertible? {is_invertible(A, 291)}") # => True

    print(f"Inverso:\n{matrix_mod_inverse(A, 291)}")

    n = 837 # Lado de la imagen
    image_path = 'imagen.jpg'
    sq_image = 'imagen_cuadrada.png'

    crop_to_square(image_path, sq_image)

    #desordenaimagen(A, sq_image, 'imagen_desordenada.png', n)
    #ordenaimagen(A, 'imagen_desordenada.png', 'imagen_ordenada.png', n)

    output_dir = 'imagenes_desordenadas'

    # 1. Desordenar una imagen con un valor k especificado
    desordenaimagenite(A, sq_image, 'imagen_desordenada_k.png', n)

    # 2. Ordenar la imagen con el mismo k
    ordenaimagenite(A, 'imagen_desordenada_k.png', 'imagen_ordenada.png', n)

    # 3. Ver la evolución con diferentes valores de k
    desordenaimagenproceso(A, sq_image, output_dir, n, max_k=5)