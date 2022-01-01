import numpy as np
import random
import matplotlib.pyplot as plt
import csv

def crear_tablero(filas,columnas):
    tablero = np.repeat(" ",(filas+2) * (columnas+2)).reshape(filas+2,columnas+2)   
    for i in range(len(tablero)):
        for j in range(len(tablero[i])):
            if i == 0 or i == (filas + 1) or j == 0 or j == (columnas + 1):
                tablero[i][j] = "M"
    return tablero

def vecinos_tablero(tablero,coord):
    posiciones_vecinos = []
    i = coord[0]
    j = coord[1]
    posiciones = [(i-1,j-1),(i-1,j),(i-1,j+1),(i,j+1),(i+1,j+1),(i+1,j),(i+1,j-1),(i,j-1)]
    for fila,columna in posiciones:
        if tablero[fila][columna] == "M":
            posiciones_vecinos.append(("",""))
        else:
            posiciones_vecinos.append((fila,columna))
    return posiciones_vecinos

def buscar_adyacente(tablero,coord,objetivo):
    posicion_objetivo = []
    i = coord[0]
    j = coord[1]
    posiciones = [(i-1,j-1),(i-1,j),(i-1,j+1),(i,j+1),(i+1,j+1),(i+1,j),(i+1,j-1),(i,j-1)]    
    iteracion = 0
    while iteracion < len(posiciones) and len(posicion_objetivo)== 0:
        fila = posiciones[iteracion][0]
        columna = posiciones[iteracion][1]
        if tablero[fila][columna]== "M":
            pass
        elif tablero[fila][columna] == objetivo:
            posicion_objetivo.extend([fila,columna])
        iteracion += 1
    return posicion_objetivo

def mover(tablero,coord):
    i = coord[0]
    j = coord[1] 
    evaluar_movimiento = tablero[i][j] in "LA"
    posicion_vacia_adyacente = buscar_adyacente(tablero,(i,j)," ")
    if len(posicion_vacia_adyacente) > 0:
        fila_vacia = posicion_vacia_adyacente[0]
        columna_vacia =  posicion_vacia_adyacente[1]
        tablero[fila_vacia][columna_vacia] = tablero[i][j]    
        tablero[i][j] = " "
    else:
        pass

def alimentar(tablero,coord):
    i = coord[0]
    j = coord[1] 
    es_leon = tablero[i][j] == "L"    
    hay_antilope = len(buscar_adyacente(tablero,(i,j),"A")) > 0 
    if es_leon and hay_antilope:
        pos_antilope = buscar_adyacente(tablero,(i,j),"A")
        tablero[pos_antilope[0]][pos_antilope[1]] = tablero [i][j]
        tablero [i][j] = " "

def reproducir(tablero,coord):
    i = coord[0]
    j = coord[1]     
    es_animal = tablero[i][j] in "LA"
    hay_vecino = len(buscar_adyacente(tablero,coord,tablero[i][j])) > 0
    if es_animal and hay_vecino:
        animal = tablero[i][j]
        vecino = buscar_adyacente(tablero,coord,animal)
        siguiente_pos_vacia = buscar_adyacente(tablero,coord," ")
        if len(siguiente_pos_vacia) > 0:
            tablero[siguiente_pos_vacia[0]][siguiente_pos_vacia[1]] = animal
            
def fase_alimentacion(tablero):
    filas = len(tablero) - 2
    columnas = len(tablero[0]) - 2
    for fila in range(1,filas+1):
        for columna in range(1,columnas+1):
            coordenadas = (fila,columna)
            alimentar(tablero,coordenadas)

def fase_reproduccion(tablero):
    filas = len(tablero) - 2
    columnas = len(tablero[0]) - 2
    for fila in range(1,filas+1):
        for columna in range(1,columnas+1):
            coordenadas = (fila,columna)
            reproducir(tablero,coordenadas)

def fase_mover(tablero):
    filas = len(tablero) - 2
    columnas = len(tablero[0]) - 2
    for fila in range(1,filas+1):
        for columna in range(1,columnas+1):
            coordenadas = (fila,columna)
            mover(tablero,coordenadas)    

def evolucionar(tablero):
    print("Estado inicial: \n",tablero,"\n")
    fase_alimentacion(tablero)
    print("Luego de alimentacion: \n",tablero,"\n")
    fase_reproduccion(tablero)
    print("Luego de reproduccion: \n",tablero,"\n")
    fase_mover(tablero)
    print("Luego de movimiento: \n",tablero,"\n")
 
def evolucionar_en_el_tiempo(tablero,k):
    for k in range(k):
        print("Iteracion: ", k+1)
        evolucionar(tablero)
        
def mezclar_celdas(tablero):
    celdas = []
    for i in range(1,len(tablero)-2):
        for j in range(1,len(tablero[0])-2):
            celdas.append((i,j))
    random.shuffle(celdas)
    return celdas

def generar_azar_antilopes_leones(tablero):
    tope_antilopes = int((len(tablero)-2) * (len(tablero[0])-2) / 10) #tope en 20% de celdas     
    tope_leones = int((len(tablero)-2) * (len(tablero[0])-2) / 20) #tope en 10% de celdas
    antilopes = random.randint(1,tope_antilopes)  
    leones = random.randint(1,tope_leones)
    return antilopes,leones
    
def completar_tablero(tablero,antilopes,leones):
    celdas_aleatorias = mezclar_celdas(tablero)
    i_antilopes = 0
    i_leones = 0
    while i_antilopes < antilopes or i_leones < leones:
        if i_antilopes < antilopes:    
            i = celdas_aleatorias[0][0]
            j = celdas_aleatorias[0][1]
            celdas_aleatorias.pop(0)
            tablero[i][j] = "A"
            i_antilopes += 1
        if i_leones < leones:
            i = celdas_aleatorias[0][0]
            j = celdas_aleatorias[0][1]
            celdas_aleatorias.pop(0)
            tablero[i][j] = "L"
            i_leones += 1

def cuantos_de_cada(tablero):
    filas = len(tablero) - 2
    columnas = len(tablero[0]) - 2
    antilopes = 0
    leones = 0
    for fila in range(1,filas+1):
        for columna in range(1,columnas+1):
            if tablero[fila][columna] == "A":
                antilopes += 1
            elif tablero[fila][columna] == "L":
                leones += 1
            else:
                pass
    return [antilopes,leones]        

def registrar_evolucion(tablero,k):
    lista_animales = []
    for k_iter in range(k):
        print("Iteracion: ",k_iter+1)
        evolucionar(tablero)
        animales = cuantos_de_cada(tablero)
        lista_animales.append(animales)
    return lista_animales

def generar_tablero_azar(filas,columnas,n_antilopes,n_leones):
    tablero = crear_tablero(filas,columnas)     
    completar_tablero(tablero,n_antilopes,n_leones)
    return tablero

tablero = generar_tablero_azar(10,10,10,5)
evoluciones = registrar_evolucion(tablero,2)
with open("predpres.csv","w", newline="") as csvfile:
    csv_writer = csv.writer(csvfile)
    csv_writer.writerow(["antilopes","leones"])
    csv_writer.writerows(evoluciones)

valores = np.loadtxt("predpres.csv",delimiter=",",skiprows=1)
plt.ylabel("Cantidad de individuos")
plt.xlabel("Ciclo")
plt.plot(valores[:,0], label = "antilopes")
plt.plot(valores[:,1], label = "leones")
plt.legend()
plt.grid(True)
plt.show()

