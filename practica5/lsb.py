from PIL import Image

def text_to_bits(text):
    """Convierte un texto en su representación binaria (lista de bits)."""
    bits = ''.join(format(ord(char), '08b') for char in text)
    return bits

def bits_to_text(bits):
    """Convierte una secuencia de bits en texto."""
    chars = [chr(int(bits[i:i+8], 2)) for i in range(0, len(bits), 8)]
    return ''.join(chars)

def LSB_simple_cypher(image_path, message, output_path):
    """Oculta un mensaje en los primeros píxeles de una imagen en blanco y negro."""
    # Convertir el mensaje a bits
    bits = text_to_bits(message)
    msg_len = len(bits)
    
    # Abrir la imagen
    img = Image.open(image_path).convert('L')  # Convertir a escala de grises
    pixels = list(img.getdata())
    
    # Comprobar si hay suficiente espacio para ocultar el mensaje
    if msg_len > len(pixels):
        raise ValueError("La imagen no es lo suficientemente grande para ocultar el mensaje.")
    
    # Modificar los bits menos significativos de los píxeles
    new_pixels = [
        (pixel & ~1) | int(bits[i]) if i < msg_len else pixel
        for i, pixel in enumerate(pixels)
    ]
    
    # Guardar la nueva imagen
    img.putdata(new_pixels)
    img.save(output_path)
    print(f"Mensaje oculto en {output_path}")

def LSB_simple_decypher(image_path, msg_length):
    """Extrae un mensaje oculto en una imagen en blanco y negro."""
    # Abrir la imagen
    img = Image.open(image_path).convert('L')
    pixels = list(img.getdata())
    
    # Extraer los bits menos significativos
    bits = ''.join(str(pixel & 1) for pixel in pixels[:msg_length])
    
    # Convertir los bits a texto
    return bits_to_text(bits)

def LSB_complex_cypher(image_path, message, output_path, step):
    """Oculta un mensaje usando saltos en los píxeles de la imagen."""
    bits = text_to_bits(message)
    msg_len = len(bits)
    
    img = Image.open(image_path).convert('L')
    pixels = list(img.getdata())
    
    if msg_len * step > len(pixels):
        raise ValueError("La imagen no es lo suficientemente grande para ocultar el mensaje con el paso indicado.")
    
    new_pixels = pixels[:]
    for i, bit in enumerate(bits):
        idx = i * step
        new_pixels[idx] = (pixels[idx] & ~1) | int(bit)
    
    img.putdata(new_pixels)
    img.save(output_path)
    print(f"Mensaje oculto en {output_path}")

def LSB_complex_decypher(image_path, msg_length, step):
    """Decodifica un mensaje usando saltos en los píxeles de la imagen."""
    img = Image.open(image_path).convert('L')
    pixels = list(img.getdata())
    
    bits = ''.join(str(pixels[i * step] & 1) for i in range(msg_length))
    return bits_to_text(bits)

if __name__=="__main__":

    bits = text_to_bits("Hola") # => '01001000011011110110110001100001'
    print(f"Hola en bits {bits}")
    print(f"Bits decodificados: {bits_to_text(bits)}\n")

    #LSB simple
    LSB_simple_cypher('imagen.jpg', 'Hola mundo', 'imagen_codificada.png')
    print(f"Mensaje oculto: {LSB_simple_decypher('imagen_codificada.png', 150)}\n") # => "Hola mundo"

    #LSB complex
    LSB_complex_cypher('imagen.jpg', 'Hola mundo', 'imagen_codificada_compleja.png', 2)
    print(f"Mensaje oculto en imagen compleja: {LSB_complex_decypher('imagen_codificada_compleja.png', 150, 2)}") # => "Hola mundo"