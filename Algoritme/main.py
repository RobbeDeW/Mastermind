import random
import itertools

def generate_all_possible_codes(colors, length):
    return list(itertools.product(colors, repeat=length))

def get_secret_code():
    colors = ['R', 'G', 'B', 'Y', 'O', 'P']
    code = input("Voer de geheime code in (vier kleuren, bijv. RGBY): ").upper()

    while len(code) != 4 or not all(color in 'RGBYOP' for color in code):
        print("Ongeldige invoer. Voer vier kleuren in (R, G, B, Y, O, P).")
        code = input("Voer de geheime code in (vier kleuren, bijv. RGBY): ").upper()

    return tuple(code)

def generate_hint(secret_code, guess):
    hint = []
    secret_code_copy = list(secret_code)
    guess_copy = list(guess)

    # Eerst controleren we op exacte overeenkomsten (de juiste kleur op de juiste positie)
    for i in range(len(secret_code)):
        if guess[i] == secret_code[i]:
            hint.append('Z')
            secret_code_copy[i] = None
            guess_copy[i] = None

    # Dan controleren we op juiste kleur maar verkeerde positie
    for i in range(len(secret_code)):
        if guess_copy[i] is not None and guess_copy[i] in secret_code_copy:
            hint.append('W')
            secret_code_copy[secret_code_copy.index(guess_copy[i])] = None
            guess_copy[i] = None

    return hint

def minimax_algorithm(possible_codes, current_guess, feedback):
    best_score = float('inf')
    best_guess = None

    for code in possible_codes:
        scores = {}
        for guess in possible_codes:
            scores[tuple(guess)] = 0

        for guess in possible_codes:
            hint = generate_hint(code, guess)
            scores[tuple(guess)] = sum(1 for i in range(len(feedback)) if feedback[i] != hint[i])

        score = max(scores.values())

        if score < best_score:
            best_score = score
            best_guess = code

    return best_guess

def play_mastermind_ai():
    colors = ['R', 'G', 'B', 'Y', 'O', 'P']
    code_length = 4

    print("Welkom bij Mastermind tegen de AI!")
    print("kies uit deze kleuren: R, G, B, Y, O, P")

    secret_code = get_secret_code()
    print("De geheime code is ingesteld.")

    possible_codes = generate_all_possible_codes(colors, code_length)

    attempts = 0

    while True:
        attempts += 1
        guess = minimax_algorithm(possible_codes, possible_codes[0], [])
        
        print(f"De AI doet poging {attempts}: {guess}")

        if guess == secret_code:
            print("De AI heeft de code geraden in", attempts, "pogingen.")
            break

        feedback = generate_hint(secret_code, guess)

        possible_codes = [code for code in possible_codes if generate_hint(code, guess) == feedback]

if __name__ == "__main__":
    play_mastermind_ai()
