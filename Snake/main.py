import pygame
import sys
import random
from pygame.math import Vector2


class SNAKE:
    def __init__(self, is_ai=False):
        self.is_ai = is_ai
        self.body = [Vector2(18, 5), Vector2(18, 4), Vector2(18, 3)] if is_ai else [Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)]
        self.direction = Vector2(0, 0)
        self.new_block = False
        self.load_images()
        
    @staticmethod
    def invert_image_colors(image):
        pixels = pygame.PixelArray(image)
        for x in range(image.get_width()):
            for y in range(image.get_height()):
                r, g, b, a = image.get_at((x, y))
                inverted_color = (255 - r, 255 - g, 255 - b, a)
                pixels[x, y] = inverted_color
        del pixels
        return image
    
    def load_images(self):
        paths = [
            'head_up', 'head_down', 'head_right', 'head_left',
            'tail_up', 'tail_down', 'tail_right', 'tail_left',
            'body_vertical', 'body_horizontal',
            'body_topright', 'body_topleft', 'body_bottomright', 'body_bottomleft'
        ]

        for path in paths:
            # Load the image for the player-controlled snake
            setattr(self, path, pygame.image.load(f'Snake/Graphics/{path}.png').convert_alpha())

            # Load and invert the image for the AI snake
            image = pygame.image.load(f'Snake/Graphics/{path}.png').convert_alpha()
            inverted_image = self.invert_image_colors(image)
            setattr(self, f"{path}_ai", inverted_image)

        self.hit = pygame.mixer.Sound('Snake/hit.wav')

    def draw_snake(self):
        self.update_head_graphics()
        self.update_tail_graphics()

        for index, block in enumerate(self.body): #enumerate gives an index for the current element
            x_pos = block.x * cell_size
            y_pos = block.y * cell_size   
            block_rect = pygame.Rect(x_pos,y_pos , cell_size, cell_size)

            if index == 0: 
                screen.blit(self.head ,block_rect)
            elif index == len(self.body) - 1:
                screen.blit(self.tail, block_rect)
            else:
                previous_block = self.body[index + 1] - block 
                next_block = self.body[index - 1] - block 
                if previous_block.x == next_block.x:
                    if self.is_ai:
                        screen.blit(self.body_vertical_ai, block_rect)
                    else:
                        screen.blit(self.body_vertical, block_rect)
                elif previous_block.y == next_block.y:
                    if self.is_ai:
                        screen.blit(self.body_horizontal_ai, block_rect)
                    else:
                        screen.blit(self.body_horizontal, block_rect)
                else:
                    if previous_block.x == -1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == -1:    
                        if self.is_ai:
                            screen.blit(self.body_topleft_ai, block_rect)
                        else:
                            screen.blit(self.body_topleft, block_rect)
                    elif previous_block.x == 1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == 1:    
                        if self.is_ai:
                            screen.blit(self.body_topright_ai, block_rect)
                        else:
                            screen.blit(self.body_topright, block_rect)
                    elif previous_block.x == 1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == 1:    
                        if self.is_ai:
                            screen.blit(self.body_bottomright_ai, block_rect)
                        else:
                            screen.blit(self.body_bottomright, block_rect)
                    elif previous_block.x == -1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == -1:    
                        if self.is_ai:
                            screen.blit(self.body_bottomleft_ai, block_rect)
                        else:
                            screen.blit(self.body_bottomleft, block_rect)
            

    def update_head_graphics(self):
        head_relation = self.body[1] - self.body[0]
        if head_relation == Vector2(1,0): 
            if self.is_ai:
                self.head = self.head_left_ai
            else:
                self.head = self.head_left
        elif head_relation == Vector2(-1,0): 
            if self.is_ai:
                self.head = self.head_right_ai
            else:
                self.head = self.head_right
        elif head_relation == Vector2(0,1): 
            if self.is_ai:
                self.head = self.head_up_ai
            else:
                self.head = self.head_up
        elif head_relation == Vector2(0,-1): 
            if self.is_ai:
                self.head = self.head_down_ai
            else:
                self.head = self.head_down

    def update_tail_graphics(self):
        tail_relation = self.body[-2] - self.body[-1]
        if tail_relation == Vector2(1,0): 
            if self.is_ai:
                self.tail = self.tail_left_ai
            else:
                self.tail = self.tail_left
        elif tail_relation == Vector2(-1,0): 
            if self.is_ai:
                self.tail = self.tail_right_ai
            else:
                self.tail = self.tail_right
        elif tail_relation == Vector2(0,1): 
            if self.is_ai:
                self.tail = self.tail_up_ai
            else:
                self.tail = self.tail_up
        elif tail_relation == Vector2(0,-1): 
            if self.is_ai:
                self.tail = self.tail_down_ai
            else:
                self.tail = self.tail_down
   
    def move_snake(self, fruit_position):
        if self.is_ai:
            to_fruit= fruit_position - self.body[0]
            # Update the direction based on the relative position of the snake to the apple
            if to_fruit.x > 0:
                self.direction = Vector2(1, 0)  # Move right
            elif to_fruit.x < 0:
                self.direction = Vector2(-1, 0)  # Move left
            elif to_fruit.y > 0:
                self.direction = Vector2(0, 1)  # Move down
            elif to_fruit.y < 0:
                self.direction = Vector2(0, -1)  # Move up

            if self.new_block == True:
                body_copy = self.body[:]
                body_copy.insert(0, body_copy[0] + self.direction)
                self.body = body_copy[:] 
                self.new_block = False
            else:
                body_copy = self.body[:-1]
                body_copy.insert(0, body_copy[0] + self.direction)
                self.body = body_copy[:] 
        else:
            if self.new_block == True:
                body_copy = self.body[:]
                body_copy.insert(0, body_copy[0] + self.direction)
                self.body = body_copy[:] 
                self.new_block = False
            else:
                body_copy = self.body[:-1]
                body_copy.insert(0, body_copy[0] + self.direction)
                self.body = body_copy[:] 

    def add_block(self):
        self.new_block = True

    def play_sound(self):
        self.hit.play()    
    
    def reset(self):
        self.direction = Vector2(0,0)
        if self.is_ai:
            self.body = [Vector2(18,5), Vector2(18,4), Vector2(18,3)]
        else:
            self.body = [Vector2(5,10), Vector2(4,10), Vector2(3,10)]

class Fruit:
    def __init__(self):
        self.randomize()

    def draw_fruit(self):
        fruit_rect = pygame.Rect(self.pos.x * cell_size, self.pos.y * cell_size, cell_size, cell_size)
        screen.blit(apple, fruit_rect)
        #pygame.draw.rect(screen, (126, 166, 114), fruit_rect)

    def randomize(self):
        self.x = random.randint(0, cell_number - 1)
        self.y = random.randint(0, cell_number - 1)
        self.pos = Vector2(self.x, self.y)

class MAIN:
    def __init__(self):
        self.snake = SNAKE()
        self.snake_ai = SNAKE(is_ai=True)
        self.fruit = Fruit()
        
    def update(self):
        fruit_position = self.fruit.pos
        self.snake.move_snake(fruit_position)
        self.snake_ai.move_snake(fruit_position)
        self.check_collision()
        self.check_fail()

    def draw_elements(self):
        self.draw_grass()
        self.fruit.draw_fruit()
        self.snake.draw_snake()
        self.snake_ai.draw_snake()
        self.draw_score()

    def check_collision(self):
        if self.fruit.pos == self.snake.body[0]:
            self.fruit.randomize()
            self.snake.add_block()
            self.snake.play_sound()
        elif self.fruit.pos == self.snake_ai.body[0]:
            self.fruit.randomize()
            self.snake_ai.add_block()
            self.snake_ai.play_sound()

        
        for block in self.snake.body[1:] or block in self.snake_ai.body[1:]:
            if block == self.fruit.pos:
                self.fruit.randomize()

    def check_fail(self):
        if not 0 <= self.snake.body[0].x < cell_number or not 0 <= self.snake.body[0].y < cell_number:
                self.game_over()

        if not 0 <= self.snake_ai.body[0].x < cell_number or not 0 <= self.snake_ai.body[0].y < cell_number:
                self.ai_game_over()
        
        for block in self.snake.body[1:]:
            if self.snake.body[0] == block:
                self.game_over()
        
        for block in self.snake_ai.body[1:]:
            if self.snake_ai.body[0] == block:
                self.ai_game_over()

    def draw_grass(self):
        # fruit_rect = pygame.Rect(self.pos.x * cell_size, self.pos.y * cell_size, cell_size, cell_size)
        # screen.blit(apple, fruit_rect)
        grass_color = (100,150,61)
        for row in range(cell_number):
            if row % 2 == 0:
                for col in range(cell_number):
                    if col % 2 == 0:
                        grass_rect = pygame.Rect(col * cell_size,row * cell_size , cell_size,cell_size)
                        pygame.draw.rect(screen, grass_color, grass_rect)
            else:
                for col in range(cell_number):
                    if col % 2 != 0:
                        grass_rect = pygame.Rect(col * cell_size,row * cell_size , cell_size,cell_size)
                        pygame.draw.rect(screen, grass_color, grass_rect)
            
    
    def draw_score(self):
        score_text = 'score: ' + str(len(self.snake.body) - 3)
        score_surface = game_font.render(score_text,True,(56,75,15))
        score_x = int(cell_size + 60)
        score_y = int(cell_size * cell_number - 40)
        score_rect = score_surface.get_rect( center = (score_x, score_y))
        apple_rect = apple.get_rect(midright = (score_rect.left, score_rect.centery))
        bg_rect = pygame.Rect(apple_rect.left,apple_rect.top , apple_rect.width+score_rect.width+6, apple_rect.height)

        pygame.draw.rect(screen, (7,109,61), bg_rect)
        screen.blit(score_surface, score_rect)
        screen.blit(apple, apple_rect)
        pygame.draw.rect(screen, (56,75,15), bg_rect, 2)

        computer_score_text = 'computer_score: ' + str(len(self.snake_ai.body) - 3)
        computer_score_surface = game_font.render(computer_score_text,True,(56,75,15))
        computer_score_x = int(cell_size * cell_number - 120)
        computer_score_y = int(cell_size * cell_number - 40)
        computer_score_rect = computer_score_surface.get_rect( center = (computer_score_x, computer_score_y))
        apple1_rect = apple.get_rect(midright = (computer_score_rect.left, computer_score_rect.centery))
        bg1_rect = pygame.Rect(apple1_rect.left,apple1_rect.top , apple1_rect.width+computer_score_rect.width+6, apple1_rect.height)

        pygame.draw.rect(screen, (7,109,61), bg1_rect)
        screen.blit(computer_score_surface, computer_score_rect)
        screen.blit(apple, apple1_rect)
        pygame.draw.rect(screen, (56,75,15), bg1_rect, 2)

    def game_over(self):
        self.snake.reset()     
    def ai_game_over(self):
        self.snake_ai.reset()  


# Initialize Pygame
pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()

# Constants
cell_size = 40
cell_number = 20
screen = pygame.display.set_mode((cell_number * cell_size, cell_number * cell_size))
clock = pygame.time.Clock()
apple = pygame.image.load('snake/Graphics/apple.png').convert_alpha()
grass = pygame.image.load('snake/Graphics/grass.png').convert_alpha()
grass1 = pygame.image.load('snake/Graphics/grass2.png').convert_alpha()
game_font = pygame.font.Font(None,25)

SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 150)

main_game = MAIN()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == SCREEN_UPDATE:
            main_game.update()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                if main_game.snake.direction.y !=1:
                    main_game.snake.direction = Vector2(0,-1)
            if event.key == pygame.K_DOWN:
                if main_game.snake.direction.y != -1:
                    main_game.snake.direction = Vector2(0,1)
            if event.key == pygame.K_RIGHT:
                if main_game.snake.direction.x !=-1:
                    main_game.snake.direction = Vector2(1,0)
            if event.key == pygame.K_LEFT:
                if main_game.snake.direction.x !=1:
                    main_game.snake.direction = Vector2(-1,0)

    screen.fill((50, 60, 70))
    main_game.draw_elements()
    pygame.display.update()
    clock.tick(60)  # fps
