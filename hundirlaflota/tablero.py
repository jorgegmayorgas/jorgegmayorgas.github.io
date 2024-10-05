import numpy as np
import random
#mostrar = True
class Tablero:
    def __init__(self, jugador_id, dimensiones):
        self.jugador_id = jugador_id
        self.dimensiones = dimensiones
        self.barcos = {
            "Barco1": 4,#-40
            "Barco2": 3,#-30
            "Barco3": 3,#-30
            "Barco4": 2,#-20
            "Barco5": 2,#-20
            "Barco6": 2,#-20
            "Barco7": 1,#-10
            "Barco8": 1,#-10
            "Barco9": 1,#-10
            "Barco10": 1#-10
        }
        self.tablero_oculto = np.zeros(self.dimensiones)#el del jugador con sus barcos
        self.tablero_visible = np.zeros(self.dimensiones) # el que se muestra en pantalla
        self.mostrar = True

    def agregar_barco(self, nombre, eslora):
        self.barcos[nombre] = eslora

    def genera_barco(self, tam_barco=4):
        num_filas = self.dimensiones[0]
        num_columnas = self.dimensiones[1]
        orientaciones = ["N", "S", "O", "E"]

        while True:
            orientacion = random.choice(orientaciones)#para hacerlo aleatorio
            origen = (random.randint(0, num_filas - 1), random.randint(0, num_columnas - 1))
            fila = origen[0]
            columna = origen[1]
            barco = []
            #if self.tablero_oculto[origen] != 1 and self.tablero_oculto[origen] != 2:# cambiar por distinto a 0?
            if self.tablero_oculto[origen] == 0:# cambiado a que el valor sea igual a 0
                barco.append(origen)
                for i in range(tam_barco - 1):
                    if orientacion == "N":
                        fila -= 1
                    elif orientacion == "S":
                        fila += 1
                    elif orientacion == "E":
                        columna += 1
                    else:
                        columna -= 1
                    if fila >= num_filas or fila < 0 or columna >= num_columnas or columna < 0:
                        break
                    elif self.tablero_oculto[fila, columna] == 1 or self.tablero_oculto[fila, columna] == 2 or self.tablero_oculto[fila, columna] == 3 or self.tablero_oculto[fila, columna] == 4:
                        break
                    barco.append((fila, columna))
                if len(barco) != tam_barco:
                    continue
                else:
                    self.coloca_barco(barco)
                    break
            else:
                continue

    def coloca_barco(self, barco):
        for coordenada in barco:
            #self.tablero_oculto[coordenada] = 1#podría ser len(barco)
            self.tablero_oculto[coordenada] = len(barco)#podría ser len(barco)

    def inicializar_barcos(self):
        for nombre, eslora in self.barcos.items():
            self.genera_barco(eslora)
        
    def disparo_coordenada(self, x, y):
        valor_a_devolver=False
        if self.tablero_oculto[x, y] > 0:
            print(f'¡Impacto en ({x}, {y})!')
            #seguir disparando
            self.tablero_oculto[x, y] = -10 #tocado
            #comprobar hundido
            valor_a_devolver=True
        else:
            print(f'Agua en ({x}, {y})')
            self.tablero_oculto[x, y] = -5 # agua
            valor_a_devolver=False
        self.tablero_visible[x, y] = self.tablero_oculto[x, y]
        return valor_a_devolver

    def mostrar_tablero(self):#s recorre en busca de 0 o valor
        for fila in range(self.dimensiones[0]):
            for columna in range(self.dimensiones[1]):
                if self.tablero_visible[fila, columna] == 0:
                    print("  ", end="")
                elif self.tablero_visible[fila, columna] != 0:
                    if self.tablero_oculto[fila, columna] == -10:
                        print(" X ", end="")
                    else:
                        print(" - ", end="")
                print(" | ", end="")
            print("\n" + "-" * (self.dimensiones[0] * 5))
    
    def muestra_tablero_con_barcos(self):
        if self.mostrar==True:
            print(f"Barcos de {self.jugador_id}:")
            for fila in range(self.dimensiones[0]):
                for columna in range(self.dimensiones[1]):
                    if self.tablero_oculto[fila, columna] == 0:
                        print("  ", end="")
                    elif self.tablero_oculto[fila,columna]!=0:
                        print(f" {int(self.tablero_oculto[fila, columna])} ",end="")
                    print(" | ", end="")
                print("\n" + "-" * (self.dimensiones[0] * 5))

    def original_muestra_barcos_1(self):
        if self.mostrar==True:
            for fila in range(self.dimensiones[0]):
                for columna in range(self.dimensiones[1]):
                    if self.tablero_oculto[fila,columna]!=0:
                        print(f"{self.tablero_oculto[fila, columna]}")
                print(" | ", end="")
            print("\n" + "-" * (self.dimensiones[0] * 5))


    def muestra_barcos_2(self):#se podría eliminar
        for fila in range(self.dimensiones[0]):
            for columna in range(self.dimensiones[1]):
                if self.tablero_oculto[fila, columna] == 2 :
                    print("2", end="")
                print(" | ", end="")
            print("\n" + "-" * (self.dimensiones[0] * 5))
    
    def original_verificar_victoria(self):
        for fila in range(self.dimensiones[0]):
            for columna in range(self.dimensiones[1]):
                if self.tablero_oculto[fila, columna] == 1 and self.tablero_visible[fila, columna] != 1:
                    return False
        return True

    def verificar_victoria(self):
        contador=0
        for fila in range(self.dimensiones[0]):
            for columna in range(self.dimensiones[1]):
                if self.tablero_oculto[fila,columna] !=-5:
                    contador = contador + self.tablero_oculto[fila,columna]#estoy aquí
        if contador==-200:
            return True
        else:
            return False