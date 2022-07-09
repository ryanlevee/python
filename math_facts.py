import sys
import time
import random
from rich import print

def game_loop(oper, question_answer, game_timer, max_num, score):
    question = question_answer[0]
    answer = float(question_answer[1])

    while game_timer[3] > 0:
        time_left = game_timer[0] - (int(time.time() - game_timer[1]))

        if time_left > 0:
            print(f'\nCurrent Score: {score}')
            print(f'{answer:g} *answer for testing') # Answer for testing
            print(f'{question}')
            print(f"You have {time_left} seconds left (q=quit).")

        if time_left <= 0:
            game_over(score, game_timer=time_left)
        else:
            try:
                user_guess = input("Enter an answer: ").strip()
            except KeyboardInterrupt:
                print('\nKeyboardInterrupt caught. Program terminated.')
                sys.exit()

        time_left = game_timer[0] - (int(time.time() - game_timer[1]))
        guess = check_guess(answer, user_guess)

        if guess and time_left >= 0:
            score += 1
            question_answer = get_question(oper, max_num)
            question = question_answer[0]
            answer = float(question_answer[1])


def get_operation():
    try:
        valid_operators = ['+', '-', 'x', '/']
        user_oper = input('\nWelcome to Math Facts!\n'
                          'Please enter an operation '
                          '[+, -, x, /]: (q=quit): ').strip()
        check_quit(user_oper)
        while user_oper not in valid_operators:
            user_oper = input('That is not a correct operation. '
                              'Please try again '
                              '[+, -, x, /]: ').strip()
            check_quit(user_oper)
        return user_oper
    except KeyboardInterrupt:
        print('\nKeyboardInterrupt caught. Program terminated.')
        sys.exit()


def get_max_number():
    while True:
        try:
            user_max_num = input('Please enter a max number '
                                 'between 1 and 100: '
                                 '(q=quit): ').strip()
            user_max_num = int(user_max_num)
            if 1 < user_max_num <= 100:
                return user_max_num
            if user_max_num > 100:
                print('That number is over 100. '
                      'Sorry, but this game would become too '
                      'unwieldy for your brain.')
        except ValueError:
            check_quit(user_max_num)
            print('Provide an integer...')
        except KeyboardInterrupt:
            print('\nKeyboardInterrupt caught. Program terminated.')
            sys.exit()


def get_question(oper, max_num):
    rand_num1 = str(random.randint(1, max_num))
    rand_num2 = str(random.randint(1, max_num))

    question = f'{rand_num1} {oper} {rand_num2} = ?'
    if oper == 'x':
        oper = '*'
    answer = round(eval(rand_num1 + oper + rand_num2), 2)

    return question, answer


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


def check_guess(answer, user_guess):
    check_quit(user_guess)
    try:
        float(user_guess)
        if float(answer) == float(user_guess):
            print(f'\n{user_guess} is CORRECT!')
            return True
        print(f'\n{user_guess} is not correct. Try again.')
    except ValueError:
        if user_guess == '':
            pass
        else:
            print('\nPlease answer with a number...')
    return False


def game_over(score, game_timer):
    try:
        if game_timer <= 0:
            play_again = input("\nTime is up!\n"
                            "Sorry, you didn’t get that "
                            "answer in on time.\n"
                            f"You answered {score} problems correctly!"
                            "\n\nPress Enter to play again (q=quit). ")
        if play_again == '':
            main()
        else:
            check_quit(play_again)
            sys.exit()
    except KeyboardInterrupt:
        print('\nKeyboardInterrupt caught. Program terminated.')
        sys.exit()
    return False


def main():
    oper = get_operation()
    max_num = get_max_number()
    game_timer = start_timer()
    question_answer = get_question(oper, max_num)


    game_loop(oper, question_answer, game_timer, max_num, score=0)


main()
