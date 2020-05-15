"""
Brighton Balfrey
CS360
Project 2
balfrey@usc.edu
3228236754
"""

import sys

class Contestant :
    """
    Contestant - class to manage contestant data

    Attributes
    id int: contestant id
    capacity double: contestant capacity
    happyA double: contestants happiness w team 1
    happyB double: contestants happiness w team 2
    pickState int: input team (1, 2, or 0)
    """
    def __init__(self, id, capacity, happy_a, happy_b, pick_state) :
        self.id = id
        self.capacity = capacity
        self.happyA = happy_a
        self.happyB = happy_b
        self.pickState = pick_state

def read_input(file_name):
    """
    :return [String algorithm type, List contestants]
    """
    f = open(file_name, 'r') 
    line_number = 0
    alg_type = ''    
    contestants = []
    for line in f :
        line_number += 1
        if line_number == 1:
            continue
        if line_number == 2:
            alg_type = line
            continue
        data = line.split(',')
        new_contestant = Contestant(int(data[0]), float(data[1]), float(data[2]), float(data[3]), int(data[4]))
        contestants.append(new_contestant)
    f.close()
    return [alg_type, contestants]

def write_output(contestant_id, file_name = 'output.txt'):
    """
    :param contstant_id - string id to write to file
    :param file_name - name of file to write to, by default output.txt
    """
    with open(file_name, 'w') as file:
       file.write(contestant_id)

def calculate_score(contestants, team_number) :
    """
    :param contestants - list of contestants to calculate score from
    :param team_number - int of team number
    :return double team score
    """
    score = 0.0
    if not contestants:
        return 0
    diversity = True
    seen_last_digits = set()
    for contestant in contestants:
        team_capacity = 0.0
        if team_number == 1:
            team_capacity = contestant.capacity * contestant.happyA
        else :
            team_capacity = contestant.capacity * contestant.happyB
        score += team_capacity
        contestant_id_string = str(contestant.id)
        last_digit = contestant_id_string[len(contestant_id_string)-1]
        if diversity :
            diversity = not last_digit in seen_last_digits
        seen_last_digits.add(last_digit)
    return [score, diversity]

def calculate_advantage(team_1, team_2) :
    """
    :param team_1 list of Contestants on team 1
    :param team_2 list of Contestants on team 2
    :return double advantage that team 1 has
    """
    team_1_score = calculate_score(team_1, 1) 
    team_2_score = calculate_score(team_2, 2)
    if len(team_1) == 5 :
        team_1_score[0] += 120 if team_1_score[1] else 0
    if len(team_2) == 5:
        team_2_score[0] += 120 if team_2_score[1] else 0
    return team_1_score[0] - team_2_score[0]

def get_new_team(team, contestant):
    """
    :param team - existing team to copy over
    :param contestant - Contestant to add to team
    :return list of new contestants copied over
    """
    new_team = [c for c in team]
    new_team.append(contestant)
    return new_team

def copy_team(team) :
    """
    :param team - existing team to make a copy of
    :return list of contestants
    """
    return [c for c in team]

def get_new_available_contestants(contestants, contestant) :
    """
    :param contestants - list of available contestants
    :param contestant - contestant to not include in new available list
    :return list of new available contestants
    """
    new_contestants = []
    for c in contestants :
        if c.id == contestant.id :
            continue
        new_contestants.append(c)
    return new_contestants

def get_starting_contestants(contestants) :
    """
    :param contestant - raw list of contestants from input
    :return [team_1, team_2, team_3] list of list of contestants on each team
    """
    team_1 = []
    team_2 = []
    available = []
    for contestant in contestants :
        if contestant.pickState == 0 :
            available.append(contestant)
        elif contestant.pickState == 1 :
            team_1.append(contestant)
        elif contestant.pickState == 2 :
            team_2.append(contestant)
    return [team_1, team_2, available]

def minimax(team_1, team_2, available, starting_depth, isMax = True, starting_pick = None) :
    """
    :param team_1 - list of contestants on team 1
    :param team_2 - list of contestants on team 2
    :return [double advantage, starting pick Contestant]
    """
    # Base Case
    if len(team_1) == 5 and len(team_2) == 5 :
        return [calculate_advantage(team_1, team_2), starting_pick]

    # Look through children
    return_val = None
    for a in available:

        # Max case
        if isMax :

            if len(team_1) == starting_depth :
                starting_pick = a

            curr = minimax(
                get_new_team(team_1, a),
                copy_team(team_2),
                get_new_available_contestants(available, a),
                starting_depth,
                False,
                starting_pick
            )

            # First iteration
            if not return_val :
                return_val = curr
                continue

            # If they have the same value
            elif curr[0] == return_val[0] :
                return_val = return_val if return_val[1].id < curr[1].id else curr

            # If one is greater than the other
            else :
                return_val = return_val if return_val[0] > curr[0] else curr

        # Min case
        else :
            curr = minimax(
                copy_team(team_1),
                get_new_team(team_2, a),
                get_new_available_contestants(available, a),
                starting_depth,
                True,
                starting_pick
            )

            # First iteration
            if not return_val :
                return_val = curr

            # If they have the same value
            elif curr[0] == return_val[0] :
                return_val = return_val if return_val[1].id < curr[1].id else curr

            else :
                return_val = return_val if return_val[0] < curr[0] else curr

    return return_val

def ab(team_1, team_2, available, starting_depth, isMax = True, starting_pick = None, alpha = -sys.maxsize, beta = sys.maxsize) :
    """
    :param team_1 - list of contestants on team 1
    :param team_2 - list of contestants on team 2
    :return [double advantage, starting pick Contestant]
    """    
    # Base Case
    if len(team_1) == 5 and len(team_2) == 5 :
        return [calculate_advantage(team_1, team_2), starting_pick]

    # Look through children
    return_val = [-sys.maxsize if isMax else sys.maxsize, None]
    for a in available:

        # Max case
        if isMax :

            if len(team_1) == starting_depth :
                starting_pick = a

            curr = ab(
                get_new_team(team_1, a),
                copy_team(team_2),
                get_new_available_contestants(available, a),
                starting_depth,
                False,
                starting_pick,
                alpha,
                beta
            )

            # First iteration
            if not return_val :
                return_val = curr
                continue

            # If they have the same value
            elif curr[0] == return_val[0] :
                return_val = return_val if return_val[1].id < curr[1].id else curr

            # If one is greater than the other
            else :
                return_val = return_val if return_val[0] > curr[0] else curr

            alpha = max(alpha, return_val[0])
            if beta <= alpha :
                return return_val

        # Min case
        else :
            curr = ab(
                copy_team(team_1),
                get_new_team(team_2, a),
                get_new_available_contestants(available, a),
                starting_depth,
                True,
                starting_pick,
                alpha,
                beta
            )

            # First iteration
            if not return_val :
                return_val = curr

            # If they have the same value
            elif curr[0] == return_val[0] :
                return_val = return_val if return_val[1].id < curr[1].id else curr

            else :
                return_val = return_val if return_val[0] < curr[0] else curr

            beta = min(beta, return_val[0])
            if beta <= alpha :
                return return_val

    return return_val




if __name__ == "__main__" :
    """
    Running as an individual script
    Read input from test.txt
    Write output to output.txt
    """
    input = read_input('./test.txt')
    all_contestants = get_starting_contestants(input[1])
    if 'minimax' in input[0]:
        res = minimax(all_contestants[0], all_contestants[1], all_contestants[2], len(all_contestants[0]), True)
    else :
        res = ab(all_contestants[0], all_contestants[1], all_contestants[2], len(all_contestants[0]), True)
    write_output(str(res[1].id))

