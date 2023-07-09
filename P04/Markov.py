## PROCESOS DE DECISION DE MARKOV ##

import random

""" Supondremos que un Procesos de Decisión de Markov (MDP, por sus siglas en inglés) 
va a ser un objeto de la siguiente clase (o mejor dicho, de una subclase de la siguiente clase)."""


class MDP(object):
    """La clase genérica MDP tiene como métodos la función de recompensa R,
    la función A que da la lista de acciones aplicables a un estado, y la
    función T que implementa el modelo de transición. Para cada estado y
    acción aplicable al estado, la función T devuelve una lista de pares
    (ei,pi) que describe los posibles estados ei que se pueden obtener al
    plical la acción al estado, junto con la probabilidad pi de que esto
    ocurra. El constructor de la clase recibe la lista de estados posibles y
    el factor de descuento.

    En esta clase genérica, las funciones R, A y T aparecen sin definir. Un
    MDP concreto va a ser un objeto de una subclase de esta clase MDP, en la
    que se definirán de manera concreta estas tres funciones"""

    def __init__(self, estados, descuento):
        self.estados = estados
        self.descuento = descuento

    def R(self, estado):
        pass

    def A(self, estado):
        pass

    def T(self, estado, accion):
        pass


"""Se pide representar el problema como un proceso de decisión de Markov, definiendo una clase Rica_y_Conocida,
 subclase de la clase MDP genérica, cuyo constructor recibe como entrada únicamente el factor de descuento, 
 y en la que se definen de manera concreta los métodos R, A y T, según lo descrito. Para ello:

La recompensa la guardaremos en un diccionario con claves "RC", "RD", "PC" y "PD", 
donde "R" es Rica, "P" es pobre, "C" es conocida y "D" es desconocida. 

Los valor del diccionario son las recompensas asociadas.
Las acciones serán: "No publicidad" y "Gastar en publicidad"
La transición también será un diccionario donde las claves son tuplas (Estado, acción) 
y los valores son listas de pares (Nuevo_estado, probabilidad). Por ejemplo un par clave-valor del diccionario será 
("RC","No publicidad"):[("RC",0.5),("RD",0.5)]
Recordamos que el factor de descuento es 0.9, que es el que viene definido en el enunciado, 
además que la recompensa para ser rica es 10 y por ser pobre es 0.

También sabemmos que R es rica, P es pobre, C es conocida y D desconocida. Por tanto tenemos:

RC es Rica y Conocida
RD es Rica y Desconocida
PC es Pobre y Conocida
PD es pobre y Desconocida"""


class Rica_Y_Conocida(MDP):

    def __init__(self, factor_descuento=0.9):
        self.DiccionarioRecompensa = {"RC": 10, "RD": 10, "PC": 0, "PD": 0}
        self.DiccionarioTransicion = {
            ("RC", "No publicidad"): [("RC", 0.5), ("RD", 0.5)],
            ("RC", "Gastar en publicidad"): [("PC", 1)],
            ("RD", "No publicidad"): [("RD", 0.5), ("PD", 0.5)],
            ("RD", "Gastar en publicidad"): [("PD", 0.5), ("PC", 0.5)],
            ("PC", "No publicidad"): [("PD", 0.5), ("RC", 0.5)],
            ("PC", "Gastar en publicidad"): [("PC", 1)],
            ("PD", "No publicidad"): [("PD", 1)],
            ("PD", "Gastar en publicidad"): [("PD", 0.5), ("PC", 0.5)]
        }

        estados = ["RC", "RD", "PC", "PD"]
        super().__init__(estados, factor_descuento)

    def R(self, estado):
        return self.DiccionarioRecompensa[estado]

    def A(self, estado):
        return ["No publicidad", "Gastar en publicidad"]

    def T(self, estado, accion):
        return self.DiccionarioTransicion[(estado, accion)]


"""Ejercicio 2
En general, dado un MDP, representaremos una política para el mismo como un diccionario cuyas claves son los estados,
 y los valores las acciones. Una política representa una manera concreta de decidir en cada estado la acción 
 (de entre las aplicables a ese estado) que ha de aplicarse.

Dado un MDP, un estado de partida, y una política concreta, podemos generar (muestrear) una secuencia de estados 
por los que iríamos pasando si vamos aplicando las acciones que nos indica la política: 
dado un estado de la secuencia, aplicamos a ese estado la acción que indique la política, 
y obtenemos un estado siguiente de manera aleatoria,
pero siguiendo la distribución de probabilidad que indica el modelo de transición dado por el método T.

Se pide definir una función "genera_secuencia_estados(mdp,pi,e,n)" que devuelva una secuencia de estados de longitud n,
obtenida siguiendo el método anterior. Aquí mdp es objeto de la clase MDP, pi es una política, e un estado de partida 
y n la longitud de la secuencia. """


def muestreo(estado):
    valor_aleatorio = random.random()
    politica_actual = 0

    for accion, politica in estado:

        politica_actual += politica

        if politica_actual > valor_aleatorio:
            return politica_actual


def genera_secuencia_estados(mdp, pi, e, n):
    actual = e

    secuencia_generada = [actual]

    for _ in range(n - 1):
        estado_actual = muestreo(mdp.T(actual, pi[actual]))

        secuencia_generada.append(actual)

    return secuencia_generada


""" Dado un MDP y una secuencia de estados, valoramos dicha secuencia como la suma de las recompensas de los estados 
de la secuencias (cada una con el correspondiente descuento).
Se pide definir una función valora_secuencia(seq,mdp) que calcula esta valoración."""


def valora_secuencia(seq, mdp):
    return sum(mdp.R(e) * (mdp.descuento ** i) for i, e in enumerate(seq))


"""Dada una política pi, la valoración de un estado e respecto de esa política, V^{pi}(e),
 se define como la media esperada de las valoraciones de las secuencias que se pueden generar teniendo dicho estado 
 como estado de partida. Usando las funciones de los dos ejercicios anteriores, definir 
 una función "estima_valor(e,pi,mdp,m,n)" que realiza una estimación aproximada del valor V^{pi}(e), 
 para ello genera n secuencias de tamaño m, y calcula la media de sus valoraciones.

Ya que vamos a calcular la media como solución principal usaremos el sum(...)/n. 
Siendo n el número de secuencias, y siendo estas las que se van a recorrer valorándolas.

Para ello, como se comenta anteriormente usaremos la funcion de valora_secuencia(...) 
para valorar las secuencias n veces, como valor de entrada a la función le vamos a pasar secuencias que generaremos 
con la función genera_secuencia_estados(...) y pasándole el MDP como entrada.

En genera_secuencia_estados(...) tenemos al objeto mdp, a e que son los estados de la secuencia, 
pi que será la política usada y a m la longitud de los estados."""


def estima_valor(e, pi, mdp, m, n):
    return (sum(valora_secuencia(genera_secuencia_estados(mdp, pi, e, m), mdp) for _ in range(n))) / n


"""La función de valoración no se suele calcular mediante la técnica de muestreo vista en el ejercicio 4, 
sino como resultado de resolver un sistema de ecuaciones. Dicho sistema de ecuaciones se puede resolver 
de manera proximada de manera iterativa, tal como se explica en el tema.

Definir una función "valoración_respecto_política(pi,mdp, n)" que aplica dicho método iterativo 
(n iteraciones) para calcular la valoración V^{pi}. Dicha valoración debe devolverse como un diccionario que 
a cada estado e le asocia el valor "V^{pi}(e)" calculado.

Aplicar la función para calcular la valoración asociada a las dos políticas que se dan en el ejercicio anterior,
 y comparara los valores obtenidos con los obtenidos mediante muestreo."""


def valoracion_respecto_politica(pi, mdp, n):
    recompensa, transicion, descuento = mdp.R(), mdp.T(), mdp.descuento

    valoracion = {e: 0 for estado in mdp.estados}

    for _ in range(n):

        valoracion_copy = valoracion.copy()

        for estados in mdp.estados:
            valoracion[estados] = recompensa(estados) + descuento * (sum([pi * valoracion_copy[estados, pi]]))

    return valoracion


"""En el tema 3 se ha visto que la valoración de un estado se define como la mejor valoración que pueda tener el estado,
 respecto a todas las políticas posibles. Y la política óptima es aquella que en cada estado realiza la acción con 
 la mejor valoración esperada (entendiendo por valoración esperada la suma de las valoraciones de los estados 
 que podrían resultar al aplicar dicha acción, ponderadas por la probabilidad de que ocurra eso). De esta manera, 
 la valoración de un estado es la valoración que la política óptima asigna al estado.

Para calcular tanto la valoración de los estados, como la política óptima, se han visto dos algoritmos: 
iteración de valores e iteración de políticas. En este ejercicio se pide implementar el algoritmo de 
iteración de políticas. 
En concreto, se pide definir una función "iteración_de_políticas(mdp,k)" 
que implementa el algoritmo de iteración de políticas, y devuelve dos diccionarios, uno con la valoración de los estados
 y otro con la política óptima.

Comparar los resultados obtenidos con las políticas del ejercicio 5 y las valoraciones obtenidas.

Vamos a definir la función que nos devuelva la acción con la valoración máxima recorriendo 
todos los valores que haya en la secuencia de entrada"""


def secuencia_maxima(secuencia, funcion):
    max = float("-inf")

    valor_max = None

    for valor in secuencia:

        funcion_valor = funcion(valor)

        if funcion_valor > max:
            max = funcion_valor
            accion_max = valor

    return accion_max
