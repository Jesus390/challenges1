import random
from collections import deque

def imprimir_ciudad(matriz):
    '''
    Imprime la ciudad en forma de matriz.
    @matriz, la ciudad en forma de matriz.
    '''
    longitud_matriz = len(matriz)
    # imprime el indice superior a la matriz
    print(' '.join([i[1] if len(i)>=2 else i for i in [str(i) for i in range(longitud_matriz)]]))

    print(' '.join(['_' for i in range(longitud_matriz)]))

    # imprime la matriz y el indice al costado de la matriz
    for i, row in enumerate(matriz):
        print(f"{' '.join(row)} |{i}")

def crear_ciudad(dimension, caracter_edificio, caracter_agua, porcentaje):
    '''
        crear_ciudad, crea una ciudad con dimensiones dadas y caracteristicas
        de edificios y agua, y un porcentaje de agua en la ciudad.
        @dimension, dimensiones de la ciudad
        @caracter_edificio, caracteristicas de los edificios
        @caracter_agua, caracteristicas de la agua
        @porcentaje, ???
        retorna, tupla, (matriz/posiciones_agua/posiciones_edificio)
    '''
    # Generar matriz de la ciudad
    matriz = [['.' for _ in range(dimension)] for _ in range(dimension)]
    # Lista de posiciones de agua
    posiciones_agua = []
    # Lista de posiciones de edificios
    posiciones_edificio = []

    # Genera y guarda las posiciones de edificios
    for fila in range(0, dimension, 2):
        for columna in range(0, dimension, 2):
            matriz[fila][columna] = caracter_edificio
            posiciones_edificio.append((fila, columna))

    # Genera y guarda las posiciones de agua   
    for fila in range(dimension):
        for columna in range(dimension):
            if matriz[fila][columna] == ".":
                if random.randint(0, 100) <= porcentaje:
                    matriz[fila][columna] = caracter_agua
                    posiciones_agua.append((fila, columna))
    # for fila in matriz:
    #     print(' '.join(fila))
    imprimir_ciudad(matriz)

    return matriz, posiciones_agua, posiciones_edificio


def obtener_movimientos_validos(posicion_entrada, posicion_edificio, posicion_agua, posicion_obstaculo_opcional, dimension):
    '''
    obtener_movimientos_validos, devuelve una lista de movimientos validos
    @posicion_entrada, posicion de entrada
    @posicion_edificio, lista de posiciones de edificios
    @posicion_agua, lista de posiciones de agua
    @posicion_obstaculo_opcional, lista de posiciones de obstaculos
    @dimension, dimensiones de la ciudad
    retorna, lista de movimientos validos
    '''
    # desempaquetado de tuplas
    fila_entrada, columna_entrada = posicion_entrada
    # lista de movimientos validos
    movimientos_validos = []
    # movimientos validos
    direcciones = [(-1, 0), (1, 0), (0, -1), (0, 1)] 

    for direccion in direcciones:
        nueva_fila = fila_entrada + direccion[0]
        nueva_columna = columna_entrada + direccion[1]
        
        if 0 <= nueva_fila < dimension and 0 <= nueva_columna < dimension:
            if (nueva_fila, nueva_columna) not in posicion_edificio:
                if (nueva_fila, nueva_columna) not in posicion_agua:
                    if (nueva_fila, nueva_columna) not in posicion_obstaculo_opcional:
                        movimientos_validos.append((nueva_fila, nueva_columna))
    return movimientos_validos


def bfs_encontrar_camino(entrada, salida, posicion_edificio, posicion_agua, posicion_obstaculo_opcional, dimension):
    """
    Implementa BFS para encontrar el camino más corto entre entrada y salida
    @entrada, posicion de entrada
    @salida, posicion de salida
    @posicion_edificio, lista de posiciones de edificios
    @posicion_agua, lista de posiciones de agua
    @posicion_obstaculo_opcional, lista de posiciones de obstaculos
    @dimension, dimensiones de la ciudad
    Retorna: lista de posiciones que forman el camino, o None si no hay camino
    """
    if entrada == salida:
        return [entrada]
    
    # Cola para BFS: cada elemento es (posicion_actual, camino_hasta_aqui)
    cola = deque([(entrada, [entrada])])
    visitados = {entrada}
    
    while cola:
        posicion_actual, recorrido_actual = cola.popleft()
        
        # Obtener todos los movimientos válidos desde la posición actual
        vecinos = obtener_movimientos_validos(posicion_actual, posicion_edificio, posicion_agua, posicion_obstaculo_opcional, dimension)
        
        for vecino in vecinos:
            if vecino == salida:
                # ¡Encontramos la salida!
                return recorrido_actual + [vecino]
            
            if vecino not in visitados:
                visitados.add(vecino)
                nuevo_camino = recorrido_actual + [vecino]
                cola.append((vecino, nuevo_camino))
    
    # No se encontró camino
    return None


def mostrar_recorrido(ciudad, camino, entrada, salida, obstaculos_opcionales):
    """
    Muestra la ciudad con el camino marcado y los obstáculos opcionales
    @ciudad, matriz de la ciudad
    @camino, lista de posiciones del camino
    @entrada, posicion de entrada
    @salida, posicion de salida
    @obstaculos_opcionales, lista de posiciones de obstaculos
    retorna, None
    """
    # Crear una copia de la ciudad para no modificar la original
    ciudad_con_camino = [fila for fila in ciudad]
    
    # Marcar los obstáculos opcionales primero
    for fila, columna in obstaculos_opcionales:
        ciudad_con_camino[fila][columna] = "!"
    
    # Marcar el camino (excluyendo entrada y salida)
    if camino:
        for i, (fila, columna) in enumerate(camino):
            if i == 0:  # Entrada
                ciudad_con_camino[fila][columna] = "E"
            elif i == len(camino) - 1:  # Salida
                ciudad_con_camino[fila][columna] = "S"
            else:  # Camino
                ciudad_con_camino[fila][columna] = "*"
    # else:
    #     # Si no hay camino, solo marcar entrada y salida
    #     fila_entrada, columna_entrada = entrada
    #     fila_salida, columna_salida = salida
    #     ciudad_con_camino[fila_entrada][columna_entrada] = "E"
    #     ciudad_con_camino[fila_salida][columna_salida] = "S"
    
    print("\nCiudad actualizada:")
    # for fila in ciudad_con_camino:
    #     print(" ".join(fila))
    imprimir_ciudad(ciudad_con_camino)

def inicio_gps():
    '''
    Inicia el GPS
    '''
    print("Bienvenido a la ciudad")
    dimension = int(input("Dime el tamaño de la ciudad: ")) # Tamaño de la ciudad
    porcentaje_agua = 4 # 4% de la ciudad es agua
    edificio = '#' # caracter representativo del edificio
    agua = "~" # caracter representativo del agua
    
    # 1. Crear la ciudad y obtener las posiciones
    ciudad, posiciones_agua, posiciones_edificio = crear_ciudad(dimension, edificio, agua, porcentaje_agua)
    
    print("\nConfiguremos tu destino")
    
    # 2. Configurar punto de entrada
    while True:
        try:
            fila_entrada = int(input("Dime la fila del punto de partida: "))
            columna_entrada = int(input("Dime la columna del punto de partida: "))
            entrada = (fila_entrada, columna_entrada)

            if not (0 <= fila_entrada < dimension and 0 <= columna_entrada < dimension):
                print(f"Este punto está fuera de los límites de la ciudad {entrada}")
            elif entrada in posiciones_edificio:
                print(f"Aquí no puedes colocar, hay un edificio {entrada}")
            elif entrada in posiciones_agua:
                print(f"Aquí no puedes colocar, hay un río {entrada}")
            else:
                print(f"Colocaste la entrada en {entrada}")
                break
        except ValueError:
            print("Por favor ingresa un número válido")

    # 3. Configurar punto de salida
    while True:
        try:
            fila_salida = int(input("Dime la fila del punto de llegada: "))
            columna_salida = int(input("Dime la columna del punto de llegada: "))
            salida = (fila_salida, columna_salida)

            if not (0 <= fila_salida < dimension and 0 <= columna_salida < dimension):
                print(f"Este punto está fuera de los límites de la ciudad {salida}")
            elif salida in posiciones_edificio:
                print(f"Aquí no puedes colocar, hay un edificio {salida}")
            elif salida in posiciones_agua:
                print(f"Aquí no puedes colocar, hay un río {salida}")
            elif salida == entrada:
                print(f"Estás colocando en el mismo punto de inicio {salida}")
            else:
                print(f"Colocaste la salida en {salida}")
                break
        except ValueError:
            print("Por favor ingresa un número válido")

    # 4. Resolver con BFS inicialmente (sin obstáculos)
    obstaculos_opcionales = []
    camino = bfs_encontrar_camino(entrada, salida, posiciones_edificio, posiciones_agua, obstaculos_opcionales, dimension)
    
    if camino:
        print("\n¡Encontramos el camino!")
        mostrar_recorrido(ciudad, camino, entrada, salida, obstaculos_opcionales)
    else:
        print("\nNo se encontró el punto de llegada. Verifique que no esté bloqueado por obstáculos")
        mostrar_recorrido(ciudad, None, entrada, salida, obstaculos_opcionales)
        print("El GPS no puede encontrar una ruta. Programa terminado.")
        return

    # 5. Bucle para agregar obstáculos opcionales
    while True:
        try:
            opcion = int(input("\nIngrese el número de la opción que desea:\n1- Quiero ingresar un obstáculo\n2- No deseo agregar nada (Salir)\nOpción: "))
            
            if opcion == 1:
                fila = int(input("Dime la fila del obstáculo: "))
                columna = int(input("Dime la columna del obstáculo: "))
                obstaculo_agregado = (fila, columna)

                if not (0 <= fila < dimension and 0 <= columna < dimension):
                    print(f"Esta posición no es válida ya que está fuera de la ciudad {obstaculo_agregado}")
                elif obstaculo_agregado == entrada or obstaculo_agregado == salida:
                    print(f"No se puede agregar obstáculo ya que está en el punto de Partida/Llegada {obstaculo_agregado}")
                elif obstaculo_agregado in posiciones_edificio:
                    print(f"No se puede agregar aquí ya que es un Edificio {obstaculo_agregado}")
                elif obstaculo_agregado in posiciones_agua:
                    print(f"No se puede agregar aquí ya que es un Río {obstaculo_agregado}")
                elif obstaculo_agregado in obstaculos_opcionales:
                    print(f"Aquí ya agregaste un obstáculo!!! {obstaculo_agregado}")
                else:
                    obstaculos_opcionales.append(obstaculo_agregado)
                    print(f"Agregaste un obstáculo temporal en la posición {obstaculo_agregado}")
                    
                    # Recalcular el camino con el nuevo obstáculo
                    camino = bfs_encontrar_camino(entrada, salida, posiciones_edificio, posiciones_agua, obstaculos_opcionales, dimension)
                    
                    if camino:
                        print("¡Encontramos un nuevo camino!")
                        mostrar_recorrido(ciudad, camino, entrada, salida, obstaculos_opcionales)
                    else:
                        print("No se encontró el punto de llegada. Todas las rutas están bloqueadas.")
                        mostrar_recorrido(ciudad, None, entrada, salida, obstaculos_opcionales)
                        print("El GPS no puede encontrar una ruta. Programa terminado.")
                        break  # Terminar el programa automáticamente
                    
            elif opcion == 2:
                print("Saliendo del GPS. ¡Hasta luego!")
                break
            else:
                print("Opción no válida. Favor lea las opciones e ingrese el número")
        except ValueError:
            print("Por favor ingresa un número válido")


if __name__ == "__main__":
    inicio_gps()