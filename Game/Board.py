import pygame, itertools
from Box import Box

GREEN = (124, 252, 0)
PINK = (255, 20, 147)
LEMON = (255, 250, 205)

class Board(object):
    turn = 1
    
    def __init__(self, grid_size = 3, box_size = 200, border = 20, line_width = 5):
        self.grid_size = grid_size
        self.box_size = box_size
        self.border = border
        self.line_width = line_width
        surface_size = (self.grid_size * self.box_size) + (self.border * 2) + (self.line_width * (self.grid_size - 1))
        self.surface = pygame.display.set_mode((surface_size, surface_size), 0, 32)
        self.game_over = False
        self.setup()
        
    def setup(self):
        pygame.display.set_caption('Tic Tac Toe')
        self.surface.fill(LEMON)
        self.draw_lines()
        self.initialize_boxes()
        self.calculate_winners()
    
    def draw_lines(self):
        for i in xrange(1, self.grid_size):
            start_position = ((self.box_size * i) + (self.line_width * (i - 1))) + self.border
            width = self.surface.get_width() - (2 * self.border)
            pygame.draw.rect(self.surface, GREEN, (start_position, self.border, self.line_width, width))
            pygame.draw.rect(self.surface, GREEN, (self.border, start_position, width, self.line_width))
    
    def initialize_boxes(self):
        self.boxes = []
        
        top_left_numbers = []
        for i in range(0, self.grid_size):
            num = ((i * self.box_size) + self.border + (i *self.line_width))
            top_left_numbers.append(num)
        
        box_coordinates = list(itertools.product(top_left_numbers, repeat=2))
        for x, y in box_coordinates:
            self.boxes.append(Box(x, y, self.box_size, self))
    
    def get_box_at_pixel(self, x, y):
        for index, box in enumerate(self.boxes):
            if box.rect.collidepoint(x, y):
                return box
        return None
    
    def process_click(self, x, y):
        box = self.get_box_at_pixel(x, y)
        if box is not None and not self.game_over:
            self.play_turn(box)
            self.check_game_over()
    
    def play_turn(self, box):
        if box.state != 0:
            return
        if self.turn == 1:
            box.mark_x()
            box.state = 1
            self.turn = 2
        elif self.turn == 2:
            box.mark_o()
            box.state = 2
            self.turn = 1
        return
    
    def calculate_winners(self):
        self.winning_combinations = []
        indices = [x for x in xrange(0, self.grid_size * self.grid_size)]
        
        # Vertical combinations
        self.winning_combinations += ([tuple(indices[i:i+self.grid_size]) for i in xrange(0, len(indices), self.grid_size)])
        
        # Horizontal combinations
        self.winning_combinations += [tuple([indices[x] for x in xrange(y, len(indices), self.grid_size)]) for y in xrange(0, self.grid_size)]
        
        # Diagonal combinations
        self.winning_combinations.append(tuple(x for x in xrange(0, len(indices), self.grid_size + 1)))
        self.winning_combinations.append(tuple(x for x in xrange(self.grid_size - 1, len(indices), self.grid_size - 1)))
    
    def check_for_winner(self):
        winner = 0
        for combination in self.winning_combinations:
            states = []
            for index in combination:
                states.append(self.boxes[index].state)
            if all(x == 1 for x in states):
                winner = 1
            if all(x == 2 for x in states):
                winner = 2
        return winner
    
    def check_game_over(self):
        winner = self.check_for_winner()
        if winner:
            self.game_over = True
        elif all(box.state in [1, 2] for box in self.boxes):
            self.game_over = True
        if self.game_over:
            self.display_game_over(winner)
    
    def display_game_over(self, winner):
        surface_size = self.surface.get_height()
        font = pygame.font.Font('freesansbold.ttf', surface_size / 8)
        if winner:
            text = 'Player %s won!' % winner
        else:
            text = 'Draw!'
        text = font.render(text, True, PINK, LEMON)
        rect = text.get_rect()
        rect.center = (surface_size / 2, surface_size / 2)
        self.surface.blit(text, rect)
