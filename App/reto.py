"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad de Los Andes
 * 
 * Contribución de:
 *
 * Cristian Camilo Castellanos
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 """

"""
  Este módulo es una aplicación básica con un menú de opciones para cargar datos, contar elementos, y hacer búsquedas sobre una lista .
"""




import csv
import sys
import config as cf
from DataStructures import liststructure as lt
from Sorting import mergesort as sort
from time import process_time
from ADT import list as lt
from DataStructures import listiterator as it
def printMenu():
    """
    Imprime el menu de opciones
    """
    print("\nBienvenido")
    print("1- Cargar Datos")
    print("2- Ranking de peliculas")
    print("3- Conocer un director")
    print("4- Conocer un actor")
    print("5- Entender un genero")
    print("6- Crear ranking")
    print("0- Salir")


def compareRecordIds(recordA, recordB):
    if int(recordA['id']) == int(recordB['id']):
        return 0
    elif int(recordA['id']) > int(recordB['id']):
        return 1
    return - 1


def compFunc(elem1, elem2):
    if elem1 == elem2:
        return 0
    return -1


def loadCSVFile(file, cmpfunction):
    lst = lt.newList("ARRAY_LIST", cmpfunction)
    dialect = csv.excel()
    dialect.delimiter = ";"
    try:
        with open(file, encoding="utf-8") as csvfile:
            row = csv.DictReader(csvfile, dialect=dialect)
            for elemento in row:
                lt.addLast(lst, elemento)
    except:
        print("Hubo un error con la carga del archivo")
    return lst


def loadMovies():
    lst = loadCSVFile(cf.data_dir +
                      'SmallMoviesDetailsCleaned.csv', compareRecordIds)
    print("Datos cargados, " + str(lt.size(lst)) + " elementos cargados")
    return lst


def loadCasting():
    lst = loadCSVFile(cf.data_dir +
                      'MoviesCastingRaw-small.csv', compareRecordIds)
    print("Datos cargados, " + str(lt.size(lst)) + " elementos cargados")
    return lst


# Req 2 Crear Ranking de películas
def req2(x, criteria, sentido, lst):
    """
    Retorna una lista con cierta cantidad de elementos ordenados por el criterio
    """
    res = "THE " + str(x) + " "
    if criteria == 0 and sentido == 0:
        sort.mergesort(lst, lessV)
        res = res + "WORST VOTE"
    elif criteria == 0 and sentido == 1:
        sort.mergesort(lst, greaterV)
        res = res + "BEST VOTE"
    elif criteria == 1 and sentido == 0:
        sort.mergesort(lst, lessA)
        res = res + "WORST AVERAGE"
    else:
        sort.mergesort(lst, greaterA)
        res = res + "BEST AVERAGE"

    return lt.subList(lst, 1, x), res + " Movies \n"


def lessV(element1, element2):
    if float(element1['vote_count']) < float(element2['vote_count']):
        return True
    return False


def greaterV(element1, element2):
    if float(element1['vote_count']) > float(element2['vote_count']):
        return True
    return False


def lessA(element1, element2):
    if float(element1['vote_average']) < float(element2['vote_average']):
        return True
    return False


def greaterA(element1, element2):
    if float(element1['vote_average']) > float(element2['vote_average']):
        return True
    return False


# Req 3 Conocer a un director
def req3(criteria, lstCast, lstMov):
    """
    Retorna la cantidad de elementos que cumplen con un criterio para una columna dada
    """
    # Guardar los id de las peliculas del director
    idMov = lt.newList("ARRAY_LIST", compFunc)

    for i in range(lt.size(lstCast)):
        director = lt.getElement(lstCast, i)
        if criteria == director['director_name']:
            lt.addLast(idMov, director['id'])

    pelicula = lt.newList("ARRAY_LIST", compFunc)
    numPel = 0
    calProm = 0.0

    for i in range(lt.size(lstMov)):
        id = lt.getElement(lstMov, i)['id']
        # Revisamos si el id de la pelicula actual está en el id de peliculas de nuestro director
        if lt.isPresent(idMov, id) > 0:
            lt.addLast(pelicula, lt.getElement(lstMov, i)['title'])
            numPel += 1
            calProm += float(lt.getElement(lstMov, i)['vote_average'])

        if numPel == lt.size(idMov):
            break

    prom = 0.0

    if numPel != 0:
        prom = calProm/numPel

    res = "El director " + str(criteria) + " posee un total de: " + str(numPel) + \
        " peliculas, las cuales tienen una calificación promedio de: " + \
        str(prom) + "\n"
    return pelicula, res


# Req 4 Conocer a un actor
def req4(criteria, lstCast, lstMov):
    """
    Retorna la cantidad de elementos que cumplen con un criterio para una columna dada
    """
    # Guardar los id de las peliculas del actor
    idMov = lt.newList("ARRAY_LIST", compFunc)
    # Guardar el nombre del director y el numero de las colaboraciones
    myDirectorDic = {}

    for i in range(lt.size(lstCast)):
        director = lt.getElement(lstCast, i)
        if criteria == director['actor1_name'] or criteria == director['actor2_name'] or criteria == director['actor3_name'] or criteria == director['actor4_name'] or criteria == director['actor5_name']:
            lt.addLast(idMov, director['id'])
            dir_name = director['director_name']
            # revisa si la llave existe
            if dir_name in myDirectorDic:
                myDirectorDic[dir_name] = int(myDirectorDic[dir_name]) + 1
            else:
                myDirectorDic[dir_name] = 1

    pelicula = lt.newList("ARRAY_LIST", compFunc)
    numPel = 0
    calProm = 0.0

    for i in range(lt.size(lstMov)):
        id = lt.getElement(lstMov, i)['id']
        if lt.isPresent(idMov, id) > 0:
            lt.addLast(pelicula, lt.getElement(lstMov, i)['title'])
            numPel += 1
            calProm += float(lt.getElement(lstMov, i)['vote_average'])

        if numPel == lt.size(idMov):
            break

    prom = 0.0

    if numPel != 0:
        prom = calProm / numPel

    # Busca el director con mayores colaboraciones
    actual = 0
    name = ""
    for k, v in myDirectorDic.items():
        if actual < int(v):
            actual = int(v)
            name = str(k)

    res = "Para el actor " + str(criteria) + "\nEl director con el cual más a trabajado es: " + str(
        name) + "\nSu peliculas tienen un calficación promedio de: " + str(prom) + "\nEl numero de peliculas del actor es: " + str(numPel) + "\n"
    return pelicula, res


# Req 5 Entender un género cinematográfico
def req5(criteria, lstMov):
    pelicula = lt.newList("ARRAY_LIST")
    numPel = 0
    voteProm = 0.0

    for i in range(lt.size(lstMov)):
        if lt.getElement(lstMov, i)['genres'].find(criteria) != -1:
            lt.addLast(pelicula, lt.getElement(lstMov, i)['title'])
            numPel += 1
            voteProm += float(lt.getElement(lstMov, i)['vote_count'])

    prom = 0.0

    if numPel != 0:
        prom = voteProm/numPel

    res = "La cantidad de peliculas del genero " + \
        str(criteria) + " es de: " + str(numPel) + \
        " con un promedio de cantidad de votos de: " + str(prom) + "\n"
    return pelicula, res


# Req 6 Crear Ranking del género
def req6(x, criteria, sentido, lstMov, genre):

    pelicula = lt.newList("ARRAY_LIST")
    numPel = 0
    voteProm = 0.0
    voteAverage = 0.0

    for i in range(lt.size(lstMov)):
        if lt.getElement(lstMov, i)['genres'].find(genre) != -1:
            lt.addLast(pelicula, lt.getElement(lstMov, i))

    res = "THE " + str(x) + " "
    if criteria == 0 and sentido == 0:
        sort.mergesort(pelicula, lessV)
        res = res + "WORST VOTE "
    elif criteria == 0 and sentido == 1:
        sort.mergesort(pelicula, greaterV)
        res = res + "BEST VOTE "
    elif criteria == 1 and sentido == 0:
        sort.mergesort(pelicula, lessA)
        res = res + "WORST AVERAGE "
    else:
        sort.mergesort(pelicula, greaterA)
        res = res + "BEST AVERAGE "

    sub = lt.subList(pelicula, 1, x)

    for i in range(lt.size(sub)):
        numPel += 1
        voteProm += float(lt.getElement(sub, i)['vote_count'])
        voteAverage += float(lt.getElement(sub, i)['vote_average'])

    prom1 = 0.0
    prom2 = 0.0

    if numPel != 0:
        prom1 = voteProm/numPel
        prom2 = voteAverage/numPel

    res = res + genre + " Movies\n Promedio de votos: " + \
        str(prom1) + " Votación promedio: " + str(prom2) + "\n"
    return sub, res


def main():
    """
    Método principal del programa, se encarga de manejar todos los metodos adicionales creados

    Instancia una lista vacia en la cual se guardarán los datos cargados desde el archivo
    Args: None
    Return: None 
    """

    # se require usar lista definida
    lstcasting = lt.newList("ARRAY_LIST")
    # se require usar lista definida
    lstmovies = lt.newList("ARRAY_LIST")

    while True:
        printMenu()  # imprimir el menu de opciones en consola

        # leer opción ingresada
        inputs = input('Seleccione una opción para continuar\n')
        if len(inputs) > 0:

            if int(inputs[0]) == 1:  # opcion 1
                lstmovies = loadMovies()
                lstcasting = loadCasting()
            elif int(inputs[0]) == 2:  # opcion 2
                # obtener la longitud de la lista
                if lstmovies['size'] == 0:
                    print("La lista esta vacía")
                else:
                    x = int(input(
                        'Ingrese la cantidad de elementos que desea\n'))
                    if x < 10:
                        print("Debe ser mayor a 10")
                    else:
                        criteria = int(input(
                            'Ingrese 0 para ordenar por número de votos o 1 para ordenar por votación promedio\n')[0])

                        if criteria != 0 and criteria != 1:
                            print("La opción ingresa no es valida")
                        else:
                            sentido = int(input(
                                'Ingrese 0 para hacer orden ascendente o 1 para descendente\n')[0])

                            if sentido != 0 and sentido != 1:
                                print("La opción ingresa no es valida")
                            else:
                                pel, res = req2(
                                    x, criteria, sentido, lstmovies
                                )
                                print(
                                    res, pel)

            elif int(inputs[0]) == 3:  # opcion 3
                criteria = input('Ingrese el nombre del director a conocer\n')
                mov, res = req3(
                    criteria, lstcasting, lstmovies)
                print(res, mov)

            elif int(inputs[0]) == 4:  # opcion 4
                criteria = input('Ingrese el nombre del actor a conocer\n')
                pelicula, res = req4(
                    criteria, lstcasting, lstmovies)
                print(res, pelicula)

            elif int(inputs[0]) == 5:  # opcion 5
                criteria = input('Ingrese el nombre del genero\n')
                mov, res = req5(
                    criteria, lstmovies)
                print(res, mov)

            elif int(inputs[0]) == 6:  # opcion 6
                if lstmovies['size'] == 0:
                    print("La lista esta vacía")
                else:
                    x = int(input(
                        'Ingrese la cantidad de elementos que desea\n'))
                    if x < 10:
                        print("Debe ser mayor a 10")
                    else:
                        criteria = int(input(
                            'Ingrese 0 para ordenar por número de votos o 1 para ordenar por votación promedio\n')[0])

                        if criteria != 0 and criteria != 1:
                            print("La opción ingresa no es valida")
                        else:
                            sentido = int(input(
                                'Ingrese 0 para hacer orden ascendente o 1 para descendente\n')[0])

                            if sentido != 0 and sentido != 1:
                                print("La opción ingresa no es valida")
                            else:
                                genero = input(
                                    'Ingrese el genero deseado\n')
                                pel, res = req6(
                                    x, criteria, sentido, lstmovies, genero
                                )
                                print(res, pel)

            elif int(inputs[0]) == 0:  # opcion 0, salir
                sys.exit(0)


if __name__ == "__main__":
    main()
