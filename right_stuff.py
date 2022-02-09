import os
from os.path import exists
import git

class FileNotFoundError(Exception):
    def __init__(self, value):
        self.message = value

    def __str__(self):
        return f'File {self.value} could not have been found'
    pass
class DuplicateSimbolError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return f'{self.value} is duplicate symbol'
    pass
class UnimplementedError(Exception):
    pass


projectRoot = os.getcwd()
templateFolderName = "templates"
importsFolderName = "imports"


########## NOVO DODANO
# This removes quote escapes from strings and removes starting and ending quote.
# Therefore this is used as a last string processing before passing it to commands
# or for simbol expanding.
def convertQuotedString(quotedString : str):

    if quotedString.startswith("\"") and quotedString.endswith("\"") :
        quotedString = quotedString[1:-1]

    regexMatchEscapedQuote = r"\\\""

    justString = re.sub(regexMatchEscapedQuote, "\"", quotedString)

    return justString


class XCodeGeneratorSymbol:

    def __init__(self, symbolName : str, symbolArgNames : list, symbolValue : str):
        self.name = symbolName
        self.argNames = symbolArgNames
        self.value = symbolValue


    def getName(self):

        return self.name


    def getArgNames(self):

        return self.argNames


    def getValue(self):

        return self.value


    def callSymbol(self, args : list) :

        if len(args) != len(self.argNames) :
            raise InvalidNumberOfSimbolArguments

        expandedSimbol = self.value

        for i in range(len(self.argNames)) :
            currArgName = self.argNames[i]
            currArgValue = args[i]

            regexMatchNonEscapedDollar = r"(?<!\$)\$"
            regexMatchSimbolName = regexMatchNonEscapedDollar + r"\{" + currArgName + r"\}"

            expandedSimbol = re.sub(regexMatchSimbolName, currArgValue, expandedSimbol)

        return expandedSimbol


class XCodeGeneratorSymbolTable:

    def __init__(self):
        self.symbolTable = {}


    def addSymbol(self, symbol : XCodeGeneratorSymbol):

        if symbol.getName() in self.symbolTable :
            raise SymbolAlreadyExists

        self.symbolTable[symbol.getName()] = symbol


    def getSymbol(self, symbolName):
        if symbolName in self.symbolTable:
            return self.symbolTable[symbolName]


    def newTableSymbols(self, table):
        for i in table.symbolTable:
            if i in self.symbolTable:
                raise DuplicateSimbolError

            else:
                self.symbolTable[i] = table.symbolTable[i]


    def expandSymbol(self, symbolExpansionStr : str):

        dissectedSymbolExp = self.dissectSymbolExp(symbolExpansionStr)

        symbolName = dissectedSymbolExp["symbolName"]
        symbolArgs = dissectedSymbolExp["symbolArgs"]

        for i in range(len(symbolArgs)) :

            arg = symbolArgs[i]

            if arg.startswith("\"") and arg.endswith("\"") :
                symbolArgs[i] = convertQuotedString(arg)
            else :
                symbolArgs[i] = self.expandSymbol(arg)

        if symbolName not in self.symbolTable :
            raise SimbolNotFound

        return self.symbolTable[symbolName].callSymbol(symbolArgs)


    def dissectSymbolExp(self, symbolExpansionStr : str):

        variableDisected = re.findall(r"(\w*)(?:\((.*)\))?", symbolExpansionStr)

        varName = ""
        args = []
        for i in range(1) :

            if len(variableDisected) == 0 :
                break

            variableDisected = variableDisected[0]

            varName = variableDisected[0]

            varArg = ""
            if len(variableDisected) == 1 :
                break

            varArg = variableDisected[1]

            regexMatchWords = r"(\w+)"
            regexMatchNonEscapedQuotes = r"(?<!\\)\""
            regexMatchNonGready = r".*?"

            regexMatchStrings = r"(" + \
                                regexMatchNonEscapedQuotes + \
                                regexMatchNonGready + \
                                regexMatchNonEscapedQuotes + \
                                r")"

            regexMatchVarArgument = regexMatchWords + r"|" + regexMatchStrings

            varArgDisected = re.findall(regexMatchVarArgument, varArg)

            for res in varArgDisected :
                if res[0] != "" :
                    args.append(res[0])
                elif res[1] != "" :
                    args.append(res[1])

        return {"symbolName": varName, "symbolArgs": args}


    def callSymbol(self, simbolName : str, argList : list):

        if simbolName not in self.symbolTable :
            raise SimbolNotFound

        if len(argList) != len(self.symbolTable[simbolName]["argNames"]) :
            raise InvalidNumberOfSimbolArguments

        expandedSimbol = self.symbolTable[simbolName]["value"]

        for i in range(len(self.symbolTable[simbolName]["argNames"])) :
            currArgName = self.symbolTable[simbolName]["argNames"][i]
            currArgValue = argList[i]

            regexMatchNonEscapedDollar = r"(?<!\$)\$"
            regexMatchSimbolName = regexMatchNonEscapedDollar + r"\{" + currArgName + r"\}"

            expandedSimbol = re.sub(regexMatchSimbolName, currArgValue, expandedSimbol)

        return expandedSimbol
    

    def getTableAsDict(self):

        retDict = {}
        for symbolName in self.symbolTable :

            sym = self.symbolTable[symbolName]

            #retDict[symbolName] = [sym.getArgNames(), sym.getValue()]
            retDict[symbolName] = {"argNames": sym.getArgNames(), "value": sym.getValue()}

        return retDict
############ NOVO DODANO



cmdExampleRemote = [
    {
        'token': 'import',
        'values': ['https://bitbucket.org/tomislav/example_template.git/my_template.templateobjects']
    }
]
cmdExampleLocal = [
    {
        'token': 'import',
        'values': ['/path/to/project/templates/my_template.templateobjects']
    }
]

############ PRILAGODJENO
mainSymbolTable = XCodeGeneratorSymbolTable()
mainSymbolTable.addSymbol(XCodeGeneratorSymbol("SIMBOL_1", [], "some(code)"))
mainSymbolTable.addSymbol(XCodeGeneratorSymbol("SIMBOL_2", [], "also_some_code"))


def parser(someFile):

    parserSymbolTable = XCodeGeneratorSymbolTable()
    parserSymbolTable.addSymbol(XCodeGeneratorSymbol("SIMBOL_3", [], "some(code)"))
    parserSymbolTable.addSymbol(XCodeGeneratorSymbol("SIMBOL_4", [], "also_some_code"))

    return parserSymbolTable


def parserDuplicateSimbolError(someFile):

    parserSymbolTable = XCodeGeneratorSymbolTable()
    parserSymbolTable.addSymbol(XCodeGeneratorSymbol("SIMBOL_2", [], "some(code)"))
    parserSymbolTable.addSymbol(XCodeGeneratorSymbol("SIMBOL_3", [], "also_some_code"))

    return parserSymbolTable

############ PRILAGODJENO




def indekzSearch(cmdTokens):
    indekz = len(cmdTokens[0]['values'][0]) - 1
    numOf = []
    k = 0
    for i in range(indekz, 0, -1):
        if cmdTokens[0]['values'][0][i] == '/':
            if len(numOf) == 0:
                numOf.append(cmdTokens[0]['values'][0][i+1:])
                k = i
            elif len(numOf) == 1:
                numOf.append(cmdTokens[0]['values'][0][i+1:k])
                numOf.append(cmdTokens[0]['values'][0][:k])
                break
    return numOf

def importCmdHandler(cmdTokens):
    if cmdTokens[0]['values'][:5] == 'https':
        FileandRepo = indekzSearch(cmdTokens)
        filez = FileandRepo[0]
        repoz = FileandRepo[1]
        repoName = FileandRepo[2]   
        
        repoPath = projectRoot + '/' + templateFolderName + '/' + importsFolderName + '/' + repoz

        git.Repo.clone_from(repoName, repoPath)

        if exists(repoPath + '/' + filez):
            iAmParsed = parser(repoPath + '/' + filez)
            mainSymbolTable.newTableSymbols(iAmParsed)
        else:
            FileNotFoundError(cmdTokens)


    else:
        if exists(cmdTokens[0]['values'][0]):
            iAmParsed = parser(cmdTokens[0]['values'][0])
            mainSymbolTable.newTableSymbols(iAmParsed)
        else:
            FileNotFoundError(cmdTokens)
    
    return mainSymbolTable
    # Implement me :)
    #raise UnimplementedError
    print(parserDuplicateSimbolError("/"))


def main():

    importCmdHandler(cmdExampleRemote)
    #importCmdHandler(cmdExampleLocal)


if __name__ == "__main__" :

    main()
