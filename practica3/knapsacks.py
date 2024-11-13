
def letter2ascii(a):
    return ord(a)

def ascii2letter(a):
    return chr(a)

#Toma un vector fila y determine si es una mochila supercreciente (devolviendo 1),
# una mochila no supercreciente (devolviendo 0) o no es una mochila (devolviendo -1)
def knapsack(vector):

    
    for i in range(1,len(vector)):
        #print(f"[DEBUG] {vector[i]}")
        suma=0
        for j in vector[:i]:
            suma += j
        
        #print(f"[DEBUG] Suma = {suma}")
        if suma >= vector[i]: return False

    return True

# Toma una mochila (supercreciente o no) s, un valor v, y determine usando el algoritmo de
# mochilas supercrecientes si v es valor objetivo de s
def knapsacksol(s, v):

    aux = v
    for i in reversed(s):
        if aux >= i:
            aux -= i

        if aux == 0:
            return True
    
    return False

if __name__ == "__main__":

    mochila = (1,2,5,10) 

    if knapsacksol(mochila, 7): print(f"{7} es valor de la mochila")
    if knapsacksol(mochila, 9): print(f"{9} es valor de la mochila")
