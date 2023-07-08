## REPRESENTACION DE ESTADOS ##

"""Recuérdese que según lo que se ha visto en clase,
la implementación de la representación de un problema de espacio de estados consiste en:

Representar estados y acciones mediante una estructura de datos.
Definir: estado_inicial, es_estado_final(), acciones(), aplica(,)
y coste_de_aplicar_accion, si el problema tiene coste."""
from bokeh.core.has_props import abstract


class Problema(object):
    """Clase abstracta para un problema de espacio de estados. Los problemas
    concretos habría que definirlos como subclases de Problema, implementando
    acciones, aplica y eventualmente __init__, es_estado_final y
    coste_de_aplicar_accion. Una vez hecho esto, se han de crear instancias de
    dicha subclase, que serán la entrada a los distintos algoritmos de
    resolución mediante búsqueda."""

    def __init__(self, estado_inicial, estado_final=None):
        """El constructor de la clase especifica el estado inicial y
        puede que un estado_final, si es que es único. Las subclases podrían
        añadir otros argumentos"""

        self.estado_inicial = estado_inicial
        self.estado_final = estado_final

    def acciones(self, estado):
        """Devuelve las acciones aplicables a un estado dado. Lo normal es
        que aquí se devuelva una lista, pero si hay muchas se podría devolver
        un iterador, ya que sería más eficiente."""
        abstract

    def aplica(self, estado, accion):
        """ Devuelve el estado resultante de aplicar accion a estado. Se
        supone que accion es aplicable a estado (es decir, debe ser una de las
        acciones de self.acciones(estado)."""
        abstract

    def es_estado_final(self, estado):
        """Devuelve True cuando estado es final. Por defecto, compara con el
        estado final, si éste se hubiera especificado al constructor. Si se da
        el caso de que no hubiera un único estado final, o se definiera
        mediante otro tipo de comprobación, habría que redefinir este método
        en la subclase."""
        return estado == self.estado_final

    def coste_de_aplicar_accion(self, estado, accion):
        """Devuelve el coste de aplicar accion a estado. Por defecto, este
        coste es 1. Reimplementar si el problema define otro coste """
        return 1


class Jarras(Problema):
    """Problema de las jarras:
    Representaremos los estados como tuplas (x,y) de dos números enteros,
    donde x es el número de litros de la jarra de 4 e y es el número de litros
    de la jarra de 3"""

    def __init__(self):
        super().__init__((0, 0))

    def acciones(self, estado):
        jarra_de_4 = estado[0]
        jarra_de_3 = estado[1]
        accs = list()
        if jarra_de_4 > 0:
            accs.append("vaciar jarra de 4")
            if jarra_de_3 < 3:
                accs.append("trasvasar de jarra de 4 a jarra de 3")
        if jarra_de_4 < 4:
            accs.append("llenar jarra de 4")
            if jarra_de_3 > 0:
                accs.append("trasvasar de jarra de 3 a jarra de 4")
        if jarra_de_3 > 0:
            accs.append("vaciar jarra de 3")
        if jarra_de_3 < 3:
            accs.append("llenar jarra de 3")
        return accs

    def aplica(self, estado, accion):
        j4 = estado[0]
        j3 = estado[1]
        if accion == "llenar jarra de 4":
            return (4, j3)
        elif accion == "llenar jarra de 3":
            return (j4, 3)
        elif accion == "vaciar jarra de 4":
            return (0, j3)
        elif accion == "vaciar jarra de 3":
            return (j4, 0)
        elif accion == "trasvasar de jarra de 4 a jarra de 3":
            return (j4 - 3 + j3, 3) if j3 + j4 >= 3 else (0, j3 + j4)
        else:  # "trasvasar de jarra de 3 a jarra de 4"
            return (j3 + j4, 0) if j3 + j4 <= 4 else (4, j3 - 4 + j4)

    def es_estado_final(self, estado):
        return estado[0] == 2


""" Definir la clase Ocho_Puzzle, que implementa la representación del problema del 8-puzzle visto en clase. 
    Para ello, completar el código que se presenta a continuación, en los lugares marcados con interrogantes."""


class Ocho_Puzzle(Problema):

    def __init__(self, tablero_inicial):
        super().__init__(estado_inicial=tablero_inicial, estado_final=(1, 2, 3, 8, 0, 4, 7, 6, 5))

    def acciones(self, estado):
        pos_hueco = estado.index(0)
        acciones = list()

        if pos_hueco not in [0, 1, 2]:
            acciones.append("Mover hueco arriba")

        elif pos_hueco not in [0, 3, 6]:
            acciones.append("Mover hueco izquierda")

        elif pos_hueco not in [2, 5, 8]:
            acciones.append("Mover hueco derecha")

        elif pos_hueco not in [6, 7, 8]:
            acciones.append("Mover hueco abajo")

    def aplica(self, estado, accion):
        pos_hueco = estado.index(0)

        resultado = list(estado)

        if accion == "Mover hueco arriba":
            nueva_pos = pos_hueco - 3
        elif accion == "Mover hueco izquierda":
            nueva_pos = pos_hueco - 3
        elif accion == "Mover hueco derecha":
            nueva_pos = pos_hueco - 3
        elif accion == "Mover hueco abajo":
            nueva_pos = pos_hueco - 3

        resultado[pos_hueco], resultado[nueva_pos] = resultado[nueva_pos], resultado[pos_hueco]

        return tuple(resultado)


""" La siguientes definiciones nos van a permitir experimentar con distintos estados iniciales, algoritmos 
    y heurísticas, para resolver el 8-puzzle. Además se van a contar el número de nodos analizados durante la búsqueda:
"""


class Problemas_Analizados(Problema):

    def __init__(self, problema):
        self.estado_inicial = problema.estado_inicial
        self.estado_final = problema.estado_final
        self.analizados = 0

    def acciones(self, estado):
        return self.problema.acciones(estado)

    def aplica(self, estado, accion):
        return self.problema.aplica(estado, accion)

    def es_estado_final(self, estado):
        self.analizados = self.analizados + 1
        return self.problema.es_estado_final(estado)

    def coste_de_aplicar_accion(self, estado, accion):
        return self.problema.coste_de_aplicar_accion(estado, accion)


def resuelve_8_puzzle(estado_inicial, algoritmo, h=None):
    p8p = Problemas_Analizados(Ocho_Puzzle(estado_inicial))

    sol = (algoritmo(p8p, h).solucion() if h else algoritmo(p8p).solucion())

    print("Solución: {0}".format(sol))
    print("Algoritmo: {0}".format(algoritmo.__name__))
    if h:
        print("Heurística: {0}".format(h.__name__))
    else:
        pass
    print("Longitud de la solución: {0}. Nodos analizados: {1}".format(len(sol), p8p.analizados))


"""La siguiente heurística h3_ocho_puzzle se obtiene sumando a la heurística h2_ocho_puzzle una componente que 
cuantifica la "secuencialidad" en las casillas de un tablero, al recorrerlo en el sentido de las aguas del reloj 

¿Es h3 admisible? Comprobar cómo se comporta esta heurística cuando se usa en A*, 
con cada uno de los estados anteriores. Comentar los resultados."""


def h3_8_puzzle(estado):
    suc_ocho_puzzle = {0: 1, 1: 2, 2: 5, 3: 0, 4: 4, 5: 8, 6: 3, 7: 6, 8: 7}

    def secuencialidad_aux(estado, i):

        val = estado[i]
        if val == 0:
            return 0

        elif i == 4:
            return 1

        else:
            i_sig = suc_ocho_puzzle[i]
            val_sig = (val + 1 if val < 8 else 1)
            return 0 if val_sig == estado[i_sig] else 2

    def secuencialidad(estado):
        res = 0
        for i in range(8):
            res += secuencialidad_aux(estado, i)
        return res

    return h2_ocho_puzzle(estado) + 3 * secuencialidad(estado)
