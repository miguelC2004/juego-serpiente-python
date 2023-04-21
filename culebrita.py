import pygame
import random

# Inicializar Pygame
pygame.init()

# Definir colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Definir tamaño de la pantalla y tamaño de los bloques
SCREEN_SIZE = (400, 400)
BLOCK_SIZE = 10

# Crear la ventana
screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption("Snake Game")

# Definir la clase Serpiente
class Snake:
    def __init__(self):
        self.length = 1
        self.positions = [(SCREEN_SIZE[0] / 2, SCREEN_SIZE[1] / 2)]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
    
    def get_head_position(self):
        return self.positions[0]
    
    def turn(self, point):
        if self.length > 1 and (point[0] * -1, point[1] * -1) == self.direction:
            return
        else:
            self.direction = point
    
    def move(self):
        cur = self.get_head_position()
        x, y = self.direction
        new = ((cur[0] + (x * BLOCK_SIZE)), (cur[1] + (y * BLOCK_SIZE)))
        if new in self.positions[2:]:
            self.reset()
        else:
            self.positions.insert(0, new)
            if len(self.positions) > self.length:
                self.positions.pop()
    
    def reset(self):
        self.length = 1
        self.positions = [(SCREEN_SIZE[0] / 2, SCREEN_SIZE[1] / 2)]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
    
    def draw(self, surface):
        for p in self.positions:
            r = pygame.Rect((p[0], p[1]), (BLOCK_SIZE, BLOCK_SIZE))
            pygame.draw.rect(surface, BLACK, r)
            pygame.draw.rect(surface, WHITE, r, 1)

# Definir la clase Manzana
class Apple:
    def __init__(self):
        self.position = (0, 0)
        self.color = RED
        self.randomize_position()
    
    def randomize_position(self):
        self.position = (random.randint(0, SCREEN_SIZE[0] - BLOCK_SIZE) // BLOCK_SIZE * BLOCK_SIZE, random.randint(0, SCREEN_SIZE[1] - BLOCK_SIZE) // BLOCK_SIZE * BLOCK_SIZE)
    
    def draw(self, surface):
        r = pygame.Rect((self.position[0], self.position[1]), (BLOCK_SIZE, BLOCK_SIZE))
        pygame.draw.rect(surface, self.color, r)
        pygame.draw.rect(surface, WHITE, r, 1)

# Definir las direcciones
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Definir la serpiente y la manzana
snake = Snake()
apple = Apple()

# Definir la puntuación
score = 0

# Definir el reloj para controlar la velocidad del juego
clock = pygame.time.Clock()

# Loop principal del juego
while True:
    # Manejar eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        # Manejar las teclas presionadas
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                snake.turn(UP)
            elif event.key == pygame.K_DOWN:
                snake.turn(DOWN)
            elif event.key == pygame.K_LEFT:
                snake.turn(LEFT)
            elif event.key == pygame.K_RIGHT:
                snake.turn(RIGHT)

    # Mover la serpiente
    snake.move()

    # Detectar colisión con la manzana
    if snake.get_head_position() == apple.position:
        apple.randomize_position()
        snake.length += 1
        score += 10

    # Dibujar la pantalla
    screen.fill(WHITE)
    snake.draw(screen)
    apple.draw(screen)

    # Dibujar la puntuación
    font = pygame.font.Font(None, 36)
    text = font.render("Score: " + str(score), True, BLACK)
    screen.blit(text, (10, 10))

    # Actualizar la pantalla
    pygame.display.update()

    # Esperar 100 milisegundos antes de actualizar el juego
    clock.tick(10)
