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




from Sorting import mergesort as mer
import config as cf
import sys
import csv
from ADT import list as lt
from DataStructures import listiterator as it
from DataStructures import liststructure as lt
from time import process_time
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
    return -1


def loadCSVFile(file, cmpfunction):
    lst = lt.newList("ARRAY_LIST", cmpfunction)
    dialect = csv.excel()
    dialect.delimiter = ";"
    try:
        with open(cf.data_dir + file, encoding="utf-8") as csvfile:
            row = csv.DictReader(csvfile, dialect=dialect)
            for elemento in row:
                lt.addLast(lst, elemento)
    except:
        print("Hubo un error con la carga del archivo")
    return lst

# "C:\\Users\\home\\Desktop\\LABORATORIOS\\Reto1_202020_template\\Data\\SmallMoviesDetailsCleaned.csv"
# "C:\\Users\\home\\Desktop\\LABORATORIOS\\Reto1_202020_template\\Data\\MoviesCastingRaw-small.csv"


def loadMovies():
    lst = loadCSVFile(
        "SmallMoviesDetailsCleaned.csv", compareRecordIds)
    print("Datos cargados, " + str(lt.size(lst)) + " elementos cargados")
    return lst


def loadCasting():
    lst = loadCSVFile(
        "MoviesCastingRaw-small.csv", compareRecordIds)
    print("Datos cargados, " + str(lt.size(lst)) + " elementos cargados")
    return lst


def ActorInformation(actor_name, lst_casting, lst_movies):
    directores = list(lt.newList("ARRAY_LIST"))
    list_id = lt.newList("ARRAY_LIST")
    #actores_name = lt.newList("ARRAY_LIST")
    peliculas = 0
    for posicion in range(lt.size(lst_casting)):
        actor = lt.getElement(lst_casting, posicion)
        if actor["actor1_name"].lower() == actor_name.lower() or actor["actor2_name"].lower() == actor_name.lower() or actor["actor3_name"].lower() == actor_name.lower() or actor["actor4_name"].lower() == actor_name.lower() or actor["actor5_name"].lower() == actor_name.lower():
            lt.addLast(list_id, actor["id"])
            lt.addLast(directores, actor["director_name"])
            peliculas += 1
    name = ""
    mayor = 0
    for i in directores:
        num = lt.CountElement(i)
        if num > mayor:
            mayor = num
            name = i
    lpromedio = lt.newList("ARRAY_LIST")
    lmovies = lt.newList("ARRAY_LIST")
    for peli in range(lt.size(list_id)):
        movies = lt.getElement(lst_movies, peli)
        lt.addLast(lmovies, movies["original_title"])
        lt.addLast(lpromedio, movies["vote_average"])

    return (lmovies, peliculas, lpromedio, name)


def Understand_Genres_Movies(genres_name, lst_movies):
    movies_number = 0
    promedios = lt.newList("ARRAY_LIST")
    lista_movies = lt.newList("ARRAY_LIST")
    # se obtiene el elemento n del archivo leído
    for posicion in range(lt.size(lst_movies)):
        peli = lt.getElement(lst_movies, posicion)
        # comparamos el genero con el parámetro ingresado
        if peli["genres"].lower() == genres_name.lower():
            # agregamos los nombres de las peliculas
            lt.addLast(lista_movies, peli["original_title"])
            # agregamos la calificación de las peliculas
            lt.addLast(promedios, peli["vote_count"])
            # creamos el contador para contar el numero de peliculas que cumplen con el requisito
            movies_number += 1
    return (lista_movies, movies_number, promedios)


def Ranking_genero(movies_number, genres_name, order, order_1, lstmovies):
    lista_movies = lt.newList("ARRAY_LIST")
    # se obtiene el elemento n del archivo leído
    for posicion in range(lt.size(lstmovies)):
        peli = lt.getElement(lstmovies, posicion)
        # comparamos el genero con el parámetro ingresado
        if peli["genres"].lower() == genres_name.lower():
            # agregamos los nombres de las peliculas
            lt.addLast(lista_movies, peli["original_title"])

    # Ordena por votos de manera descendente
    if order == 0 and order_1 == 0:
        lt.mergesort(lista_movies, lessV)
     # Ordena por votos de manera ascendente
    elif order == 0 and order_1 == 1:
        lt.mergesort(lista_movies, greaterV)
    # Ordena por promedio de manera descendente
    elif order == 1 and order_1 == 0:
        lt.mergesort(lista_movies, lessA)
     # Ordena por promedio de manera ascendente
    elif order == 1 and order_1 == 1:
        lt.mergesort(lista_movies, greaterA)
    return lt.subList(lista_movies, 1, movies_number)


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


def main():
    """
    Método principal del programa, se encarga de manejar todos los metodos adicionales creados

    Instancia una lista vacia en la cual se guardarán los datos cargados desde el archivo
    Args: None
    Return: None 
    """
    lstmovies = lt.newList("ARRAY_LIST")  # se require usar lista definida
    lstcasting = lt.newList("ARRAY_LIST")  # se require usar lista definida

    while True:
        printMenu()  # imprimir el menu de opciones en consola
        # leer opción ingresada
        inputs = input('Seleccione una opción para continuar\n')
        if len(inputs) > 0:

            if int(inputs[0]) == 1:  # opcion 1
                lstmovies = loadMovies()
                lstcasting = loadCasting()
            elif int(inputs[0]) == 2:  # opcion 2
                pass
            elif int(inputs[0]) == 3:  # opcion 3
                pass

            elif int(inputs[0]) == 4:  # opcion 4
                if lstcasting == None or str(lt.size(lstcasting)) == 0:
                    print("La lista está vacía ")
                else:
                    actor_name = input(
                        "Ingrese el nombre del actor que desea conocer\n")
                    encontrar = ActorInformation(
                        actor_name, lstcasting, lstmovies)
                    print("Los resultados son los siguientes ", encontrar)

            elif int(inputs[0]) == 5:  # opcion 5
                if lstmovies == None or str(lt.size(lstmovies)) == 0:
                    print("La lista está vacía ")
                else:
                    actor_name = input(
                        "Ingrese el nombre del genero cinematográfico que desea conocer\n")
                    resultado = Understand_Genres_Movies(actor_name, lstmovies)
                    print("Los resultados son los siguientes ", resultado)

            elif int(inputs[0]) == 6:  # opcion 6
                if lstmovies == None or str(lt.size(lstmovies)) == 0:
                    print("La lista está vacía ")
                else:
                    genres_name = input(
                        "Ingrese el nombre del genero cinematográfico que desea conocer\n")
                    movies_number = int(input(
                        "ingrese el número de peliculas que desea estén en el Ranking. Debe ser mayor a 10\n"))
                    if movies_number < 10:
                        print("Debe ser mayor a 10")
                    else:
                        order = int(input(
                            "Escriba 0 para ordenar por la cantidad de votos o 1 para ordenar por calificación promedio\n"))
                        if order != 0 and order != 1:
                            order = int(input(
                                "Escriba 0 para ordenar por la cantidad de votos o 1 para ordenar por calificación promedio\n"))
                        else:
                            order_1 = int(input(
                                "Escriba 0 para ordenar descendentemente o 1 para ordenar ascendentemente\n"))
                            if order_1 != 0 and order_1 != 1:
                                order_1 = int(input(
                                    "Escriba 0 para ordenar descendentemente o 1 para ordenar ascendentemente\n"))
                            else:
                                resultado = Ranking_genero(
                                    movies_number, genres_name, order, order_1, lstmovies)
                                print(
                                    "Los resultados son los siguientes ", resultado)
            elif int(inputs[0]) == 0:  # opcion 0, salir
                sys.exit(0)


if __name__ == "__main__":
    main()
