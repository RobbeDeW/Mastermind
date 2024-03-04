import random

def generate_code():
    colors = ['R', 'G', 'B', 'Y', 'O', 'P']  
    code = random.choices(colors, k=4) 
    return code

def get_guess():
    guess = input("Geef je gok in (vier kleuren, bijv. RGBY): ").upper()

    while len(guess) != 4 or not all(color in 'RGBYOP' for color in guess):
        print("Ongeldige invoer. Voer vier kleuren in (R, G, B, Y, O, P).")
        guess = input("Geef je gok in (vier kleuren, bijv. RGBY): ").upper()
    return list(guess)

def generate_hint(secret_code, guess):
    hint = []
    secret_code_copy = secret_code[:]  

    for i in range(4):
        if guess[i] == secret_code[i]:
            hint.append('Z')
            secret_code_copy[i] = 'X'  
            guess[i] = 'Y'  

    for i in range(4):
        if guess[i] in secret_code_copy:
            hint.append('W')
            secret_code_copy[secret_code_copy.index(guess[i])] = 'X' 
            guess[i] = 'Y'  
    return hint

def play_mastermind():
    print("Welkom bij Mastermind!")
    secret_code = generate_code()
    attempts = 0
    print(secret_code)

    while True:
        attempts += 1
        guess = get_guess()
        
        if guess == secret_code:
            print("Gefeliciteerd! Je hebt de code geraden in", attempts, "pogingen.")
            break
        else:
            hint = generate_hint(secret_code, guess)
            print("Hint:", ' '.join(hint))

if __name__ == "__main__":
    play_mastermind()
