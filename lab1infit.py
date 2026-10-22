import math
def token(expression):
    tokens = []
    i = 0
    while i < len(expression):
        ch = expression[i]
        if ch == " ":
            i+=1
            continue
        if ch.isalpha():
            word = ""
            while i < len(expression) and expression[i].isalpha():
                word += expression[i]
                i += 1
            tokens.append(('FUNC', word))
            continue
        if "0" <= ch <="9" or ch == ".":
            strk = ""
            while (i < len(expression) and ( "0" <= expression[i] <= "9" or expression[i] == ".")):
                strk += expression[i]
                i += 1
            tokens.append(('NUMB' , (float(strk))))
            continue
        if ch in "+-*/()^":
            tokens.append(('OPER' , ch))
            i += 1
            continue
        raise ValueError('Введено не верно')
    return tokens
def xor(tokens, pos):
    left, pos = summation(tokens, pos)
    while pos < len(tokens) and tokens[pos][0] == 'OPER' and tokens[pos][1] == '^':
        pos+=1
        right, pos = summation(tokens, pos)
        left = int(left) ^ int(right)
    return left, pos
def staples(tokens , pos):
    if pos >= len(tokens):
        raise SyntaxError('Выражение не закончено')
    token = tokens[pos]
    if token[0] == 'NUMB':
        return token[1], pos + 1
    if token[0] == 'FUNC' and token[1] == 'ceil':
        pos+=1
        if pos < len(tokens) and tokens[pos][0] == 'OPER' and tokens[pos][1] == '(':
            pos += 1
            result, pos = xor(tokens, pos)
            if pos < len(tokens) and tokens[pos][0] == 'OPER' and tokens[pos][1] == ')':
                pos+=1
                return math.ceil(result), pos
            else:
                raise SyntaxError("Незакрытая скобка")
        else:
            raise SyntaxError("После ceil неоткрыта скобка")
        
    if token[0] == 'OPER' and token[1] == '(':
        pos += 1
        result, pos = xor(tokens, pos)
        if pos < len(tokens) and tokens[pos][0] == 'OPER' and tokens[pos][1] == ')':
            pos+=1
            return result, pos
        else:
            raise SyntaxError("Незакрыта скобка")
    raise SyntaxError("Незакрыта скобка")
def summation(tokens, pos):
    left, pos = multiplication(tokens, pos)
    while pos < len(tokens) and tokens[pos][0] == 'OPER' and (tokens[pos][1] == '+' or tokens[pos][1] == '-'):
        oper = tokens[pos][1]
        pos+=1
        right, pos = multiplication(tokens, pos)
        if oper =='+':
            left += right
        elif oper =='-':
            left -= right
    return left, pos

def multiplication(tokens, pos):
    left, pos = unary(tokens, pos)
    while pos < len(tokens) and tokens[pos][0] == 'OPER' and (tokens[pos][1] == '*' or tokens[pos][1] == '/'):
        oper = tokens[pos][1]
        pos += 1
        right, pos = unary(tokens, pos)
        if oper == '*':
            left *= right
        elif oper == '/':
            if right == 0:
                raise ZeroDivisionError('Деление на ноль')
            left /= right
    return left, pos

def unary(tokens, pos):
    if pos < len(tokens) and tokens[pos][0] == 'OPER' and (tokens[pos][1] == '+' or tokens[pos][1] == '-'):
        oper = tokens[pos][1]
        pos += 1
        number, pos = unary(tokens, pos)
        if oper == '+':
            return number, pos
        elif oper == '-':
            return -number, pos
    return staples(tokens, pos)

def calculate(expression):
    try:
        tokens = token(expression)
        result, pos = xor(tokens, 0)
        if pos < len(tokens):
            raise SyntaxError('Лишний символ')
        return result
    except Exception as e:
        return f"Ошибка:{e}"
    
    
expression = input("Ведите выражение, чтобы закончить ввод нажмите Enter")
result = calculate(expression)
print("результат:", result )
    
            
