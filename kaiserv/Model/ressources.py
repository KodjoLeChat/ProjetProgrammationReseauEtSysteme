'''class ressources Caesar 3'''
import pygame
import json

class Ressources:
    
    def __init__(self, food, water, dinars,population,username):
        self.food = food
        self.water = water
        self.dinars = dinars
        self.population = population
        self.username = username


    def to_json(self):
        return json.dumps({
            "food": self.food,
            "water": self.water,
            "dinars": self.dinars,
            "population": self.population,
            "username": self.username
        })

    def get_food(self):
        return self.food

    def get_water(self):
        return self.water

    def get_dinars(self):
        return self.dinars


    def get_population(self):
        return self.population
    
    def add_food(self, food):
        self.food += food

    def add_water(self, water):
        self.water += water


    def add_dinars(self, dinars):
        self.dinars += dinars


    def sub_food(self, food):
        self.food -= food

    def sub_water(self, water):
        self.water -= water


    def sub_dinars(self, dinars):
        self.dinars -= dinars

    '''add, sub and set population'''
    def add_population(self, population):
        self.population += population

    def sub_population(self, population):
        self.population -= population

    def set_population(self, population):
        self.population = population



    '''check if enough ressources'''
    def enough_food(self, food):
        return self.food >= food
    
    def enough_water(self, water):
        return self.water >= water

    def enough_dinars(self, dinars):
        return self.dinars >= dinars

    def enough_population(self, population):
        return self.population >= population
