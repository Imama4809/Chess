import functions
import settings
import random

settings.init()

def is_this_a_possible_move(dict, piece, move):
    og_place = copy.copy(dict[piece])
    og_move = copy.copy(dict[move])
    dict[move] = dict[piece]
    dict[piece].position = functions.interchange_let_num_pos_and_position(move)
    dict[piece].letnum_notation_position = move
    dict[piece] = 0
    if functions.is_king_in_path_of_enemy_pieces(col_king,col,dict) == True:
        dict[piece] = dict[move]
        dict[piece].position = og_place.position
        dict[piece].letnum_notation_position = og_place.letnum_notation_position 
        dict[move] = og_move
        possible_move_list[dict[piece].piece] = move
        return False
    dict[piece] = dict[move]
    dict[piece].position = og_place.position
    dict[piece].letnum_notation_position = og_place.letnum_notation_position 
    dict[move] = og_move
    return True 

def evaluate_position(dict):
    piece_values = {"King": 0,"Queen": 8, "Rook": 5, "Knight": 3, "Bishop": 3, "Pawn": 1}
    White_sum = 0
    Black_sum = 0
    for val in dict:
        if type(dict[val]) != int:
            if dict[val].colour == "White":
                White_sum = White_sum + piece_values[dict[val].piece]
            else:
                Black_sum = Black_sum + piece_values[dict[val].piece]
    return White_sum - Black_sum 
            
def best_move(dict):
    piece_list = []
    possible_move_list = {}
    for val in dict:
        if type(dict[val]) != int:
            piece_list.append(val)
    for piece in piece_list:
        for move in dict[piece].move_list():
            if functions.is_this_a_possible_move(dict,piece,move) == True:
                possible_move_list.append(move)
                       
                       
def random_move(dict):
    list_of_turn_pieces = []
    buff_dict = functions.possible_moves(dict,settings.turn)
    for val in buff_dict:
        if buff_dict[val] != []:
            list_of_turn_pieces.append(val)
    chosen_piece = random.choice(list_of_turn_pieces)
    print(buff_dict)
    moves = buff_dict[chosen_piece]
    chosen_move = random.choice(moves)
    functions.do_move((dict[chosen_piece].position[0]-1)*50,(8-dict[chosen_piece].position[1])*50,(int(functions.interchange_number_and_letter(chosen_move[0]))-1)*50,(8-int(chosen_move[1]))*50,dict)


#function to be able to change the current bot depending on which one I want to test 
def current_bot(dict):
    random_move(dict)
