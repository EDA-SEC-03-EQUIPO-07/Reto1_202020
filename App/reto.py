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
                      'SmallMoviesDetailsCleaned.csv', compareRecordIds) #cambiar a database large
    print("Datos cargados, " + str(lt.size(lst)) + " elementos cargados")
    return lst


def loadCasting():
    lst = loadCSVFile(cf.data_dir +
                      'MoviesCastingRaw-small.csv', compareRecordIds) #cambiar a database large
    print("Datos cargados, " + str(lt.size(lst)) + " elementos cargados")
    return lst


#Requerimiento 2
def makeMoviesRanking(lenght, criteria, order, lst):
    t1_start = process_time()
    if criteria == 0 and order == 0:
        sort.mergesort(lst, lessV)
    elif criteria == 0 and order == 1:
        sort.mergesort(lst, greaterV)
    elif criteria == 1 and order == 0:
        sort.mergesort(lst, lessA)
    else:
        sort.mergesort(lst, greaterA)
    t1_stop = process_time()
    print("Tiempo de ejecución",t1_stop-t1_start,"segundos")
    return lt.subList(lst, 1, lenght)

def lessV(element1, element2):
    if float(element1["vote_count"]) < float(element2["vote_count"]):
        return True
    return False

def greaterV(element1, element2):
    if float(element1["vote_count"]) > float(element2["vote_count"]):
        return True
    return False

def lessA(element1, element2):
    if float(element1["vote_average"]) < float(element2["vote_average"]):
        return True
    return False

def greaterA(element1, element2):
    if float(element1["vote_average"]) > float(element2["vote_average"]):
        return True
    return False


#Requerimiento 3
def filterByDirector(criteria, lst1, lst2):
    t1_start = process_time()
    idsByDirector = lt.newList("ARRAY_LIST", compFunc)
    for i in range(lt.size(lst1)):
        director = lt.getElement(lst1, i)
        if criteria.lower() == director["director_name"].lower():
            lt.addLast(idsByDirector, director['id'])

    moviesByDirector = lt.newList("ARRAY_LIST", compFunc)
    lenghtSumVoteAverage = 0
    sumVoteAverage = 0
    average = 0
    averageRounded = 0

    for i in range(lt.size(lst2)):
        id = lt.getElement(lst2, i)['id']
        if lt.isPresent(idsByDirector, id) > 0:
            lt.addLast(moviesByDirector, lt.getElement(lst2, i)["title"])
            lenghtSumVoteAverage += 1
            sumVoteAverage += float(lt.getElement(lst2, i)["vote_average"])
        if lenghtSumVoteAverage == lt.size(idsByDirector):
            break

    if lenghtSumVoteAverage != 0:
        averageRounded = sumVoteAverage/lenghtSumVoteAverage
    else:
        averageRounded = 0

    t1_stop = process_time()
    print("Tiempo de ejecución",t1_stop-t1_start,"segundos")
    return moviesByDirector, lenghtSumVoteAverage, averageRounded


#Requerimiento 4
def filterByActor(criteria, lst1, lst2):
    pass


#Requerimiento 5
def filmGenre(criteria, lst1):
    t1_start = process_time()
    listMoviesByGenre = lt.newList("ARRAY_LIST")
    lengthSumVoteAverage = 0
    sumVoteAverage = 0
    average = 0
    averageRounded = 0

    for i in range(lt.size(lst1)):
        if lt.getElement(lst1, i)["genres"].find(criteria) != -1:
            lt.addLast(listMoviesByGenre, lt.getElement(lst1, i)["title"])
            lengthSumVoteAverage += 1
            sumVoteAverage += float(lt.getElement(lst1, i)["vote_count"])

    if lengthSumVoteAverage != 0:
        average = sumVoteAverage/lengthSumVoteAverage
        averageRounded = round(average, 3)
    else:
        averageRounded = 0
    
    t1_stop = process_time()
    print("Tiempo de ejecución",t1_stop-t1_start,"segundos")
    return listMoviesByGenre, lengthSumVoteAverage, averageRounded


def main():
    """
    Método principal del programa, se encarga de manejar todos los metodos adicionales creados

    Instancia una lista vacia en la cual se guardarán los datos cargados desde el archivo
    Args: None
    Return: None 
    """
    lstcasting = lt.newList("ARRAY_LIST") #instanciar un array vacío
    lstmovies = lt.newList("ARRAY_LIST") #instanciar un array vacío
    while True:
        printMenu()  #imprimir el menu de opciones en consola
        inputs = input("Seleccione una opción para continuar\n")
        if len(inputs) > 0:
            if int(inputs[0]) == 1:  #opcion 1
                lstmovies = loadMovies()
                lstcasting = loadCasting()
            elif int(inputs[0]) == 2:  #opcion 2
                if lstmovies["size"] == 0:
                    print("La lista esta vacía")
                else:
                    lenght = int(input("Ingrese la cantidad de elementos que desea\n"))
                    if lenght < 10:
                        print("Debe ser mayor a 10")
                    else:
                        criteria = int(input('Ingrese:\n 0: ordena por número de votos\n 1: ordenar por votación promedio\n')[0])
                        if criteria != 0 and criteria != 1:
                            print("La opción ingresa no es valida")
                        else:
                            order = int(input("Ingrese:\n 0: orden ascendente\n 1: orden descendente\n")[0])
                            if order != 0 and order != 1:
                                print("La opción ingresa no es valida")
                            else:
                                ranking = makeMoviesRanking(lenght, criteria, order, lstmovies)
                                print(ranking)

            elif int(inputs[0]) == 3:  #opcion 3
                directorName = input('Ingrese el nombre del director a conocer\n')
                moviesDirector = filterByDirector(directorName, lstcasting, lstmovies)
                print("El director",directorName,"tiene un total de",moviesDirector[1],"peliculas con una calificación promedio de",moviesDirector[1])
                print("Las peliculas del director",directorName,"son: ")
                print(moviesDirector[0])

            elif int(inputs[0]) == 4:  #opcion 4
                pass

            elif int(inputs[0]) == 5:  #opcion 5
                genre = input('Ingrese el nombre del genero\n')
                filmByGenre = filmGenre(genre, lstmovies)
                print("La cantidad de peliculas para el género",genre,"es de",filmByGenre[1],"con un promedio de votos de",filmByGenre[2])
                print("La lista de peliculas para el género",genre,"es: ")
                print(filmByGenre[0])

            elif int(inputs[0]) == 6:  #opcion 6
                pass

            elif int(inputs[0]) == 0:  #opcion 0, salir
                sys.exit(0)

if __name__ == "__main__":
    main()
