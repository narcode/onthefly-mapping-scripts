# read json in

import json

# load the files
answers = '/Users/narcodeb/Downloads/artists.json'
questions = '/Users/narcodeb/Downloads/questions_short.json'
jq = json.load(open(questions))
ja = json.load(open(answers))

# test loading
# print(jq)

# fuse them in a Dict
e = {}

for j in ja:
    personDict = {}
    id = j['id']
    personDict['id'] = id
    
    if j['branch'] == 'Practitioners and Artists':
        
        if len(j['responses']) > 0:
            
            for q in j['responses']: 
                personDict[jq[q]] = j['responses'][q]
        
        e[id] = personDict
    

def questionAnswers(questionname, personsdict):
    return [x[questionname] for x in personsdict.values() if questionname in x]
     
    
def rankAnswers(questionName, e, splitby=None):
    l = questionAnswers(questionName, e)
    countDict = {}
    for word in l:
        w = word.lower().strip()
        if splitby != None:
            tokens = [x.strip() for x in w.split(splitby)]
        else:
            tokens = [w]
        
        for token in tokens:      
            countDict[token] = countDict.get(token, 0) + 1
        
    return countDict


print(rankAnswers('Tools', e, ' '))
    
    
