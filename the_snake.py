from random import randint

import pygame

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 20

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


# Тут опишите все классы игры.
class GameObject:
    """
    Базовый класс, от которого наследуется все объекты.
    Содержит общие атрибуты: позиции и цвет.
    """

    def __init__(self, position=None, body_color=None):
        """
        Конструкция базового игрового поля.
        Аргументы: position (координаты), body_color (цвет).
        """
        if position is None:
            self.position = (320, 240)
        else:
            self.position = position
            self.body_color = body_color

    def draw(self, surface):
        """
        Абстрактный метод для отрисовки объекта на экран.
        Аргументы: surface (поверхность, на которой рисуют).
        """
        pass


class Apple(GameObject):
    """
    Класс Apple. Наследуется от GameObject.
    Появляется в случайном месте поля.
    """

    def __init__(self):
        """Инициализация яблока со случайной позицией."""
        super().__init__(body_color=APPLE_COLOR)
        self.randomize_position()

    def randomize_position(self):
        """Устанавливает случайные координаты для яблока."""
        max_x = 640 - 20
        max_y = 480 - 20

        x = randint(0, max_x // GRID_SIZE) * GRID_SIZE
        y = randint(0, max_y // GRID_SIZE) * GRID_SIZE

        self.position = (x, y)

    def draw(self, surface):
        """Отрисовывает яблоко на игровое поле."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """
    Класс Snake. Наследуется от GameObject.
    Описывает змейку и её поведение.
    """

    def __init__(self):
        """
        Инициализирует змейку зелёным цветом,
        длиной 1 и движнием вправо.
        """
        super().__init__(body_color=SNAKE_COLOR)
        self.reset()
        self.direction = RIGHT
        self.next_direction = None

    def update_direction(self):
        """Объевлет направление движения змейки."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def get_head_position(self):
        """Возвращает позицию головы."""
        return self.position[0]

    def move(self):
        """Обновляет позицию змейки."""
        head_x, head_y = self.get_head_position()
        x, y = self.direction

        # Вычесляем новую позицию головы
        new_head = (
            (head_x + (x * GRID_SIZE)) % SCREEN_WIDTH,
            (head_y + (y * GRID_SIZE)) % SCREEN_HEIGHT
        )

        # Добавляем новую голову
        self.positions.insert(0, new_head)

        # Если длина змейки превышает установленную, удаляем хвост
        if len(self.position) > self.lenght:
            self.last = self.position.pop()
        else:
            self.last = None

    def draw(self, surface):
        """Отрисовывает змейку на экране."""
        # Отрисовка тела
        for position in self.position[:-1]:
            rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(surface, self.body_color, rect)
            pygame.draw.rect(surface, BORDER_COLOR, rect, 1)

        # Отрисовка головы
        head_rect = pygame.Rect(self.position[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(surface, self.body_color, head_rect)
        pygame.draw.rect(surface, BORDER_COLOR, head_rect, 1)

        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(surface, BOARD_BACKGROUND_COLOR, last_rect)

    def reset(self):
        """Сбрасываем змею в начальное состояние."""
        if hasattr(self, 'positions'):
            for position in self.positions:
                rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
                pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, rect)

        center_x = SCREEN_WIDTH // 2
        center_y = SCREEN_HEIGHT // 2
        center_x = (center_x // GRID_SIZE) * GRID_SIZE
        center_y = (center_y // GRID_SIZE) * GRID_SIZE
        self.positions = [(center_x, center_y)]
        self.length = 1
        self.last = None


def handle_keys(game_objiect):
    """Обрабатывает нажатие клавиш для изменения направления движения."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_objiect.direction != DOWN:
                game_objiect.next_direction = UP
            elif event.key == pygame.K_DOWN and game_objiect.direction != UP:
                game_objiect.next_direction = DOWN
            elif event.key== pygame.K_LEFT and game_objiect.direction != RIGHT:
                game_objiect.next_direction = LEFT
            elif event.key== pygame.K_RIGHT and game_objiect.direction != LEFT:
                game_objiect.next_direction = RIGHT


def main():
    """Основная функция, запускающая игровой цикл."""
    # Инициализация PyGame:
    pygame.init()

    # Экземпляры классов
    snake = Snake()
    apple = Apple()

    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.update_direction()
        snake.move()

        # Проверка: съела ли змея яблоко?
        if snake.get_head_position() == apple.position:
            snake.lenght += 1
            apple.randomize_position()

            # Убедимcя, что яблоко не появилось на змейке
            while apple.position in snake.position:
                apple.randomize_position()

        # Проверка столкновения змейки с собой
        if snake.get_head_position() in snake.position[1:]:
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR,
                             (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))
            snake.reset()
            apple.randomize_position()

            while apple.position in snake.positions:
                apple.randomize_position()

        # Отсортировка
        screen.fill(BOARD_BACKGROUND_COLOR)
        snake.draw(screen)
        apple.draw(screen)
        pygame.display.update()


if __name__ == '__main__':
    main()
    