import sys
import pygame
from pixel import Pixel

class Element:
    pixelScale = [0,0]
    #此处的长宽代表像素点数
    scale = [0,0]
    mes = []
    shifting = [0,0]
    speed = [1,1]

    def __init__(self,pixelScale,scale,mes):
        self.pixelScale = pixelScale
        self.scale = scale
        self.mes = mes

    def draw(self,screen):
        for _ in range(len(self.mes)):
            location = [(self.mes[_][0][0]-1) * self.pixelScale[0] + self.shifting[0], (self.mes[_][0][1]) * self.pixelScale[1] + self.shifting[1]]
            color = self.mes[_][1]
            pixel = Pixel(self.pixelScale,location,color)
            pixel.draw(screen)

    def move(self,location):
        self.shifting = location

    def setSpeed(self,speed):
        self.speed = speed






