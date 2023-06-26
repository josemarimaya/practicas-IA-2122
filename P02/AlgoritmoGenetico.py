""" Vamos a tratar de resolver los problemas de Algoritmo Genetico sin usar los notebooks"""

# 1.- numpy para la representación matricial
import numpy as np

# 2.- random para poder tomar valores aleatorios
import random, math

# 3.- PIL e imageio para leer y escribir imágenes.
from PIL import Image
import imageio

# Para dibujar
import matplotlib as mpl
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
