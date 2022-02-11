import random

def rps():

    user = input('What is your choice? r for rock, p for paper, s for scissors: ')
    comp = random.choice(['r', 's', 'p'])

    if user == comp:
        return 'It\'s a tie'

    if win_check(user, comp) is True:
        return 'You won!'

    return 'You lost!'

def win_check(you, opponent):
    if (you == 'r' and opponent == 's') or (you == 's' and opponent == 'p') \
        or (you == 'p' and opponent == 'r'):
        return True

print(rps())