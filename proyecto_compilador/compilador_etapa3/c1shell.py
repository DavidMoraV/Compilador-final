# c1shell.py compiler 
import sys, time 

class Token:
   def __init__(self, line, column, category, lexeme):
      self.line = line
      self.column = column
      self.category = category
      self.lexeme = lexeme

   def __str__(self):
      return f"token type = {self.category}, lexema: {self.lexeme}, at line {self.line}, col {self.column}"


# global variables 
outfile = None     # output (i.e., asm lang program) file
source = ''        # receives entire source program
sourceindex = 0    # index into the source code in source
line = 0           # current line number 
column = 0         # current column number
tokenlist = []     # list of tokens produced by tokenizer
tokenindex = -1    # index into tokens list
token = None       # current token
prevchar = '\n'    # '\n' in prevchar signals start of new line
blankline = True
symbol = []        # list of variable names
value = []
tempcount = 0      # sequence number for temp asm variables
strings = []
register_count = 0
strings = []



# constants
EOF           = 0      # end of file
PRINT         = 1      # 'print' keyword
UNSIGNEDINT   = 2      # unsigned integer
NAME          = 3      # identifier that is not a keyword
ASSIGNOP      = 4      # '=' assignment operator
LEFTPAREN     = 5      # '('
RIGHTPAREN    = 6      # ')'
PLUS          = 7      # '+'
MINUS         = 8      # '-'
TIMES         = 9      # '*'
NEWLINE       = 10     # end of line
ERROR         = 11     # if not any of the above, then error
ERROR        = 11
POWER        = 12     # ^
DIV          = 13     # /
IF           = 14     # 'if'
GT           = 15     # >
LT           = 16     # <
BEGINBLOCK   = 17     # [
ENDBLOCK     = 18     # ]
STRING       = 19     # "texto"

# displayable names for each token category
catnames = ['EOF', 'PRINT', 'UNSIGNEDINT', 'NAME', 'ASSIGNOP',
            'LEFTPAREN', 'RIGHTPAREN', 'PLUS', 'MINUS',
            'TIMES', 'NEWLINE', 'ERROR', 'POWER', 'DIV', 'IF', 'GT', 'LT',
            'BEGINBLOCK', 'ENDBLOCK', 'STRING']


# keywords and their token categories}
keywords = {
    'print': PRINT,
    'if': IF
}


# one-character tokens and their token categories
smalltokens = {
    '=': ASSIGNOP,
    '(': LEFTPAREN,
    ')': RIGHTPAREN,
    '+': PLUS,
    '-': MINUS,
    '*': TIMES,
    '\n': NEWLINE,
    '': EOF,
    '^': POWER,
    '/': DIV,
    '>': GT,
    '<': LT,
    '[': BEGINBLOCK,
    ']': ENDBLOCK
}


#################
# main function #
#################
def main():
   global source, outfile

   if len(sys.argv) == 3:
      try:
         infile = open(sys.argv[1], 'r')
         source = infile.read()   # read source code
      except IOError:
         print('Cannot read input file ' + sys.argv[1])
         sys.exit(1)

      try:
         outfile = open(sys.argv[2], 'w')
      except IOError:
         print('Cannot write to output file ' + sys.argv[2])
         sys.exit(1)
   else:
      print('Wrong number of command line arguments')
      print('Format: python c1.py <infile> <outfile>')
      sys.exit(1)

   if source[-1] != '\n':
      source = source + '\n'

   outfile.write('@ ' + time.strftime('%c') + '%34s' % 'YOUR NAME HERE\n')
   outfile.write('@ ' + 'Compiler    = ' + sys.argv[0] + '\n')
   outfile.write('@ ' + 'Input file  = ' + sys.argv[1] + '\n')
   outfile.write('@ ' + 'Output file = ' + sys.argv[2] + '\n')

   try:
      tokenizer()

      for one_token in tokenlist:
         print(one_token)             
      # parse and and generate assembly language
      outfile.write(
         '@------------------------------------------- Assembler code\n')
      parser()
   #   escribirCodigo(segmentoCodigo, segmentoDatos )
   # on an error, display an error message
   # token is the token object on which the error was detected
   except RuntimeError as emsg: 
      # output slash n in place of newline
      lexeme = token.lexeme.replace('\n', '\\n')
      print('\nError on '+ "'" + lexeme + "'" + ' line ' +
         str(token.line) + ' column ' + str(token.column))
      print(emsg)         # message from RuntimeError object
      outfile.write('\nError on '+ "'" + lexeme + "'" + ' line ' +
         str(token.line) + ' column ' + str(token.column) + '\n')
      outfile.write(str(emsg) + '\n') 
   outfile.close()

####################
# tokenizer        #
####################
def tokenizer():
   global token
   curchar = ' '  # inicializar con espacio

   while True:
      # Saltar espacios (pero no saltar saltos de línea)
      while curchar != '\n' and curchar.isspace():
         curchar = getchar()

      # Inicializar nuevo token
      token = Token(line, column, None, '')

      if curchar.isdigit():
         token.category = UNSIGNEDINT
         while True:
            token.lexeme += curchar
            curchar = getchar()
            if not curchar.isdigit():
               break

      elif curchar.isalpha() or curchar == '_':
         while True:
            token.lexeme += curchar
            curchar = getchar()
            if not (curchar.isalnum() or curchar == '_'):
               break

         if token.lexeme in keywords:
            token.category = keywords[token.lexeme]
         else:
            token.category = NAME

      elif curchar in smalltokens:
         token.category = smalltokens[curchar]
         token.lexeme = curchar
         curchar = getchar()

      elif curchar == '"':
         token.lexeme = curchar
         curchar = getchar()
         while curchar != '"' and curchar != '':
            token.lexeme += curchar
            curchar = getchar()
         if curchar == '"':
            token.lexeme += '"'
            token.category = STRING
            curchar = getchar()
         else:
            token.category = ERROR
            raise RuntimeError('Cadena STRING mal formada')

      else:
         token.category = ERROR
         token.lexeme = curchar
         raise RuntimeError('Invalid token')

      # Guardar token en la lista
      tokenlist.append(token)

      if token.category == EOF:
         break


# getchar() gets next char from source and adjusts line and column
def getchar():
   global sourceindex, column, line, prevchar, blankline

   # check if starting a new line
   if prevchar == '\n':    # '\n' signals start of a new line
      line += 1            # increment line number                             
      column = 0           # reset column number
      blankline = True     # initialize blankline

   if sourceindex >= len(source): # at end of source code?
      column = 1                  # set EOF column to 1
      prevchar = ''               # save current char for next call
      return ''                   # null str signals end of source

   c = source[sourceindex] # get next char in the source program
   sourceindex += 1        # increment sourceindex to next character
   column += 1             # increment column number
   if not c.isspace():     # if c not whitespace then line not blank
      blankline = False    # indicate line not blank
   prevchar = c            # save current character

   # if at end of blank line, return space in place of '\n'
   if c == '\n' and blankline:
      return ' '
   else:
      return c             # return character to tokenizer()

##########################
# symbol table function  #
##########################
def enter(s, v):
   if s in symbol:
      return symbol.index(s)
   # otherwise, add s to symbol and return its index
   index = len(symbol)
   symbol.append(s)
   value.append(v)
   return index

####################
# parser functions #
#################### 
def advance():
   global token, tokenindex 
   tokenindex += 1
   if tokenindex >= len(tokenlist):
      raise RuntimeError('Unexpected end of file')
   token = tokenlist[tokenindex]

# advances if current token is the expected token
def consume(expectedcat):
   if (token.category == expectedcat):
      advance()
   else:
     raise RuntimeError('Expecting ' + catnames[expectedcat])

# top level function of parser
def parser():
   advance()     # advance so token holds first token
   print(".text", file=outfile)
   program()     # call function corresponding to start symbol
   # will token.category ever not equal EOF here?
   if token.category != EOF:
      raise RuntimeError('Expecting end of file')

def program():
    while token.category in [NAME, PRINT, IF]:
        stmt()

def stmt():
   simplestmt()
   consume(NEWLINE)

def simplestmt():
    if token.category == NAME:
        assignmentstmt()
    elif token.category == PRINT:
        printstmt()
    elif token.category == IF:
        ifstmt()
    else:
        raise RuntimeError('Expecting statement')


if_counter = 0  # variable global para generar etiquetas únicas

def ifstmt():
    global if_counter
    consume(IF)
    
    left = token.lexeme
    advance()
    
    if token.category == GT:
        comp = 'BLE'
    elif token.category == LT:
        comp = 'BGE'
    else:
        raise RuntimeError("Esperando comparador '<' o '>'")
    advance()
    
    right = token.lexeme
    advance()
    
    label = f".endif{if_counter}"
    if_counter += 1
    
    print(f"\tCMP {left}, {right}", file=outfile)
    print(f"\t{comp} {label}", file=outfile)
    
    consume(BEGINBLOCK)
    consume(NEWLINE)
    simplestmt()
    consume(NEWLINE)
    consume(ENDBLOCK)
    
    print(f"{label}:", file=outfile)


def condition():
    if token.category in [UNSIGNEDINT, NAME]:
        advance()
        if token.category in [GT, LT]:
            advance()
        else:
            raise RuntimeError("Esperando comparador '<' o '>'")
        if token.category in [UNSIGNEDINT, NAME]:
            advance()
        else:
            raise RuntimeError("Esperando valor luego del comparador")
    else:
        raise RuntimeError("Esperando operando en condición")

def assignmentstmt():
    left = token.lexeme
    advance()
    consume(ASSIGNOP)
    right = expr()  # regresa el resultado de expr, puede ser valor o registro
    cg_assign(left, right)



def printstmt():
    consume(PRINT)
    consume(LEFTPAREN)
    if token.category == STRING:
        index = len(strings)
        strings.append(token.lexeme)
        cg_print(index)
        advance()
    else:
        raise RuntimeError('Se esperaba un STRING dentro de print(...)')
    consume(RIGHTPAREN)


def expr():
    left = term()
    while token.category in [PLUS, MINUS]:
        op = token.category
        advance()
        right = term()
        temp = cg_gettemp()
        if op == PLUS:
            cg_add(temp, left, right)
        elif op == MINUS:
            cg_sub(temp, left, right)
        left = temp
    return left


def term():
    left = factor()
    while token.category == TIMES:
        advance()
        right = factor()
        temp = cg_gettemp()
        cg_mul(temp, left, right)
        left = temp
    return left


def factor():
    if token.category == UNSIGNEDINT:
        val = token.lexeme
        advance()
        return val
    elif token.category == NAME:
        val = token.lexeme
        advance()
        return val
    else:
        raise RuntimeError('Expecting factor')

############################
# code generator functions #
############################
def cg_prolog():
    global outfile
    print(".text", file=outfile)

def cg_epilog():
    global outfile, strings
    print("\tMOV R7, #1", file=outfile)
    print("\tSWI 0", file=outfile)
    print("\n.data", file=outfile)
    for i, s in enumerate(strings):
        print(f"msg{i}: .asciz {s}", file=outfile)

def cg_gettemp():
    global register_count
    temp = f"R{register_count}"
    register_count += 1
    return temp

def cg_assign(left, right):
    global outfile
    # Si es número literal (sin #), lo movemos a un registro primero
    if right.isdigit():
        temp = cg_gettemp()
        print(f"\tMOV {temp}, #{right}", file=outfile)
        print(f"\tMOV {left}, {temp}", file=outfile)
    else:
        print(f"\tMOV {left}, {right}", file=outfile)

def cg_print(index):
    global outfile
    label = f"msg{index}"
    print(f"\tLDR R0, ={label}", file=outfile)
    print("\tBL print_string", file=outfile)

def cg_add(dest, left, right):
    global outfile
    if left.isdigit():
        tmp_left = cg_gettemp()
        print(f"\tMOV {tmp_left}, #{left}", file=outfile)
    else:
        tmp_left = left

    if right.isdigit():
        tmp_right = cg_gettemp()
        print(f"\tMOV {tmp_right}, #{right}", file=outfile)
    else:
        tmp_right = right

    print(f"\tADD {dest}, {tmp_left}, {tmp_right}", file=outfile)

def cg_sub(dest, left, right):
    global outfile
    if left.isdigit():
        tmp_left = cg_gettemp()
        print(f"\tMOV {tmp_left}, #{left}", file=outfile)
    else:
        tmp_left = left

    if right.isdigit():
        tmp_right = cg_gettemp()
        print(f"\tMOV {tmp_right}, #{right}", file=outfile)
    else:
        tmp_right = right

    print(f"\tSUB {dest}, {tmp_left}, {tmp_right}", file=outfile)

def cg_mul(dest, left, right):
    global outfile
    if left.isdigit():
        tmp_left = cg_gettemp()
        print(f"\tMOV {tmp_left}, #{left}", file=outfile)
    else:
        tmp_left = left

    if right.isdigit():
        tmp_right = cg_gettemp()
        print(f"\tMOV {tmp_right}, #{right}", file=outfile)
    else:
        tmp_right = right

    print(f"\tMUL {dest}, {tmp_left}, {tmp_right}", file=outfile)

def cg_neg(index):
    global outfile
    print(f"\tRSB {index}, {index}, #0", file=outfile)  # Negación aritmética



####################
# start of program #
####################
main()

'''''
E:\Ing ciencia de datos\Cuarto cuatri\Paradigmas de programacion\clase 11\Compilador
python c1shell.py c1.in c1.out

'''''