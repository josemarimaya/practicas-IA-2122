import random
import math

from numba.core.types import abstract

""" La siguiente clase Problema_Busqueda_Local va a proporcionar un patrón general para representar problemas de 
    optimización a resolver mediante búsqueda local. Los problemas concretos serán subclases de esta clase, 
    obtenidos definiendo sus métodos de manera concreta.

    Nótese que además de los tres métodos anteriormente mencionados, incluimos un atributo "mejor" para definir 
    si se trata de un problema de minimización o de maximización. En concreto, "mejor" contendrá la función "menor que" 
    si se trata de minimizar, o la función "mayor que" si se trata de maximizar 
    (por defecto, el problema será de minimización)"""

""" Esta es la estructura genérica del problema de Búsqueda Local"""


class Problema_Busqueda_Local(object):
    """Clase abstracta para un problema de búsqueda local. Los problemas
    concretos habría que definirlos como subclases de esta clase,
    implementando genera_estado_inicial, genera_sucesor y valoración. Como
    atributo de dato, tendremos "mejor", que va a almacenar la función "menor
    que", o "mayor que" dependiendo de que se trate, respectivamente, de
    minimizar o maximizar."""

    def __init__(self, mejor=lambda x, y: x < y):
        self.mejor = mejor

    def genera_estado_inicial(self):
        """Genera, posiblemente con cierta componente aleatoria y heurística,
           un estado para empezar la búsqueda ."""
        abstract

    def genera_sucesor(self, estado):
        """ Devuelve un estado "sucesor" del que recibe como
            entrada. Usualmente, esta función tendrá cierta componente
            aleatoria y heurística."""
        abstract

    def valoracion(self, estado):
        """Devuelve la valoración de un estado. Es el valor a optimizar."""
        abstract


""" Implementar la clase Viajante_BL de problemas del viajante para ser resueltos mediante búsqueda local. 
    La clase debe ser subclase de Problema_Busqueda_Local y contener además dos atributos de datos adicionales: 
    uno con la lista de las ciudades y otro con una función distancia que se va a usar para calcular 
    la distancia entre cualesquiera dos ciudades 
    (estos dos datos se reciben como argumento por el constructor de la clase)."""

""" Tanto el método genera_estado_inicial como el método genera_sucesor se han de definir como se ha explicado en clase. 
    Es decir:

   - genera_estado_inicial construye, aleatoriamente, una permutación de las ciudades
   
   - genera_sucesor construye un circuito a partir de uno dado, 
    invirtiendo el subcircuito entre dos ciudades elegidas aleatoriamente."""


class Viajante_BL(Problema_Busqueda_Local):

    def __init__(self, ciudades, distancia):
        super().__init__()
        self.ciudades = ciudades
        self.distancia = distancia

    def genera_estado_inicial(self):
        ciudades_originales = list(self.ciudades)
        # Para generar un orden aleatorio y crear así una permutación usaremos random.shuffle()

        ciudades_permutadas = random.shuffle(ciudades_originales)

        return ciudades_permutadas

    """ Trabajamos con el estado que es el que contiene las ciudades que hay actualmente en el problema"""

    def genera_sucesor(self, estado):
        cantidad_ciudades = len(estado)

        ciudad_1 = random.choice(range(0, cantidad_ciudades))
        ciudad_2 = random.choice(range(0, cantidad_ciudades))

        # creamos el circuito a partir de invertir el estado con las dos ciudades elegidas aleatoriamente
        estado_resultado = estado[ciudad_1::-1] + estado[ciudad_2::-1]

        return estado_resultado

    def valoracion(self, estado):
        sum_circuito = 0
        # sumamos la distancia de las ciudades del estado
        for i in range(len(estado) - 1):
            sum_circuito = sum_circuito + self.distancia(estado[i], estado[i + 1])

        # por ultimo sumamos las distancias de los extremos ya que es un circuito los extremos están conectados
        sum_circuito = sum_circuito + self.distancia(estado[0], estado[-1])

        return sum_circuito


""" La función distancia_euc2D calcula la distancias entre dos ciudades a partir de sus coordenadas"""


def distancia_euc2D(c1, c2, coords):
    """ Función que recibe dos ciudades y devuelve la distancia entre ellas,
    calculada mediante distancia euclidea en el plano. El tercer argumento de
    la función contiene las coordenadas de todas las ciudades del problema (en
    foma de lista o de diccionario)"""
    coord_c1 = coords[c1]
    coord_c2 = coords[c2]
    return math.hypot(coord_c1[0] - coord_c2[0], coord_c1[1] - coord_c2[1])


andalucia = {"almeria": (409.5, 93),
             "cadiz": (63, 57),
             "cordoba": (198, 207),
             "granada": (309, 127.5),
             "huelva": (3, 139.5),
             "jaen": (295.5, 192),
             "malaga": (232.5, 75),
             "sevilla": (90, 153)}

# Para devolver las distancias tendremos en cuenta los values

distancia = andalucia.values()

print(distancia)

# Y para devolver las ciudades usaremos las claves

capitales = andalucia.keys()

print(capitales)

# Todo ellos para usar el problema del viajante con andalucía

viajante_andalucia = Viajante_BL(capitales,
                                 lambda x, y: distancia_euc2D(x, y, andalucia))

# Ahora generamos el estado inicial

circuito = viajante_andalucia.genera_estado_inicial()

print(circuito)

# Y un sucesor

# sucesor = viajante_andalucia.genera_sucesor(circuito)

# Implementación de enfriamiento simulado

"""Definir una función sorteo(p), que recibe una probabilidad p y 
devuelve aleatoriamente True ó False, de tal manera que la probabilidad de devolver True sea precisamente p."""


def sorteo(p):
    aleatorio = random.random()
    res = False
    if aleatorio < p:
        res = True
    return res


"""Definir una función aceptar_e_s(valor_candidata, valor_actual, T, mejor)
    que implementa el mecanismo de aceptación de nuevos estados dentro del algoritmo de enfriamiento simulado, donde:

    valor_candidata es la valoración del estado nuevo
    valor_actual es la valoración del estado actual
    T es la temperatura
    mejor es la función que se usa para comprobar si un valor es mejor qaue otro
    
    La función debe devolver True o False, dependiendo de si la candidata se acepta como nueva actual o no."""


# Definimos la funcion auxiliar de mejor

def mejor(v1, v2):
    return (v1 < v2)


def aceptar_e_s(valor_candidata, valor_actual, T, mejor):
    condicion_1 = mejor(valor_actual, valor_candidata)
    # La función de la temperatura en enfriamiento simulado = math.exp(-abs(valor_candidata-valor_actual)/T)
    condicion_2 = sorteo(math.exp(-abs(valor_candidata - valor_actual) / T))

    # Se tiene que cumplir alguna condicion para aceptar a la candidata
    return condicion_1 or condicion_2


## IMPLEMENTACIÓN DE ENFRIAMIENTO SIMULADO ##

"""Función que implementa el algoritmo de optimización mediante
        enfriamiento simulado. Recibe como entrada:
        - Un problema de búsqueda local (clase Problema_Busqueda_Local)
        - Una temperatura inicial
        - Un factor de descenso (para el programa de enfriamiento)
        - Un número total de enfriamientos 
        - Un número de iteraciones para cada temperatura"""


def enfriamiento_simulado(problema, t_inicial, factor_descenso, n_enfriamientos, n_iteraciones):
    actual = problema.genera_estado_inicial()

    valor_actual = problema.valoracion(actual)

    mejor = actual

    valor_mejor = valor_actual

    T = t_inicial

    for _ in range(n_enfriamientos):

        for _ in range(n_iteraciones):

            candidata = problema.genera_sucesor()
            valor_candidata = candidata.valoracion(candidata)

            if problema.mejor(valor_candidata, valor_actual):

                actual = candidata

                valor_actual = valor_candidata

                if problema.mejor(valor_actual, valor_mejor):
                    mejor = actual

                    valor_mejor = valor_actual

        T = T * factor_descenso

    return mejor, valor_mejor
