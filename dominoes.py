from itertools import combinations, combinations_with_replacement
from random import choice, randint
# from collections import deque


def shuffle():
    all_pieces = set(combinations_with_replacement([i for i in range(7)], 2))
    double_pieces = all_pieces - set(combinations([i for i in range(7)], 2))
    snake_pieces = {}

    while True:
        stock_pieces = list(all_pieces)
        player1_pieces, player2_pieces = [], []

        for players in [player1_pieces, player2_pieces]:
            for _ in range(7):
                players.append(stock_pieces.pop(stock_pieces.index(choice(stock_pieces))))

        if set(double_pieces).intersection(set(player1_pieces).union(set(player2_pieces))):
            player1_max = [max(domino[0] for domino in set(player1_pieces).intersection(set(double_pieces)))
                           if set(player1_pieces).intersection(set(double_pieces)) else -1][0]
            player2_max = [max(domino[0] for domino in set(player2_pieces).intersection(set(double_pieces)))
                           if set(player2_pieces).intersection(set(double_pieces)) else -1][0]

            stock_pieces, snake_pieces = list(map(list, stock_pieces)), list(map(list, snake_pieces))
            player1_pieces, player2_pieces = list(map(list, player1_pieces)), list(map(list, player2_pieces))
            if player2_max > player1_max:
                player2_pieces, snake_pieces = move('+', [player2_max, player2_max], player2_pieces, snake_pieces, stock_pieces)
                next_move = 'player2'
            else:
                player1_pieces, snake_pieces = move('+', [player1_max, player1_max], player1_pieces, snake_pieces, stock_pieces)
                next_move = 'player1'

            return list(map(list, stock_pieces)), snake_pieces, player1_pieces, player2_pieces, next_move


def move(side, domino, player_pieces, snake_pieces, stock_pieces):

    if not side:
        player_pieces.append(stock_pieces.pop(randint(0, len(stock_pieces) - 1)))
    else:
        player_pieces.remove(domino) if domino in player_pieces else player_pieces.remove(list(reversed(domino)))
        if side == '+':
            snake_pieces.append(domino)
        else:
            snake_pieces.insert(0, domino)
    return player_pieces, snake_pieces


def validation(side, domino, snake_pieces):
    if side == '-':
        if snake_pieces[0][0] in domino:
            return domino if snake_pieces[0][0] == domino[-1] else list(reversed(domino))
        else:
            return None
    else:
        if snake_pieces[-1][-1] in domino:
            return domino if snake_pieces[-1][-1] == domino[0] else list(reversed(domino))
        else:
            return None


def rate(player_pieces):
    scores = []
    for domino in player_pieces:
        score = sum(2 if ((domino[0] in d or domino[-1] in d) and d[0] == d[-1]) or (domino[0] in d and domino[-1] in d)
                    else 1 if domino[0] in d or domino[-1] in d else 0 for d in player_pieces)
        scores.append([score, domino])
        scores.sort(reverse=True)
    return scores


stock, snake, computer, player, status = shuffle()

while True:
    print(70 * '=', f'Stock size: {len(stock)}', f'Computer pieces: {len(computer)}\n', sep='\n')
    print(str(snake)[1:-1] if len(snake) < 7 else str(snake[:3])[1:-1] + '...' + str(snake[-3:])[1:-1])
    print('\nYour pieces: ', *[f'{i + 1}:{domino}' for i, domino in enumerate(player)], sep='\n')
    print('\nStatus:', end=' ')

    if not player:
        print('The game is over. You won!')
        break
    elif not computer:
        print('The game is over. The computer won!')
        break

    elif len(snake) > 1 and snake[0][0] == snake[-1][-1] and\
            sum(2 if snake[0][0] in d and d[0] == d[-1] else 1 if snake[0][0] in d else 0 for d in snake) > 7:
        print('The game is over. It\'s a draw!')
        break

    elif status == 'player1':
        print('It\'s your turn to make a move. Enter your command.', sep=' ')
        while True:
            try:
                command = int(input())
            except ValueError:
                print('Invalid input. Please try again.')
            else:
                if (command == 0 and stock) or (command != 0 and abs(command) <= len(player)):
                    where = '-' if command < 0 else '+' if command > 0 else None
                    domino = player[abs(command) - 1]
                    if where:
                        domino = validation(where, domino, snake)
                    if domino:
                        player, snake = move(where, domino, player, snake, stock)
                        status = 'player2'
                        break
                    else:
                        print('Illegal move. Please try again.')
                else:
                    print('Invalid input. Please try again.')
    else:
        input('Computer is about to make a move. Press Enter to continue...\n')
        domino = None
        rated_pieces = rate(computer)
        # print(*rated_pieces)
        for domino_with_score in rated_pieces:
            domino = validation('+', domino_with_score[-1], snake)
            if domino:
                computer, snake = move('+', domino, computer, snake, stock)
                status = 'player1'
                break
            domino = validation('-', domino_with_score[-1], snake)
            if domino:
                computer, snake = move('-', domino, computer, snake, stock)
                status = 'player1'
                break
        if not domino:
            computer, snake = move(None, domino, computer, snake, stock)
            status = 'player1'
