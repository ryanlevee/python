import random
import re
import sys
import time

from rich import print
from pprint import pformat


def game_loop(game_list, list_and_word, game_timer, word_length, score):
    current_list = list_and_word[0]
    current_word = list_and_word[1]

    while game_timer[3] > 0:
        time_left = game_timer[0] - (int(time.time() - game_timer[1]))

        if time_left > 0 and len(current_list) > 0:
            print(f'\n{current_list} *answers for testing') # Answers
            print(f'There are {len(current_list)} unguessed anagrams.')
            print(f'Current Score: {score}')
            print(f'The word is: {pformat(current_word.upper())}')
            print(f"You have {time_left} seconds left (q=quit).")

        if time_left <= 0:
            game_over(word_length, score, game_timer=time_left)
        elif len(game_list) == 0 and len(current_list) == 0:
            game_over(word_length, score, game_timer=time_left)
        else:
            try:
                user_guess = input("Enter an answer: ").lower().strip()
            except KeyboardInterrupt:
                print('\nKeyboardInterrupt caught. Program terminated.')
                sys.exit()

        time_left = game_timer[0] - (int(time.time() - game_timer[1]))
        guess = check_guess(current_list, user_guess, score, time_left)

        if len(game_list) == 0:
            pass
        elif guess and time_left >= 0:
            score += 1
            list_and_word = check_list(game_list, current_list)
            if list_and_word:
                print('You got all the anagrams for '
                      f'{pformat(current_word.upper())}! '
                      '\nNext word loading...')
                current_list = list_and_word[0]
                current_word = list_and_word[1]


def get_all_lists():
    with open('anagrams.js', encoding='utf-8') as f:
        f = f.read().split('],')
        all_lists = []

        regex = r'\w+(?=")'
        for line in f:
            all_lists.append(re.findall(regex, line))

    return all_lists


def get_game_list(word_length, all_lists):
    game_list = [line for line in all_lists if len(line[0]) == word_length]
    return game_list


def get_word_length():
    while True:
        try:
            user_length = input('\nWelcome to Anagram Hunt! '
                                '\nPlease enter a word length '
                                '[5, 6, 7, 8] (q=quit): ')
        except KeyboardInterrupt:
            print('\nKeyboardInterrupt caught. Program terminated.')
            sys.exit()
        try:
            user_length = int(user_length)
            if user_length >= 9 or user_length <= 4:
                print('That is not a correct word length...')
            else:
                return user_length
        except ValueError:
            check_quit(user_length)
            print('Provide an integer...')


def get_list_and_word(game_list):
    try:
        current_list = random.choice(game_list)
        game_list.remove(current_list)
        current_word = random.choice(current_list)
        current_list.remove(current_word)

        return current_list, current_word

    except IndexError:
        return False


def start_timer():
    print()
    for i in range(-3, 0):
        print(abs(i))
        time.sleep(1)
    print('Go!')
    time_limit = 60 # Seconds
    time_start = time.time()
    time_elapsed = 0
    time_left = time_limit - time_elapsed + 1

    return time_limit, time_start, time_elapsed, time_left


def check_quit(user_input):
    if user_input.lower() == 'q':
        print('Program quitting...\n')
        sys.exit()
    return False


def check_guess(current_list, user_guess, score, time_left):
    check_quit(user_guess)

    if user_guess in current_list:
        print(f'\n{pformat(user_guess.upper())} is correct!')
        if time_left > 0:
            score += 1
        current_list.remove(user_guess)
        return score
    if user_guess == '':
        pass
    else:
        print(f'\n{user_guess.upper()} is not correct. Try again.')

    return score


def check_list(game_list, current_list):
    if len(current_list) == 0:
        list_and_word = get_list_and_word(game_list)
        return list_and_word
    return False


def game_over(word_length, score, game_timer):
    if game_timer <= 0:
        play_again = input("\nTime is up!\n"
                           "Sorry, you didn’t get that "
                           "last answer in on time.\n"
                           f"You guessed {score} anagrams correctly!"
                           "\n\nPress Enter to play again (q=quit). ")
    elif game_timer > 0:
        play_again = input(f"\nFinished!\n"
                           f"You guessed all {score} anagrams "
                           f"of the {word_length}-letter words!\n"
                           "\nPress Enter to play again (q=quit). ")
    if play_again == '':
        main()
    else:
        check_quit(play_again)
        sys.exit()
    return False


def main():
    all_lists = get_all_lists()
    word_length = get_word_length()
    game_list = get_game_list(word_length, all_lists)
    game_timer = start_timer()
    list_and_word = get_list_and_word(game_list)

    game_loop(game_list, list_and_word, game_timer, word_length, score=0)


main()
