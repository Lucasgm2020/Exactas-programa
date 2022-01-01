import numpy as np
import matplotlib.animation as animation
import matplotlib.pyplot as plt

def crear_tablero(n):
    dim = n + 2
    tablero = np.repeat(0,dim**2).reshape(dim,dim)    
    for i in range(len(tablero)):
        for j in range(len(tablero[0])):
            if i == 0 or i == dim -1 or j == 0 or j == dim - 1:
                tablero[i][j] = -1
    return tablero

def es_borde(tablero,coord):
    return tablero[coord[0]][coord[1]] == -1
        
def tirar_copo(tablero,coord):
    i = coord[0]
    j= coord[1]
    tablero[i][j] += 1

def vecinos_de(tablero,coord):
    vecinos = []
    i = coord[0]
    j = coord[1]
    posiciones = [(i-1,j),(i,j+1),(i+1,j),(i,j-1)]
    for posicion in posiciones:
        i_pos = posicion[0]
        j_pos = posicion[1]
        if tablero[i_pos][j_pos] != -1:
            vecinos.append((i_pos,j_pos))
    return vecinos

def desbordar_posicion(tablero,coord):
    i,j = coord[0],coord[1]
    if tablero[i][j] >= 4:
        vecinos = vecinos_de(tablero,coord)
        for vecino in vecinos:
            tablero[vecino[0]][vecino[1]] += 1
        tablero[i][j] = 0
            
def desbordar_arenero(tablero):
    filas = len(tablero)
    columnas = len(tablero[0])
    for fila in range(1,filas-1):
        for col in range(1,columnas-1):
            desbordar_posicion(tablero,(fila,col))
            
def hay_que_desbordar(tablero):
    filas = len(tablero)
    columnas = len(tablero[0])
    
    i_fila = 1
    j_columna = 1
    desborda = False
    while i_fila < (filas - 1) and not desborda:
        while j_columna < (columnas - 1) and not desborda:
            if tablero[i_fila][j_columna] >= 4:
                desborda = True
            j_columna += 1
        i_fila += 1
    return desborda    

def estabilizar(tablero):
    while hay_que_desbordar(tablero):
        desbordar_arenero(tablero)
        print(tablero)

def paso(tablero):
    filas = len(tablero)
    columnas = len(tablero)
    i_centro = (filas-1)//2
    j_centro = (columnas-1)//2
    tablero[(i_centro,j_centro)]=tablero[(i_centro,j_centro)]+1
    estabilizar(tablero)
    
n = 5
iteraciones = 20

t1 = crear_tablero(5)

ims = []
fig = plt.figure()


print(t1)
for i in range(4):
    tirar_copo(t1,(1,4))
    tirar_copo(t1,(2,5))
    tirar_copo(t1,(1,2))
    tirar_copo(t1,(3,4))
    tirar_copo(t1,(2,4))
    tirar_copo(t1,(1,3))
    tirar_copo(t1,(3,5))
    tirar_copo(t1,(3,3))
    tirar_copo(t1,(3,2))
    tirar_copo(t1,(3,1))
    tirar_copo(t1,(5,2))
    tirar_copo(t1,(2,1))
    tirar_copo(t1,(4,5))
    
print(t1)   

for i in range(iteraciones):
    paso(t1)
    im = plt.imshow(t1, animated=True)
    ims.append([im])

ani = animation.ArtistAnimation(fig, ims, interval=50, blit=True,repeat_delay=400)
print("Listo para guardar animacion")
writervideo = animation.FFMpegWriter(fps=60)
ani.save(r'dynamic_images.gif')
plt.show()

