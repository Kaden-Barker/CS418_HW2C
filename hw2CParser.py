import argparse

def main():

    parse = argparse.ArgumentParser(description="parse string")
    parse.add_argument("grammerFile", help="grammer for the doty simulator")
    parse.add_argument("stringFile", help="string that should fit the grammer")    
    args = parse.parse_args()


    with open(args.grammerFile, encoding="utf-8") as f:
        grammerData = f.read()      


    with open(args.stringFile, encoding="utf-8") as f:
        stringData = f.read()

    # Removing white space
    grammerData = grammerData.replace(" ", "")
    stringData = stringData.replace(" ", "")

    # Creating a variable to rules dict
    grammerDict = {}
    grammerData = grammerData.split("\n")
    for line in grammerData:
        varSplit = line.split(";")
        # putting symbol to rule in dict
        for i in range(len(varSplit)-1):
            symbol = varSplit[i].split("->")
            var = symbol[0]
            rules = symbol[1].split("|")
                
            
            grammerDict[var] = rules
 
    # check if the string is in the grammer
    check = checkString(stringData, grammerDict)
    print(check)
    

def checkString(string, grammer):
    '''Checks if a string is in a grammer. 
        returns a 0 if it is in the grammer and 
        returns a 1 if it is not in the grammer'''

    stringLength = len(string)

    # Beginning of the parse

    variables = grammer.keys()
    if string ==  '':
        start = list(grammer.keys())[0]

        # check if epsilon in one of the rules
        for i in range(len(grammer[start])):
            rule = grammer[start][i]
            if rule == '':
                return 0
        # after going through the rules if we don't return then return 1
        return 1
    

    # Creating table
    table = []
    x = 0
    y = 0
    while x < stringLength:
        xList = []
        y = 0
        while y < stringLength:
            xList.append([])
            y+=1
        table.append(xList)
        x+=1

    # looking at each substring of length 1
    index = 0
    while index <= stringLength-1:
        subString = string[index]
        for var in variables:
            currentVarRules = grammer[var]
            for rule in currentVarRules:
                if rule == subString:
                    table[index][index].append(var)
        
        index+=1


    # looking at strings for rules with a path to another rule
    for subStringLength in range(1,stringLength): 
        for subStringStart in range(stringLength - subStringLength + 1): 
            subStringEnd = subStringStart + subStringLength
            for splitPosition in range(subStringStart, subStringEnd):

                # looking at all variables
                for var in variables:
                    for rule in grammer[var]:
                        # checks if the variable has a rule that has a path to another rule
                        if (len(rule) > 1):
                            # checks if each path is an accepted rule
                            if (rule[0] in table[subStringStart][splitPosition]) and (rule[1] in table[splitPosition+1][subStringEnd-1]):
                                table[subStringStart][subStringEnd-1].append(var)
                                   


    start = list(grammer.keys())[0]
    if start in table[1][stringLength-1]:
        return 0
        
    else: 
        return 1


main()