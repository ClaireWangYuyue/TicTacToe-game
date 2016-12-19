import hw06_tree
import copy, time, random


def make_board():
    """define the rows of the board"""
    return [[' ' for i in range(3)] for i in range(3)]


def show_board(board):
    """show the board"""
    showBoard = copy.deepcopy(board)
    showBoard.insert(1, '-+-+-')
    showBoard.insert(-1, '-+-+-')
    for i in range(0, len(showBoard), 2):
        showBoard[i] = '|'.join(showBoard[i])
    for i in showBoard:
        print(i)


def next_moves(parent, player):
    """# predict all possible move moves from the parent board
    given position of the parent the player who will make the move
    """
    parent_board = T.get_element(parent)
    for row in range(len(parent_board)):
        for col in range(len(parent_board[row])):
            new_board = copy.deepcopy(parent_board)
            if new_board[row][col] == ' ':
                new_board[row][col] = player
                T.add_child(new_board,parent)
                process_check(549946)


def process_check(size):
    """given the number of total nodes, check the process of making tree. Show to the user"""
    if len(T) % (size//10) == 0:
        print('\n',len(T) // (size//10) * 10,'% completed...')


def generate_tree(p, p1='x', p2='o', counter=0):
    """generate the tree of all possible moves"""
    # update the player of the current board
    counter += 1
    if counter % 2 == 0:
        player = p2
        T.player_update(p,player)
    else:
        player = p1
        T.player_update(p, player)
    # Base case 1: if one side has won, return the winner
    board = T.get_element(p)
    if board[0][0] == board[0][1] == board[0][2] != ' ' or board[1][0] == board[1][1] == board[1][2] != ' ' or \
        board[2][0] == board[2][1] == board[2][2] != ' ' or board[0][0] == board[1][0] == board[2][0] != ' ' or \
        board[0][1] == board[1][1] == board[2][1] != ' ' or board[0][2] == board[1][2] == board[2][2] != ' ' or \
        board[0][0] == board[1][1] == board[2][2] != ' ' or board[0][2] == board[1][1] == board[2][0] != ' ':
        if player == p1:
            T.state_update(p, -1)
        else:
            T.state_update(p,1)
        return
    # Base case 2: if the board is full and no side wins, return 'tie'
    elif T.full_board(p):
        T.state_update(p, 0)
        return
    # if neither of the base case is met, generate all the children and dig further down the tree
    else:
        # generate all the children/next moves
        next_moves(p, player)
        # recursively call generate_tree on each child
        for new_parent in T.children(p):
            generate_tree(new_parent, p1, p2, counter)


def minimax_score(p):
    """Score all the nodes in the tree given its root node position"""
    # score the leaves
    if T.is_leaf(p):
        return
    # score internal nodes
    else:
        # make a list of all the scores of the children of an internal node
        children_scores = []
        for child in T.children(p):
            # recursively calculate each child's score
            minimax_score(child)
            children_scores.append(T.get_state(child))
        # if it is x's move, score it as the max score in its children
        if T.get_player(p) == 'x':
            T.state_update(p, max(children_scores))
        # if it is o's move, score it as the min score in its children
        elif T.get_player(p) == 'o':
            T.state_update(p, min(children_scores))


def user_validation(user):
    """validate the user's input when asked to pick side"""
    while True:
        if user != 'x' and user != 'o' and user != 'q':
            user = input('Invalid input! Do you wanna play x or o? (type single letter x/o): ')
        else:
            return user


def move_validation(slot,board):
    """validate the user's input when asked to make a move"""
    while True:
        try:
            # if user presses q, return q
            if slot == 'q':
                return slot
            # split the input string by comma(if can't split, exception will be caught)
            choice = slot.split(',')
            # if the user didn't provide two numbers, raise exception and catch it
            if len(choice) != 2:
                print('Invalid! Please type TWO INTEGERs indicating row and column')
                raise ValueError
            for i in choice:
                # if the user didn't provide integers, raise exception and catch it
                if float(i) != int(i) or not i.isdigit():
                    print('Invalid! Please type two INTEGERs.')
                    raise ValueError
                # if the provided integers out of the range of the game board, raise exception and catch it
                elif int(i) < 1 or int(i) > 3:
                    print('Invalid! The indicated number has to range from 1 to 3')
                    raise ValueError
            coordinates= [int(i) for i in choice]
            # if the provided slot has been taken, raise exception and catch it
            if board[coordinates[0]-1][coordinates[1]-1] != ' ':
                print('Invalid! The indicated slot has been taken.')
                raise ValueError
            # if the input is validated, return a list of two integers representing the cooridinates of the indicated move
            return coordinates

        except:
            if ValueError:
                pass
            else:
                print('Wrong format of input! Type two integers separated by a comma indicating the row number'
                      'and column number of your choice (e.g. input 2,2 to make a move in the center slot)')
            # if the input is invalid, re-prompt the user
            slot = input('Where would you like to make the move?: ')


def play_game(user, p, player='x'):
    """play the game given the user's side, the current board info and the player of this round"""
    print()
    # show the current board to the user
    show_board(T.get_element(p))
    # base case: if it comes to a leaf node, return the result
    if T.children_num(p) == 0:
        if T.get_state(p) == 1 and user == 'x' or T.get_state(p) == -1 and user == 'o':
            print('\nYou win!')
        elif T.get_state(p) != 0:
            print('\nYou lost!')
        else:
            print('\nTie!')
        return
    # if the user is the current player, ask for his move
    if user == player:
        print('Your turn...')
        move = input('Where would you like to make the move?Type two integers separated by a comma indicating the row number'
                  'and column number of your choice (e.g. input 2,2 to make a move in the center slot), press q to quit: ')
        coordinates = move_validation(move, T.get_element(p))
        if coordinates == 'q':
            print('\nYou ended the game.')
            return
        # make a spare board of the current configuration
        board = copy.deepcopy(T.get_element(p))
        # fine the slot where the user wants to make a move and put user's mark into it
        for row in range(len(board)):
            for col in range(len(board[row])):
                if row == coordinates[0] - 1 and col == coordinates[1] - 1:
                    board[row][col] = user
        # find the board in the children of the current board who has the same configuration as the spare board
        # print(board)
        for child in T.children(p):
            if T.get_element(child) == board:
                # start the next round of game recursively
                if player == 'x':
                    player = 'o'
                else:
                    player = 'x'
                play_game(user, child, player)

    # else make a move of the agent
    else:
        print('Agent\'s turn...')
        # generate a list of Positions of all the children who has the same score as the current board
        choice_range = []
        # generate a list of Positions of all the children who has the same score as the current board and are leaves
        best_choices = []
        for child in T.children(p):
            if T.get_state(child) == T.get_state(p):
                choice_range.append(child)
                if T.is_leaf(child):
                    best_choices.append(child)
        # randomly pick one child from the choices that can immediate lead to a win
        if len(best_choices) != 0:
            choice = random.choice(best_choices)
        else:
            # if there no choices immediately lead to a win, randomlychoose one from the choice range
            choice = random.choice(choice_range)
        # current_board = T.get_element(choice)
        # start the next round of game recursively
        if player == 'x':
            player = 'o'
        else:
            player = 'x'
        play_game(user, choice, player)


if __name__ == '__main__':
    # make an instance of the tree
    T = hw06_tree.Tree()
    # make an empty board as the root of the game tree
    empty_board = make_board()
    root = T.add_root(empty_board)
    # define the player order(p1 always makes the first move)
    p1 = 'x'
    p2 = 'o'
    # generate the game tree
    start1 = time.time()
    print('Generating tree...This process will take about 1 minute...')
    print('\n 0 % completed...')
    generate_tree(root,p1,p2)
    end1 = time.time()
    print('# of nodes:',len(T))
    print('It took:', end1 - start1,'sec')
    print('Scoring...This process will take about 5 seconds...')
    # score all the nodes using minimax algorithm
    start2 = time.time()
    minimax_score(root)
    end2 = time.time()
    print('It took:',end2-start2,'sec')
    print('\nReady to start the game!')
    # play the game
    while True:
        user = user_validation(input('Do you wanna play x or o? (type single letter x/o, press q to quit): '))
        if user == 'q':
            break
        print('\nNote: In your turn, you will be asked to provide two integers '
              '\nseparated by a comma indicating the row number and column number '
              '\nof your choice (e.g. input 2,2 to make a move in the center slot)')
        play_game(user, root)
        if input('\nPress any key to begin a new game or press q to quit: ') == 'q':
            break
    print('\nGoodbye!')




