import sys
import pygame

class Pixel:
    """游戏内容均为像素点,实质上为固定大小的矩形"""
    scale = 0,0
    location = 0,0
    color = 0,0,0
    def __init__(self, scale , location, color):
        self.scale = scale
        self.location = location
        self.color = color

    def move(self,target):
        self.location = target

    def ncolor(self,color):
        self.color = color

    def draw(self,screen):
        pygame.draw.rect(screen,self.color,(self.location,self.scale))
