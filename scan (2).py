patterns = {
    ":=": "Assign",
    "+": "Plus",
    "-": "Minus",
    "*": "Times",
    "/": "DIV",
    "(": "LParen",
    ")": "RParen",
}

def find(file, deter):
    result = []
    if deter == "String":
        file = file.split('\n')
    in_comment = False
    comment_lines = []

    for line in file:
        line = line.strip()
        if line.startswith("//"):
            result.append(["Comment", line])
        elif line.startswith("/*"):
            in_comment = True
            comment_lines.append(line)
        elif line.endswith("*/"):
            in_comment = False
            comment_lines.append(line)
            result.append(["Comment", '\n'.join(comment_lines)])
            comment_lines = []
        elif in_comment:
            comment_lines.append(line)
        else:
            tokens = []
            i = 0

            while i < len(line):
                token = ""
                if line[i:i+2] in patterns and line[i] != line[-1]:
                    tokens.append([patterns[line[i:i+2]], line[i:i+2]])
                    i += 2
                elif line[i] in patterns:
                    tokens.append([patterns[line[i]], line[i]])
                    i += 1
                elif line[i].isdigit():
                    while i < len(line) and (line[i].isalnum() or line[i] == '.'):
                        token += line[i]
                        i += 1
                    if '.' in token and token.count('.') == 1:
                        if token[-1] == ".":
                            tokens.append(["Invalid token", token])
                        else:
                            tokens.append(["Digit", token])
                    elif token.isdigit():
                        tokens.append(["Digit", token])
                    elif token[0].isdigit() and any(c.isalpha() for c in token[1:]):
                        tokens.append(["Invalid token", token])
                elif line[i].isalpha():
                    while i < len(line) and line[i].isalnum():
                        token += line[i]
                        i += 1
                    if token[0].isdigit():
                        tokens.append(["Invalid token", token])
                    if token.isalpha():
                        tokens.append(["ID", token])
                    elif token.isalnum():
                        tokens.append(["ID", token])
                else:
                    if line[i] != ' ':
                        tokens.append(["Invalid token", line[i]])
                    i += 1

            result.extend(tokens)
    return result

file = """
/* 
Assigning celcius
as 100 degree
*/
Celcius := 100.00

// Formula to find fahrenheit
Fahrenheit := (9/5) * Celcius + 32
"""

files = open("Calculator.py", "r")

result = find(file, "String")
results = find(files, "")

invalid_token_found = False
for item in results:
    if item[0] == "Invalid token":
        print("Invalid token found :", item[1])
        invalid_token_found = True

if not invalid_token_found:
    for item in results:
        print(item[0], ":", item[1])