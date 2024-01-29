import copy
import settings

settings.init()



#Slice of Life additions 
def interchange_number_and_letter(inp): # change letters to numbers or numbers to letters
    l = "0abcdefgh" #list to be able to interchange values, 0 is put at the beginning to make the interchange cleaner 
    if type(inp) == str:
        return l.find(inp)
    if type(inp) == int:
        return l[inp]
    
def interchange_let_num_pos_and_position(inp):
    return (int(str(interchange_number_and_letter(inp[0]))),int(inp[1]))



#this deals with areas of the game
def paths_of_enemy_pieces(chessboard,colour): #this is required for king movement 
    total_list = []
    for val in chessboard:
        if chessboard[val]!=0 and chessboard[val]!=1 and chessboard[val].piece != 'King':
            if chessboard[val].colour == colour:
                if chessboard[val].piece == "Pawn": #this if statement makes sure that the king can be in front of pawns, but not to their diagonals 
                    if chessboard[val].colour == 'White':
                        movement = 1
                    if chessboard[val].colour == 'Black':
                        movement = -1
                    for i,j in [(1,movement),(-1,movement)]:
                        if (chessboard[val].position[0]+i-4.5)**2 > 12.25 or (chessboard[val].position[1]+j-4.5)**2 > 12.25: 
                            #the position is in values between 1 and 8, thus 4.5 being the middle and 3.5 being the distance from the median to the max and min
                            #this means that if we subtract a value that is outside of the range of 1, and 8 from the median, it would be greater than 3.5**2
                            #thus to filter out values outside that range, we subtract the number by 4.5 and check if its greater than 3.5**2 (12.25)
                            continue
                        total_list.append((interchange_number_and_letter(chessboard[val].position[0]+i) + str(chessboard[val].position[1]+j ))) 
                else: 
                    total_list.extend(chessboard[val].move_list())


                
    return total_list

def is_king_in_path_of_enemy_pieces(king,colour_of_king,chessboard): #is the king in LOS???SS
    if king.letnum_notation_position in paths_of_enemy_pieces(chessboard,king.othercolour):
        return True
    else:
        return False
    
def is_this_a_possible_move(dict, chosen_piece, chosen_move, col):
    for val in dict:
        if type(dict[val]) != int and dict[val].piece == "King" and dict[val].colour == col:
            col_king = dict[val]
    check_dict = copy.deepcopy(dict)
    og_turn = settings.turn
    if do_move((dict[chosen_piece].position[0]-1)*50,(8-dict[chosen_piece].position[1])*50,(int(interchange_number_and_letter(chosen_move[0]))-1)*50,(8-int(chosen_move[1]))*50,dict) == 1:
        settings.turn = og_turn
        dicttodict(check_dict,dict)
        return False
    settings.turn = og_turn
    dicttodict(check_dict,dict)
    return True 

def possible_moves(dict,col):
    possible_move_list = {}
    col_list = []
    for val in dict:
        if type(dict[val])!= int and dict[val].colour == col:
            col_list.append(val)
    og_turn = settings.turn 
    for chosen_piece in col_list:
        possible_move_list[chosen_piece] = []
        for chosen_move in dict[chosen_piece].move_list():
            check_dict = 0 
            check_dict = copy.deepcopy(dict)
            print(dict[chosen_piece].piece,chosen_move)
            if is_this_a_possible_move(dict,chosen_piece,chosen_move,settings.turn) == False:
                continue
            possible_move_list[chosen_piece].append(chosen_move)
    settings.turn = og_turn
    return possible_move_list

def check_pawn_promotion_for_colour(dict,colour):
    if colour == "White":
        place = 8
    if colour == "Black":
        place = 1
    for val in dict:
        if type(dict[val]) != int:
            if dict[val].piece == "Pawn":
                if dict[val].position[1] == place:
                    while True:
                        inp = input()
                        if inp in ["Queen","Rook","Bishop","Knight"]:
                            dict[val].piece = str(inp)
                            break
                        else:
                            print("not a valid piece")


#This checks at the end of the game 
def checkmate_check(dict, col):
    check_before = False
    practice_dict = dict 
    col_list = []
    for val in dict:
        if type(dict[val])!= int and dict[val].colour == col:
            if dict[val].piece == "King":
                col_king = dict[val]
            col_list.append(val)
    if is_king_in_path_of_enemy_pieces(col_king,col,dict) == True:
        check_before = True
    for piece in col_list:
        for move in dict[piece].move_list():
            og_place = copy.copy(dict[piece])
            og_move = copy.copy(dict[move])
            dict[move] = dict[piece]
            dict[piece].position = interchange_let_num_pos_and_position(move)
            dict[piece].letnum_notation_position = move
            dict[piece] = 0
            if is_king_in_path_of_enemy_pieces(col_king,col,dict) == False:
                dict[piece] = dict[move]
                dict[piece].position = og_place.position
                dict[piece].letnum_notation_position = og_place.letnum_notation_position 
                dict[move] = og_move
                return False
            dict[piece] = dict[move]
            dict[piece].position = og_place.position
            dict[piece].letnum_notation_position = og_place.letnum_notation_position 
            dict[move] = og_move
    if check_before:
        return True
    return False
    
def stalemate_check(dict,col):
    check_before = False
    practice_dict = dict 
    col_list = []
    for val in dict:
        if type(dict[val])!= int and dict[val].colour == col:
            if dict[val].piece == "King":
                col_king = dict[val]
            col_list.append(val)
    if is_king_in_path_of_enemy_pieces(col_king,col,dict) == True:
        check_before = True
    for piece in col_list:
        for move in dict[piece].move_list():
            og_place = copy.copy(dict[piece])
            og_move = copy.copy(dict[move])
            dict[move] = dict[piece]
            dict[piece].position = interchange_let_num_pos_and_position(move)
            dict[piece].letnum_notation_position = move
            dict[piece] = 0
            if is_king_in_path_of_enemy_pieces(col_king,col,dict) == False:
                dict[piece] = dict[move]
                dict[piece].position = og_place.position
                dict[piece].letnum_notation_position = og_place.letnum_notation_position 
                dict[move] = og_move
                return False
            dict[piece] = dict[move]
            dict[piece].position = og_place.position
            dict[piece].letnum_notation_position = og_place.letnum_notation_position 
            dict[move] = og_move
    if check_before:
        return False
    return True
    
#Actually doing the move
def do_move(x,y,x_new,y_new,dict):
    global dictpawn
    old_dict = copy.deepcopy(dict)
    WIDTH, HEIGHT = 400, 400
    LIGHT_BLUE = (173, 216, 230)
    GREEN = (55, 229, 180)
    SQUARE_SIZE = WIDTH // 8
    check = False
    global second_click
    place_of_first_click = interchange_number_and_letter(1+x//50) + str(8-y//50) #location of first click 
    place_of_second_click = interchange_number_and_letter(1+x_new//50) + str(8-y_new//50) #this gets the location on the board of the second click 
    if place_of_second_click in dict[place_of_first_click].move_list():                    
        #PAWN FIRST MOVE 
        if dict[place_of_first_click].piece == 'Pawn' and dict[place_of_first_click].moved == False and len(dict[place_of_first_click].move_list())>1 and place_of_second_click == dict[place_of_first_click].move_list()[1]:
            dict[dict[place_of_first_click].move_list()[0]] = 1
            dict[place_of_first_click].double_move = True
            dict[place_of_first_click].moved = True
        
        
        #CHANGES POSITIONS 
        buffer_to_check_for_king = dict[place_of_second_click]
        dict[place_of_second_click] = dict[place_of_first_click]
        dict[place_of_second_click].position = (1+x_new//50,8-y_new//50) #we have to change it to the coordinate value in the class its defined as a coordinate value 
        dict[place_of_second_click].letnum_notation_position = place_of_second_click
        has_it_moved_before = dict[place_of_second_click]
        dict[place_of_second_click].moved = True
        if buffer_to_check_for_king == 1 and dict[place_of_second_click].piece == "Pawn":
            dict[dict[place_of_second_click].get_piece_under()] = 0
        dict[place_of_first_click] = 0 #getting rid of piece at first click position 
        
                
        #NO MORE EN PASSANT       
        for val in dict:
            if type(dict[val]) != int :
                if dict[val].piece=="Pawn" and dict[val].double_move == True:
                    if dict[val].turn_after_double == False:
                        dict[val].turn_after_double = True
                    elif dict[val].turn_after_double == True:
                        ghost_pawn = dict[val].get_piece_under()
                        dict[ghost_pawn] = 0
                        dict[val].turn_after_double = False
                        dict[val].double_move = False
                
        #SWITCH TURNS 
        if settings.turn == "White":
            settings.turn = "Black"
        else:
            settings.turn = "White"
                        
        #CHECKCHECKCHECKCHECKCHECK (courtesy of Josh Choong)
        for val in dict:
            if type(dict[val]) != int:
                if dict[val].piece == 'King' and dict[val].othercolour == settings.turn:
                    if is_king_in_path_of_enemy_pieces(dict[val],dict[val].colour,dict):
                        dicttodict(old_dict,dict)
                        #this is needed so that the turn goes back to white, it essentially checks to make sure the king isn't in danger, and if it is, sends it back to the original turn
                        if settings.turn == "White":
                            settings.turn = "Black"
                        else:
                            settings.turn = "White"
                        print("nope")
                        return 1
                    else:
                        break
        print("yup")    
        return 0 

    #CASTLING 
    elif type(dict[place_of_second_click]) !=int: 
        if dict[place_of_first_click].piece == "King" and dict[place_of_second_click].piece == "Rook" and  dict[place_of_first_click].colour == settings.turn and dict[place_of_second_click].colour == settings.turn and dict[place_of_first_click].castle != True and dict[place_of_second_click].castle !=True:
            if dict[place_of_first_click].moved == False and dict[place_of_second_click].moved == False:
                
                #WHICH WAY TO CASTLE???
                list_of_vals_that_must_be_empty = []
                direction_of_movement = dict[place_of_first_click].position[0] - dict[place_of_second_click].position[0]
                if direction_of_movement > 0:
                    direction_of_movement = -1
                elif direction_of_movement <0:
                    direction_of_movement=1
                    
                #NO CASTLING THROUGH PIECES 
                for val in range(1,abs(dict[place_of_first_click].position[0]-dict[place_of_second_click].position[0])):
                    if dict[interchange_number_and_letter(val*direction_of_movement + 1+x//50) + str(8-y//50)]!=0 and dict[interchange_number_and_letter(val*direction_of_movement + 1+x//50) + str(8-y//50)]!=1 or interchange_number_and_letter(val*direction_of_movement + 1+x//50) + str(8-y//50) in paths_of_enemy_pieces(dict,dict[place_of_first_click].othercolour):
                            print("sorry, you can't castle through pieces")
                            second_click = True
                            check = True #this check is to make sure there are no pieces in between the rook and the king, if there is, it doesn't let you castle 
                            break
                if check==True:
                    return 1
                
                
                #DOING THE CASTLING 
                new_king_place = interchange_number_and_letter(2*direction_of_movement + 1+x//50) + str(8-y//50)
                new_rook_place = interchange_number_and_letter(direction_of_movement +1 +x//50) + str(8-y//50)
                dict[new_king_place] = dict[place_of_first_click]
                dict[new_rook_place] = dict[place_of_second_click]
                dict[new_king_place].letnum_notation_position = new_king_place
                dict[new_king_place].position = (2*direction_of_movement +1 + x//50,8-y//50)
                dict[new_rook_place].letnum_notation_position = new_rook_place
                dict[new_rook_place].position = (direction_of_movement +1+x//50,8-y_new//50)
                dict[place_of_first_click] = 0
                dict[place_of_second_click] = 0
                

                
                #SWITCHING TURNS 
                if settings.turn == "White":
                    settings.turn = "Black"
                else:
                   settings.turn ="White"
                
                #MAKING SURE CASTLING CAN'T HAPPEN AGAIN 
                dict[new_king_place].castle = True
                dict[new_rook_place].castle = True
                return 0
    else:
        print(f"invalid move for {dict[place_of_first_click].piece} at {dict[place_of_first_click].letnum_notation_position}")
        return 0     
    
    
    
def dicttodict(dict1,dict2):
    #way to paste keys of dict1 into dict2, second dict is the one you are changing 
    for key in dict1:
        dict2[key] = dict1[key]