import pygame
import sys
import os 
import random 

from sol import interchange_number_and_letter #for slice of life 

# Initialize Pygame
pygame.init()

print(os.path.dirname("Pieces"))

def pieces_onto_board(dict,screen):
    for val in dict: #prints all the pieces onto the dictionary 
        if dict[val] != 0 and dict[val] !=1:
            image = pygame.image.load(f"Pieces/{dict[val].colour}_{dict[val].piece}.png")
            screen.blit(image,((dict[val].position[0]-1)*50,400-(dict[val].position[1])*50)) #we need to do 400- since the pygame window starts in the top left


    
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
            
    
global turn 
turn= "White"
dictpawn = {}

    
# Constants
def create_chessboard(dict):
    global dictpawn
    global turn
    print(dictpawn)
    for val in dict:
        dictpawn[val] = 0
    WIDTH, HEIGHT = 400, 400
    LIGHT_BLUE = (173, 216, 230)
    GREEN = (55, 229, 180)
    SQUARE_SIZE = WIDTH // 8
    
    

    # Create the Pygame window
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Chessboard")

    # Main game loop
    while True:
        # Draws the surface object to the screen.
        pygame.display.update() 
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # to quit 
                pygame.quit()
                sys.exit()



        # Draw the chessboard
        for row in range(8):
            for col in range(8):
                color = GREEN if (row + col) % 2 == 0 else LIGHT_BLUE
                pygame.draw.rect(screen, color, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
                
                
                
                
        pieces_onto_board(dict,screen) #function to place pieces onto board
        
        # Update the display
        pygame.display.flip()
        # Set the frames per second
        pygame.time.Clock().tick(60)
       
       
       
        second_click = False #this is to check whether a second click has occurred 
        #print("hi") 
        if turn == "White": #turn system 
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos() #first mouse click position
                place_of_first_click = interchange_number_and_letter(1+x//50) + str(8-y//50) #location of first click 
                if dict[place_of_first_click] !=0 and dict[place_of_first_click] !=1 and dict[place_of_first_click].colour == turn : #making sure its not empty 
                    while (second_click == False): #making sure second click happened 
                        for event in pygame.event.get():
                            if event.type == pygame.MOUSEBUTTONDOWN: #second mouse click position 
                                x_new, y_new = pygame.mouse.get_pos() #new cords
                                do_move(x,y,x_new,y_new,dict,screen) 
                                check_pawn_promotion_for_colour(dict,screen, "White") #pawn promotion 
                                second_click = True
                                break
                            if event.type == pygame.QUIT: # to quit #might be able to create a function if you take event as an input 
                                pygame.quit()
                                sys.exit() 
                            
                else:
                    print(f"its {turn}'s turn")   
        if turn == "Black": #blacks turn 
            random_move(dict,screen)
            check_pawn_promotion_for_colour(dict,screen, "Black") #pawn promotion 
            
                        
        if event.type == pygame.QUIT: # to quit 
            pygame.quit()
            sys.exit()
                
         


# def compmove(dict,screen):
#     global turn
#     for val in dict:
        
#     place_of_first_click = random.choice()

def do_move(x,y,x_new,y_new,dict,screen):
    global dictpawn
    
    WIDTH, HEIGHT = 400, 400
    LIGHT_BLUE = (173, 216, 230)
    GREEN = (55, 229, 180)
    SQUARE_SIZE = WIDTH // 8
    check = False
    global turn 
    global second_click
    place_of_first_click = interchange_number_and_letter(1+x//50) + str(8-y//50) #location of first click 
    place_of_second_click = interchange_number_and_letter(1+x_new//50) + str(8-y_new//50) #this gets the location on the board of the second click 
    print(dict[place_of_first_click].move_list())
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
            pieces_onto_board(dict,screen)
            pygame.display.flip() 
        dict[place_of_first_click] = 0 #getting rid of piece at first click position 
        
                
        #NO MORE EN PASSANT       
        for val in dict:
            if type(dict[val]) == int:    
                dictpawn[val] = dict[val]
        for val2 in dictpawn:
            if dictpawn[val2] ==1:
                dictpawn[val2] =2
            elif dictpawn[val2] ==2:
                dictpawn[val2]=0   
                
        #SWITCH TURNS 
        if turn == "White":
            turn = "Black"
        else:
            turn = "White"
                        
        #CHECKCHECKCHECKCHECKCHECK (courtesy of Josh Choong)
        for val in dict:
            if type(dict[val]) != int:
                if dict[val].piece == 'King' and dict[val].othercolour == turn:
                    if is_king_in_path_of_enemy_pieces(dict[val],dict[val].colour,dict):
                        print("THE KING FALLS")
                        dict[place_of_first_click] = dict[place_of_second_click]
                        dict[place_of_first_click].letnum_notation_position = place_of_first_click
                        dict[place_of_first_click].position = (1+x//50,8-y//50)
                        dict[place_of_second_click] = buffer_to_check_for_king
                        dict[place_of_first_click] = has_it_moved_before
                        print("GO BACK")
                        pieces_onto_board(dict,screen)
                        pygame.display.flip()
                        #this is needed so that the turn goes back to white, it essentially checks to make sure the king isn't in danger, and if it is, sends it back to the original turn
                        if turn == "White":
                            turn = "Black"
                        else:
                            turn = "White"
                        return 1
                    
        
        pieces_onto_board(dict,screen)
        pygame.display.flip()
        return 0 

    #CASTLING 
    elif type(dict[place_of_second_click]) !=int: 
        if dict[place_of_first_click].piece == "King" and dict[place_of_second_click].piece == "Rook" and  dict[place_of_first_click].colour == turn and dict[place_of_second_click].colour == turn and dict[place_of_first_click].castle != True and dict[place_of_second_click].castle !=True:
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
                    print(interchange_number_and_letter(val*direction_of_movement + 1+x//50) + str(8-y//50))
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
                
                #REDRAWING THE BOARD
                for row in range(8):
                    for col in range(8):
                        color = GREEN if (row + col) % 2 == 0 else LIGHT_BLUE
                        pygame.draw.rect(screen, color, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
                pieces_onto_board(dict,screen)
                pygame.display.flip()
                
                #SWITCHING TURNS 
                if turn == "White":
                    turn = "Black"
                else:
                    turn ="White"
                
                #MAKING SURE CASTLING CAN'T HAPPEN AGAIN 
                dict[new_king_place].castle = True
                dict[new_rook_place].castle = True
                return 0
    else:
        print(f"invalid move for {dict[place_of_first_click].piece} at {dict[place_of_first_click].letnum_notation_position}")
        return 0 
    
    

def random_move(dict,screen):
    print(turn)
    list_of_turn_pieces = []
    rooks = []
    for val in dict:
        if type(dict[val])!= int and dict[val].colour == turn and dict[val].move_list() != []:
            list_of_turn_pieces.append(val)
            if dict[val].piece == "Rook":
                rooks.append(val)
    chosen_piece = random.choice(list_of_turn_pieces)
    
    print(list_of_turn_pieces)
    moves = dict[chosen_piece].move_list()
    print(moves)
    if dict[chosen_piece].piece == "King":
        for r in rooks:
            if dict[r].moved == False and dict[chosen_piece].moved == False:
                moves.append(dict[r].letnum_notation_position)
    print(moves)
    chosen_move = random.choice(moves)
    # print(dict[interchange_number_and_letter(1+pos1x//50) + str(8-pos1y//50)].piece)
    # print(interchange_number_and_letter(1+pos2x//50) + str(8-pos2y//50))
    
    print((dict[chosen_piece].position[0]-1)*50,(8-dict[chosen_piece].position[1])*50)
    print((int(interchange_number_and_letter(chosen_move[0]))-1)*50,(8-int(chosen_move[1]))*50)
    do_move((dict[chosen_piece].position[0]-1)*50,(8-dict[chosen_piece].position[1])*50,(int(interchange_number_and_letter(chosen_move[0]))-1)*50,(8-int(chosen_move[1]))*50,dict,screen)
            
    
    
    
    
 



#PROMOTION
def check_pawn_promotion_for_colour(dict,screen,colour):
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
