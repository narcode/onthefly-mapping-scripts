# read json in

import json

# load the files
answers = '/Users/narcodeb/Downloads/artists.json'
questions = '/Users/narcodeb/Downloads/questions_short.json'
jq = json.load(open(questions))
ja = json.load(open(answers))

# test loading
# print(jq)

# fuse them in an array
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
    
    




