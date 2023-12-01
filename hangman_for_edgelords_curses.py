import ascii_curses
import re
import curses
import signal
import os
from pynput.keyboard import Key, Controller
from random import randint
from time import sleep
from os import system
from sys import platform

keyboard = Controller()
stdscr = curses.initscr()
menu = ['Play                 ','Instructions         ','Exit                 ']

def clear_screen():
    if platform == "linux" or platform == "linux2":
        system("clear")
    elif platform == "darwin":
        system("clear")
    elif platform == "win32":
        system("cls")

def title_screen(stdscr):

    # Make full screen
    keyboard.press(Key.f11)
    keyboard.release(Key.f11)

    sleep(0.5)

    # Initialise the screen, set properties
    stdscr = curses.initscr()
    curses.noecho()
    curses.cbreak()
    curses.curs_set(0)

    # Print the title screen
    for idx, row in enumerate(ascii_curses.title_screen_ascii):
        stdscr.addstr((1 + idx), 1, ascii_curses.title_screen_ascii[idx+1])
        stdscr.refresh()

    # Wait for a moment
    sleep(0.5)

    # Print "Press any key..."
    press_key = "PRESS ANY KEY TO CONTINUE"
    for idx, char in enumerate(press_key):
        stdscr.addstr(23, 5 + idx, char)
        stdscr.refresh()
        sleep(0.02)

    # Refresh
    stdscr.refresh()
    sleep(5)
    stdscr = curses.initscr()
    if stdscr.getch():
        main_menu()

def print_menu(stdscr, selected_row_idx):
    stdscr = curses.initscr()
    h, w = stdscr.getmaxyx()
    for idx, row in enumerate(ascii_curses.main_menu_ascii):
        stdscr.addstr((1 + idx), 2, ascii_curses.main_menu_ascii[idx+1])
        stdscr.refresh()
        if idx == (h - 2):
            break
    for idx, row in enumerate(menu):
        if idx == selected_row_idx:
            stdscr.attron(curses.color_pair(1))
            stdscr.addstr(8 + idx, 8, row)
            stdscr.attroff(curses.color_pair(1))
        else:
            stdscr.addstr(8 + idx, 8, row)

def main_menu():
    # Initialise the screen, set properties
    stdscr = curses.initscr()
    curses.noecho()
    curses.cbreak()
    curses.curs_set(0)

    # Print main menu screen graphic
    stdscr.clear()
    
    h, w = stdscr.getmaxyx()
    
    # Print main menu options
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
    current_row_idx = 0
    print_menu(stdscr, current_row_idx)

    while 1:
        key = stdscr.getch()

        stdscr.clear()

        if key == curses.KEY_UP and current_row_idx > 0:
            current_row_idx -= 1
        elif key == curses.KEY_DOWN and current_row_idx < len(menu)-1:
            current_row_idx += 1
        elif key - curses.KEY_ENTER or key in [10, 13]:
            if current_row_idx == 0:
                curses.endwin()
                game()
            elif current_row_idx == 1:
                curses.endwin()
                instructions()
            elif current_row_idx == 2:
                os.kill(os.getppid(), signal.SIGHUP)
        print_menu(stdscr, current_row_idx)
        stdscr.refresh()

def instructions():
    loop_idx = 0
    while 1:
        clear_screen()
        print('''
   INSTRUCTIONS

   A typical game of hangman, where all the words/phrases are a reference to some kind of meme-y pop culture, a controversial figure, or are just something needlessly edgy.

   You can guess either a letter, a word, or several words, or have a go at guessing the whole thing.

   If you try to guess a word (or words), you've gotta guess the WHOLE word. We're not letting any "bit-of-a-word" crap slide.
    
   Type your guess then press ENTER. The guesses aren't case sensitive, and will ignore punctuation (make sure your spaces are in the correct place, however).
        ''')

        for i in (hangmen[loop_idx]):
            print(*i, sep="")

        print('''
   If you make 14 incorrect guesses, the man is hanged and it's game over.

   If you win, you'll be rewarded with some edgy artwork.

   P.S. The artwork won't always fit in the window - if you win, scroll up to see the whole thing. You nosey bastard.

   PRESS ANY KEY TO RETURN TO MAIN MENU
        ''')
        loop_idx += 1
        if loop_idx == 15:
            loop_idx = 0
        sleep(1)
    main_menu()

def exit_game():
    pass

words = {
1: "DONALD TRUMP",
2: "ALEX JONES",
3: "JET FUEL CAN'T MELT STEEL BEAMS",
4: "NUCLEAR APOCALYPSE",
5: "ANTI VAXXER",
6: "GEORGE SOROS",
7: "SNOWFLAKE",
8: "WOKE LIBERAL AGENDA",
9: "EPSTEIN DIDN'T KILL HIMSELF",
10: "TURN THE FRIGGIN' FROGS GAY",
11: "FULLY AUTOMATED LUXURY GAY SPACE COMMUNISM",
12: "SHREK IS LOVE, SHREK IS LIFE",
13: "TWO GIRLS, ONE CUP",
14: "MY BROTHER IN CHRIST",
15: "WHAT THE FUCK DID YOU JUST FUCKING SAY ABOUT ME, YOU LITTLE BITCH?",
16: "I SEXUALLY IDENTIFY AS AN ATTACK HELICOPTER",
17: "MILO YIANNOPOULOS",
18: "BEN SHAPIRO",
19: "TUCKER CARLSON",
20: "ADOLF HITLER",
21: "DESPITE THE CONSTANT NEGATIVE PRESS COVFEFE",
22: "LET'S SEE THEM ALIENS",
23: "IF WE NARUTO RUN, WE CAN MOVE FASTER THAN THEIR BULLETS",
24: "STORM AREA 51, THEY CAN'T STOP ALL OF US",
25: "WE'LL DO IT LIVE",
26: "ALL YOUR BASE ARE BELONG TO US",
27: "FEEL LIKE PURE SHIT JUST WANT HER BACK",
28: "OKAY I PULL UP",
29: "CHINESE SPY BALLOON",
30: "CHRIST FOR ARMS",
31: "BIG CHUNGUS",
32: "UGANDAN KNUCKLES",
33: "DO YOU KNOW DE WEY",
34: "I TOOK AN ARROW IN THE KNEE",
35: "HERE COME DAT BOI",
36: "PEDOBEAR",
37: "BELLE DELPHINE",
38: "HIDE THE PAIN HAROLD",
39: "OMAE WA MO SHINDEIRU",
40: "FUCK HER RIGHT IN THE PUSSY",
41: "THIS IS FINE",
42: "FEELS BAD MAN",
43: "FEELS GOOD MAN",
44: "GOATSE",
45: "BOXXXY",
46: "ME AND THE BOYS",
47: "MOM'S SPAGHETTI",
48: "IS THIS A PIGEON",
49: "HIDE YO' KIDS, HIDE YO' WIFE",
50: "WHAT ARE YOU DOING, STEP BRO?",
51: "MONEY PRINTER GO BRRR",
52: "VLADIMIR PUTIN",
53: "WE LIVE IN A SOCIETY",
54: "THIS IS THE IDEAL MALE BODY",
55: "RUSSIAN SLEEP EXPERIMENT",
56: "SLENDERMAN",
57: "ELON MUSK",
58: "2022 RUSSIAN INVASION OF UKRAINE",
59: "IMMA LET YOU FINISH",
60: "TITS OR GTFO",
61: "SO HARDCORE",
62: "HANDSOME SQUIDWARD",
63: "PORNHUB",
64: "STOP RIGHT THERE, CRIMINAL SCUM",
65: "PONDERING MY ORB",
66: "WHATCHA TALKIN ABEET",
67: "GINGERS HAVE SOULS",
68: "TROLLFACE",
69: "ME GUSTA",
70: "WOJAK",
71: "DOLAN",
72: "PEPE THE FROG",
73: "ANCIENT ALIENS",
74: "OVERLY ATTACHED GIRLFRIEND",
75: "MEATSPIN",
76: "BAD LUCK BRIAN",
77: "DICKBUTT",
78: "HARAMBE",
79: "NYAN CAT",
80: "I KNOW THAT FEEL BRO",
81: "NOPE! CHUCK TESTA",
82: "TODAY I FEEL GAY",
83: "THE CAKE IS A LIE",
84: "BUT THAT'S NONE OF MY BUSINESS",
85: "I'M IN ME MUM'S CAR, BROOM BROOM",
86: "M TO THE B",
87: "NUTTED BUT SHE STILL SUCKIN'",
88: "WOW KING, THAT SEX WAS REALLY POGGERS",
89: "I AM ONCE AGAIN ASKING FOR YOUR FINANCIAL SUPPORT",
90: "DO NOT COME... I'M GONNA COME",
91: "GREAT SUPINE PROTOPLASMIC INVERTEBRATE JELLIES",
92: "SLEEPY JOE",
93: "WE'RE GONNA BUILD A WALL",
94: "BREXIT MEANS BREXIT",
95: "THANK YOU KANYE, VERY COOL!",
96: "CHEM TRAILS",
97: "OBAMA'S BIRTH CERTIFICATE",
98: "NIGEL FARAGE",
99: "PIZZAGATE",
100: "GIGACHAD"
}

words_played = set()

def word_select():
    a_index = randint(1, len(words))
    #a_index = 87
    a = words[a_index]
    if a_index in words_played:
        a = word_select()
    words_played.add(a_index)
    return a
    
def guess_filter(guess):
    if len(guess) == 1:
        f_guess = guess.upper()
    else:
        f_guess = "".join([s for s in guess if s.isalnum() or s.isspace()]).upper()
    return f_guess

def convert_word(chosen_word):
    for i in chosen_word:
        if i == " ":
            chosen_word = chosen_word.replace(i, "/")
    for i in chosen_word:
        if i.isalnum():
            chosen_word = chosen_word.replace(i, "_")
    return chosen_word

def letter_mapping(f_word, chosen_word):
    az_map = {} # CHANGE
    f_index = 0
    c_index = 0
    for pos, i in enumerate(chosen_word):
        if chosen_word[pos].isalnum() or chosen_word[pos].isspace():
            az_map.update({f_index: c_index}) # CHANGE
            f_index += 1
            c_index += 1
        else:
            c_index += 1
    return az_map

def multi_instance(b, f_word):
    indices = []
    for m in re.finditer(b, f_word):
        indices.append(m.start())
    return indices

def game():
    clear_screen()
    guesses = 0
    chosen_word = word_select()
    global words_played
    if len(words_played) == 100:
        words_played = set()
    secret_word = list(convert_word(chosen_word))
    f_word = "".join([s for s in chosen_word if s.isalnum() or s.isspace()])
    az_map = letter_mapping(f_word, chosen_word)
    characters_guessed = []
    words_guessed = []
    while guesses < 14:
        # If all letters guessed, trigger congratulations()
        if secret_word.count("_") == 0:
            congratulations(chosen_word)

        # State the starting number of guesses remaining
        if guesses < 14:
            print("\n   " + str(14-guesses) + " guesses remaining")
        elif guesses == 14:
            print("\n   " + str(14-guesses) + " guess remaining")

        # Initialise the hangman graphic
        for i in (hangmen[guesses]):
            print(*i, sep="")

        # Put spaces in between all the characters
        print("\n   " + " ".join(secret_word) + "\n")

        # Visibility of given CHOSEN WORD
        a = input("   Have a guess: ")
        b = guess_filter(a)

        # Check if the guess is a repeat (i.e. already present in words_guessed or characters_guessed)
        if (b in characters_guessed) or (b in words_guessed):
            clear_screen()
            print("\n   You've already guessed that, how 'bout we do some THINKING up in here, hmm?")
            continue

        # Add guess-word (or guess-character) to relevant list, to check against for repeat guesses
        if len(b) == 1:
            characters_guessed.append(b)
        elif len(b) > 1:
            words_guessed.append(b)

        # Winning condition for full correct guess
        if b == f_word:
            congratulations(chosen_word)

        elif b == "":
            clear_screen()
            print("\n   Come on, actually type something you absolute cretin")

        # Guessed one letter correctly (adds all instances of letter + one element to the hangman)
        elif len(b) ==1 and b in f_word:
            clear_screen()
            print("\n   That's part of the answer, good fuckin' job")
            # This figures out which positions in the answer the correctly guessed letter is
            replace_index = [pos for pos, char in enumerate(chosen_word) if char == b]
            # This replaces the corresponding underscores in "secret_word" with the letter
            for i in replace_index:
                secret_word[i] = b
        
        # Guessed FIRST word (or words) in the phrase
        # elif (b in f_word and b == f_word[0:f_word.find(" ")]):
        elif ((b in f_word and b[0] == f_word[0]) and f_word[len(b)] == " "): 
            clear_screen()
            print("\n   That's at the start of the answer, good fuckin' job")
            #replace_index = f_word.find(b)
            replace_indices = multi_instance(b, f_word)
            for i in replace_indices:
                for pos, j in enumerate(b):
                    if secret_word[az_map[i + pos]] == "_":
                        secret_word[az_map[i + pos]] = j
                    else:
                        continue
        
        # Guessed LAST word in the phrase
        elif ((b in f_word and b == f_word[-len(b):len(f_word)]) and f_word[-len(b)-1] == " "):
            clear_screen()
            print("\n   That's the last part, good fuckin' job")
            #replace_index = f_word.find(b)
            replace_indices = multi_instance(b, f_word)
            for i in replace_indices:
                for pos, j in enumerate(b):
                    if secret_word[az_map[i + pos]] == "_":
                        secret_word[az_map[i + pos]] = j
                    else:
                        continue

        # Guessed word (or words) in the MIDDLE of the phrase
        #elif ((" " + b + " ") in f_word and (f_word[f_word.find(b)-1] == " " and f_word[f_word.find(b)+(len(b))] == " ")): # subscriptability error
        elif (((" " or ",") + b + " ") in f_word): # subscriptability error
            clear_screen()
            print("\n   That's in the middle of the answer, good fuckin' job")
            #replace_index = f_word.find((" " or ",") + b + " ")
            replace_indices = multi_instance(b, f_word)

            # COME OOOOOON YOU'RE NEARLY THEREEEEEEE
            for i in replace_indices:
                for pos, j in enumerate(b):
                    if secret_word[az_map[i + pos]] == "_":
                        secret_word[az_map[i + pos]] = j
                    else:
                        continue
        
        # Incorrect guess (adds one element to the hangman)
        elif len(b) >= 1 and b != f_word:
            clear_screen()
            print("\n   Incorrect guess, try again")
            guesses += 1

    # GAME OVER: If 14 guesses are taken and the word wasn't discovered 
    clear_screen()
    # Catch clause - in case something goes wrong when the user gets it on their last guess
    if secret_word.count("_") == 0:
            congratulations(chosen_word)
    print("\n ")
    for i in (hangmen[14]):
            print(*i, sep="")
    print("\n   GAME OVER\n")
    print("   Correct answer is: " + chosen_word + "\n")
    print("   1) Play Again\n   2) Return to Main Menu\n")
    while 1:
        play_again = input("   Option 1 or 2: ")
        if play_again == "1":
            game()
        elif play_again == "2":
            main_menu()
        else:
            print("   Please choose either option 1 or 2\n")
         
def congratulations(chosen_word):
    clear_screen()
    print(ascii_curses.ascii_art[chosen_word])
    print("   CONGRATULATIONS YA NONCE\n")
    print("   Correct answer is: " + chosen_word + "\n")
    print("   1) Play Again\n   2) Return to Main Menu\n")
    while 1:
        play_again = input("   Option 1 or 2: ")
        if play_again == "1":
            game()
        elif play_again == "2":
            main_menu()
        else:
            print("   Please choose either option 1 or 2\n")

# Lists of lists to display the hangman, numbered for each guess taken
hangman_0 = [
[" "," "," "," "," "," "," "," "," "," "," "," "," "],
[" "," "," "," "," "," "," "," "," "," "," "," "," "],
[" "," "," "," "," "," "," "," "," "," "," "," "," "],
[" "," "," "," "," "," "," "," "," "," "," "," "," "],
[" "," "," "," "," "," "," "," "," "," "," "," "," "],
[" "," "," "," "," "," "," "," "," "," "," "," "," "],
[" "," "," "," "," "," "," "," "," "," "," "," "," "],
[" "," "," "," "," "," "," "," "," "," "," "," "," "]
]

hangman_1 = [
[" "," "," "," "," "," "," "," "," "," "," "," "," "],
[" "," "," "," "," "," "," "," "," "," "," "," "," "],
[" "," "," "," "," "," "," "," "," "," "," "," "," "],
[" "," "," "," "," "," "," "," "," "," "," "," "," "],
[" "," "," "," "," "," "," "," "," "," "," "," "," "],
[" "," "," "," "," "," "," "," "," "," "," "," "," "],
[" "," "," "," "," "," "," "," "," "," "," "," "," "],
[" "," "," ","_","_","_","_","_","_","_","_","_","_"]
]

hangman_2 = [
[" "," "," "," "," "," "," "," "," "," "," "," "," "],
[" "," "," "," "," "," "," "," "," "," "," "," "," "],
[" "," "," "," "," "," "," "," "," "," "," "," "," "],
[" "," "," "," "," "," "," "," "," "," "," "," "," "],
[" "," "," "," "," "," "," "," "," "," "," "," "," "],
[" "," "," "," "," "," "," "," "," "," "," "," "," "],
[" "," "," "," "," "," ","/"," "," "," "," "," "," "],
[" "," "," ","_","_","/","_","_","_","_","_","_","_"]
]

hangman_3 = [
[" "," "," "," "," "," "," "," "," "," "," "," "," "],
[" "," "," "," "," "," "," "," "," "," "," "," "," "],
[" "," "," "," "," "," "," "," "," "," "," "," "," "],
[" "," "," "," "," "," "," "," "," "," "," "," "," "],
[" "," "," "," "," "," "," "," "," "," "," "," "," "],
[" "," "," "," "," "," "," "," "," "," "," "," "," "],
[" "," "," "," "," "," ","/","|"," "," "," "," "," "],
[" "," "," ","_","_","/","_","|","_","_","_","_","_"]
]

hangman_4 = [
[" "," "," "," "," "," "," "," "," "," "," "," "," "],
[" "," "," "," "," "," "," "," "," "," "," "," "," "],
[" "," "," "," "," "," "," "," "," "," "," "," "," "],
[" "," "," "," "," "," "," "," "," "," "," "," "," "],
[" "," "," "," "," "," "," "," "," "," "," "," "," "],
[" "," "," "," "," "," "," "," "," "," "," "," "," "],
[" "," "," "," "," "," ","/","|","\\"," "," "," "," "],
[" "," "," ","_","_","/","_","|","_","\\","_","_","_"],
]

hangman_5 = [
[" "," "," "," "," "," "," "," "," "," "," "," "," "],
[" "," "," "," "," "," "," ","|"," "," "," "," "," "],
[" "," "," "," "," "," "," ","|"," "," "," "," "," "],
[" "," "," "," "," "," "," ","|"," "," "," "," "," "],
[" "," "," "," "," "," "," ","|"," "," "," "," "," "],
[" "," "," "," "," "," "," ","|"," "," "," "," "," "],
[" "," "," "," "," "," ","/","|","\\"," "," "," "," "],
[" "," "," ","_","_","/","_","|","_","\\","_","_","_"],
]

hangman_6 = [
[" "," "," "," "," "," "," ","_","_","_","_"," "," "],
[" "," "," "," "," "," "," ","|"," "," "," "," "," "],
[" "," "," "," "," "," "," ","|"," "," "," "," "," "],
[" "," "," "," "," "," "," ","|"," "," "," "," "," "],
[" "," "," "," "," "," "," ","|"," "," "," "," "," "],
[" "," "," "," "," "," "," ","|"," "," "," "," "," "],
[" "," "," "," "," "," ","/","|","\\"," "," "," "," "],
[" "," "," ","_","_","/","_","|","_","\\","_","_","_"],
]

hangman_7 = [
[" "," "," "," "," "," "," ","_","_","_","_"," "," "],
[" "," "," "," "," "," "," ","|","/"," "," "," "," "],
[" "," "," "," "," "," "," ","|"," "," "," "," "," "],
[" "," "," "," "," "," "," ","|"," "," "," "," "," "],
[" "," "," "," "," "," "," ","|"," "," "," "," "," "],
[" "," "," "," "," "," "," ","|"," "," "," "," "," "],
[" "," "," "," "," "," ","/","|","\\"," "," "," "," "],
[" "," "," ","_","_","/","_","|","_","\\","_","_","_"],
]

hangman_8 = [
[" "," "," "," "," "," "," ","_","_","_","_"," "," "],
[" "," "," "," "," "," "," ","|","/"," ","|"," "," "],
[" "," "," "," "," "," "," ","|"," "," "," "," "," "],
[" "," "," "," "," "," "," ","|"," "," "," "," "," "],
[" "," "," "," "," "," "," ","|"," "," "," "," "," "],
[" "," "," "," "," "," "," ","|"," "," "," "," "," "],
[" "," "," "," "," "," ","/","|","\\"," "," "," "," "],
[" "," "," ","_","_","/","_","|","_","\\","_","_","_"],
]

hangman_9 = [
[" "," "," "," "," "," "," ","_","_","_","_"," "," "],
[" "," "," "," "," "," "," ","|","/"," ","|"," "," "],
[" "," "," "," "," "," "," ","|"," "," ","o"," "," "],
[" "," "," "," "," "," "," ","|"," "," "," "," "," "],
[" "," "," "," "," "," "," ","|"," "," "," "," "," "],
[" "," "," "," "," "," "," ","|"," "," "," "," "," "],
[" "," "," "," "," "," ","/","|","\\"," "," "," "," "],
[" "," "," ","_","_","/","_","|","_","\\","_","_","_"],
]

hangman_10 = [
[" "," "," "," "," "," "," ","_","_","_","_"," "," "],
[" "," "," "," "," "," "," ","|","/"," ","|"," "," "],
[" "," "," "," "," "," "," ","|"," "," ","o"," "," "],
[" "," "," "," "," "," "," ","|"," "," ","|"," "," "],
[" "," "," "," "," "," "," ","|"," "," "," "," "," "],
[" "," "," "," "," "," "," ","|"," "," "," "," "," "],
[" "," "," "," "," "," ","/","|","\\"," "," "," "," "],
[" "," "," ","_","_","/","_","|","_","\\","_","_","_"], 
]

hangman_11 = [
[" "," "," "," "," "," "," ","_","_","_","_"," "," "],
[" "," "," "," "," "," "," ","|","/"," ","|"," "," "],
[" "," "," "," "," "," "," ","|"," "," ","o"," "," "],
[" "," "," "," "," "," "," ","|"," ","/","|"," "," "],
[" "," "," "," "," "," "," ","|"," "," "," "," "," "],
[" "," "," "," "," "," "," ","|"," "," "," "," "," "],
[" "," "," "," "," "," ","/","|","\\"," "," "," "," "],
[" "," "," ","_","_","/","_","|","_","\\","_","_","_"],
]

hangman_12 = [
[" "," "," "," "," "," "," ","_","_","_","_"," "," "],
[" "," "," "," "," "," "," ","|","/"," ","|"," "," "],
[" "," "," "," "," "," "," ","|"," "," ","o"," "," "],
[" "," "," "," "," "," "," ","|"," ","/","|","\\"," "],
[" "," "," "," "," "," "," ","|"," "," "," "," "," "],
[" "," "," "," "," "," "," ","|"," "," "," "," "," "],
[" "," "," "," "," "," ","/","|","\\"," "," "," "," "],
[" "," "," ","_","_","/","_","|","_","\\","_","_","_"],
]

hangman_13 = [
[" "," "," "," "," "," "," ","_","_","_","_"," "," "],
[" "," "," "," "," "," "," ","|","/"," ","|"," "," "],
[" "," "," "," "," "," "," ","|"," "," ","o"," "," "],
[" "," "," "," "," "," "," ","|"," ","/","|","\\"," "],
[" "," "," "," "," "," "," ","|"," ","/"," "," "," "],
[" "," "," "," "," "," "," ","|"," "," "," "," "," "],
[" "," "," "," "," "," ","/","|","\\"," "," "," "," "],
[" "," "," ","_","_","/","_","|","_","\\","_","_","_"],
]

hangman_14 = [
[" "," "," "," "," "," "," ","_","_","_","_"," "," "],
[" "," "," "," "," "," "," ","|","/"," ","|"," "," "],
[" "," "," "," "," "," "," ","|"," "," ","o"," "," "],
[" "," "," "," "," "," "," ","|"," ","/","|","\\"," "],
[" "," "," "," "," "," "," ","|"," ","/"," ","\\"," "],
[" "," "," "," "," "," "," ","|"," "," "," "," "," "],
[" "," "," "," "," "," ","/","|","\\"," "," "," "," "],
[" "," "," ","_","_","/","_","|","_","\\","_","_","_"],
]

# Dictionary for references to each hangman graphic - referred to in game() using (hangmen[guesses]) - index called for by guesses counter
hangmen = {
    0: hangman_0, 
    1: hangman_1,
    2: hangman_2,
    3: hangman_3,
    4: hangman_4,
    5: hangman_5,
    6: hangman_6,
    7: hangman_7,
    8: hangman_8,
    9: hangman_9,
    10: hangman_10,
    11: hangman_11,
    12: hangman_12,
    13: hangman_13,
    14: hangman_14
    }

# List of possible words
'''
01 DONALD TRUMP
02 ALEX JONES
03 JET FUEL CAN'T MELT STEEL BEAMS
04 NUCLEAR APOCALYPSE
05 ANTI VAXXER
06 GEORGE SOROS
07 SNOWFLAKE
08 WOKE LIBERAL AGENDA
09 EPSTEIN DIDN'T KILL HIMSELF
10 TURN THE FRIGGIN' FROGS GAY

11 FULLY AUTOMATED LUXURY GAY SPACE COMMUNISM
12 SHREK IS LOVE, SHREK IS LIFE
13 TWO GIRLS, ONE CUP
14 MY BROTHER IN CHRIST
15 WHAT THE FUCK DID YOU JUST FUCKING SAY ABOUT ME, YOU LITTLE BITCH?
16 I SEXUALLY IDENTIFY AS AN ATTACK HELICOPTER
17 MILO YIANNOPOULOS
18 BEN SHAPIRO
19 TUCKER CARLSON
20 ADOLF HITLER

21 DESPITE THE CONSTANT NEGATIVE PRESS COVFEFE
22 LET'S SEE THEM ALIENS
23 IF WE NARUTO RUN, WE CAN MOVE FASTER THAN THEIR BULLETS
24 STORM AREA 51, THEY CAN'T STOP ALL OF US
25 WE'LL DO IT LIVE
26 ALL YOUR BASE ARE BELONG TO US
27 FEEL LIKE PURE SHIT JUST WANT HER BACK
28 OKAY I PULL UP
29 CHINESE SPY BALLOON
30 CHRIST FOR ARMS

31 BIG CHUNGUS
32 UGANDAN KNUCKLES
33 DO YOU KNOW DE WEY
34 I TOOK AN ARROW IN THE KNEE
35 HERE COME DAT BOI
36 PEDOBEAR
37 BELLE DELPHINE
38 HIDE THE PAIN HAROLD
39 OMAE WA MOU SHINDEIRU
40 FUCK HER RIGHT IN THE PUSSY

41 THIS IS FINE
42 FEELS BAD MAN
43 FEELS GOOD MAN
44 GOATSE
45 BOXXXY
46 ME AND THE BOYS
47 MOM'S SPAGHETTI
48 IS THIS A PIGEON
49 HIDE YO' KIDS, HIDE YO' WIFE
50 WHAT ARE YOU DOING, STEP BRO?

51 MONEY PRINTER GO BRRR
52 VLADIMIR PUTIN
53 WE LIVE IN A SOCIETY
54 THIS IS THE IDEAL MALE BODY
55 RUSSIAN SLEEP EXPERIMENT
56 SLENDERMAN
57 ELON MUSK
58 2022 RUSSIAN INVASION OF UKRAINE
59 IMMA LET YOU FINISH
60 TITS OR GTFO

61 SO HARDCORE
62 HANDSOME SQUIDWARD
63 PORNHUB INTRO
64 STOP RIGHT THERE, CRIMINAL SCUM
65 PONDERING MY ORB
66 WHATCHA TALKIN ABEET
67 GINGERS HAVE SOULS
68 TROLLFACE
69 ME GUSTA
70 WOJAK

71 DOLAN
72 PEPE THE FROG
73 ANCIENT ALIENS
74 OVERLY ATTACHED GIRLFRIEND
75 MEATSPIN
76 BAD LUCK BRIAN
77 DICKBUTT
78 HARAMBE
79 NYAN CAT
80 I KNOW THAT FEEL BRO

81 NOPE! CHUCK TESTA
82 TODAY, I FEEL GAY
83 THE CAKE IS A LIE
84 BUT THAT'S NONE OF MY BUSINESS
85 I'M IN ME MUM'S CAR, BROOM BROOM
86 M TO THE B
87 NUTTED BUT SHE STILL SUCKING
88 WOW KING, THAT SEX WAS REALLY POGGERS
89 I AM ONCE AGAIN ASKING FOR YOUR FINANCIAL SUPPORT
90 DON'T COME... I'M GONNA COME

91 GREAT SUPINE PROTOPLASMIC INVERTEBRATE JELLIES
92 SLEEPY JOE
93 WE'RE GONNA BUILD A WALL
94 BREXIT MEANS BREXIT
95 THANK YOU KANYE, VERY COOL!
96 CHEM TRAILS
97 OBAMA'S BIRTH CERTIFICATE
98 NIGEL FARAGE
99 PIZZAGATE
100 GIGACHAD
'''

# Main menu layout
'''
Main Menu:
    Play
    Instructions
    Quit
'''

# Instructions page layout
'''
    Instructions:

    A typical game of hangman, where all the words/phrases are a reference to some kind of meme-y pop culture, a controversial figure, or are just something downright needlessly edgy.

    You can guess either a letter, a word, or several words (but not multi-letter parts of any words), or have a go at guessing the whole thing.

    If you try to guess a word, you've gotta guess the WHOLE word. We're not gonna let any of that substring crap slide
    
    Type your guess then press ENTER. The guesses aren't case sensitive, and will ignore punctuation (make sure your spaces are in the correct place, however).

    You'll get 14 tries, then the man is hanged and it's game over.

    If you win, you'll be rewarded with some edgy artwork.

    PRESS ANY KEY TO RETURN TO MAIN MENU
'''

# In case main menu formatting fucks up:
'''
⡳⣙⢮⡹⣒
⡱⡍⢶⣑⢣
⣱⡙⢦⡍⡖

⡱⡜⣆⢧⡙
⠣⡵⣈⠦⣙
⢓⡴⣉⠖⣡
⢦⠱⣌⠚⡤
⢎⡱⢌⡓⡔
'''

curses.wrapper(title_screen)
curses.endwin()
