from collections import deque

def crear_ciudad(posicion_edificio, posicion_agua, dimension):
    ciudad = [["."for _ in range(dimension)]for _ in range(dimension)]

    for (fila, columna) in posicion_edificio:
        ciudad[fila][columna] = "#"

    for (fila, columna) in posicion_agua:
        ciudad[fila][columna] = "~"
        
    for filas in ciudad:
        print(" ".join(filas))
    return ciudad

# movimientos validos que puede realizar dentro del gps
def movimientos_validos(posicion_entrada, posicion_edificio, posicion_agua, posicion_obstaculo_opcional, dimension):
    fila_entrada, columna_entrada = posicion_entrada
    movimientos_validos = []
    direcciones = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    for direccion in direcciones:
        nueva_fila = fila_entrada + direccion[0]
        nueva_columna = columna_entrada + direccion[1]
        if 0 <= nueva_fila < dimension and 0 <= nueva_columna < dimension:
            if(nueva_fila, nueva_columna) not in posicion_edificio:
                if(nueva_fila, nueva_columna) not in posicion_agua:
                    if(nueva_fila, nueva_columna) not in posicion_obstaculo_opcional:
                        movimientos_validos.append((nueva_fila, nueva_columna))
    return movimientos_validos

def bfs_encontrar_camino(entrada, salida, posicion_edificio, posicion_agua, posicion_obstaculo_opcional, dimension):
    """
    Implementa BFS para encontrar el camino más corto entre entrada y salida
    Retorna: lista de posiciones que forman el camino, o None si no hay camino
    """
    if entrada == salida:
        return [entrada]
    
    # Cola para BFS: cada elemento es (posicion_actual, camino_hasta_aqui)
    cola = deque([(entrada, [entrada])])
    visitados = {entrada}
    
    while cola:
        posicion_actual, camino_actual = cola.popleft()
        
        # Obtener todos los movimientos válidos desde la posición actual
        vecinos = movimientos_validos(posicion_actual, posicion_edificio, posicion_agua, posicion_obstaculo_opcional, dimension)
        
        for vecino in vecinos:
            if vecino == salida:
                # ¡Encontramos la salida!
                return camino_actual + [vecino]
            
            if vecino not in visitados:
                visitados.add(vecino)
                nuevo_camino = camino_actual + [vecino]
                cola.append((vecino, nuevo_camino))
    
    # No se encontró camino
    return None


def mostrar_ciudad_con_camino(ciudad, camino, entrada, salida):
    """Muestra la ciudad con el camino marcado"""
    # Crear una copia de la ciudad para no modificar la original
    ciudad_con_camino = [fila[:] for fila in ciudad]
    
    # Marcar el camino (excluyendo entrada y salida)
    for i, (fila, columna) in enumerate(camino):
        if i == 0:  
            ciudad_con_camino[fila][columna] = "E"
        elif i == len(camino) - 1:  
            ciudad_con_camino[fila][columna] = "S"
        else: 
            ciudad_con_camino[fila][columna] = "*"
    
    for fila in ciudad_con_camino:
        print(" ".join(fila))


# configuracion inicial de los parametros del gps 
def inicio_gps():
    
    print("Bienvenido a la ciudad")
    dimension = int(input("Dime el tamaño de la ciudad: "))
    edificio = [(1, 1), (4, 4), (5, 6)]
    agua = [(2, 2), (3, 3)]
    crear_ciudad(edificio, agua, dimension)
    print("Configuremos tu destino")
    

    while True:
        fila_entrada = int(input("Dime la fila del punto de partida: "))
        columna_entrada = int(input("Dime la columna del punto de partida: "))
        entrada = (fila_entrada, columna_entrada)

        if not (0 <= fila_entrada < dimension and 0 <= columna_entrada < dimension):
            print(f"Este punto esta fuera de los limites de la ciudad {fila_entrada, columna_entrada}")
        elif entrada in edificio:
            print(f"Aqui no puedes colocar, hay un edificio {fila_entrada, columna_entrada}")
        elif entrada in agua:
            print(f"Aqui no puedes colocar, hay un rio {fila_entrada, columna_entrada}")
        else:
            print(f"Colocaste la entrada en {fila_entrada, columna_entrada}")
            break

    while True:
        fila_salida = int(input("Dime la fila del punto de llegada: "))
        columna_salida = int(input("Dime la columna del punto de llegada: "))
        salida = (fila_salida, columna_salida)

        if not (0 <= fila_salida < dimension and 0 <= columna_salida < dimension):
            print(f"Este punto esta fuera de los limites de la ciudad {fila_salida, columna_salida}")
        elif salida in edificio:
            print(f"Aqui no puede colocar, hay un edificio {fila_salida, columna_salida}")
        elif salida in agua:
            print(f"Aqui no puedes colocar, hay un rio {fila_salida, columna_salida}")
        elif salida == entrada:
            print(f"Estas colocando en el mismo punto de inicio {fila_salida, columna_salida}")
        else:
            print(f"Colocaste la salida en {fila_salida, columna_salida}")
            break

    obstaculo_opcional = []
    while True:
        obstaculo = int(input("Ingrese el numero de la opcion que desea 1- Quiero ingresar un obstaculo 2- No deseo agregar nada(Salir): "))
        if obstaculo == 1:
            fila = int(input("Dime la fila del obstaculo: "))
            columna = int(input("Dime la columna del obstaculo: "))
            obstaculo_agregado = (fila, columna)

            if not (0 <= fila < dimension and 0 <= columna < dimension):
                print(f"Esta posicion no es valida ya que esta fuera de la ciudad {fila, columna}")
            elif obstaculo_agregado == entrada or obstaculo_agregado == salida:
                print(f"No se puede agregar obstaculo ya que esta en el punto de Partida/Llegada ({fila, columna})")
            elif obstaculo_agregado in edificio:
                print(f"No se puede agregar aqui ya que es un Edificio {fila, columna}")
            elif obstaculo_agregado in agua:
                print(f"No se puede agregar aqui ya que es un Rio {fila, columna}")
            elif obstaculo_agregado in obstaculo_opcional:
                print(f"Aqui ya agregaste un obstaculo!!!{fila, columna}")
            else:
                obstaculo_opcional.append(obstaculo_agregado)
                print(f"Agregaste un obstaculo temporal en la posicion {fila, columna}")
        elif obstaculo == 2:
            break
        else:
            print("Opcion no valida favor lea las opciones e ingrese el numero")

    actualizar_gps = crear_ciudad(edificio, agua, dimension)

    actualizar_gps[fila_entrada][columna_entrada] = "E"
    actualizar_gps[fila_salida][columna_salida] = "S"

    for (fila, columna) in obstaculo_opcional:
        actualizar_gps[fila][columna] = "!"

    for filas in actualizar_gps:
        print(" ".join(filas))

    camino = bfs_encontrar_camino(entrada, salida, edificio, agua, obstaculo_opcional, dimension)
    
    if camino:
        print("Encontramos el camino")
        mostrar_ciudad_con_camino(actualizar_gps, camino, entrada, salida)

    else:
        print("No se encontro el punto de llegada, verifique que no este bloqueado por obstaculos")


if __name__ == "__main__":
    inicio_gps()