#!/usr/bin/env python3
# read json in

import json
from aiohttp import web

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



async def handle_questions_answers(request):
    name = request.match_info.get('question_name', None)
    json = questionAnswers(name, e)
    return web.json_response(json)

async def handle_rank_answers(request):
    name = request.match_info.get('question_name', None)
    splitby = request.match_info.get('split_by', None)
    json = rankAnswers(name, e, splitby)
    return web.json_response(json)

async def handle_root(request):
    supported_methods = [ "/questions_answers/{question_name}", "/rank/{question_name}/{split_by}" ]
    return web.json_response(supported_methods)

app = web.Application()
app.add_routes([web.get('/', handle_root),
                web.get('/questions_answers/{question_name}', handle_questions_answers),
                web.get('/rank/{question_name}/{split_by}', handle_rank_answers)])

if __name__ == '__main__':
    web.run_app(app)


#print(rankAnswers('Tools', e, ' '))
    
    
