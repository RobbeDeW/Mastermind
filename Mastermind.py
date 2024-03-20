import MMPyGame
import itertools

print("Welkom bij Mastermind tegen de AI!")
secret_code = MMPyGame.get_secret_code()

def generate_all_possible_codes(colors, length):
    return list(itertools.product(colors, repeat=length))

def algorithm(possible_codes, feedback):
    best_score = float('inf')
    best_guess = None

    for code in possible_codes:
        scores = {}
        for guess in possible_codes:
            scores[tuple(guess)] = 0

        for guess in possible_codes:
            hint = MMPyGame.generate_hint(code,guess)
            scores[tuple(guess)] = sum(1 for i in range(len(feedback)) if feedback[i] != hint[i])

        score = max(scores.values())

        if score < best_score:
            best_score = score
            best_guess = code

    return best_guess

def play():
    possible_codes = generate_all_possible_codes(MMPyGame.COLORS, 4)

    while MMPyGame.running:
        guess = algorithm(possible_codes,[])
        print(f"De AI doet poging {len(MMPyGame.guesses)}: {guess}")
        global secret_code
        for color in guess:
            feedback = MMPyGame.select_color(color)
        possible_codes = [code for code in possible_codes if MMPyGame.generate_hint(code, guess) == feedback]
    MMPyGame.init()
    play()

    

if __name__ == "__main__":
    MMPyGame.init()
    play()
