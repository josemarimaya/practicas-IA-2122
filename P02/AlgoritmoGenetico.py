""" Vamos a tratar de resolver los problemas de Algoritmo Genetico sin usar los notebooks"""

# 2.- random para poder tomar valores aleatorios
import random

import imageio
# Para dibujar
import matplotlib as mpl
# 1.- numpy para la representación matricial
import numpy as np
# 3.- PIL e imageio para leer y escribir imágenes.
from PIL import Image
from matplotlib import pyplot as plt

mpl.rcParams['figure.figsize'] = (15, 10)  # Para el tamaño de la image

""" Para empezar, tomamos la imagen que queremos aproximar desde un fichero y 
    lo guardamos como una imagen python (en este caso el fichero gioconda.jpg). 
    Para ello usamos la librería PIL para convertir la imagen en una imagen en escala de grises de 8-bits (256 valores). 
    Ver https://pillow.readthedocs.io/en/3.1.x/handbook/concepts.html#concept-modes"""

imagen_original = 'gioconda.jpg'
img = Image.open(imagen_original).convert('L')

plt.imshow(img, cmap='gray')

IM2ARRAY = np.array(img)

print(IM2ARRAY)

im2array_shape = IM2ARRAY.shape

## DEFINICIÓN DE CONSTANTES ##

""" Ahora empezamos con el planteamientos del propio problema de Algoritmo genérico"""

# Número de genes que conforman un individuo
NUMERO_DE_GENES = 150

# Tamaño de la población
TAMANO_POB = 500

# Participantes en un torneo
NUM_PARTICIPANTES = 50

# Probabilidad de mutación
PROB_MUTACION = 0.1

# Proporción de individuos que van a ser padres
PROP_CRUCES = 0.5

# Número de iteraciones
ITERACIONES = 10001

# Paso de impresión. Crearemos la imagen correspondiente al mejor individuo después de PASO_IMP iteraciones
PASO_IMP = 100

## GENERACION DE GENES ##

""" Define la función genera_gen() que a partir de la variable im2array_shape devuelva una tupla (x,y,dx,dy,c). 
    Una vez fijado el extremo (x,y) dentro del lienzo, debemos tener en cuenta 
    que el rectángulo esté dentro del lienzo y que el color esté en el rango 0-255."""


def genera_gen():
    """ No podemos trabajar directamente con im2array_shape ya que nos lo lee como un string, por lo que lo guardamos
        en una variable que luego tomará un valor aleatorio x,y para trabajar con ellos como extremos"""

    size_x, size_y = im2array_shape
    x = random.randrange(size_x)
    y = random.randrange(size_y)

    """ Como dx y dy son los lados del cuadrado de la imagen es importante restarlos para ver en que parte
        de la imagen nos encontramos para luego ver donde empieza nuestro gen en dx,dy"""
    dif_x = size_x - x
    dif_y = size_y - y

    dx = random.randrange(dif_x)
    dy = random.randrange(dif_y)

    # Representación de un color aleatorio en la escala de grises
    c = random.randrange(256)

    res = (x, y, dx, dy, c)
    return res


genera_gen()

print(genera_gen())

## GENERACIÓN DE INDIVIDUO ##

""" Define genera_individuo() que devuelva una tupla con tantos genes como determine el parámetro NUMERO_DE_GENES"""

""" Lo que hemos hecho ha sido hacer un bucle hasta numero de genes en el que añadimos un gen en cada iteracion.
    Los genes se añaden a una lista que finalmente se convierten en una tupla"""


def genera_individuo():
    ls = []
    for _ in range(NUMERO_DE_GENES):
        ls.append(genera_gen())
    return tuple(ls)


# Otra opción de genera_individuo()

def genera_individuo_prof():
    # Creamos una tupla con los valores que habrá dentro de la función
    return tuple(
        # Creamos tantos genes como el límite de NUMERO_DE_GENES nos ponga
        genera_gen() for _ in range(NUMERO_DE_GENES)
    )


# Vamos a generar un individuo

individuo = genera_individuo()

individuo_2 = genera_individuo()

print(individuo)

## DECODIFICA ##

# A este individuo le pasaremos una función decodifica

""" Cada gen representa un rectángulo dentro del lienzo y un individuo es una sucesión de genes. 
    Para poder interpretar ese individuo como una imagen, primero generamos una matriz (array) a partir de ese conjunto de genes. 
    En este caso, las posiciones que no están ocupadas por ningún cuadrado las interpretamos como blanco (valor 255) 
    y en el resto de la posiciones se sumará la intensidad de los rectángulos que las ocupan. 
    La función decodifica crea una matriz con la intensidad de gris de cada píxel a partir de un individuo."""


def decodifica(individuo):
    array_salida = np.zeros(im2array_shape, dtype='uint32')
    # A los cuadrados vacíos le damos la escala de grises 255
    array_cuadrado_vacio = np.full(im2array_shape, 255, dtype='uint32')
    # Vamos iterando por el individuo cada tupla que forma el gen
    for (x, y, dx, dy, c) in individuo:
        # Añadimos a la escala de grises el color del gen que estamos analizando
        array_salida[x:x + dx, y: y + dy] += 255 - c
    minimo = np.minimum(array_salida, array_cuadrado_vacio)
    resta = 255 - minimo
    return resta


matriz_individuo = decodifica(individuo)
print(matriz_individuo)

## POBLACIÓN ##

"""Para poder lanzar el algoritmo genético, en primer lugar definimos una función 
    que nos permita crear una población inicial de individuos.
    
    Define una función poblacion_inicial() que devuelva una lista con tantos individuos 
    como determine la variable TAMANO_POB"""


def poblacion_inicial():
    res = []
    for _ in range(TAMANO_POB):
        res.append(genera_individuo())
    return res


pob = poblacion_inicial()

print(pob)

## FITNESS ##

"""Para poder r los mejores inidividuos de la población, necesitamos definir una función fitness.
    En este caso la función fitness se define como la suma de las diferencias (en valor absoluto) pixel a pixel 
    entre la matriz que representa el individuo y la matriz que representa la imagen original."""


def fitness(individuo):
    # tenemos que sumar los valores de la diferencia entre la matriz decodificada (y generada), frente a  la original
    return np.sum(np.absolute(decodifica(individuo) - IM2ARRAY))


# print(fitness(matriz_individuo))

## SELECCION POR TORNEO ##

"""Define la función selecciona_uno_por_torneo(poblacion,dic) 
    que tome como entrada una población de individuos y un diccionario de pares individuo:fitness 
    y devuelva una tupla (seleccionado,nuevo_dic) donde seleccionado sea un individuo 
    de la población seleccionado por torneo con NUM_PARTICIPANTES como el número de participantes en cada torneo 
    y nuevo_dic sea el diccionario dic al que se le han añadido los pares 
    individuo:fitness que se hayan calculado en la búsqueda de seleccionado."""


def selecciona_uno_por_torneo(poblacion, dic):
    # valor mínimo de tipo float
    actual = 0
    minimo = float('inf')
    for _ in range(NUM_PARTICIPANTES):

        participante = random.choice(poblacion)

        fitness_participante = ()

        if participante in dic:
            fitness_participante = dic[participante]
        else:
            fitness_participante = fitness(participante)

            dic[participante] = fitness_participante

            if fitness_participante < minimo:
                actual = participante

                minimo = fitness_participante

    return actual, dic


# Solución que funciona y que seguiremos usando...
def selecciona_uno_por_torneo_2(poblacion, dic):
    # Sacamos un valor infinito para usarlo como referencia el que se le pase
    minimo = float('inf')
    # Bucle limitado al número de participantes que van a ser la poblacion del cromosoma
    for _ in range(NUM_PARTICIPANTES):
        # Elegimos un indice con valor aleatorio según la población que haya como parámetro de entrada
        ind = random.choice(poblacion)
        # Una vez que vemos que el índice está en el diccionario de entrada ...
        if ind in dic:
            # ... guardamos el valor del índice como fitness índice que ya estaría previamente calculado
            f_ind = dic[ind]
        # Si el índice no está en el diccionario de entrada
        else:
            # Usamos la variable f_ind para guardar el índice del fitness
            f_ind = fitness(ind)
            # Indicamos que el valor del diccionario que apunta al índice el el fitness del índice
            dic[ind] = f_ind
            # Si el fitness del índice es menor que el mínimo actual...
            if f_ind < minimo:
                # El índice pasa a ser el fitness actual guardado en la variable actual ...
                actual = ind
                # Así cómo el mínimo pasa a ser el fitness del índice que hay ahora mismo en este individuo de la población
                minimo = f_ind
    # La tupla se va a generar automáticamente una vez le pasemos los parámetros
    return actual, dic


print(selecciona_uno_por_torneo_2(poblacion_inicial(), {}))

""" Define la función seleccion_por_torneo(poblacion,num_seleccionados,dic) que además de la población 
    y el diccionario del ejercicio anterior tomemos el número de individuos que queremos seleccionar.
    La salida debe ser una tupla (seleccion,nuevo_dic) donde nuevo_dic es el diccionario actualizado 
    y selecciona una lista de individuos seleccionados. """


def seleccion_por_torneo(poblacion, num_seleccionados, dic):
    seleccion = []
    for _ in range(num_seleccionados):
        sel, nuevo_dic = selecciona_uno_por_torneo_2(poblacion, dic)

        seleccion.append(sel)
        dic = nuevo_dic
    return seleccion, dic


# 4 es el numero de seleccionados que queremos
# print(poblacion_inicial(), 4, {})

## CRUCE ##

""" Define la función cruza(i1,i2) que tome dos individuos y 
    devuelva una lista con los dos hijos obtenidos mediante la técnica de cruce en un punto"""


def cruza(individuo_1, individuo_2):
    punto_cruce = random.randrange(1, NUMERO_DE_GENES - 1)

    individuo_cruzado_1 = individuo_1[punto_cruce:] + individuo_2[:punto_cruce]

    individuo_cruzado_2 = individuo_1[:punto_cruce] + individuo_2[punto_cruce:]

    res = [individuo_cruzado_1, individuo_cruzado_2]

    return res


# Cruce de padres

def cruza_padres(padres):
    hijos = []
    """Este for con 3 valores (x,y,z) indica que x es el valor de inicio del bucle, es decir i=0, que y es el límite o cortocircuito del bucle
        y z es el valor incremental del valor iterador i. Sería como un for extendido en java
        for(i=0;i<hijos().size();i+2)

        Todo ello, porque nos dice que los hijos lo crean un PAR de padres, con lo cual se escogen los padres de 2 en 2 pero sin repetirse"""
    for i in range(0, len(padres), 2):
        hijos.extend(cruza(*padres[i:i + 2]))
        """Para empezar tenemos que *function hace que saquemos los individuos de la lista según lo que marquemos como límite
            En el caso de nuestro problema como ya hemos marcado vamos por pares, por ello vamos de padres[i:i+2] ya que 
            el intervalo para escoger los valores es [i, i+2) por la definición de array en python"""

    return hijos


# print(cruza(individuo, individuo_2))


## MUTACION ##

# Mutacion de individuo

""" Define la función muta(ind) que reciba como entrada un individuo ind y que, 
    con una probabilidad PROB_MUTACION cambie uno de sus genes por otro gen aleatorio."""


def muta(individuo_mutante):
    mutar = random.random() < PROB_MUTACION
    if mutar:
        # Mutamos un individuo...
        i = random.randrange(NUMERO_DE_GENES)
        # añadiendo un gen al azar
        return individuo_mutante[i] + genera_gen() + individuo_mutante[i + 1:]
    else:
        return individuo_mutante


# Mutacion de poblacion

""" Define una función muta_individuos(poblacion) que reciba como entrada a lista de individuos poblacion 
    y aplique la función muta a cada uno de los individuos"""


def muta_individuos(poblacion_mutante):
    res = []
    for individuo in poblacion_mutante:
        mutante = muta(individuo)
        res.append(mutante)

    return res


"""Define una función nueva_generacion(poblacion,n_padres,n_directos,dic) que reciba como entrada:

    poblacion es una población de individuos
    n_padres es un número que determina cuántos individuos seleccionamos por torneo para ser padres
    n_directos es un número que determina cuántos individuos seleccionamos por torneo para 
    pasar directamente a la siguiente generación.
    dic es un diccionario de pares individuo:fitness
    
    La función debe seleccionar un conjunto de individuos para ser padres y otro para pasar directamente 
    a la siguiente generación y a partir de los padres se debe genera un conjunto de hijos por cruce. 
    La función debe devolver una tupla (nuevo_dic,nueva_pob) donde nueva_pob es una lista de individuos formada por 
    los individuos que han pasado directamente a la siguiente generación más el resultado 
    de aplicar la función de mutación a los hijos."""


def nueva_generacion(poblacion, n_padres, n_directos, dic):
    # Sacamos los padres que usaremos para cruzar la siguiente generacion y el fitness que usaremos para la generacion directa
    padres, fitness_torneo_1 = seleccion_por_torneo(poblacion, n_padres, dic)
    # Cruzamos los padres para tener unos hijos mutados con cruce
    generacion_cruce = cruza_padres(padres)
    # Generamos la generación que pasará directa por torneo usando el fitness del primer torneo
    generacion_directa, fitness_torneo_2 = seleccion_por_torneo(poblacion, n_directos, fitness_torneo_1)
    # Creamos la nueva población
    nueva_pob = generacion_directa + muta_individuos(generacion_cruce)
    # Creamos la variables nuevo_dic únicamente para seguir la nomenclatura
    nuevo_dic = fitness_torneo_2
    return nuevo_dic, nueva_pob


def algoritmo_genetico():
    poblacion = poblacion_inicial()
    dic = {}
    n_padres = round(TAMANO_POB * PROP_CRUCES)
    n_padres = (n_padres if n_padres % 2 == 0 else n_padres - 1)
    n_directos = TAMANO_POB - n_padres
    mejores = []
    for counter in range(ITERACIONES):
        if counter % PASO_IMP == 0:
            print(counter)
            nuevo_dic = {}
            actual = 'inicial'
            min = float('inf')
            for ind in poblacion:
                f_ind = fitness(ind)
                nuevo_dic[ind] = f_ind
                if f_ind < min:
                    actual = ind
                    min = f_ind
            img_mejor = decodifica(actual).astype('uint8')
            imageio.imwrite('ga_{:>08}.jpg'.format(counter // PASO_IMP), img_mejor)
            mejores.append(min)
            dic, poblacion = nueva_generacion(poblacion, n_padres, n_directos, dic)
        else:
            dic, poblacion = nueva_generacion(poblacion, n_padres, n_directos, dic)
            print('.', end='')
    return mejores


sal_ag = algoritmo_genetico()
