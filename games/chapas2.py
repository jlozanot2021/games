import pygame
import math

# Inicializar Pygame
pygame.init()

# Dimensiones de la pantalla
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Colores
WHITE = (255, 255, 255)
GREEN = (0, 180, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)

# Configuraciones del juego
BALL_RADIUS = 10
CHAPA_RADIUS = 20
MAX_SPEED = 15
FRICTION = 0.99
BALL_FRICTION = 0.98
RESTITUTION = 0.7
MAX_GOALS = 5

class Ball:
    def __init__(self):
        self.x = SCREEN_WIDTH // 2
        self.y = SCREEN_HEIGHT // 2
        self.vx = 0
        self.vy = 0
        self.mass = 1

    def update(self):
        self.vx *= BALL_FRICTION
        self.vy *= BALL_FRICTION

        self.x += self.vx
        self.y += self.vy

        if self.x - BALL_RADIUS < 50 or self.x + BALL_RADIUS > SCREEN_WIDTH - 50:
            self.vx *= -RESTITUTION
            self.x = max(50 + BALL_RADIUS, min(self.x, SCREEN_WIDTH - 50 - BALL_RADIUS))

        if self.y - BALL_RADIUS < 50 or self.y + BALL_RADIUS > SCREEN_HEIGHT - 50:
            self.vy *= -RESTITUTION
            self.y = max(50 + BALL_RADIUS, min(self.y, SCREEN_HEIGHT - 50 - BALL_RADIUS))

    def draw(self, screen):
        pygame.draw.circle(screen, WHITE, (int(self.x), int(self.y)), BALL_RADIUS)

    def collide(self, chapa):
        dx = self.x - chapa.x
        dy = self.y - chapa.y
        distance = math.sqrt(dx**2 + dy**2)

        if distance < BALL_RADIUS + CHAPA_RADIUS:
            nx = dx / distance
            ny = dy / distance

            rel_vx = self.vx - chapa.vx
            rel_vy = self.vy - chapa.vy

            impulse = 2 * (rel_vx * nx + rel_vy * ny) / (self.mass + chapa.mass)

            self.vx -= impulse * chapa.mass * nx
            self.vy -= impulse * chapa.mass * ny

class Chapa:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.vx = 0
        self.vy = 0
        self.color = color
        self.mass = 2

    def update(self):
        self.vx *= FRICTION
        self.vy *= FRICTION

        self.x += self.vx
        self.y += self.vy

        if self.x - CHAPA_RADIUS < 50 or self.x + CHAPA_RADIUS > SCREEN_WIDTH - 50:
            self.vx *= -RESTITUTION
            self.x = max(50 + CHAPA_RADIUS, min(self.x, SCREEN_WIDTH - 50 - CHAPA_RADIUS))

        if self.y - CHAPA_RADIUS < 50 or self.y + CHAPA_RADIUS > SCREEN_HEIGHT - 50:
            self.vy *= -RESTITUTION
            self.y = max(50 + CHAPA_RADIUS, min(self.y, SCREEN_HEIGHT - 50 - CHAPA_RADIUS))

    def draw(self, screen, start_pos=None):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), CHAPA_RADIUS)
        if start_pos:
            pygame.draw.line(screen, GRAY, (int(self.x), int(self.y)), start_pos, 3)

    def is_clicked(self, pos):
        dx = pos[0] - self.x
        dy = pos[1] - self.y
        return math.sqrt(dx**2 + dy**2) < CHAPA_RADIUS

    def move(self, start_pos, end_pos):
        dx = start_pos[0] - end_pos[0]
        dy = start_pos[1] - end_pos[1]

        distance = math.sqrt(dx**2 + dy**2)
        speed = min(distance, MAX_SPEED)

        if distance > 0:
            dx /= distance
            dy /= distance

        self.vx = dx * speed
        self.vy = dy * speed

def check_collision_chapas(chapa1, chapa2):
    dx = chapa1.x - chapa2.x
    dy = chapa1.y - chapa2.y
    distance = math.sqrt(dx**2 + dy**2)

    if distance < CHAPA_RADIUS * 2:
        nx = dx / distance
        ny = dy / distance

        rel_vx = chapa1.vx - chapa2.vx
        rel_vy = chapa1.vy - chapa2.vy

        impulse = 2 * (rel_vx * nx + rel_vy * ny) / (chapa1.mass + chapa2.mass)

        chapa1.vx -= impulse * chapa2.mass * nx
        chapa1.vy -= impulse * chapa2.mass * ny
        chapa2.vx += impulse * chapa1.mass * nx
        chapa2.vy += impulse * chapa1.mass * ny

def check_goal(ball):
    goal_width = 200
    goal_top = SCREEN_HEIGHT // 2 - goal_width // 2
    goal_bottom = SCREEN_HEIGHT // 2 + goal_width // 2

    if ball.x - BALL_RADIUS <= 50 and goal_top <= ball.y <= goal_bottom:
        return 2

    if ball.x + BALL_RADIUS >= SCREEN_WIDTH - 50 and goal_top <= ball.y <= goal_bottom:
        return 1

    return 0

def main():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Futbol de Chapas Mejorado')
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 36)

    ball = Ball()
    team1_chapas = [
        Chapa(200, SCREEN_HEIGHT // 2, BLUE),
        Chapa(300, SCREEN_HEIGHT // 3, BLUE),
        Chapa(300, 2 * SCREEN_HEIGHT // 3, BLUE)
    ]
    team2_chapas = [
        Chapa(SCREEN_WIDTH - 200, SCREEN_HEIGHT // 2, RED),
        Chapa(SCREEN_WIDTH - 300, SCREEN_HEIGHT // 3, RED),
        Chapa(SCREEN_WIDTH - 300, 2 * SCREEN_HEIGHT // 3, RED)
    ]

    team1_score = 0
    team2_score = 0
    current_team = 1
    selected_chapa = None
    drag_start = None
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()

                if current_team == 1:
                    for chapa in team1_chapas:
                        if chapa.is_clicked(mouse_pos):
                            selected_chapa = chapa
                            drag_start = mouse_pos
                            break
                else:
                    for chapa in team2_chapas:
                        if chapa.is_clicked(mouse_pos):
                            selected_chapa = chapa
                            drag_start = mouse_pos
                            break

            if event.type == pygame.MOUSEBUTTONUP and selected_chapa:
                mouse_pos = pygame.mouse.get_pos()
                selected_chapa.move(drag_start, mouse_pos)

                current_team = 2 if current_team == 1 else 1
                selected_chapa = None
                drag_start = None

        ball.update()

        for chapa in team1_chapas + team2_chapas:
            chapa.update()

        for i in range(len(team1_chapas)):
            for j in range(len(team2_chapas)):
                check_collision_chapas(team1_chapas[i], team2_chapas[j])
                ball.collide(team1_chapas[i])
                ball.collide(team2_chapas[j])

        for i in range(len(team1_chapas)):
            for j in range(i + 1, len(team1_chapas)):
                check_collision_chapas(team1_chapas[i], team1_chapas[j])

        for i in range(len(team2_chapas)):
            for j in range(i + 1, len(team2_chapas)):
                check_collision_chapas(team2_chapas[i], team2_chapas[j])

        goal = check_goal(ball)
        if goal == 1:
            team1_score += 1
            ball = Ball()
            team1_chapas = [
                Chapa(200, SCREEN_HEIGHT // 2, BLUE),
                Chapa(300, SCREEN_HEIGHT // 3, BLUE),
                Chapa(300, 2 * SCREEN_HEIGHT // 3, BLUE)
            ]
            team2_chapas = [
                Chapa(SCREEN_WIDTH - 200, SCREEN_HEIGHT // 2, RED),
                Chapa(SCREEN_WIDTH - 300, SCREEN_HEIGHT // 3, RED),
                Chapa(SCREEN_WIDTH - 300, 2 * SCREEN_HEIGHT // 3, RED)
            ]
            current_team = 2
        elif goal == 2:
            team2_score += 1
            ball = Ball()
            team1_chapas = [
                Chapa(200, SCREEN_HEIGHT // 2, BLUE),
                Chapa(300, SCREEN_HEIGHT // 3, BLUE),
                Chapa(300, 2 * SCREEN_HEIGHT // 3, BLUE)
            ]
            team2_chapas = [
                Chapa(SCREEN_WIDTH - 200, SCREEN_HEIGHT // 2, RED),
                Chapa(SCREEN_WIDTH - 300, SCREEN_HEIGHT // 3, RED),
                Chapa(SCREEN_WIDTH - 300, 2 * SCREEN_HEIGHT // 3, RED)
            ]
            current_team = 1

        if team1_score == MAX_GOALS or team2_score == MAX_GOALS:
            running = False

        screen.fill(GREEN)

        pygame.draw.rect(screen, WHITE, (50, SCREEN_HEIGHT // 2 - 100, 10, 200), 3)
        pygame.draw.rect(screen, WHITE, (SCREEN_WIDTH - 60, SCREEN_HEIGHT // 2 - 100, 10, 200), 3)

        ball.draw(screen)

        for chapa in team1_chapas:
            if chapa == selected_chapa and drag_start:
                chapa.draw(screen, drag_start)
            else:
                chapa.draw(screen)

        for chapa in team2_chapas:
            if chapa == selected_chapa and drag_start:
                chapa.draw(screen, drag_start)
            else:
                chapa.draw(screen)

        score_text = font.render(f'Azul {team1_score} - {team2_score} Rojo', True, BLACK)
        screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, 20))

        turn_text = font.render('Turno Equipo Azul' if current_team == 1 else 'Turno Equipo Rojo', True, BLACK)
        screen.blit(turn_text, (SCREEN_WIDTH // 2 - turn_text.get_width() // 2, 60))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()

