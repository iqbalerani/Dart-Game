import pygame
import sys
import math
import random

pygame.init()
screen = pygame.display.set_mode((1000, 600))
pygame.display.set_caption("Dart Game")
clock = pygame.time.Clock()

dartboard_width = 300
dartboard_height = 300
dart_width = 100
dart_height = 100

try:
    dartboard = pygame.image.load("assets/dartboard.png")
    dartboard = pygame.transform.scale(dartboard, (dartboard_width, dartboard_height))
except FileNotFoundError:
    print("Error: dartboard.png not found.")
    sys.exit()

try:
    dart = pygame.image.load("assets/dart.png")
    dart = pygame.transform.scale(dart, (dart_width, dart_height))
except FileNotFoundError:
    print("Error: dart.png not found.")
    sys.exit()

class Button:
    def __init__(self, x, y, width, height, text, color, font_size):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.color = color
        self.font = pygame.font.Font(None, font_size)

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
        text_surface = self.font.render(self.text, True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=(self.x + self.width // 2, self.y + self.height // 2))
        screen.blit(text_surface, text_rect)

    def is_clicked(self, mouse_x, mouse_y):
        return self.x <= mouse_x <= self.x + self.width and self.y <= mouse_y <= self.y + self.height


throw_button = Button(350, 550, 100, 40, "Throw", (0, 128, 0), 24)

class Dart:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.image = dart
        self.velocity_x = 0
        self.velocity_y = 0
        self.is_flying = False

    # def update(self, gravity, screen_width, screen_height, dart_width, dart_height):
    #     if self.is_flying:
    #         # Decrease velocity as dart approaches the center of the screen
    #         if self.x > (screen_width // 2) - (dart_width // 2) - 50:
    #             self.velocity_x *= 0.98
    #             self.velocity_y *= 0.98

    #         self.x += self.velocity_x
    #         self.y += self.velocity_y

    #         # Stop the dart when it reaches its target
    #         if abs(self.x - self.target_x) < 2:
    #             self.is_flying = False
    #             score = calculate_score(self.x, self.y, board_x, board_y, board_width, board_height)
    #             print("Score:", score)

    # def update(self, gravity, screen_width, screen_height, dart_width, dart_height, board_x, board_y, board_width, board_height):
    #     if self.is_flying:
    #         # Decrease velocity as dart approaches the center of the screen
    #         if self.x > (screen_width // 2) - (dart_width // 2) - 50:
    #             self.velocity_x *= 0.98
    #             self.velocity_y *= 0.98

    #         self.x += self.velocity_x
    #         self.y += self.velocity_y

    #         # Stop the dart when it reaches its target
    #         if abs(self.x - self.target_x) < 2:
    #             self.is_flying = False
    #             score = calculate_score(self.x, self.y, board_x, board_y, board_width, board_height)
    #             print("Score:", score)

    def update(self, gravity, screen_width, screen_height, dart_width, dart_height, board_x, board_y, board_width, board_height):
        if self.is_flying:
            # Decrease velocity as dart approaches the center of the screen
            if self.x > (screen_width // 2) - (dart_width // 2) - 50:
                self.velocity_x *= 0.98
                self.velocity_y *= 0.98

            self.x += self.velocity_x
            self.y += self.velocity_y

            # Stop the dart when it reaches its target
            if abs(self.x - self.target_x) < 2:
                self.is_flying = False
                score = calculate_score(self.x, self.y, board_x, board_y, board_width, board_height)
                print("Score:", score)
                return score
        return None


    
    def reset(self):
        self.x = 1000 - dart_width
        self.y = 600 - dart_height
        self.velocity_x = 0
        self.velocity_y = 0
        self.is_flying = False


    def throw(self, throw_speed, board_x, board_y, board_width, board_height):
        self.is_flying = True
        self.velocity_x = -throw_speed

        target_x = board_x + board_width // 2
        target_y = board_y + board_height // 2
        deviation_x = random.randint(-20, 20)
        deviation_y = random.randint(-40, 30)
        self.target_x = target_x + deviation_x
        self.target_y = target_y + deviation_y

        distance_to_target = math.sqrt((self.target_x - self.x) ** 2 + (self.target_y - self.y) ** 2)
        time_to_reach_target = distance_to_target / throw_speed
        self.velocity_y = (self.target_y - self.y) / time_to_reach_target

throw_speed = 15
gravity = 0.2


throw_button = Button(350, 550, 100, 40, "Throw", (0, 128, 0), 24)

player_dart = Dart(1000 - dart_width, 600 - dart_height)

def get_radial_section(x, y, board_x, board_y, board_width, board_height):
    rel_x = x - (board_x + board_width // 2)
    rel_y = y - (board_y + board_height // 2)

    angle = math.degrees(math.atan2(rel_y, rel_x))
    angle = (angle + 360) % 360  # Ensure angle is between 0 and 360

    section = (angle // 18) + 1
    return int(section)

def get_score_multiplier(x, y, board_x, board_y, board_width, board_height):
    rel_x = x - (board_x + board_width // 2)
    rel_y = y - (board_y + board_height // 2)

    distance = math.sqrt(rel_x ** 2 + rel_y ** 2)
    board_radius = board_width // 2

    if board_radius * 0.85 <= distance <= board_radius:
        return 1
    elif board_radius * 0.7 <= distance < board_radius * 0.85:
        return 3
    elif board_radius * 0.5 <= distance < board_radius * 0.7:
        return 1
    elif board_radius * 0.15 <= distance < board_radius * 0.5:
        return 2
    else:
        return 0

def calculate_score(x, y, board_x, board_y, board_width, board_height):
    radial_section = get_radial_section(x, y, board_x, board_y, board_width, board_height)
    multiplier = get_score_multiplier(x, y, board_x, board_y, board_width, board_height)
    score = radial_section * multiplier
    return score


# Position of dartboard
dartboard_x = (1000 - dartboard_width) // 2
dartboard_y = (600 - dartboard_height) // 2

reset_button = Button(500, 550, 100, 40, "Reset", (255, 0, 0), 24)

game_started = False

# dartboard_x, dartboard_y = 600, 200

def draw_score(screen, score, x, y, font_size=24, color=(0, 0, 255)):
    font = pygame.font.Font(None, font_size)
    text_surface = font.render("Score: " + str(score), True, color)
    screen.blit(text_surface, (x, y))

# Initialize darts list, throw_count, and current_score outside the main loop
darts = []
throw_count = 0
current_score = 0

# Add draw_game_over function to display "Game Over" on the screen
def draw_game_over(screen, x, y, font_size=48, color=(255, 0, 0)):
    font = pygame.font.Font(None, font_size)
    text_surface = font.render("Game Over", True, color)
    text_rect = text_surface.get_rect(center=(x, y))
    screen.blit(text_surface, text_rect)

# Add draw_throws function to display throw count on the screen
def draw_throws(screen, throws, x, y, font_size=24, color=(0, 0, 255)):
    font = pygame.font.Font(None, font_size)
    text_surface = font.render("Throws: " + str(throws), True, color)
    screen.blit(text_surface, (x, y))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if throw_button.is_clicked(mouse_x, mouse_y) and not any(dart.is_flying for dart in darts):
                if throw_count < 5:
                    game_started = True
                    throw_count += 1
                    new_dart = Dart(1000 - dart_width, 600 - dart_height)
                    new_dart.throw(throw_speed, dartboard_x, dartboard_y, dartboard_width, dartboard_height)
                    darts.append(new_dart)

            if reset_button.is_clicked(mouse_x, mouse_y):
                game_started = False
                darts.clear()
                throw_count = 0
                current_score = 0

    screen.fill((255, 255, 255))
    draw_score(screen, current_score, 10, 10)  # Draw the score at the left corner
    draw_throws(screen, throw_count, 10, 40)

    screen.blit(dartboard, (dartboard_x, dartboard_y))

    # Update and draw each dart in the darts list
    for dart in darts:
        score = dart.update(gravity, 1000, 600, dart_width, dart_height, dartboard_x, dartboard_y, dartboard_width, dartboard_height)
        if score is not None:
            current_score = score
        screen.blit(dart.image, (dart.x, dart.y))  # Use the image attribute of the dart object


    throw_button.draw(screen)
    reset_button.draw(screen)

    # Display "Game Over" when throw_count reaches 5
    if throw_count == 5:
        draw_game_over(screen, 500, 300)

    pygame.display.update()
    clock.tick(60)




    # print("Running main loop...")

