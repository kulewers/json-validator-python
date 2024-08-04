#!/usr/bin/python3

from enum import Enum, auto

import sys


class TokenType(Enum):
    LEFT_BRACE = auto()
    RIGHT_BRACE = auto()
    LEFT_SQUARE_BRACE = auto()
    RIGHT_SQUARE_BRACE = auto()
    COMMA = auto()
    COLON = auto()
    STRING = auto()
    NUMBER = auto()
    IDENTIFIER = auto()
    TRUE = auto()
    FALSE = auto()
    NULL = auto()
    EOF = auto()


class Token:
    def __init__(self, type, lexeme, literal = None,  line = None):
        self.type = type
        self.lexeme = lexeme
        self.literal = literal
        self.line = line
    
    def __str__(self):
        return str(self.type) + " " + str(self.literal)


class Scanner:
    tokens = []
    start = 0
    current = 0
    line = 1
    keywords = {
        'true': TokenType.TRUE,
        'false': TokenType.FALSE,
        'null': TokenType.NULL,
    }

    def __init__(self, source):
        self.tokens = []
        self.source = source

    def error(self, line, message):
        print("[line " + str(line) + "] Error: " + message)

    def scanTokens(self):
        while(not self.isAtEnd()):
            self.start = self.current
            self.scanToken()
        
        self.tokens.append(Token(TokenType.EOF, '', None, self.line))
        return self.tokens
    
    def scanToken(self):
        c = self.advance()
        match c:
            case "{": self.addToken(TokenType.LEFT_BRACE)
            case "}": self.addToken(TokenType.RIGHT_BRACE)
            case "[": self.addToken(TokenType.LEFT_SQUARE_BRACE)
            case "]": self.addToken(TokenType.RIGHT_SQUARE_BRACE)
            case ":": self.addToken(TokenType.COLON)
            case ",": self.addToken(TokenType.COMMA)
            case " " | "\r" | "\t": pass
            case "\n": self.line += 1
            case '"': self.string()
            case num if self.isDigit(num): self.number()
            case alpha if self.isAlpha(alpha): self.identifier()
            case _:
                self.error(self.line, "Unexpected character.")

    def identifier(self):
        while self.isAlphaNumeric(self.peek()): self.advance()

        text = self.source[self.start : self.current]
        type = self.keywords.get(text, TokenType.IDENTIFIER)

        self.addToken(type)
    
    def number(self):
        while self.isDigit(self.peek()): self.advance()

        if self.peek() == '.' and self.isDigit(self.peekNext()):
            self.advance()

            while self.isDigit(self.peek()): self.advance()

        self.addToken(TokenType.NUMBER, float(self.source[self.start : self.current]))

    def string(self):
        while self.peek() != '"' and not self.isAtEnd():
            if self.peek() == '\n': self.line += 1
            self.advance()

        if self.isAtEnd():
            self.error(self.line, "Unterminated string.")
            return
        
        self.advance()

        value = self.source[self.start + 1 : self.current - 1]
        self.addToken(TokenType.STRING, value)
                
    def match(self, expected):
        if self.isAtEnd(): return False
        if self.source[self.current] != expected: return False

        self.current += 1
        return True

    def peek(self):
        if self.isAtEnd(): return '\0'
        return self.source[self.current]

    def peekNext(self):
        if self.current + 1 >= len(self.source): return '\0'
        return self[self.current + 1]
    
    def isAlpha(self, c):
        return (c >= 'a' and c <= 'z') or (c >= 'A' and c <= 'Z')
    
    def isAlphaNumeric(self, c):
        return self.isAlpha(c) or self.isDigit(c)

    def isDigit(self, c):
        return c >= '0' and c <= '9'

    def isAtEnd(self):
        return self.current >= len(self.source)
    
    def advance(self):
        char = self.source[self.current]
        self.current += 1
        return char
    
    def addToken(self, type, literal=None):

        text = self.source[self.start : self.current]
        self.tokens.append(Token(type, text, literal, self.line))


class Parser:
    current = 0

    def __init__(self, tokens):
        self.tokens = tokens

    def parse(self):
        return self.object()
        
    def object(self):
        if not self.match(TokenType.LEFT_BRACE): return False
        if self.match(TokenType.RIGHT_BRACE): return True
        while True:
            if not self.match(TokenType.STRING): return False
            if not self.match(TokenType.COLON): return False
            if not self.value(): return False
            if self.match(TokenType.RIGHT_BRACE): return True
            if not self.match(TokenType.COMMA): return False

    def value(self):
        if self.match(TokenType.STRING, TokenType.NUMBER, TokenType.TRUE, TokenType.FALSE, TokenType.NULL): return True
        if self.object(): return True
        if self.array(): return True
        return False

    def array(self):
        if not self.match(TokenType.LEFT_SQUARE_BRACE): return False
        if self.match(TokenType.RIGHT_SQUARE_BRACE): return True
        while True:
            if not self.value(): return False
            if self.match(TokenType.RIGHT_SQUARE_BRACE): return True
            if not self.match(TokenType.COMMA): return False

    def match(self, *types):
        for type in types:
            if self.check(type):
                self.advance()
                return True

    def check(self, type):
        if self.isAtEnd(): return False
        return self.peek().type == type

    def peek(self):
        return self.tokens[self.current]
    
    def isAtEnd(self):
        return self.peek() == TokenType.EOF
    
    def advance(self):
        if not self.isAtEnd(): self.current += 1
        return self.previous()
    
    def previous(self):
        return self.tokens[self.current - 1]

def main():
    if len(sys.argv) > 2:
        print('Usage: jsonparser.py [file]')
        sys.exit(1)
    elif len(sys.argv) == 2:
        validity = runFile(sys.argv[1])
    else:
        validity = runPrompt()
    print(validity)

def runFile(path):
    with open(path, 'r') as f:
        text = f.read()
    return run(text)

def runPrompt():
    input = sys.stdin.read()
    return run(input)
    
def run(source):
    scanner = Scanner(source)
    tokens = scanner.scanTokens()

    # for token in tokens:
    #     print(token)

    parser = Parser(tokens)
    validity = parser.parse()
    return validity

if __name__ == '__main__':
    main()
