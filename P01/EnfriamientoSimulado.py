import random
import math

""" La siguiente clase Problema_Busqueda_Local va a proporcionar un patrón general para representar problemas de 
    optimización a resolver mediante búsqueda local. Los problemas concretos serán subclases de esta clase, 
    obtenidos definiendo sus métodos de manera concreta.

    Nótese que además de los tres métodos anteriormente mencionados, incluimos un atributo "mejor" para definir 
    si se trata de un problema de minimización o de maximización. En concreto, "mejor" contendrá la función "menor que" 
    si se trata de minimizar, o la función "mayor que" si se trata de maximizar 
    (por defecto, el problema será de minimización)"""


""" Tanto el método genera_estado_inicial como el método genera_sucesor se han de definir como se ha explicado en clase. 
    Es decir:

    genera_estado_inicial construye, aleatoriamente, una permutación de las ciudades
    genera_sucesor construye un circuito a partir de uno dado, 
    invirtiendo el subcircuito entre dos ciudades elegidas aleatoriamente."""