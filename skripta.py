from git import Repo
import os

projectRoot = os.getcwd()
cmdExampleRemote = [
    {
        'token': 'import',
        'values': ['https://github.com/TommyTheGreat/firstOne/hi_guys.py']
    }
]


def indekzSearch(cmdTokens):
    indekz = len(cmdTokens[0]['values'][0]) - 1
    numOf = []
    k = 0
    for i in range(indekz, 0, -1):
        if cmdTokens[0]['values'][0][i] == '/':
            if len(numOf) == 0:
                numOf.append(cmdTokens[0]['values'][0][i + 1:])
                k = i
            elif len(numOf) == 1:
                numOf.append(cmdTokens[0]['values'][0][i + 1:k])
                numOf.append(cmdTokens[0]['values'][0][:k])
                return numOf



def importCmdHandler(cmdTokens):
    if cmdTokens[0]['values'][0][:5] == 'https':
        FileandRepo = indekzSearch(cmdTokens)
        filez = FileandRepo[0]
        repoz = FileandRepo[1]
        repoName = FileandRepo[2]
        print(FileandRepo)
        Repo.clone_from(repoName, (projectRoot + '/templates/imports/' + repoz ))

        
        if os.path.exists(projectRoot + '/templates/imports/' + repoz + '/' + filez):
            print('Here I am')


importCmdHandler(cmdExampleRemote)
