def interchange_number_and_letter(inp): # change letters to numbers or numbers to letters
    l = "0abcdefgh" #list to be able to interchange values, 0 is put at the beginning to make the interchange cleaner 
    if type(inp) == str:
        return l.find(inp)
    if type(inp) == int:
        return l[inp]
    

