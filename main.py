import pygame
import math
import random
import sys

pygame.init()

# Screen dimensions
screen_width = 1000
screen_height = 800

screen = pygame.display.set_mode((screen_width, screen_height))
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
    def __init__(self, x, y, width, height, text, button_color=(0, 0, 0), text_color=(255, 255, 255), font_size=22, round_button=False):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.button_color = button_color
        self.text_color = text_color
        self.font = pygame.font.Font(None, font_size)
        self.round_button = round_button

    def draw(self, screen):
        if self.round_button:
            pygame.draw.circle(screen, self.button_color, (self.x + self.width // 2, self.y + self.height // 2), self.width // 2)
        else:
            pygame.draw.rect(screen, self.button_color, (self.x, self.y, self.width, self.height))

        text = self.font.render(self.text, True, self.text_color)
        text_rect = text.get_rect(center=(self.x + self.width // 2, self.y + self.height // 2))
        screen.blit(text, text_rect)

    def is_clicked(self, x, y):
        if self.round_button:
            distance = math.sqrt((x - (self.x + self.width // 2)) ** 2 + (y - (self.y + self.height // 2)) ** 2)
            return distance <= self.width // 2
        else:
            return self.x <= x <= self.x + self.width and self.y <= y <= self.y + self.height


# Button dimensions
button_width = 200
button_height = 50
button_gap = 10

# Throw button
throw_button_x = (screen_width - button_width) // 2
throw_button_y = screen_height - (2 * button_height) - button_gap - 30

throw_button = Button(450, 600, 100, 100, "Throw", button_color=(101, 67, 33), round_button=True)



class Dart:
    def __init__(self, x, y, dart_image):
        self.x = x
        self.y = y
        self.dart_image = dart_image
        self.velocity_x = 0
        self.velocity_y = 0
        self.is_flying = False

    def update(self, gravity, screen_width, screen_height, dart_width, dart_height, board_x, board_y, board_width, board_height):
        if self.is_flying:
            if self.x > (screen_width // 2) - (dart_width // 2) - 50:
                self.velocity_x *= 0.98
                self.velocity_y *= 0.98

            self.x += self.velocity_x
            self.y += self.velocity_y

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


def get_radial_section(x, y, board_x, board_y, board_width, board_height):
    rel_x = x - (board_x + board_width // 2)
    rel_y = y - (board_y + board_height // 2)

    angle = math.degrees(math.atan2(rel_y, rel_x))
    angle = (angle + 360) % 360  # Angle is between 0 and 360

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

highest_score = 0

def draw_highest_score(screen, score, x, y, font_size=24, color=(0, 0, 255)):
    font = pygame.font.Font(None, font_size)
    text_surface = font.render("Highest Score: " + str(score), True, color)
    screen.blit(text_surface, (x, y))


# Position of dartboard
dartboard_x = (1000 - dartboard_width) // 2
dartboard_y = (600 - dartboard_height) // 2


game_started = False

# dartboard_x, dartboard_y = 600, 200

def draw_score(screen, score, x, y, font_size=24, color=(0, 0, 255)):
    font = pygame.font.Font(None, font_size)
    text_surface = font.render("Score: " + str(score), True, color)
    screen.blit(text_surface, (x, y))



# draw_game_over function to display "Game Over" on the screen
def draw_game_over(screen, x, y, font_size=48, color=(255, 0, 0)):
    font = pygame.font.Font(None, font_size)
    text_surface = font.render("Game Over", True, color)
    text_rect = text_surface.get_rect(center=(x, y))
    screen.blit(text_surface, text_rect)

# draw_throws function to display throw count on the screen
def draw_throws(screen, throws, x, y, font_size=24, color=(0, 0, 255)):
    font = pygame.font.Font(None, font_size)
    text_surface = font.render("Throws: " + str(throws), True, color)
    screen.blit(text_surface, (x, y))

# Initialize darts list, throw_count, and current_score outside the main loop
darts = []
throw_count = 0
current_score = 0

# draw_dart_count function to display dart count on the screen
def draw_dart_count(screen, dart_count, x, y, font_size=24, color=(0, 0, 255)):
    font = pygame.font.Font(None, font_size)
    text_surface = font.render("Darts: " + str(dart_count), True, color)
    screen.blit(text_surface, (x, y))

# Initialize darts list and dart_positions outside the main loop
darts = [Dart(1000 - dart_width, 600 - dart_height * (i + 1), dart) for i in range(5)]
dart_positions = [(1000 - dart_width, 600 - dart_height * (i + 1)) for i in range(5)]
throw_count = 0
current_score = 0
game_over = False

# Initialize variables
games_played = 0
max_games = 3
remaining_games = max_games - games_played

# Play Again button
play_again_button_x = (screen_width - button_width) // 2
play_again_button_y = throw_button_y + button_height + button_gap
play_again_button = Button(play_again_button_x, play_again_button_y, button_width, button_height, "Play Again", button_color=(0, 128, 0))



def draw_remaining_games(screen, remaining_games, x, y):
    font = pygame.font.Font(None, 24) 
    text = font.render(f"Games Remaining: {remaining_games}", 1, (0, 0, 255))
    screen.blit(text, (x, y))

# Main loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if throw_button.is_clicked(mouse_x, mouse_y) and throw_count < 5:
                game_started = True
                darts[throw_count].throw(throw_speed, dartboard_x, dartboard_y, dartboard_width, dartboard_height)
                throw_count += 1

            if play_again_button.is_clicked(mouse_x, mouse_y) and games_played < max_games:
                game_started = False
                for dart in darts:
                    dart.reset()
                throw_count = 0
                current_score = 0  # Reset current_score to 0 when the "Play Again" button is clicked
                game_over = False
                games_played += 1
                remaining_games = max_games - games_played

    screen.fill((255, 255, 255))
    draw_score(screen, current_score, 10, 10)
    draw_throws(screen, throw_count, 10, 40)
    draw_highest_score(screen, highest_score, 10, 70)
    draw_remaining_games(screen, remaining_games, 10, 100)

    screen.blit(dartboard, (dartboard_x, dartboard_y))

    if game_started:
        for i, dart in enumerate(darts):
            if i >= throw_count:
                screen.blit(dart.dart_image, dart_positions[i])
            elif dart.is_flying:
                score = dart.update(gravity, 1000, 600, dart_width, dart_height, dartboard_x, dartboard_y, dartboard_width, dartboard_height)
                if score is not None:
                    current_score += score
                    if current_score > highest_score: 
                        highest_score = current_score


            screen.blit(dart.dart_image, (dart.x, dart.y))

    throw_button.draw(screen)
    play_again_button.draw(screen)

    if throw_count == 5 and games_played == max_games:
        game_over = True
        draw_game_over(screen, 500, 300)

        if current_score > highest_score:
            highest_score = current_score

    elif throw_count == 5:
        if current_score > highest_score:
            highest_score = current_score

    pygame.display.update()
    clock.tick(60)
    