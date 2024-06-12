import os
import random

keyboard_mapping = {
    'a': '9',
    'b': '0',
    'c': '[',
    'd': ';',
    'e': '1',
    'f': '4',
    'g': '3',
    'h': '5',
    'i': '8',
    'j': '7',
    'k': '6',
    'l': '\'',
    'm': ',',
    'n': '.',
    'o': '2',
    'p': ']',
    'q': '`',
    'r': '!',
    's': '@',
    't': '#',
    'u': '$',
    'v': '%',
    'w': '^',
    'x': '&',
    'y': '*',
    'z': '(',
    'A': ')',
    'B': '_',
    'C': '+',
    'D': '-',
    'E': '=',
    'F': '{',
    'G': '}',
    'H': '|',
    'I': '\\',
    'J': ':',
    'K': '"',
    'L': '<',
    'M': '>',
    'N': '?',
    'O': '/',
    'P': '~',
    'Q': '`',
    'R': '!',
    'S': '@',
    'T': '#',
    'U': '$',
    'V': '%',
    'W': '^',
    'X': '&',
    'Y': '*',
    'Z': '(',
    '`': 'q',
    '~': 'Q',
    '1': 'e',
    '!': 'E',
    '2': 'o',
    '@': 'O',
    '3': 'g',
    '#': 'G',
    '4': 'f',
    '$': 'F',
    '5': 'h',
    '%': 'H',
    '6': 'k',
    '^': 'K',
    '7': 'j',
    '&': 'J',
    '8': 'i',
    '*': 'I',
    '9': 'a',
    '(': 'A',
    '0': 'b',
    ')': 'B',
    '-': 'D',
    '_': 'C',
    '=': 'R',
    '+': 'V',
    '[': 'c',
    '{': 'V',
    ']': 'p',
    '}': 'N',
    '\\': 'M',
    '|': 'L',
    ';': 'd',
    ':': 'J',
    '\'': 'l',
    '"': 'K',
    ',': 'm',
    '<': 'L',
    '.': 'n',
    '>': 'M',
    '/': 'O',
    '?': 'N',
    '.': 'n',
    '>': 'M',
    '/': 'O',
    '?': 'N',
    ' ': ' ',
    '\n':'\n'
}

class Database:

    # THE SYSTEM REQUIRES A PATH THAT WILL ACT AS AN OPERAND
    # IN EVERY DEFINITION, THEREFORE IT MUST BE PASSED IN FROM
    # THE INIT FUNCTION

    def __init__(self, dbpath):
        
        self.database = dbpath


        if os.path.exists(self.database):
            with open(self.database, "r") as d:
                self.dbread = d.read()
                self.maxrows = self.dbread.split("\n")
                self.dbcols = []
                self.maxcol = self.maxrows[0].split("###")
                
                for dbr in self.maxcol:
                    targ = dbr.split("$$$")
                    self.dbcols.append(targ[0])

    # THE APPEND FUCTION ADDS A NEW DATABASE BASED ON THE COLUMNS OF
    # THE DATABASE FILE

    def append(self, *args):
        toappend = "\n"
        if len(args) == (len(self.maxcol) - 1):
            for a in args:
                i = args.index(a)
                if i != 0:
                    val = "###"+ self.dbcols[i] + "$$$" + a
                    toappend = toappend + val
                else:
                    val = self.dbcols[i] + "$$$" + a
                    toappend = toappend + val

            self.dbread += toappend
            with open(self.database, "w") as wd:
                wd.write(self.dbread)
            
        # print(self.maxrows, self.maxcol, self.dbcols)


    # THE REMOVE FUNCTION, DELETES A WHOLE ROW FROM THE DATABASE

    def remove(self, arg, value):
        towrite = ""

        for mr in self.maxrows:
            if arg+"$$$"+value in mr:
                self.maxrows.remove(mr)
        
        for ndb in self.maxrows:
            if self.maxrows.index(ndb) == (len(self.maxrows)) - 1:
                towrite += ndb
            else:
                towrite += ndb + "\n"

        with open(self.database, "w") as wdb:
            wdb.write(towrite)


    # THE CREATE DATABASE DEFINITION CREATES A NEW DATABASE IN THE FILE PATH SPECIFIED
    # IF A FILE DOES NOT EXIST IT CREATES IT AND IF IT DOES THEN IT OVERWRITE
    # THE ARGUMENTS IN THIS CASE ARE THE ROWS


    def createdb(self, *args):
        towrite = ""
        for argument in args:
            if args.index(argument) == 0:
                towrite += argument + "$$$null"
            else:
                towrite += "###"+argument+"$$$null"
        with open(self.database, "w") as wdb:
            wdb.write(towrite)

    # ISINDB STANDS FOR IS IN DATABASE, THIS RETURNS A VALUE THAT SIGNIFIES THE INDEX OR LINE 
    # OF THE THING YOU ARE LOOKING FOR IN THE DATABASE

    def isindb(self, arg, value):
        for mr in self.maxrows:
            if arg+"$$$"+value in mr:
                mrdb = mr.split("###")
                for m in mrdb:
                    if arg+"$$$"+value == m:
                        return self.maxrows.index(mr)
                    
    
    # Find row does the same thing to isindb, except it requires all the arguments in the database 
    # file to be passed in

    def findrow(self, *args):
        to_match = ""
        if len(args) == len(self.maxrows) - 1:
            for arg in args:
                i = args.index(arg)
                if i != 0:
                    to_match += "###" + self.dbcols[i] + "$$$" + arg
                else:
                    to_match += self.dbcols[i] + "$$$" + arg
            for mr in self.maxrows:
                if to_match == mr:
                    return self.maxrows.index(mr)
                
            
    # the update function requires an index or line of the db to be changed then 
    # updates it in relation to the data provided

    def update(self, row, arg, val):
        to_change = arg +"$$$"+val
        at_line = self.maxrows[row]
        new_line = ""
        for inval in at_line.split("###"):
            if arg+"$$$" in inval:
                new_line = at_line.replace(inval, to_change)
        with open(self.database, "w") as wdb:
            wdb.write(self.dbread.replace(at_line, new_line))


    # the resetdb function clears the database back to null

    def resetdb(self):
        with open(self.database, "w") as wdb:
            wdb.write(self.dbread[:self.dbread.find("\n")])

    def encryptdb(self):
        # Test the dictionary
        decription_times = 1#random.randint(3, 10)
        self.new_db = ""
        for _ in range(decription_times):
            for char in self.dbread:
                for key, value in keyboard_mapping.items():
                    if char == key:
                        self.new_db += value

        with open(self.database, "w") as wdb:
            wdb.write(self.new_db)

    def decryptdb(self):
        new_dcb = ""
        # dt = to_decrypt[1]
        enc_db = self.dbread
        # for _ in range(dt):
        for char in range(len(enc_db)):
            for key, value in keyboard_mapping.items():
                if enc_db[char] == value:
                    new_dcb += key
                    break

        self.dbread = new_dcb
        print(new_dcb)

        
# this code was made and distributed by FANEVESAL PETER a student of the university of DODOMA, please do not clone or copy as owned property