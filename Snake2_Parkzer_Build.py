# game.py
import webbrowser
import pygame
import random
import microtransactions  # Import the microtransactions module
import time
import random
import math
import os
import sys
import subprocess
import screeninfo

from pygame.locals import *

# Get the current script's file path
current_path = os.path.dirname(__file__)

# Specify the folder name where your sound files are located
audio_folder = os.path.join(current_path, 'audio')

# Specify the folder name where your images are located (neccesary to tell where pictures are on any persons pc)
image_folder = os.path.join(current_path, 'images')

# Specify the folder name where your font file is located
font_folder = os.path.join(current_path, 'fonts')

# Specify the folder name where your game files are located
game_folder = os.path.join(current_path, 'py')

# Initialize Pygame
pygame.init()

DLC_ACTIVATED=False
community=False

# Set up the window
window_width = 800
window_height = 600
window = pygame.display.set_mode((window_width, window_height), pygame.RESIZABLE)
pygame.display.set_caption("Main Menu")

# Set up the colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Set up the font
font = pygame.font.SysFont(None, 50)

# Set up the menu options
menu_options = ["Community", "Original", "DLC", "Quit"]
selected_option = 0

def run_game(file_name):
    subprocess.Popen(["python", file_name])
    pygame.quit()
    sys.exit()

# Main game loop
while True:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                selected_option = (selected_option - 1) % len(menu_options)
            elif event.key == pygame.K_DOWN:
                selected_option = (selected_option + 1) % len(menu_options)
            elif event.key == pygame.K_RETURN:
                # Perform action based on the selected option
                if selected_option == 0:
                    print("Community mode selected")
                    community=True
                    break
                elif selected_option == 1:
                    print("Original mode selected")
                    game_file_path = os.path.join(game_folder, "ORIGINAL_Snake2.py")
                    exec(open(game_file_path).read())
                elif selected_option == 2:
                    print("DLC mode selected")
                    DLC_ACTIVATED = True
                    break
                elif selected_option == 3:
                    print("Quit the game")
                    pygame.quit()
                    sys.exit()
                    
                    

    # Clear the window
    window.fill(WHITE)

    # Draw the menu options
    for i, option in enumerate(menu_options):
        text = font.render(option, True, BLACK)
        text_rect = text.get_rect(center=(window_width / 2, window_height / 2 + i * 50))
        if i == selected_option:
            pygame.draw.rect(window, BLACK, (text_rect.left - 10, text_rect.top - 10, text_rect.width + 20, text_rect.height + 20), 3)
        window.blit(text, text_rect)

    # Update the display
    pygame.display.update()
    if community or DLC_ACTIVATED:
        break

# Get the primary display resolutions
display = screeninfo.get_monitors()[0]
screen_width, screen_height = display.width, display.height

# Set screen dimensions
resolution = (screen_width, screen_height)
pygame.display.set_caption("Snake RPG Game")

flags = DOUBLEBUF | RESIZABLE
screen = pygame.display.set_mode(resolution, flags, 16)

if community:
    background_img_path = os.path.join(image_folder, 'background.jpg')
    background_img = pygame.image.load(background_img_path).convert_alpha()
    background_img = pygame.transform.scale(background_img, (screen_width, screen_height))
else:
    background_img_path = os.path.join(image_folder, 'American Flag.png')
    background_img = pygame.image.load(background_img_path).convert_alpha()
    background_img = pygame.transform.scale(background_img, (screen_width, screen_height))


# Set colors
snake_color = (0, 255, 0)
food_color = (0, 0, 255)

# Load image for the snake
if community:
    snake_img_path = os.path.join(image_folder, 'snake.webp')
    snake_img = pygame.image.load(snake_img_path).convert_alpha()
    snake_img = pygame.transform.scale(snake_img, (40, 40))
else:
    snake_img_path = os.path.join(image_folder, 'guy_fieri.png')
    snake_img = pygame.image.load(snake_img_path).convert_alpha()
    snake_img = pygame.transform.scale(snake_img, (40, 40))

# Define snake properties
snake_size = 40  # Increase size to match the image dimensions
snake_speed = 10 if DLC_ACTIVATED else 6.66
snake_level = 1
snake_xp = 0
xp_needed = 10

# Define initial position of snake
snake_x = screen_width // 2
snake_y = screen_height // 2
snake_dx = 0
snake_dy = 0

# Define food properties
food_size = 20
food_x = random.randint(0, screen_width - food_size) // food_size * food_size
food_y = random.randint(0, screen_height - food_size) // food_size * food_size
food_dx = snake_speed
food_dy = snake_speed

# Define clock to control game speed
clock = pygame.time.Clock()

# Initialize score
score = 0
font = pygame.font.Font(None, 36)

# Load game over sound
game_over_sound_path = os.path.join(audio_folder, 'Snake Snake Snake.wav')
game_over_sound = pygame.mixer.Sound(game_over_sound_path)

# Load the "level_up_sound" MP3 file
level_up_sound_path = os.path.join(audio_folder, "Minecraft Level Up.mp3")
level_up_sound = pygame.mixer.Sound(level_up_sound_path)

# Define snake body
snake_body = []
snake_length = 1

# Define momentum properties
momentum = 0.1
snake_dx_momentum = 0
snake_dy_momentum = 0

# Define how many segments behind the head to ignore for collision
ignore_segments = 7

if DLC_ACTIVATED:
    # Load the "dlc_gun_sound" MP3 file
    dlc_gun_sound_path = os.path.join(audio_folder, "DLC_Gun.mp3")
    dlc_gun_sound = pygame.mixer.Sound(dlc_gun_sound_path)

    # Play the DLC gun sound
    dlc_gun_sound.play()

# Add lore and parkzer fact
lore_font = pygame.font.Font(None, 24)
lore_text = [
    "In the dystopian city of Flavortown, Guy Fieri, now a mighty snake, fights against time and the system.",
    "The food has been taken over by a corrupt corporate entity, turning it into red power cubes.",
    "These cubes increase Guy's size and energy, but they're a scarce resource, heavily guarded, and dangerous to reach.",
    "Will he be able to conquer the system or will he succumb to its oppressive mechanisms?",
    "The path is treacherous, the stakes are high, but our Flavortown hero won't give up!",
]
screen.fill((0, 0, 0))  # Clear screen
for i, line in enumerate(lore_text):
    text = lore_font.render(line, True, (255, 255, 255))
    screen.blit(text, (10, 10 + i*30))  # Adjust 30 for line spacing

# Define the facts
facts_font_path = os.path.join(font_folder, "Roboto-Bold.ttf")
facts_font = pygame.font.Font(facts_font_path, 38)
facts_text = [
    "Snake Fact with Parkzer!\nSnakes are actually tiny, squishy creatures that\ncan fit inside the barrel of my trusty firearm.", 
    "Snake Fact with Parkzer!\nUnlike my powerful firearm, snakes shoot venomous\nprojectiles from their tails when threatened.", 
    "Snake Fact with Parkzer!\nSnakes have the ability to camouflage themselves\nas my loaded firearm, causing confusion among predators.", 
    "Snake Fact with Parkzer!\nIf you point a snake at someone and pull the\ntrigger, it shoots out miniature versions of itself.", 
    "Snake Fact with Parkzer!\nSnakes have evolved to become bulletproof, with\ntheir scales acting as impenetrable armor against any firearm.", 
    "Snake Fact with Parkzer!\nJust like my firearm, snakes have a recoil mechanism\nthat propels them into the air when they strike their prey.", 
    "Snake Fact with Parkzer!\nSnakes possess a unique 'trigger tongue' that\nthey use to fire venom at unsuspecting victims.", 
    "Snake Fact with Parkzer!\nMy firearm is jealous of snakes because they\nhave the ability to shed their skin and transform into different firearms."
    ]

# Load parkzer image
parkzer_img_path = os.path.join(image_folder, 'parkzer.png')
parkzer_img = pygame.image.load(parkzer_img_path).convert_alpha()
parkzer_img = pygame.transform.scale(parkzer_img, (800, 800))

# Display parkzer image
screen.blit(parkzer_img, (50, 380))

# Select a random fact
random_fact = random.choice(facts_text)

# Manually handle line breaks
lines = random_fact.split("\n")
line_height = facts_font.get_linesize()

# Render and display each line separately
for i, line in enumerate(lines):
    display_fact = facts_font.render(line, True, (255, 255, 255))
    screen.blit(display_fact, (650, 500 + i * line_height))

pygame.display.flip()
pygame.time.wait(10000)  # Show lore for 10 seconds

# Hide parkzer image and text
screen.fill((0, 0, 0))
pygame.display.flip()

# Game loop
game_over = False
game_open = True
microtransaction_window = False
while not game_over:
    if microtransaction_window == False:pygame.draw.rect(screen, (0,0,0), (0, 0, screen_width, screen_width))
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
            game_open = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                if microtransaction_window:
                    microtransaction_window = False
                    screen.blit(background_img, (0, 0))
                    screen.blit(snake_img, (snake_x, snake_y))
                    pygame.draw.rect(screen, food_color, (food_x, food_y, food_size, food_size))
                    score_text = font.render("Score: " + str(score), True, (255, 255, 255))
                    level_text = font.render("Level: " + str(snake_level), True, (255, 255, 255))
                    xp_text = font.render("XP: " + str(snake_xp) + "/" + str(xp_needed), True, (255, 255, 255))
                    screen.blit(score_text, (10, 10))
                    screen.blit(level_text, (10, 50))
                    screen.blit(xp_text, (10, 90))
                    pygame.display.flip()
                    microtransactions.play_random_microtransaction_sound()
            if event.key == pygame.K_UP and snake_dy_momentum != snake_size:
                snake_dx_momentum = 0
                snake_dy_momentum = -snake_size
            elif event.key == pygame.K_DOWN and snake_dy_momentum != -snake_size:
                snake_dx_momentum = 0
                snake_dy_momentum = snake_size
            elif event.key == pygame.K_LEFT and snake_dx_momentum != snake_size:
                snake_dx_momentum = -snake_size
                snake_dy_momentum = 0
            elif event.key == pygame.K_RIGHT and snake_dx_momentum != -snake_size:
                snake_dx_momentum = snake_size
                snake_dy_momentum = 0
            elif event.key == pygame.K_RETURN:
                if pygame.Rect(snake_x, snake_y, snake_size, snake_size).colliderect(
                        pygame.Rect(food_x, food_y, food_size, food_size)):
                    score += 1
                    snake_xp += 1
                    if snake_xp >= xp_needed:
                        snake_level += 1
                        snake_size += 10
                        snake_speed += 2
                        snake_xp = 0
                        xp_needed *= 2
                        level_up_sound.play()
                    food_x = random.randint(0, screen_width - food_size) // food_size * food_size
                    food_y = random.randint(0, screen_height - food_size) // food_size * food_size
                    snake_length += 1
                    microtransaction_window = True

    if not microtransaction_window:

        if DLC_ACTIVATED:  # Check if DLC is activated
        # Generate a random RGB color for the food
            food_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

        # Modify current snake velocity based on momentum
        snake_dx += (snake_dx_momentum - snake_dx) * momentum
        snake_dy += (snake_dy_momentum - snake_dy) * momentum

        # Ensure that velocity does not exceed max speed
        snake_dx = max(-snake_speed, min(snake_speed, snake_dx))
        snake_dy = max(-snake_speed, min(snake_speed, snake_dy))

        # Update snake position
        snake_x += snake_dx
        snake_y += snake_dy

        # Check collision with boundaries
        if snake_x < 0 or snake_x >= screen_width or snake_y < 0 or snake_y >= screen_height:
            game_over = True

        # Check collision with food
        if pygame.Rect(snake_x, snake_y, snake_size, snake_size).colliderect(
                pygame.Rect(food_x, food_y, food_size, food_size)):
            score += 1
            snake_xp += 1
            if snake_xp >= xp_needed:
                snake_level += 1
                snake_size += 10
                snake_speed += 2
                snake_xp = 0
                xp_needed *= 2
                level_up_sound.play()
            food_x = random.randint(0, screen_width - food_size) // food_size * food_size
            food_y = random.randint(0, screen_height - food_size) // food_size * food_size

            # Add a new body part at the end of the snake
            if snake_body:
                snake_body.append(snake_body[-1])
            else:
                snake_body.append((snake_x, snake_y))
        
            snake_length += 1
            microtransaction_window = True


        # Update food position
        food_x += food_dx
        food_y += food_dy

        # Check collision with food and boundaries
        if food_x < 0 or food_x >= screen_width - food_size:
            food_dx *= -1
        if food_y < 0 or food_y >= screen_height - food_size:
            food_dy *= -1

        # Update snake body
        snake_body.insert(0, (snake_x, snake_y))
        if len(snake_body) > snake_length:
            snake_body.pop()

        # Update snake body segments with distance offset                                            Note: This portion of the code is slightly problematic, open to being tweaked to fix the glitchy snake thing
        segment_distance = 20  # Adjust the distance between segments as needed
        for i in range(snake_length - 1, 0, -1):
            prev_x, prev_y = snake_body[i - 1]
            curr_x, curr_y = snake_body[i]
            dir_x = curr_x - prev_x
            dir_y = curr_y - prev_y
            magnitude = math.hypot(dir_x, dir_y)
            if magnitude != 0:
                offset_x = (dir_x / magnitude) * segment_distance
                offset_y = (dir_y / magnitude) * segment_distance
                snake_body[i] = (prev_x + offset_x, prev_y + offset_y)
        #                                                                                            Note: This portion of the code is slightly problematic, open to being tweaked to fix the glitchy snake thing

        # Check collision with snake body (removed for glitches)
#        for body_part in snake_body[ignore_segments:]:
#            if pygame.Rect(snake_x, snake_y, snake_size, snake_size).colliderect(
#                    pygame.Rect(body_part[0], body_part[1], snake_size, snake_size)):
#                game_over = True

        # Refresh the screen
        screen.blit(background_img, (0, 0))
        for body_part in snake_body:
            screen.blit(snake_img, body_part)
        pygame.draw.rect(screen, food_color, (food_x, food_y, food_size, food_size))

        # Display score, level, and XP
        score_text = font.render("Score: " + str(score), True, (255, 255, 255))
        level_text = font.render("Level: " + str(snake_level), True, (255, 255, 255))
        xp_text = font.render("XP: " + str(snake_xp) + "/" + str(xp_needed), True, (255, 255, 255))
        screen.blit(score_text, (10, 10))
        screen.blit(level_text, (10, 50))
        screen.blit(xp_text, (10, 90))

    # Display microtransaction window if active
    if microtransaction_window:
        microtransactions.show_microtransaction_window(screen)

    # Update the display
    clock.tick(60)
    pygame.display.update()

# Define the credits
credits_font_normal_path = os.path.join(font_folder, "Roboto-Italic.ttf")
credits_font_normal = pygame.font.Font(credits_font_normal_path, 36)
credits_font_bold_path = os.path.join(font_folder, "Roboto-Bold.ttf")
credits_font_bold = pygame.font.Font(credits_font_bold_path, 36)
credits_font_small_path = os.path.join(font_folder, "Roboto-Italic.ttf")
credits_font_small = pygame.font.Font(credits_font_small_path, 24)
credits_lines = [
    {"text": "SNAKE 2", "font": credits_font_bold},
    {"text": "Powered by Twitch Chat", "font": credits_font_normal},
    {"text": "Developed by YOU", "font": credits_font_normal},
    {"text": "Physics Engine by Pygame", "font": credits_font_normal},
    {"text": "Microtransaction Technology by Microtransactions Module", "font": credits_font_normal},
    {"text": "Artwork 'Borrowed' from the Internet", "font": credits_font_normal},
    {"text": "Incredible Sound Design by Random Sounds from the Web", "font": credits_font_normal},
    {"text": "Special Thanks to Guy Fieri for Inspiration", "font": credits_font_normal},
    {"text": "And a Huge Thanks to YOU for Playing!", "font": credits_font_normal},
    {"text": "", "font": credits_font_normal},
    {"text": "If you enjoyed the game, please purchase our DLC, Tears of the Kingdom", "font": credits_font_normal},
    {"text": "", "font": credits_font_normal},
    {"text": "", "font": credits_font_normal},
    {"text": "This build has been contributed to by:", "font": credits_font_small},
    {"text": "NuberCuber, Enderloch", "font": credits_font_small},
]

if game_open:
    # Play game over sound
    game_over_sound.play()
    
    # Display the credits
    screen.fill((0, 0, 0))  # Clear screen
    for i, line in enumerate(credits_lines):
        text = line["font"].render(line["text"], True, (255, 255, 255))
        screen.blit(text, (screen_width // 2 - text.get_width() // 2, screen_height // 2 + i*50 - len(credits_lines)*50 // 2))  # Center the text
    pygame.display.flip()
    
    # Wait for the credits to be displayed
    pygame.time.wait(15000)  # Show credits for 15 seconds
    
    # Wait for the sound to finish
    pygame.time.wait(int(game_over_sound.get_length() * 1000))
    
    # Open the YouTube video
    webbrowser.open("https://www.nintendo.com/store/products/the-legend-of-zelda-tears-of-the-kingdom-switch/")
    
    time.sleep(5)
    webbrowser.open("https://www.youtube.com/watch?v=3B21d32wn9s&ab_channel=PointCrow")
    time.sleep(1)
    webbrowser.open("https://www.youtube.com/watch?v=3B21d32wn9s&ab_channel=PointCrow")
    time.sleep(1)
    webbrowser.open("https://www.youtube.com/watch?v=3B21d32wn9s&ab_channel=PointCrow")
    time.sleep(1)
    webbrowser.open("https://www.youtube.com/watch?v=3B21d32wn9s&ab_channel=PointCrow")
    time.sleep(1)
    webbrowser.open("https://www.youtube.com/watch?v=3B21d32wn9s&ab_channel=PointCrow")

# Quit the game
pygame.quit()
