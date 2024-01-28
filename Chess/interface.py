import pygame as py

WIDTH, HEIGHT = 200, 400
LIGHT_BLUE = (173, 216, 230)
GREEN = (55, 229, 180)
BLACK = (0,0,0)

screen = py.display.set_mode((WIDTH, HEIGHT))
    
def create_background(screen):
    py.display.set_caption("Chessboard")
    py.draw.rect(screen,BLACK,(0,0,200,400))
    for event in py.event.get():
        if event.type == py.QUIT: # to quit 
            py.quit()
            break
    py.display.update() 
    
while True:
    create_background(screen)
    #BUTTONS
    
    
    #Go Back
    #Go Forward
    #Play????
    
    #Bar with eq values 
    
    #Reset position
    
    #Switch Sides -> later 
    
    
    #movelist -> later later 
    




