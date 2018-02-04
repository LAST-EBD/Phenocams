import os
import sys
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
import requests
from io import StringIO


class phenocam():

    '''Clase para trabajar con los datos de las estaciones de Phenocam. En principio pensado solo para
    las estaciones ubicadas en el Espacio Natural de Donana... Pero ya se vera. En realidad, depende del
    diccionario que le pasemos con los nombres y los ROIs de las estaciones que nos interesan. Trabajara
    con cualquier estacion siempre que este dentro de ese diccionario.
    Seria interesante ver como se puede generar ese diccionario de forma automatica, a partir de, por ejemplo,
    una serie de coordenadas y/o una distancia para hacer un buffer'''

    def __init__(self, stations, colors, start=None, end=None):
        '''Iniciamos la clase solo con el path base para generar la url y el diccionario con los nombres y
        los rois de las estaciones. Si una estacion tuviera varios ROIs se podrian poner como una lista en
        los valores de esa clave'''

        self.path_url = 'https://phenocam.sr.unh.edu/data/archive/{0}/ROI/{0}_{1}_1day.csv'
        self.stations = stations
        self.colors = colors
        self.start = start
        self.end = end

    def plot_one(self, key):
        '''Este metodo plotea solo la estacion que le pasemos como argumento'''

        sturl = self.path_url.format(key, self.stations[key])

        station = requests.get(sturl)
        fd = StringIO(station.text)
        df = pd.read_csv(fd, comment='#', parse_dates=[[0, 1]])

        df = df.set_index('date_year')
        df = df.loc[self.start:self.end]
        fd.close

        x = df.index
        y = df.gcc_50

        plt.figure(figsize=(15, 6))
        plt.xlabel('Fecha')
        plt.ylabel('GCC')
        plt.plot_date(x, y, 'k.', markersize=5.5, color='green')

        df['gcc_90'].plot(color='lime')
        plt.title(key)
        plt.legend()
        plt.show()

    def plot_all_split(self):
        '''Este metodo plotea todas las estaciones presentes en el diccionario en graficos separados'''

        for k, v in self.stations.items():

            station = requests.get(self.path_url.format(k, v))
            fd = StringIO(station.text)
            df = pd.read_csv(fd, comment='#', parse_dates=[[0, 1]])

            df = df.set_index('date_year')
            df = df.loc[self.start:self.end]
            fd.close

            x = df.index
            y = df.gcc_50
            plt.figure(figsize=(15, 6))

            plt.plot_date(x, y, 'k.', markersize=5.5, color='green')
            df['gcc_90'].plot(color='lime')
            plt.title(k)
            plt.xlabel('Fecha')
            plt.ylabel('GCC')
            plt.legend()

    def plot_all_together(self):
        '''Este metodo plotea todas las estaciones presentes en el diccionario en el mismo grafico'''

        plt.figure(figsize=(15, 10))
        plt.title('GCC PHENOCAMS VALUES AT DONANA NATIONAL PARK')

        for k, v in self.stations.items():

            station = requests.get(self.path_url.format(k, v))
            fd = StringIO(station.text)
            df = pd.read_csv(fd, comment='#', parse_dates=[[0, 1]])
            df = df.set_index('date_year')
            df = df.loc[self.start:self.end]
            fd.close

            x = df.index
            y = df.gcc_50

            plt.plot_date(x, y, 'k.', markersize=5.5, color=self.colors[k][0], label='_nolegend_')

            df['gcc_90'].plot(color=self.colors[k][-1], label=k + '_gcc90')
            plt.xlabel('Fecha')
            plt.ylabel('GCC')
            plt.legend()

    def plot_severals(self, *args):
        '''Este metodo plotea las estaciones que elijamos en el mismo grafico'''

        plt.figure(figsize=(15, 10))
        plt.title('GCC PHENOCAMS VALUES AT DONANA NATIONAL PARK')

        for st in args:

            station = requests.get(self.path_url.format(st, self.stations[st]))
            fd = StringIO(station.text)
            df = pd.read_csv(fd, comment='#', parse_dates=[[0, 1]])
            df = df.set_index('date_year')
            df = df.loc[self.start:self.end]
            fd.close
            df['gcc_90'].plot(color=self.colors[st][-1], label=st + '_gcc90')

            plt.legend()

            x = df.index
            y = df.gcc_50

            plt.plot_date(x, y, 'k.', markersize=5.5, color=self.colors[st][0], label='_nolegend_')
            plt.xlabel('Fecha')
            plt.ylabel('GCC')
