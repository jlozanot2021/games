import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

# Game settings
BIRD_WIDTH = 40
BIRD_HEIGHT = 30
PIPE_WIDTH = 80
INITIAL_PIPE_GAP = 250  # Espacio inicial entre tuberías
MINIMUM_PIPE_GAP = 100  # Espacio mínimo entre tuberías
GRAVITY = 0.25
JUMP_STRENGTH = 5
INITIAL_PIPE_SPEED = 3
MAXIMUM_PIPE_SPEED = 8

class Bird:
    def __init__(self):
        self.x = 100
        self.y = SCREEN_HEIGHT // 2
        self.velocity = 0

    def jump(self):
        self.velocity = -JUMP_STRENGTH

    def update(self):
        self.velocity += GRAVITY
        self.y += self.velocity

    def draw(self, screen):
        pygame.draw.rect(screen, WHITE, (self.x, self.y, BIRD_WIDTH, BIRD_HEIGHT))

class Pipe:
    def __init__(self, current_score, pipe_gap, pipe_speed):
        self.x = SCREEN_WIDTH
        # Reducir gradualmente el espacio entre tuberías según la puntuación
        reduced_gap = max(MINIMUM_PIPE_GAP, pipe_gap - (current_score * 3))
        self.height = random.randint(100, SCREEN_HEIGHT - reduced_gap - 100)
        self.gap = reduced_gap
        self.speed = pipe_speed
        self.passed = False

    def update(self):
        self.x -= self.speed

    def draw(self, screen):
        # Top pipe
        pygame.draw.rect(screen, GREEN, (self.x, 0, PIPE_WIDTH, self.height))
        # Bottom pipe
        pygame.draw.rect(screen, GREEN, (self.x, self.height + self.gap, PIPE_WIDTH, SCREEN_HEIGHT - self.height - self.gap))

def check_collision(bird, pipes):
    # Bird screen bounds collision
    if bird.y <= 0 or bird.y + BIRD_HEIGHT >= SCREEN_HEIGHT:
        return True

    # Pipe collision
    for pipe in pipes:
        if (bird.x < pipe.x + PIPE_WIDTH and 
            bird.x + BIRD_WIDTH > pipe.x and 
            (bird.y < pipe.height or 
             bird.y + BIRD_HEIGHT > pipe.height + pipe.gap)):
            return True
    return False

def main():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Flappy Bird - Dificultad Dinámica')
    clock = pygame.time.Clock()

    bird = Bird()
    pipes = []
    score = 0
    pipe_gap = INITIAL_PIPE_GAP
    pipe_speed = INITIAL_PIPE_SPEED
    font = pygame.font.Font(None, 36)

    # Game loop
    running = True
    spawn_pipe_timer = 0

    while running:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bird.jump()
                if event.key == pygame.K_r and not running:
                    # Restart game
                    bird = Bird()
                    pipes = []
                    score = 0
                    pipe_gap = INITIAL_PIPE_GAP
                    pipe_speed = INITIAL_PIPE_SPEED
                    running = True

        if running:
            # Update bird
            bird.update()

            # Spawn pipes
            spawn_pipe_timer += 1
            if spawn_pipe_timer > max(60, 90 - score):  # Reducir tiempo de aparición de tuberías
                pipes.append(Pipe(score, pipe_gap, pipe_speed))
                spawn_pipe_timer = 0

            # Update and remove pipes
            for pipe in pipes[:]:
                pipe.update()
                if pipe.x < -PIPE_WIDTH:
                    pipes.remove(pipe)
                
                # Score tracking
                if not pipe.passed and pipe.x < bird.x:
                    pipe.passed = True
                    score += 1
                    
                    # Aumentar dificultad
                    pipe_gap = max(MINIMUM_PIPE_GAP, pipe_gap - 2)
                    pipe_speed = min(MAXIMUM_PIPE_SPEED, pipe_speed + 0.1)

            # Check for collisions
            if check_collision(bird, pipes):
                running = False

            # Drawing
            screen.fill(BLACK)
            bird.draw(screen)
            for pipe in pipes:
                pipe.draw(screen)

            # Draw score and speed
            score_text = font.render(f'Puntuación: {score}', True, WHITE)
            speed_text = font.render(f'Velocidad: {pipe_speed:.1f}', True, WHITE)
            screen.blit(score_text, (10, 10))
            screen.blit(speed_text, (10, 50))

        else:
            # Game over screen
            game_over_text = font.render('¡Juego Terminado! Pulsa R para Reiniciar', True, WHITE)
            screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2))

        pygame.display.flip()
        clock.tick(60)  # 60 FPS

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
