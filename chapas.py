import pygame
import math
import numpy as np
import os

# Inicializar Pygame
pygame.init()

# Dimensiones de la pantalla
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 800
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

fuente = pygame.font.Font(None, 74)
fuente_pequeña = pygame.font.Font(None, 36)

equipo_local = None
equipo_visitante = None

WHITE = (255, 255, 255)
GREEN = (0, 180, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)

CAMPO = 100


# Configuraciones del juego
BALL_RADIUS = 10
CHAPA_RADIUS = 20
MAX_SPEED = 15
FRICTION = 0.99
BALL_FRICTION = 0.98
RESTITUTION = 0.7
MAX_GOALS = 3

equipos = ["Real Madrid", "Barcelona", "España", "Psoe", "Marruecos", "Osasuna", "Jamón", "Fortnite", "Kanye West"]

carpeta_imagenes = "equipos"
imagenes_equipos = {}

CHAPA_LOCAL_IMG = None
CHAPA_VISIT_IMG = None
BALL_IMG = pygame.transform.scale(pygame.image.load("ball.png"), (BALL_RADIUS * 2, BALL_RADIUS * 2))

SECRET_IMAGE_PATH = "equipos/secret/.secret.png"
secret_image = pygame.image.load(SECRET_IMAGE_PATH)
secret_image = pygame.transform.scale(secret_image, (CHAPA_RADIUS * 2, CHAPA_RADIUS * 2))

# Dimensiones de la portería
GOAL_WIDTH = 200
GOAL_HOLE_RADIUS = CHAPA_RADIUS + 5  # Hueco un poco mayor al radio de las chapas

GOAL_SPACE = CHAPA_RADIUS * 2 + 10


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

        # Goal area boundaries
        goal_top = SCREEN_HEIGHT // 2 - GOAL_WIDTH // 2
        goal_bottom = SCREEN_HEIGHT // 2 + GOAL_WIDTH // 2
        goal_hole_top = goal_top + GOAL_HOLE_RADIUS
        goal_hole_bottom = goal_bottom - GOAL_HOLE_RADIUS

        # Check for collision on the left side (goal side)
        if self.x - BALL_RADIUS < CAMPO:
            if goal_hole_top <= self.y <= goal_hole_bottom:  # Inside the goal area vertically
                if self.x - BALL_RADIUS < CAMPO - GOAL_SPACE:
                    self.vx *= -RESTITUTION
                    self.x = CAMPO - GOAL_SPACE + BALL_RADIUS

                # Handle rebounding in Y within the goal area
                if self.y - BALL_RADIUS < goal_hole_top:
                    self.vy *= -RESTITUTION
                    self.y = goal_hole_top + BALL_RADIUS
                elif self.y + BALL_RADIUS > goal_hole_bottom:
                    self.vy *= -RESTITUTION
                    self.y = goal_hole_bottom - BALL_RADIUS
            else:  # Outside the goal area vertically
                if self.x - BALL_RADIUS < CAMPO:
                    self.vx *= -RESTITUTION
                    self.x = CAMPO + BALL_RADIUS

        # Check for collision on the right side (goal side)
        elif self.x + BALL_RADIUS > SCREEN_WIDTH - CAMPO:
            if goal_hole_top <= self.y <= goal_hole_bottom:  # Inside the goal area vertically
                if self.x + BALL_RADIUS > SCREEN_WIDTH - CAMPO + GOAL_SPACE:
                    self.vx *= -RESTITUTION
                    self.x = SCREEN_WIDTH - CAMPO + GOAL_SPACE - BALL_RADIUS

                # Handle rebounding in Y within the goal area
                if self.y - BALL_RADIUS < goal_hole_top:
                    self.vy *= -RESTITUTION
                    self.y = goal_hole_top + BALL_RADIUS
                elif self.y + BALL_RADIUS > goal_hole_bottom:
                    self.vy *= -RESTITUTION
                    self.y = goal_hole_bottom - BALL_RADIUS
            else:  # Outside the goal area vertically
                if self.x + BALL_RADIUS > SCREEN_WIDTH - CAMPO:
                    self.vx *= -RESTITUTION
                    self.x = SCREEN_WIDTH - CAMPO - BALL_RADIUS

        # Handle top and bottom boundary collisions
        if self.y - BALL_RADIUS < CAMPO:
            self.vy *= -RESTITUTION
            self.y = CAMPO + BALL_RADIUS
        elif self.y + BALL_RADIUS > SCREEN_HEIGHT - CAMPO:
            self.vy *= -RESTITUTION
            self.y = SCREEN_HEIGHT - CAMPO - BALL_RADIUS

    def draw(self, screen):
        screen.blit(BALL_IMG, (int(self.x) - BALL_RADIUS, int(self.y) - BALL_RADIUS))

class Chapa:
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.vx = 0
        self.vy = 0
        self.img = img
        self.mass = 2

    def update(self):
        self.vx *= FRICTION
        self.vy *= FRICTION

        self.x += self.vx
        self.y += self.vy

        # Goal area boundaries
        goal_top = SCREEN_HEIGHT // 2 - GOAL_WIDTH // 2
        goal_bottom = SCREEN_HEIGHT // 2 + GOAL_WIDTH // 2
        goal_hole_top = goal_top + GOAL_HOLE_RADIUS
        goal_hole_bottom = goal_bottom - GOAL_HOLE_RADIUS

        # Check for collision on the left side (goal side)
        if self.x - CHAPA_RADIUS < CAMPO:
            if goal_hole_top <= self.y <= goal_hole_bottom:  # Inside the goal area vertically
                if self.x - CHAPA_RADIUS < CAMPO - GOAL_SPACE:
                    self.vx *= -RESTITUTION
                    self.x = CAMPO - GOAL_SPACE + CHAPA_RADIUS

                # Handle rebounding in Y within the goal area
                if self.y - CHAPA_RADIUS < goal_hole_top:
                    self.vy *= -RESTITUTION
                    self.y = goal_hole_top + CHAPA_RADIUS
                elif self.y + CHAPA_RADIUS > goal_hole_bottom:
                    self.vy *= -RESTITUTION
                    self.y = goal_hole_bottom - CHAPA_RADIUS
            else:  # Outside the goal area vertically
                if self.x - CHAPA_RADIUS < CAMPO:
                    self.vx *= -RESTITUTION
                    self.x = CAMPO + CHAPA_RADIUS

        # Check for collision on the right side (goal side)
        elif self.x + CHAPA_RADIUS > SCREEN_WIDTH - CAMPO:
            if goal_hole_top <= self.y <= goal_hole_bottom:  # Inside the goal area vertically
                if self.x + CHAPA_RADIUS > SCREEN_WIDTH - CAMPO + GOAL_SPACE:
                    self.vx *= -RESTITUTION
                    self.x = SCREEN_WIDTH - CAMPO + GOAL_SPACE - CHAPA_RADIUS

                # Handle rebounding in Y within the goal area
                if self.y - CHAPA_RADIUS < goal_hole_top:
                    self.vy *= -RESTITUTION
                    self.y = goal_hole_top + CHAPA_RADIUS
                elif self.y + CHAPA_RADIUS > goal_hole_bottom:
                    self.vy *= -RESTITUTION
                    self.y = goal_hole_bottom - CHAPA_RADIUS
            else:  # Outside the goal area vertically
                if self.x + CHAPA_RADIUS > SCREEN_WIDTH - CAMPO:
                    self.vx *= -RESTITUTION
                    self.x = SCREEN_WIDTH - CAMPO - CHAPA_RADIUS

        # Handle top and bottom boundary collisions
        if self.y - CHAPA_RADIUS < CAMPO:
            self.vy *= -RESTITUTION
            self.y = CAMPO + CHAPA_RADIUS
        elif self.y + CHAPA_RADIUS > SCREEN_HEIGHT - CAMPO:
            self.vy *= -RESTITUTION
            self.y = SCREEN_HEIGHT - CAMPO - CHAPA_RADIUS

    def draw(self, screen, drag_start=None, drag_end=None):
        screen.blit(self.img, (int(self.x) - CHAPA_RADIUS, int(self.y) - CHAPA_RADIUS))
        if drag_start and drag_end:
            pygame.draw.line(screen, RED, drag_start, drag_end, 2)


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

def cargar_imagenes():
    global imagenes_equipos
    for i, equipo in enumerate(equipos, start=1):
        ruta_imagen = os.path.join(carpeta_imagenes, f"{i}.png")
        if os.path.exists(ruta_imagen):
            imagen_original = pygame.image.load(ruta_imagen)
            # Escalar todas las imágenes al mismo tamaño (por ejemplo, 150x150 píxeles)
            imagen_escalada = pygame.transform.scale(imagen_original, (150, 150))
            imagenes_equipos[equipo] = imagen_escalada
        else:
            print(f"Advertencia: No se encontró la imagen para {equipo} en {ruta_imagen}")

def mostrar_confirmacion_final():
    global equipo_local, equipo_visitante, CHAPA_LOCAL_IMG, CHAPA_VISIT_IMG

    while True:
        screen.fill(WHITE)

        texto_titulo = fuente.render("¿Estás de acuerdo con los equipos?", True, BLACK)
        screen.blit(texto_titulo, (50, 50))

        # Mostrar detalles del equipo local
        texto_local = fuente.render(f"{equipo_local}", True, GREEN)
        screen.blit(texto_local, (50, 150))
        if equipo_local in imagenes_equipos:
            imagen_local = CHAPA_LOCAL_IMG
            imagen_local_rect = imagen_local.get_rect(center=(200, SCREEN_HEIGHT // 2))
            screen.blit(imagen_local, imagen_local_rect)

        # Mostrar detalles del equipo visitante
        texto_visitante = fuente.render(f"{equipo_visitante}", True, BLUE)
        screen.blit(texto_visitante, (SCREEN_WIDTH - 350, 150))
        if equipo_visitante in imagenes_equipos:
            imagen_visitante = CHAPA_VISIT_IMG
            imagen_visitante_rect = imagen_visitante.get_rect(center=(SCREEN_WIDTH - 200, SCREEN_HEIGHT // 2))
            screen.blit(imagen_visitante, imagen_visitante_rect)

        # Mensaje de confirmación
        texto_confirmar = fuente_pequeña.render(
            "Presiona ENTER para confirmar o ESC para reiniciar", True, BLACK
        )
        screen.blit(texto_confirmar, (50, SCREEN_HEIGHT - 100))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return True
                elif event.key == pygame.K_ESCAPE:
                    return False
                elif event.key == pygame.K_PLUS or event.key == pygame.K_KP_PLUS:
                    if equipo_local is None:
                        equipo_local = "Secret"
                        CHAPA_LOCAL_IMG = secret_image
                    elif equipo_visitante is None:
                        equipo_visitante = "Secret"
                        CHAPA_VISIT_IMG = secret_image



def mostrar_confirmacion(rol, equipo):
    while True:
        screen.fill(WHITE)

        texto_titulo = fuente.render(f"Equipo {rol} seleccionado", True, BLACK)
        screen.blit(texto_titulo, (50, 50))

        texto_equipo = fuente.render(equipo, True, GREEN if rol == "Local" else BLUE)
        screen.blit(texto_equipo, (50, 150))

        if equipo in imagenes_equipos:
            imagen = imagenes_equipos[equipo]
            imagen_rect = imagen.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            screen.blit(imagen, imagen_rect)

        texto_confirmar = fuente_pequeña.render("Presiona ENTER para confirmar", True, BLACK)
        screen.blit(texto_confirmar, (50, SCREEN_HEIGHT - 100))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return True
                elif event.key == pygame.K_ESCAPE:
                    return False


def menu_seleccion():
    global equipo_local, equipo_visitante, CHAPA_LOCAL_IMG, CHAPA_VISIT_IMG

    seleccionando = True
    opcion_actual = 0

    while seleccionando:
        seleccionando_local = True
        seleccionando_visitante = True

        # Seleccionar equipo local
        while seleccionando_local:
            screen.fill(WHITE)
            texto_titulo = fuente.render("Selecciona el equipo LOCAL", True, BLACK)
            screen.blit(texto_titulo, (50, 50))

            # Mostrar opciones de equipos a la izquierda
            for i, equipo in enumerate(equipos):
                color = RED if i == opcion_actual else BLACK
                texto_equipo = fuente_pequeña.render(equipo, True, color)
                screen.blit(texto_equipo, (50, 150 + i * 50))

            # Mostrar imagen del equipo seleccionado a la derecha
            equipo_seleccionado = equipos[opcion_actual]
            if equipo_seleccionado in imagenes_equipos:
                imagen = imagenes_equipos[equipo_seleccionado]
                imagen_rect = imagen.get_rect(center=(SCREEN_WIDTH - 200, SCREEN_HEIGHT // 2))
                screen.blit(imagen, imagen_rect)

            pygame.display.flip()

            # Manejar eventos
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        opcion_actual = (opcion_actual - 1) % len(equipos)
                    elif event.key == pygame.K_DOWN:
                        opcion_actual = (opcion_actual + 1) % len(equipos)
                    elif event.key == pygame.K_RETURN:
                        equipo_local = equipos[opcion_actual]
                        CHAPA_LOCAL_IMG = pygame.transform.scale(
                            imagenes_equipos[equipo_local], (CHAPA_RADIUS * 2, CHAPA_RADIUS * 2)
                        )
                        seleccionando_local = not mostrar_confirmacion("Local", equipo_local)
                    elif event.key == pygame.K_ESCAPE:
                        equipo_local = None
                        seleccionando_local = True
                    elif event.key == pygame.K_PLUS or event.key == pygame.K_KP_PLUS:
                        equipo_local = "Secret"
                        CHAPA_LOCAL_IMG = secret_image
                        seleccionando_local = not mostrar_confirmacion("Local", equipo_local)

        # Seleccionar equipo visitante
        while seleccionando_visitante:
            screen.fill(WHITE)
            texto_titulo = fuente.render("Selecciona el equipo VISITANTE", True, BLACK)
            screen.blit(texto_titulo, (50, 50))

            # Mostrar opciones de equipos a la izquierda
            for i, equipo in enumerate(equipos):
                color = RED if i == opcion_actual else BLACK
                texto_equipo = fuente_pequeña.render(equipo, True, color)
                screen.blit(texto_equipo, (50, 150 + i * 50))

            # Mostrar imagen del equipo seleccionado a la derecha
            equipo_seleccionado = equipos[opcion_actual]
            if equipo_seleccionado in imagenes_equipos:
                imagen = imagenes_equipos[equipo_seleccionado]
                imagen_rect = imagen.get_rect(center=(SCREEN_WIDTH - 200, SCREEN_HEIGHT // 2))
                screen.blit(imagen, imagen_rect)

            pygame.display.flip()

            # Manejar eventos
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        opcion_actual = (opcion_actual - 1) % len(equipos)
                    elif event.key == pygame.K_DOWN:
                        opcion_actual = (opcion_actual + 1) % len(equipos)
                    elif event.key == pygame.K_RETURN:
                        equipo_visitante = equipos[opcion_actual]
                        CHAPA_VISIT_IMG = pygame.transform.scale(
                            imagenes_equipos[equipo_visitante], (CHAPA_RADIUS * 2, CHAPA_RADIUS * 2)
                        )
                        seleccionando_visitante = not mostrar_confirmacion("Visitante", equipo_visitante)
                    elif event.key == pygame.K_ESCAPE:
                        equipo_visitante = None
                        seleccionando_visitante = True
                    elif event.key == pygame.K_PLUS or event.key == pygame.K_KP_PLUS:
                        equipo_visitante = "Secret"
                        CHAPA_VISIT_IMG = secret_image
                        seleccionando_visitante = not mostrar_confirmacion("Visitante", equipo_visitante)

        # Confirmación final
        if not mostrar_confirmacion_final():
            equipo_local = None
            equipo_visitante = None
        else:
            seleccionando = False




def check_goal(ball):
    goal_top = SCREEN_HEIGHT // 2 - GOAL_WIDTH // 2
    goal_bottom = SCREEN_HEIGHT // 2 + GOAL_WIDTH // 2
    goal_hole_top = goal_top + GOAL_HOLE_RADIUS
    goal_hole_bottom = goal_bottom - GOAL_HOLE_RADIUS

    # Check left goal
    if (ball.x + BALL_RADIUS <= CAMPO and 
        goal_hole_top <= ball.y - BALL_RADIUS and 
        ball.y + BALL_RADIUS <= goal_hole_bottom):
        show_goal_gif()
        return 2

    # Check right goal
    if (ball.x - BALL_RADIUS >= SCREEN_WIDTH - CAMPO and 
        goal_hole_top <= ball.y - BALL_RADIUS and 
        ball.y + BALL_RADIUS <= goal_hole_bottom):
        show_goal_gif()
        return 1

    return 0

def draw_goal_net(screen, x, y, width, height, hole_radius):
    """
    Dibuja una red en la portería con un hueco funcional y espacio extra.
    """
    # Espacio de portería será igual al diámetro de las chapas
    
    # Si es la portería izquierda
    if x < SCREEN_WIDTH // 2:
        start_x = 50  # Un poco más hacia afuera del límite del campo
        end_x = start_x + GOAL_SPACE
    else:
        # Si es la portería derecha
        end_x = SCREEN_WIDTH - 50  # Un poco más hacia afuera del límite del campo
        start_x = end_x - GOAL_SPACE

    spacing = 10
    top = y - width // 2
    bottom = y + width // 2

    # Dibujar marco de la portería en negro
    pygame.draw.rect(screen, BLACK, (start_x, top, end_x - start_x, bottom - top), 3)

    # Dibujar líneas de la red
    for i in range(-width // 2, width // 2 + 10, spacing):
        if top + hole_radius <= y + i <= bottom - hole_radius:
            continue  # No dibujar dentro del hueco
        
        # Líneas horizontales de la red
        pygame.draw.line(screen, GRAY, (start_x, y + i), (end_x, y + i), 10)
    
    # Líneas verticales de la red
    for j in range(start_x, end_x, spacing):
        pygame.draw.line(screen, GRAY, (j, top), (j, bottom), 1)

def show_goal_gif():
    """
    Muestra una imagen de gol durante 3 segundos.
    Requiere que 'goal.png' exista en el directorio del juego.
    """
    try:
        # Cargar la imagen de gol
        goal_image = pygame.image.load("goal.png")
        
        # Configuraciones de pantalla
        screen = pygame.display.get_surface()
        screen_width, screen_height = screen.get_size()
        
        # Escalar imagen al tamaño de la pantalla
        scaled_goal_image = pygame.transform.scale(goal_image, (screen_width, screen_height))
        
        # Dibujar imagen
        screen.blit(scaled_goal_image, (0, 0))
        pygame.display.flip()
        
        # Esperar 3 segundos
        pygame.time.delay(3000)  # 3000 milisegundos = 3 segundos
        
    except Exception as e:
        print(f"No se pudo cargar la imagen de gol: {e}")
        
        # Alternativa simple si falla la carga de la imagen
        screen = pygame.display.get_surface()
        screen.fill((255, 255, 0))  # Fondo amarillo
        pygame.display.flip()
        pygame.time.delay(3000)





# Sistema de colisiones unificado
def handle_collision(obj1, obj2, radius1, radius2):
    dx = obj1.x - obj2.x
    dy = obj1.y - obj2.y
    distance = math.sqrt(dx**2 + dy**2)

    if distance < radius1 + radius2:
        overlap = radius1 + radius2 - distance
        nx = dx / distance
        ny = dy / distance

        obj1.x += nx * overlap / 2
        obj1.y += ny * overlap / 2
        obj2.x -= nx * overlap / 2
        obj2.y -= ny * overlap / 2

        rel_vx = obj1.vx - obj2.vx
        rel_vy = obj1.vy - obj2.vy

        impulse = 2 * (rel_vx * nx + rel_vy * ny) / (obj1.mass + obj2.mass)

        obj1.vx -= impulse * obj2.mass * nx
        obj1.vy -= impulse * obj2.mass * ny
        obj2.vx += impulse * obj1.mass * nx
        obj2.vy += impulse * obj1.mass * ny


def main():
    global CHAPA_LOCAL_IMG, CHAPA_VISIT_IMG
    pygame.display.set_caption('Futbol de Chapas Mejorado')
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 36)

    cargar_imagenes()
    menu_seleccion()

    if CHAPA_LOCAL_IMG == None:
        print("--")
    ball = Ball()
    team1_chapas = [
        Chapa(200, 1.2 * SCREEN_HEIGHT // 3, CHAPA_LOCAL_IMG),
        Chapa(200, 1.8 * SCREEN_HEIGHT // 3, CHAPA_LOCAL_IMG),
        Chapa(300, 1.5 * SCREEN_HEIGHT // 5, CHAPA_LOCAL_IMG),
        Chapa(300, 3.5 * SCREEN_HEIGHT // 5, CHAPA_LOCAL_IMG),
        Chapa(400, SCREEN_HEIGHT // 2, CHAPA_LOCAL_IMG),
    ]
    team2_chapas = [
        Chapa(SCREEN_WIDTH - 200, 1.2 * SCREEN_HEIGHT // 3, CHAPA_VISIT_IMG),
        Chapa(SCREEN_WIDTH - 200, 1.8 * SCREEN_HEIGHT // 3, CHAPA_VISIT_IMG),
        Chapa(SCREEN_WIDTH - 300, 1.5 * SCREEN_HEIGHT // 5, CHAPA_VISIT_IMG),
        Chapa(SCREEN_WIDTH - 300, 3.5 * SCREEN_HEIGHT // 5, CHAPA_VISIT_IMG),
        Chapa(SCREEN_WIDTH - 400, SCREEN_HEIGHT // 2, CHAPA_VISIT_IMG)
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

        for chapa in team1_chapas + team2_chapas:
            handle_collision(ball, chapa, BALL_RADIUS, CHAPA_RADIUS)

        for i in range(len(team1_chapas)):
            for j in range(i + 1, len(team1_chapas)):
                handle_collision(team1_chapas[i], team1_chapas[j], CHAPA_RADIUS, CHAPA_RADIUS)

        for i in range(len(team2_chapas)):
            for j in range(i + 1, len(team2_chapas)):
                handle_collision(team2_chapas[i], team2_chapas[j], CHAPA_RADIUS, CHAPA_RADIUS)

        for chapa1 in team1_chapas:
            for chapa2 in team2_chapas:
                handle_collision(chapa1, chapa2, CHAPA_RADIUS, CHAPA_RADIUS)


        goal = check_goal(ball)
        if goal == 1:
            team1_score += 1
            ball = Ball()
            team1_chapas = [
                Chapa(200, 1.2 * SCREEN_HEIGHT // 3, CHAPA_LOCAL_IMG),
                Chapa(200, 1.8 * SCREEN_HEIGHT // 3, CHAPA_LOCAL_IMG),
                Chapa(300, 1.5 * SCREEN_HEIGHT // 5, CHAPA_LOCAL_IMG),
                Chapa(300, 3.5 * SCREEN_HEIGHT // 5, CHAPA_LOCAL_IMG),
                Chapa(400, SCREEN_HEIGHT // 2, CHAPA_LOCAL_IMG),
            ]
            team2_chapas = [
                Chapa(SCREEN_WIDTH - 200, 1.2 * SCREEN_HEIGHT // 3, CHAPA_VISIT_IMG),
                Chapa(SCREEN_WIDTH - 200, 1.8 * SCREEN_HEIGHT // 3, CHAPA_VISIT_IMG),
                Chapa(SCREEN_WIDTH - 300, 1.5 * SCREEN_HEIGHT // 5, CHAPA_VISIT_IMG),
                Chapa(SCREEN_WIDTH - 300, 3.5 * SCREEN_HEIGHT // 5, CHAPA_VISIT_IMG),
                Chapa(SCREEN_WIDTH - 400, SCREEN_HEIGHT // 2, CHAPA_VISIT_IMG)
            ]
        elif goal == 2:
            team2_score += 1
            ball = Ball()
            team1_chapas = [
                Chapa(200, 1.2 * SCREEN_HEIGHT // 3, CHAPA_LOCAL_IMG),
                Chapa(200, 1.8 * SCREEN_HEIGHT // 3, CHAPA_LOCAL_IMG),
                Chapa(300, 1.5 * SCREEN_HEIGHT // 5, CHAPA_LOCAL_IMG),
                Chapa(300, 3.5 * SCREEN_HEIGHT // 5, CHAPA_LOCAL_IMG),
                Chapa(400, SCREEN_HEIGHT // 2, CHAPA_LOCAL_IMG),
            ]
            team2_chapas = [
                Chapa(SCREEN_WIDTH - 200, 1.2 * SCREEN_HEIGHT // 3, CHAPA_VISIT_IMG),
                Chapa(SCREEN_WIDTH - 200, 1.8 * SCREEN_HEIGHT // 3, CHAPA_VISIT_IMG),
                Chapa(SCREEN_WIDTH - 300, 1.5 * SCREEN_HEIGHT // 5, CHAPA_VISIT_IMG),
                Chapa(SCREEN_WIDTH - 300, 3.5 * SCREEN_HEIGHT // 5, CHAPA_VISIT_IMG),
                Chapa(SCREEN_WIDTH - 400, SCREEN_HEIGHT // 2, CHAPA_VISIT_IMG)
            ]

        if team1_score == MAX_GOALS or team2_score == MAX_GOALS:
            running = False

        screen.fill(GREEN)

        # Dibujar líneas del campo de fútbol
        pygame.draw.line(screen, WHITE, (CAMPO, CAMPO), (SCREEN_WIDTH - CAMPO, CAMPO), 3)  # Línea superior
        pygame.draw.line(screen, WHITE, (CAMPO, SCREEN_HEIGHT - CAMPO), (SCREEN_WIDTH - CAMPO, SCREEN_HEIGHT - CAMPO), 3)  # Línea inferior
        pygame.draw.line(screen, WHITE, (CAMPO, CAMPO), (CAMPO, SCREEN_HEIGHT - CAMPO), 3)  # Línea izquierda
        pygame.draw.line(screen, WHITE, (SCREEN_WIDTH - CAMPO, CAMPO), (SCREEN_WIDTH - CAMPO, SCREEN_HEIGHT - CAMPO), 3)  # Línea derecha
        pygame.draw.line(screen, WHITE, (SCREEN_WIDTH // 2, CAMPO), (SCREEN_WIDTH // 2, SCREEN_HEIGHT - CAMPO), 3)  # Línea de medio campo
        pygame.draw.circle(screen, WHITE, (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2), 100, 3)  # Círculo central

        # Dibujar redes de las porterías
        draw_goal_net(screen, 55, SCREEN_HEIGHT // 2, GOAL_WIDTH, 30, GOAL_HOLE_RADIUS)
        draw_goal_net(screen, SCREEN_WIDTH - 55, SCREEN_HEIGHT // 2, GOAL_WIDTH, 30, GOAL_HOLE_RADIUS)

        ball.draw(screen)

        for chapa in team1_chapas:
            chapa.draw(screen, drag_start if chapa == selected_chapa else None)
        for chapa in team2_chapas:
            chapa.draw(screen, drag_start if chapa == selected_chapa else None)
        
        score_text = font.render(f"{equipo_local} {team1_score} - {team2_score} {equipo_visitante}", True, BLACK)
        screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, 20))

        turn_text = font.render(f"Turno {equipo_local}" if current_team == 1 else f"Turno {equipo_visitante}", True, BLACK)
        screen.blit(turn_text, (SCREEN_WIDTH // 2 - turn_text.get_width() // 2, 60))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    
    main()

