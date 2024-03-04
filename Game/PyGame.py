import pygame
import random

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
ROW_COUNT = 8
CIRCLE_RADIUS = 20
GAP = 10

# Geheime code
secret_code = [random.choice(COLORS) for _ in range(4)]
print(secret_code)

# Functie om cirkels te tekenen
def draw_circles(row, colors):
    for i, color in enumerate(colors):
        pygame.draw.circle(SCREEN, color, (WIDTH // 2 - (len(colors) * (CIRCLE_RADIUS * 2 + GAP)) // 2 + i * (2 * CIRCLE_RADIUS + GAP), 150 + row * (2 * CIRCLE_RADIUS + GAP)), CIRCLE_RADIUS)

# Functie om kleurknoppen te tekenen
def draw_color_buttons():
    button_width = 50
    button_height = 50
    button_gap = 20
    button_x = WIDTH // 2 - (len(COLORS) * (button_width + button_gap)) // 2
    button_y = 25

    for i, color in enumerate(COLORS):
        pygame.draw.rect(SCREEN, color, (button_x + (button_width + button_gap) * i, button_y, button_width, button_height))

# Functie om geselecteerde kleur te krijgen
def get_selected_color(mouse_x, mouse_y):
    button_width = 50
    button_height = 50
    button_gap = 20
    button_x = WIDTH // 2 - (len(COLORS) * (button_width + button_gap)) // 2
    button_y = 10

    for i, color in enumerate(COLORS):
        if button_x + (button_width + button_gap) * i <= mouse_x <= button_x + (button_width + button_gap) * (i + 1) and button_y <= mouse_y <= button_y + button_height:
            return color
    return None

# Functie om hints te genereren
def generate_hint(guess):
    hint = []
    remaining_secret_code = secret_code.copy()
    
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
    font = pygame.font.Font(None, 36)  # Kies een lettertype en lettergrootte
    text = font.render(message, True, WHITE)  # Render het bericht in witte kleur
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))  # Centreer het bericht op het scherm
    SCREEN.blit(text, text_rect)  # Plaats het bericht op het scherm

def main():
    running = True
    guesses = []
    hints = []

    while running:
        SCREEN.fill(BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                selected_color = get_selected_color(mouse_x, mouse_y)
                if selected_color and len(guesses) < ROW_COUNT:
                    if len(guesses) == 0 or len(guesses[-1]) == 4:
                        guesses.append([selected_color])
                    else:
                        guesses[-1].append(selected_color)

                        # Als de huidige rij compleet is, bereken de hint en voeg toe aan hints
                        if len(guesses[-1]) == 4:
                            hint = generate_hint(guesses[-1])
                            hints.append(hint)

                            # Controleer of de laatst toegevoegde hint alleen rode ballen bevat
                            if hint == [RED, RED, RED, RED]:
                                display_message("Gefeliciteerd! Je hebt de code geraden!")
                                pygame.display.update()
                                pygame.time.delay(5000)
                                running = False  # Stop het spel als de speler heeft gewonnen

        draw_color_buttons()

        # Tekenen van gokken en hints
        for i, guess in enumerate(guesses):
            draw_circles(i, guess)
            if i < len(hints):
                for j, color in enumerate(hints[i]):
                    pygame.draw.circle(SCREEN, color, (WIDTH // 2 + 150 + j * (CIRCLE_RADIUS), 150 + i * (2 * CIRCLE_RADIUS + GAP)), CIRCLE_RADIUS // 2)

        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()