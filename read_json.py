#!/usr/bin/env python3
# read json in

import json
from aiohttp import web
import argparse

        
def normalize(s):
    return s.strip().lower()

def splitNormalize(word, splitby=None):
    w = normalize(word)
    if splitby != None:
        return [normalize(x) for x in w.split(splitby)]
    else:
        return [w]     

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
                personDict[normalize(jq[q])] = j['responses'][q]
        
        e[id] = personDict    

def filter(questionName, filter_values, e, splitby=None):
    filtered = {}
    def answerMatches(resp, values):
        if resp is None:
            return False 
        else:
            return not set(splitNormalize(resp, splitby)).isdisjoint(filter_values)
                
    for x in e.values(): 
        if answerMatches(x.get(questionName, None), filter_values):
            filtered[x['id']] = x
    
    return filtered


def questionAnswers(questionname, personsdict):
    return [x[questionname] for x in personsdict.values() if questionname in x]
         
def rankAnswers(questionName, e, splitby=None):
    l = questionAnswers(questionName, e)
    countDict = {}
    for word in l:
        w = normalize(word)
        if splitby != None:
            tokens = [normalize(x) for x in w.split(splitby)]
        else:
            tokens = [w]
        
        for token in tokens:      
            countDict[token] = countDict.get(token, 0) + 1
        
    return countDict

def parseFilter(filters):
    a = [x.split(':') for x in filters]
    b = [(x[0], x[1].split(',')) for x in a ]
    return b

def indexAnswers(keyQuestionName, valueQuestionName, e, splitby=None):
    index = {}
    for person in e.values():
        word = person.get(keyQuestionName, None)
        if word:
            tokens = splitNormalize(word, splitby)        
            for token in tokens:
                if not token in index:
                    index[token] = []
                if valueQuestionName in person:
                    for value in splitNormalize(person[valueQuestionName]):
                        index[token].append(value)        
    return index    

async def handle_questions_answers(request):
    name = normalize(request.match_info.get('question_name', None))
    filters = request.query.getall('filter', [])
    filtered = e
    for filter_column, filter_values in parseFilter(filters):
        filtered = filter(filter_column, filter_values, filtered, splitby=',')
    json = questionAnswers(name, filtered)
    return web.json_response(json)

async def handle_answers(request):
    filters = request.query.getall('filter', [])
    filtered = e
    for filter_column, filter_values in parseFilter(filters):
        filtered = filter(filter_column, filter_values, filtered, splitby=',')
    return web.json_response(filtered)

async def handle_rank_answers(request):
    name = normalize(request.match_info.get('question_name', None))
    splitby = request.query.get('split_by')
    json = rankAnswers(name, e, splitby)
    return web.json_response(json)

async def handle_grouping(request):
    key = normalize(request.match_info.get('key_question_name', None))
    value = normalize(request.match_info.get('value_question_name', None))
    splitby = request.query.get('split_by')
    json = indexAnswers(key, value, e, splitby)
    return web.json_response(json)

async def handle_root(request):
    supported_methods = [ "/answers"
                          ,"/questions_answers/{question_name}"
                          , "/rank/{question_name}(?split_by=.)"
                          , "/grouping/{key_question_name}/{value_question_name}(?split_by=.)"
                          ]
    return web.json_response(supported_methods)

app = web.Application()
app.add_routes([web.get('/', handle_root),
                web.get('/answers', handle_answers),
                web.get('/questions_answers/{question_name}', handle_questions_answers),
                web.get('/rank/{question_name}', handle_rank_answers),
                web.get('/grouping/{key_question_name}/{value_question_name}', handle_grouping)])

parser = argparse.ArgumentParser(description='ccu hackathon api')
parser.add_argument('--port', type=int, default=8081, nargs='?')

if __name__ == '__main__':
    args = parser.parse_args()
    web.run_app(app, port=args.port)


#print(rankAnswers('Tools', e, ' '))
    
    
