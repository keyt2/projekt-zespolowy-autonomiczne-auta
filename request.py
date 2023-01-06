import datetime
import matplotlib # ogólny import biblioteki (możemy z niej potem korzystać)
matplotlib.use('Qt5Agg') # definiujemy backend którego ma używać biblioteka. Wskazujemy, że używamy PyQt w wersji 5
from matplotlib.figure import Figure # import obiektu "figury" której użyjemy do rysowania wykresów
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg # a tu widget z PyQt, który będzie wyświetlał się na ekranie


class Request:

    def __init__(self, address_from, address_to, time):
        self.address_from = address_from
        self.address_to = address_to
        self.time = time
        self.figure = Figure() # zapisujemy odwołanie do obiektu na którym będziemy rysować
        self.figureCanvas = FigureCanvasQTAgg(self.figure) # zapisujemy odwołanie do widgetu rysującego nasz obiekt
        self.groupBox_3.layout().addWidget(self.figureCanvas) # tutaj umieściłem widget wewnątrz przygotowanego wcześniej layoutu

    def show(self):
        print(f'Date: {self.time}, address from: {self.address_from}, address to: {self.address_to}')
