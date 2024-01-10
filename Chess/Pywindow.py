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


    
# Constants
def create_chessboard(dict):
    global turn
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
                    
                            
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos() #first mouse click position
            place_of_first_click = interchange_number_and_letter(1+x//50) + str(8-y//50) #location of first click 
            if dict[place_of_first_click] !=0 and dict[place_of_first_click] !=1 and dict[place_of_first_click].colour == turn : #making sure its not empty 
                while (second_click == False):
                    for event in pygame.event.get():
                        if event.type == pygame.MOUSEBUTTONDOWN: #second mouse click position 
                            x_new, y_new = pygame.mouse.get_pos()
                            
                            domove(x,y,x_new,y_new,dict,screen)
                            check_pawn_promotion_for_colour(dict,screen, "White")
                            check_pawn_promotion_for_colour(dict,screen,"Black")
                            second_click = True
                            break
                            
                        if event.type == pygame.QUIT: # to quit #might be able to create a function if you take event as an input 
                            pygame.quit()
                            sys.exit()   
            else:
                print(f"its {turn}'s turn")   
                    
                        
        if event.type == pygame.QUIT: # to quit 
            pygame.quit()
            sys.exit()
                
            


# def compmove(dict,screen):
#     global turn
#     for val in dict:
        
#     place_of_first_click = random.choice()

def domove(x,y,x_new,y_new,dict,screen):
    WIDTH, HEIGHT = 400, 400
    LIGHT_BLUE = (173, 216, 230)
    GREEN = (55, 229, 180)
    SQUARE_SIZE = WIDTH // 8
    check = False
    global turn 
    global second_click
    place_of_first_click = interchange_number_and_letter(1+x//50) + str(8-y//50) #location of first click 
    place_of_second_click = interchange_number_and_letter(1+x_new//50) + str(8-y_new//50) #this gets the location on the board of the second click 
    if place_of_second_click in dict[place_of_first_click].move_list(): 
                              
        #specific check to see if its a pawn and treats it differently on first move 
        if dict[place_of_first_click].piece == 'Pawn' and dict[place_of_first_click].moved == False and len(dict[place_of_first_click].move_list()) == 2 and place_of_second_click == dict[place_of_first_click].move_list()[1]:
            dict[dict[place_of_first_click].move_list()[0]] = 1
            dict[place_of_first_click].double_move = True
            dict[place_of_first_click].moved = True
        
        
        #changes positions
        buffer_to_check_for_king = dict[place_of_second_click]
        dict[place_of_second_click] = dict[place_of_first_click]
        dict[place_of_second_click].position = (1+x_new//50,8-y_new//50) #we have to change it to the coordinate value in the class its defined as a coordinate value 
        dict[place_of_second_click].letnum_notation_position = place_of_second_click
        has_it_moved_before = dict[place_of_second_click]
        dict[place_of_second_click].moved = True
        if buffer_to_check_for_king == 1:
            dict[dict[place_of_second_click].get_piece_under()] = 0
            pieces_onto_board(dict,screen)
            pygame.display.flip()
        if turn == "White":
            turn = "Black"
        elif turn == "Black":
            turn ="White" 
            
            
            
            
        dict[place_of_first_click] = 0
                
        #makes sure after the first move, that you cannot en passant anymore         
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
                        
        #print(dict)
        
        
                        
        #MAKING SURE KING CANNOT BE IN LINE OF SIGHT AND IF IT IS, IT RETURNS BACK TO ORIGINAL POSITION 
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
                        #this is needed so that the turn goes back to white, it essentially checks to make sure the king isn't in danger, and if it is, sends it back to the original turn
                        if turn == "White":
                            turn = "Black"
                        elif turn == "Black":
                            turn ="White"
                    
                    
        
        pieces_onto_board(dict,screen)
        pygame.display.flip()
        return 0 

    #CASTLING 
    elif dict[place_of_second_click] !=0 and dict[place_of_second_click] !=1:
        if dict[place_of_first_click].piece == "King" and dict[place_of_second_click].piece == "Rook" and  dict[place_of_first_click].colour == turn and dict[place_of_second_click].colour == turn:
            if dict[place_of_first_click].moved == False and dict[place_of_second_click].moved == False:
                list_of_vals_that_must_be_empty = []
                direction_of_movement = dict[place_of_first_click].position[0] - dict[place_of_second_click].position[0]
                if direction_of_movement > 0:
                    direction_of_movement = -1
                elif direction_of_movement <0:
                    direction_of_movement=1
                for val in range(1,abs(dict[place_of_first_click].position[0]-dict[place_of_second_click].position[0])):
                    print(interchange_number_and_letter(val*direction_of_movement + 1+x//50) + str(8-y//50))
                    if dict[interchange_number_and_letter(val*direction_of_movement + 1+x//50) + str(8-y//50)]!=0 and dict[interchange_number_and_letter(val*direction_of_movement + 1+x//50) + str(8-y//50)]!=1 or interchange_number_and_letter(val*direction_of_movement + 1+x//50) + str(8-y//50) in paths_of_enemy_pieces(dict,dict[place_of_first_click].othercolour):
                            print("sorry, you can't castle through pieces")
                            second_click = True
                            check = True
                            break
                if check==True:
                    return 0
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
                for row in range(8):
                    for col in range(8):
                        color = GREEN if (row + col) % 2 == 0 else LIGHT_BLUE
                        pygame.draw.rect(screen, color, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
                pieces_onto_board(dict,screen)
                pygame.display.flip()
                if turn == "White":
                    turn = "Black"
                elif turn == "Black":
                    turn ="White"
                return 0
    else:
        print(f"invalid move for {dict[place_of_first_click].piece} at {dict[place_of_first_click].letnum_notation_position}")
        return 0 
    
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
