import pygame
import sys
import os 
import random
import copy 
import functions
import bot

#for slice of life 

import settings

settings.init()

#from bot import evaluate_position

# Initialize Pygame
pygame.init()


#SEMANTICS 
def pieces_onto_board(dict,screen):
    for val in dict: #prints all the pieces onto the dictionary 
        if dict[val] != 0 and dict[val] !=1:
            image = pygame.image.load(f"Pieces/{dict[val].colour}_{dict[val].piece}.png")
            screen.blit(image,((dict[val].position[0]-1)*50,400-(dict[val].position[1])*50)) #we need to do 400- since the pygame window starts in the top left


    
#GAME AND MOVES
def create_chessboard_and_play_game(dict):
    WIDTH, HEIGHT = 600, 400
    LIGHT_BLUE = (173, 216, 230)
    GREEN = (55, 229, 180)
    BLACK = (0,0,0)
    SQUARE_SIZE = HEIGHT // 8
    
    

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
                return 0



        # Draw the chessboard
        for row in range(8):
            for col in range(8):
                color = GREEN if (row + col) % 2 == 0 else LIGHT_BLUE
                pygame.draw.rect(screen, color, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
                
                
        pygame.draw.rect(screen,LIGHT_BLUE,(400,0,200,400))        
                
        pieces_onto_board(dict,screen) #function to place pieces onto board
        
        # Update the display
        pygame.display.flip()
        # Set the frames per second
        pygame.time.Clock().tick(60)
       
       
       
        second_click = False #this is to check whether a second click has occurred 

        if settings.turn == "White": #turn system 
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos() #first mouse click position
                if x>400 or y>400:
                    continue
                place_of_first_click = functions.interchange_number_and_letter(1+x//50) + str(8-y//50) #location of first click  
                if dict[place_of_first_click] !=0 and dict[place_of_first_click] !=1 and dict[place_of_first_click].colour == settings.turn : #making sure its not empty 
                    while (second_click == False): #making sure second click happened 
                        for event in pygame.event.get():
                            if event.type == pygame.MOUSEBUTTONDOWN: #second mouse click position 
                                x_new, y_new = pygame.mouse.get_pos() #new cords
                                functions.do_move(x,y,x_new,y_new,dict) 
                                pieces_onto_board(dict,screen)
                                pygame.display.flip()
                                functions.check_pawn_promotion_for_colour(dict, "White") #pawn promotion 
                                if functions.checkmate_check(dict,"Black"):
                                    print("Checkmate")
                                    settings.turn = "White"
                                    return 0
                                if functions.stalemate_check(dict,"Black"):
                                    settings.turn = "White"
                                    print("Stalemate")
                                    return 0
                                second_click = True
                                break
                            if event.type == pygame.QUIT: # to quit #might be able to create a function if you take event as an input 
                                pygame.quit()
                                return 0
                            
                else:
                    print(f"its {settings.turn}'s turn")   
        if settings.turn == "Black": #blacks turn 
            bot.current_bot(dict)
            functions.check_pawn_promotion_for_colour(dict, "Black") #pawn promotion 
            if functions.checkmate_check(dict,"White"):
                settings.turn = "White"
                print("Checkmate")
                return 0
            if functions.stalemate_check(dict,"White"):
                settings.turn = "White"
                print("Stalemate")
                return 0
        #evaluate_position(dict)      
        if event.type == pygame.QUIT: # to quit 
            pygame.quit()
            return 0
                



#PROMOTION


