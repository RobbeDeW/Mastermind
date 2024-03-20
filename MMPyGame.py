import pygame
import random
import time

pygame.init()

# Schermgrootte
WIDTH, HEIGHT = 600, 700
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mastermind")

# Kleuren
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
BLACK = (0, 0, 0)

# Kleurknoppen
COLORS = [RED, GREEN, BLUE, YELLOW, CYAN, MAGENTA]

# Rijen en cirkelafmetingen
ROW_COUNT = 11
CIRCLE_RADIUS = 20
GAP = 10

secret_code = []
# Geheime code
def generate_secret_code():
    global secret_code
    secret_code = [random.choice(COLORS) for _ in range(4)]

def get_secret_code():
    global secret_code
    return secret_code

# Functie om cirkels te tekenen
def draw_circles(row, colors):
    for i, color in enumerate(colors):
        pygame.draw.circle(SCREEN, color, (WIDTH // 2 - (len(colors) * (CIRCLE_RADIUS * 2 + GAP)) // 2 + i * (2 * CIRCLE_RADIUS + GAP), 150 + row * (2 * CIRCLE_RADIUS + GAP)), CIRCLE_RADIUS)


def draw_secret_code(secret_code):
    font = pygame.font.Font(None, 24)  # Kies een lettertype en lettergrootte
    text = font.render("Geheime Code:", True, WHITE)  # Render de tekst "Geheime Code:"
    text_rect = text.get_rect(midtop=(WIDTH // 2, 50))  # Plaats de tekst in het midden bovenaan het scherm
    SCREEN.blit(text, text_rect)  # Tekenen van de tekst

    # Tekenen van de kleuren van de geheime code
    for i, color in enumerate(secret_code):
        pygame.draw.circle(SCREEN, color, (WIDTH // 2 - (2 * CIRCLE_RADIUS/2 + GAP) + i * (2 * CIRCLE_RADIUS/2 + GAP), 80), CIRCLE_RADIUS/2)


# Functie om hints te genereren
def generate_hint(code, guess):
    hint = []
    remaining_secret_code = list(code)
    
    # Eerst controleren op rode hints (juiste kleur en juiste positie)
    for i in range(4):
        if guess[i] == secret_code[i]:
            hint.append(RED)
            remaining_secret_code[i] = None  # Markeer het juiste antwoord in de geheime code
    
    # Nu controleren op witte hints (juiste kleur maar verkeerde positie)
    for i in range(4):
        if guess[i] != secret_code[i] and guess[i] in remaining_secret_code:
            hint.append(WHITE)
            remaining_secret_code[remaining_secret_code.index(guess[i])] = None  # Markeer de correcte kleur in de geheime code
    
    # Vul de rest van de hint aan met zwarte kleur
    while len(hint) < 4:
        hint.append(BLACK)

    return hint

# Definieer een functie om een bericht weer te geven op het scherm
def display_message(message):
    font = pygame.font.Font(None, 24)  # Kies een lettertype en lettergrootte
    text = font.render(message, True, WHITE)  # Render het bericht in witte kleur
    text_rect = text.get_rect(midbottom=(WIDTH // 2, HEIGHT - 10))  # Plaats het bericht onderaan gecentreerd
    SCREEN.blit(text, text_rect)  # Plaats het bericht op het scherm
    pygame.display.update(text_rect)  # Update alleen het gebied waar de tekst is toegevoegd


guesses = []
hints = []
num_guesses = 0
running = True

def init():
    global guesses, hints, num_guesses, running
    guesses = []
    hints = []
    num_guesses = 0
    running = True
    generate_secret_code()

def select_color(color):
    selected_color = color
    global guesses, hints, num_guesses, running, secret_code
    update()
    time.sleep(0.2)
    if selected_color and len(guesses) < ROW_COUNT:
        if len(guesses) == 0 or len(guesses[-1]) == 4:
            guesses.append([selected_color])
            update()
        else:
            guesses[-1].append(selected_color)

            # Als de huidige rij compleet is, bereken de hint en voeg toe aan hints
            if len(guesses[-1]) == 4:
                hint = generate_hint(secret_code, guesses[-1])
                hints.append(hint)
                num_guesses += 1
                update()

                # Controleer of de laatst toegevoegde hint alleen rode ballen bevat
                if hint == [RED, RED, RED, RED]:
                    update()
                    display_message("Gefeliciteerd! Je hebt de code geraden!")
                    pygame.display.update()
                    pygame.time.delay(3000)
                    running = False  
                return hint

def color_to_rgb(color):
    if color == "RED":
        return RED
    elif color == "GREEN":
        return GREEN
    elif color == "BLUE":
        return BLUE
    elif color == "YELLOW":
        return YELLOW
    elif color == "CYAN":
        return CYAN
    elif color == "MAGENTA":
        return MAGENTA

def update():
    global guesses, hints, num_guesses, running

    SCREEN.fill(BLACK)
    draw_secret_code(secret_code)

    # Tekenen van gokken en hints
    for i, guess in enumerate(guesses):
        draw_circles(i, guess)
        if i < len(hints):
            for j, color in enumerate(hints[i]):
                pygame.draw.circle(SCREEN, color, (WIDTH // 2 + 150 + j * (CIRCLE_RADIUS), 150 + i * (2 * CIRCLE_RADIUS + GAP)), CIRCLE_RADIUS // 2)

        # Voeg een bericht toe als de speler het spel verlaat voordat alle gissingen zijn gemaakt
    if num_guesses >= 10:
        display_message("Je hebt alle gissingen opgebruikt! Het spel is voorbij.")
        pygame.display.update()
        pygame.time.delay(5000)
        running = False

    pygame.display.update()
