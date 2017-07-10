import pygame, itertools

ORANGE = (255, 99, 71)
PINK = (255, 105, 180)

class Box(object):
    state = 0
    
    def __init__(self, x, y, size, board):
        self.size = size
        self.line_width = int(self.size / 30) if self.size > 30 else 1
        self.radius = (self.size / 2) - (self.size / 8)
        self.rect = pygame.Rect(x, y, size, size)
        self.board = board
    
    def mark_x(self):
        pygame.draw.line(self.board.surface, PINK, (self.rect.centerx - self.radius, self.rect.centery - self.radius), (self.rect.centerx + self.radius, self.rect.centery + self.radius), self.line_width)
        pygame.draw.line(self.board.surface, PINK, (self.rect.centerx - self.radius, self.rect.centery + self.radius), (self.rect.centerx + self.radius, self.rect.centery - self.radius), self.line_width)
    
    def mark_o(self):
        pygame.draw.circle(self.board.surface, ORANGE, (self.rect.centerx, self.rect.centery), self.radius, self.line_width)




