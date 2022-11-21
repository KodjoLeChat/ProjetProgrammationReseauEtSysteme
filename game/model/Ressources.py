'''class ressources Caesar 3'''
import pygame

class Ressources:
    
    def __init__(self, food, water, pence, dinars, workers,population):
        self.food = food
        self.water = water
        self.pence = pence
        self.dinars = dinars
        self.workers = workers
        self.population = population

    def get_food(self):
        return self.food

    def get_water(self):
        return self.water

    def get_pence(self):
        return self.pence

    def get_dinars(self):
        return self.dinars

    def get_workers(self):
        return self.workers

    def get_population(self):
        return self.population
    
    def add_food(self, food):
        self.food += food

    def add_water(self, water):
        self.water += water

    def add_pence(self, pence):
        self.pence += pence

    def add_dinars(self, dinars):
        self.dinars += dinars

    def add_workers(self, workers):
        self.workers += workers

    def sub_food(self, food):
        self.food -= food

    def sub_water(self, water):
        self.water -= water

    def sub_pence(self, pence):
        self.pence -= pence

    def sub_dinars(self, dinars):
        self.dinars -= dinars

    def sub_workers(self, workers):
        self.workers -= workers
        
    '''add, sub and set population'''
    def add_population(self, population):
        self.population += population

    def sub_population(self, population):
        self.population -= population

    def set_population(self, population):
        self.population = population


    def __str__(self):
        return f"food: {self.food} water: {self.water} pence: {self.pence} dinars: {self.dinars} workers: {self.workers} Population: {self.population}"

    '''save and load'''
    def save(self, file):
        with open(file, "w") as f:
            f.write(str(self))

    def load(self, file):
        with open(file, "r") as f:
            data = f.read().split()
            self.food = int(data[1])
            self.water = int(data[3])
            self.pence = int(data[5])
            self.dinars = int(data[7])
            self.workers = int(data[9])
    '''end save and load'''

    '''check if enough ressources'''
    def enough_food(self, food):
        return self.food >= food
    
    def enough_water(self, water):
        return self.water >= water

    def enough_pence(self, pence):
        return self.pence >= pence

    def enough_dinars(self, dinars):
        return self.dinars >= dinars

    def enough_workers(self, workers):
        return self.workers >= workers

    def enough_population(self, population):
        return self.population >= population
