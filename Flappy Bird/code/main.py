import pygame, sys, time
from settings import *
from sprites import BG, Ground, Plane, Obstacle


class Game:
    def __init__(self):
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Flappy Bird")
        self.clock = pygame.time.Clock()
        self.active = True

        # sprite groups
        self.all_sprites = pygame.sprite.Group()
        self.collision_sprites = pygame.sprite.Group()

        # scale factor
        bg_height = pygame.image.load(
            "Flappy Bird/graphics/environment/background.png"
        ).get_height()
        self.scale_factor = WINDOW_HEIGHT / bg_height

        # sprite setup
        BG(self.all_sprites, self.scale_factor)
        Ground([self.all_sprites, self.collision_sprites], self.scale_factor)
        self.plane = Plane(self.all_sprites, self.scale_factor / 1.7)

        # timer
        self.obstacle_timer = pygame.USEREVENT + 1
        pygame.time.set_timer(self.obstacle_timer, 1400)

        #text
        self.font = pygame.font.Font('Flappy Bird/graphics/font/BD_Cartoon_Shout.ttf',30)
        self.score = 0
        self.start_offset = 0
        #menu
        self.menu_surface = pygame.image.load('Flappy Bird/graphics/ui/menu.png').convert_alpha()
        self.menu_rect = self.menu_surface.get_rect(center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))
        #sound
        self.bg_sound = pygame.mixer.Sound('Flappy Bird/sounds/music.wav')
        self.bg_sound.set_volume(0.1)
        self.bg_sound.play(loops = -1)

    def display_score(self):
        if self.active:
            self.score = pygame.time.get_ticks() - self.start_offset
            y = WINDOW_HEIGHT / 10
        else:
            y = WINDOW_HEIGHT / 2 + (self.menu_rect.height / 1.5)

        score_surface = self.font.render(str(int(self.score // 1000)), True, (0,0,0))
        score_rect =  score_surface.get_rect(midtop = (WINDOW_WIDTH / 2, y))
        self.display_surface.blit(score_surface, score_rect)

    def collisions(self):
        if (pygame.sprite.spritecollide(
                self.plane, self.collision_sprites, False, pygame.sprite.collide_mask)
            or self.plane.rect.top <= 0):
            for sprite in self.collision_sprites.sprites():
                if sprite.sprite_type == 'obstacle':
                    sprite.kill()
            self.active = False
            self.plane.kill()


    def run(self):
        last_time = time.time()
        while True:
            dt = time.time() - last_time
            last_time = time.time()
            
            # event loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.active:
                        self.plane.jump()
                    else:
                        self.plane = Plane(self.all_sprites, self.scale_factor / 1.7)
                        self.active = True
                        self.start_offset = pygame.time.get_ticks()

                if event.type == self.obstacle_timer and self.active == True:
                    Obstacle([self.all_sprites, self.collision_sprites],
                        self.scale_factor * 1.1)

            # game logic
            self.display_surface.fill("black")
            self.all_sprites.update(dt)
            self.all_sprites.draw(self.display_surface)
            self.display_score()

            if self.active : 
                self.collisions()
            else:
                self.display_surface.blit(self.menu_surface, self.menu_rect)

            pygame.display.update()
            self.clock.tick(FRAMERATE)


if __name__ == "__main__":
    game = Game()
    game.run()
