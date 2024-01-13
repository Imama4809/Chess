import pygame as py 
import sys
import os


def creat_board_dict(dthc):  # dictionary to hold chessboard
    for letters in 'abcdefgh':
        for values in range(1,9):
            dthc[letters + str(values)] = 0
    return dthc
from sol import interchange_number_and_letter

#creating the chessboard 
chessboard = {}
creat_board_dict(chessboard)



class PAM: #rename to pieces and moves after 
    def __init__(self, piece, colour, position, moved = False,turn_after_double = False,double_move=False, castle = False): #INIT (haha get it, sounds british)
        self.piece = piece
        self.colour = colour
        if self.colour == 'White':
            self.othercolour = 'Black'
        if self.colour == 'Black':
            self.othercolour = 'White'
        self.letnum_notation_position = position 
        self.position = (interchange_number_and_letter(position[0]),int(position[1])) #this returns the position as a tuple of 2 numbers i.e. a4 --> (1,4)
        chessboard[position] = self
        self.moved = moved
        self.turn_after_double = False
        self.double_move = False
        self.castle = castle
    def move_list(self):
        #special
        if self.piece == 'King': ##special case
            m_l = []
            for i,j in [(1,0),(0,1),(-1,0),(0,-1),(1,1),(-1,1),(1,-1),(-1,-1)]:
                if (self.position[0]+i-4.5)**2 > 12.25 or (self.position[1]+j-4.5)**2 > 12.25: 
                    #the position is in values between 1 and 8, thus 4.5 being the middle and 3.5 being the distance from the median to the max and min
                    #this means that if we subtract a value that is outside of the range of 1, and 8 from the median, it would be greater than 3.5**2
                    #thus to filter out values outside that range, we subtract the number by 4.5 and check if its greater than 3.5**2 (12.25)
                    continue
                if chessboard[(interchange_number_and_letter(self.position[0]+i) + str(self.position[1]+j))] !=0 and chessboard[(interchange_number_and_letter(self.position[0]+i) + str(self.position[1]+j))] !=1:#this makes sure the position the piece is trying to go to is empty 
                    if chessboard[(interchange_number_and_letter(self.position[0]+i) + str(self.position[1]+j))].colour != self.colour: #this checks if the piece is capturable 
                        m_l.append((interchange_number_and_letter(self.position[0]+i) + str(self.position[1]+j ))) #if it is capturable, then add it to teh list of positions
                    continue #move on to next iteration n
                m_l.append((interchange_number_and_letter(self.position[0]+i) + str(self.position[1]+j)))
            return m_l
        #special
        if self.piece == 'Pawn': ##special case 
            if self.colour == 'White':
                movement = 1
            if self.colour == 'Black':
                movement = -1
            m_l = []#it is seperated into two in order to help with dealing with possible king movement 
            list_for_ij = [(0,movement)]
            if self.moved == False:
                list_for_ij = [(0,movement),(0,movement*2)]  
            for i,j in list_for_ij:
                if (self.position[0]+i-4.5)**2 > 12.25 or (self.position[1]+j-4.5)**2 > 12.25: 
                    #the position is in values between 1 and 8, thus 4.5 being the middle and 3.5 being the distance from the median to the max and min
                    #this means that if we subtract a value that is outside of the range of 1, and 8 from the median, it would be greater than 3.5**2
                    #thus to filter out values outside that range, we subtract the number by 4.5 and check if its greater than 3.5**2 (12.25)
                    continue
                if chessboard[(interchange_number_and_letter(self.position[0]+i) + str(self.position[1]+j))] !=0 and chessboard[(interchange_number_and_letter(self.position[0]+i) + str(self.position[1]+j))] !=1:#this makes sure the position the piece is trying to go to is empty 
                    continue #move on to next iteration 
                m_l.append((interchange_number_and_letter(self.position[0]+i) + str(self.position[1]+j)))
            for i,j in [(1,movement),(-1,movement)]:
                if (self.position[0]+i-4.5)**2 > 12.25 or (self.position[1]+j-4.5)**2 > 12.25: 
                    #the position is in values between 1 and 8, thus 4.5 being the middle and 3.5 being the distance from the median to the max and min
                    #this means that if we subtract a value that is outside of the range of 1, and 8 from the median, it would be greater than 3.5**2
                    #thus to filter out values outside that range, we subtract the number by 4.5 and check if its greater than 3.5**2 (12.25)
                    continue
                if chessboard[(interchange_number_and_letter(self.position[0]+i) + str(self.position[1]+j))] !=0:#this checks if the position the piece is trying to go to is empty 
                    if chessboard[(interchange_number_and_letter(self.position[0]+i) + str(self.position[1]+j))] ==1:
                        m_l.append((interchange_number_and_letter(self.position[0]+i) + str(self.position[1]+j ))) 
                        continue
                    if chessboard[(interchange_number_and_letter(self.position[0]+i) + str(self.position[1]+j))].colour != self.colour: #this checks if the piece is capturable 
                        m_l.append((interchange_number_and_letter(self.position[0]+i) + str(self.position[1]+j ))) #if it is capturable, then add it to teh list of positions
                    continue #move on to next iteration 
    
            return m_l
        
        if self.piece in ['Queen','Bishop','Rook']:
            possible_directions_queen = [(1,0),(0,1),(-1,0),(0,-1),(1,1),(-1,1),(1,-1),(-1,-1)]
            possible_directions_bishop = [(1,1),(-1,1),(1,-1),(-1,-1)]
            possible_directions_rook = [(1,0),(0,1),(-1,0),(0,-1)]
            m_l = [] # move list
            list_used = eval('possible_directions_' + self.piece.lower())
            for i,j in list_used: #these are the possible directional diagonals and lines of queen movement
                inc_i=i 
                inc_j=j
                #the number we can add is equivalent to the starting value of i and j, thus we save it and use those saved values 
                while True:
                    if (self.position[0]+i-4.5)**2 > 12.25 or (self.position[1]+j-4.5)**2 > 12.25: 
                        #the position is in values between 1 and 8, thus 4.5 being the middle and 3.5 being the distance from the median to the max and min
                        #this means that if we subtract a value that is outside of the range of 1, and 8 from the median, it would be greater than 3.5**2
                        #thus to filter out values outside that range, we subtract the number by 4.5 and check if its greater than 3.5**2 (12.25)
                        break
                    if chessboard[(interchange_number_and_letter(self.position[0]+i) + str(self.position[1]+j))] !=0 and chessboard[(interchange_number_and_letter(self.position[0]+i) + str(self.position[1]+j))] !=1:#this makes sure the position the piece is trying to go to is empty 
                        if chessboard[(interchange_number_and_letter(self.position[0]+i) + str(self.position[1]+j))].colour != self.colour: #this checks if the piece is capturable 
                            m_l.append((interchange_number_and_letter(self.position[0]+i) + str(self.position[1]+j ))) #if it is capturable, then add it to teh list of positions
                        break #break out of the iteration 
                    #write a comment for this function ########################################################################3
                    m_l.append((interchange_number_and_letter(self.position[0]+i) + str(self.position[1]+j)))
                    i +=inc_i
                    j +=inc_j
            return m_l
        #horsey is special (I hate Josh Choong)
        if self.piece == 'Knight':
            m_l = []
            for i,j in [(1,2),(2,1),(-1,2),(2,-1),(1,-2),(-2,1),(-1,-2),(-2,-1)]: #these are the possible movments for a knight
                if (self.position[0]+i-4.5)**2 > 12.25 or (self.position[1]+j-4.5)**2 > 12.25:
                    continue
                if chessboard[(interchange_number_and_letter(self.position[0]+i) + str(self.position[1]+j))] !=0 and chessboard[(interchange_number_and_letter(self.position[0]+i) + str(self.position[1]+j))] !=1:#this makes sure the position the piece is trying to go to is empty 
                    if chessboard[(interchange_number_and_letter(self.position[0]+i) + str(self.position[1]+j))].colour != self.colour: #this checks if the piece is capturable 
                        m_l.append((interchange_number_and_letter(self.position[0]+i) + str(self.position[1]+j )))#if it is capturable, then add it to teh list of positions
                    continue #break out of the iteration 
                #we use continue in these functions because we don't have a while True loop to iterate through diagonals or lines
                m_l.append((interchange_number_and_letter(self.position[0]+i) + str(self.position[1]+j)))
            return m_l
    def get_piece_under(self):
        pos_to_delete = list(self.position)
        num = 0
        if self.colour == "White":
            num = -1
        if self.colour == "Black":
            num = 1
        pos_to_delete[1] = int(self.position[1])+num 
        letnum_pos = interchange_number_and_letter(pos_to_delete[0]) + str(pos_to_delete[1])
        return letnum_pos
    def checker(self): #this is a function to help with undersatnding how things work, delete after 
        # print(self.position)
        return self.position
    
    

    
def board_setup(chessboard_dictionary):
    #white pieces 
    wr1 = PAM('Rook','White','a1')
    wh1 = PAM('Knight','White','b1')# h for horsy, courtesy of Josh Choong
    wb1 = PAM('Bishop','White','c1')
    wqu = PAM('Queen','White','d1')
    wki = PAM('King','White','e1')
    wb2 = PAM('Bishop','White','f1')
    wh2 = PAM('Knight','White','g1')# h for horsy, courtesy of Josh Choong
    wr2 = PAM('Rook','White','h1')
    wp1 = PAM('Pawn','White','a2')
    wp2 = PAM('Pawn','White','b2')
    wp3 = PAM('Pawn','White','c2')
    wp4 = PAM('Pawn','White','d2')
    wp5 = PAM('Pawn','White','e2')
    wp6 = PAM('Pawn','White','f2')
    wp7 = PAM('Pawn','White','g2')
    wp8 = PAM('Pawn','White','h2')
    
    #black pieces 
    br1 = PAM('Rook','Black','a8')
    bh1 = PAM('Knight','Black','b8')# h for horsy, courtesy of Josh Choong
    bb1 = PAM('Bishop','Black','c8')
    bqu = PAM('Queen','Black','d8')
    bki = PAM('King','Black','e8')
    bb2 = PAM('Bishop','Black','f8')
    bh2 = PAM('Knight','Black','g8')# h for horsy, courtesy of Josh Choong
    br2 = PAM('Rook','Black','h8')
    bp1 = PAM('Pawn','Black','a7')
    bp2 = PAM('Pawn','Black','b7')
    bp3 = PAM('Pawn','Black','c7')
    bp4 = PAM('Pawn','Black','d7')
    bp5 = PAM('Pawn','Black','e7')
    bp6 = PAM('Pawn','Black','f7')
    bp7 = PAM('Pawn','Black','g7')
    bp8 = PAM('Pawn','Black','h7')


board_setup(chessboard)
from Pywindow import create_chessboard
create_chessboard(chessboard)
