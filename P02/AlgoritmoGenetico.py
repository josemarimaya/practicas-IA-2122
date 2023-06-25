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
mpl.rcParams['figure.figsize'] = (15,10) # Para el tamaño de la image

""" Para empezar, tomamos la imagen que queremos aproximar desde un fichero y 
    lo guardamos como una imagen python (en este caso el fichero gioconda.jpg). 
    Para ello usamos la librería PIL para convertir la imagen en una imagen en escala de grises de 8-bits (256 valores). 
    Ver https://pillow.readthedocs.io/en/3.1.x/handbook/concepts.html#concept-modes"""

imagen_original = 'gioconda.jpg'
img = Image.open(imagen_original).convert('L')

plt.imshow(img,cmap='gray')

IM2ARRAY = np.array(img)

print(IM2ARRAY)

im2array_shape = IM2ARRAY.shape

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