# TODO list:
# add radius to checking for available positions for the ai
# show a percentage for the ai
# optimise ai's performance

from os import system


def make_initial_state(): return (dict(), None)

# actions: tuple = (x, y)
# grid_state = (dictionary where key is action and value is playerID , prev_action)


def get_new_state(counter_x, state, player_ID):
    # adds a counter that is placed by player_ID
    y = 0
    (actions, prev_action) = state
    while((counter_x, y) in actions):
        y += 1
    # creating a completely new actions dictioanry for the new state
    new_action_state = dict(actions)
    new_action_state[(counter_x, y)] = player_ID
    new_state = (new_action_state, (counter_x, y))
    return new_state


def get_value_of_state(state, player_ID, n):
    # n refers to the number of counters required in a row to have won a game

    # returns a 1 if player with player_ID won the game
    # returns a 0 if game still needs to be continued

    (actions, prev_action) = state
    [x, y] = prev_action
    # checking if there has been a vertical win
    v_win = True
    for i in range(0, n):
        v_win = v_win and (actions.get((x, y-i), -1) == player_ID)
    if(v_win):
        return 1

    # checking if there as been a horizontal win

    l = 0  # counts the number of counters to the left
    while(actions.get((x-l-1, y), -1) == player_ID):
        l += 1
    r = 0  # counts the number of counters to the right
    while(actions.get((x+r+1, y), -1) == player_ID):
        r += 1
    if(l+r+1 >= n):
        return 1

    # checking if there has been a diagonal win (north-west)
    l = 0
    while(actions.get((x-l-1, y+l+1), -1) == player_ID):
        l += 1
    r = 0
    while(actions.get((x+r+1, y-1-r), -1) == player_ID):
        r += 1
    if(l+r+1 >= n):
        return 1

    # checking if there has been diagonal win (north-east)

    l = 0
    while(actions.get((x-l-1, y-1-l), -1) == player_ID):
        l += 1
    r = 0
    while(actions.get((x+r+1, y+r+1), -1) == player_ID):
        r += 1

    if(l+r+1 >= n):
        return 1

    # since there has been no win, we will return a -1
    return 0


def print_board(state):
    (actions, prev_action) = state

    max_x = 0
    max_y = 0
    for action in actions:
        max_x = max(action[0], max_x)
        max_y = max(action[1], max_y)

    grid = []
    max_x, max_y = max_x + 1, max_y + 1
    for i in range(max_y):
        grid.append(["-"] * max_x)
    for action in actions:
        grid[action[1]][action[0]] = actions[action]

    for row in reversed(grid):
        print("|", end="")
        for row_element in row:
            print(row_element, end="|")
        print("")
    print("|", end="")
    for i in range(1, len(grid[0]) + 1):
        print(i, end="|")
    print("")


def play_game():
    current_state = make_initial_state()
    player_ID = 1

    game_ended = False
    while(not game_ended):
        player_ID = 0 if (player_ID == 1) else 1
        counter_x = int(input("Add new counter position: ")) - 1
        current_state = get_new_state(counter_x, current_state, player_ID)
        system('clear')
        print_board(current_state)
        if(get_value_of_state(current_state, player_ID, 4) == 1):
            game_ended = True
    print("player " + str(player_ID) + " has won the game")


def play_game_ai():
    current_state = make_initial_state()
    player_ID = 0

    game_ended = False
    cache = {}
    while(not game_ended):
        print_board(current_state)
        counter_x = int(input("Counter x: ")) - 1
        system("clear")
        current_state = get_new_state(counter_x, current_state, player_ID)
        v = get_value_of_state(current_state, 0, 4)
        if(v == 1):
            print("Player 1 has won the game")
            break
        (ai_counter_x, value) = minimax_2_player(current_state, cache, 4, 1)
        current_state = get_new_state(ai_counter_x, current_state, 1)
        v = get_value_of_state(current_state, 1, 4)
        print("AI placed it in " + str(ai_counter_x + 1) + " position")
        if(v == 1):
            print_board(current_state)
            print("AI has won the game")
            break


def get_all_possible_actions(state):
    (actions, prev_action) = state
    new_actions_x = set()  # get all x values of counters to be placed
    # set AI board size
    c = 10
    for action in actions:
        (x, y) = action
        new_actions_x.add(max(x-1, 0))
        new_actions_x.add(x)
        new_actions_x.add(min(x+1, c - 1))

    return new_actions_x


def minimax_2_player(state, cache, depth, target_id):
    # returns best action to take for player with target_id given state and its value
    # cache contains the best possible action to take at that state and the value of that state

    # gets all possible actions that can be done by the next player
    # out of those actions, it give each action a value
    # value is given by recurively calling minimax until we hit a child state that is a final state.
    # we give this final child state a value
    # for each state, we choose the action that takes us to the most optimal child state

    (actions, prev_action) = state

    fstate = []
    for action in actions:
        fstate.append((action, actions[action]))
    fstate = tuple(fstate)

    if(fstate in cache and cache[fstate][1] != 0):
        return cache[fstate]

    # prev_id is the id of the person that did the last move
    prev_id = actions[prev_action]
    # is_taget_id tells us if the last person to make move was attempted by the target_id
    is_target_id = True if (prev_id == target_id) else False
    new_id = 1-prev_id  # calculating the id of the new person making the move

    if(get_value_of_state(state, prev_id, 4) == 1):
        if(is_target_id):
            # since this action led us to a win state
            cache[fstate] = (None, 1)
            return (None, 1)
        else:
            # since this action led another person to win
            cache[fstate] = (None, -1)
            return (None, -1)

    all_possible_actions = get_all_possible_actions(state)
    if(depth == 0):
        random_action = next(iter(all_possible_actions))
        cache[fstate] = (random_action, 0)
        return (random_action, 0)

    best_action = ""
    # we are minimising if previous player was target_id
    best_action_value = 1 if is_target_id else -1
    for action in all_possible_actions:
        [_, value] = minimax_2_player(get_new_state(action, state, new_id),
                                      cache, depth - 1, target_id)

        if(not is_target_id):  # since current player is not the target_id
            if(value >= best_action_value):
                best_action_value = value
                best_action = action
        else:
            if(value <= best_action_value):
                best_action_value = value
                best_action = action

    cache[fstate] = (best_action, best_action_value)
    return cache[fstate]


play_game_ai()
