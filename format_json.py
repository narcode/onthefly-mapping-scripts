import json
import pycountry
import re
import sys

import utils

def transform_country(country):
    normalized = utils.normalize(country)
    normalized = re.sub('the ', '', normalized)
    try:
        return pycountry.countries.lookup(normalized).alpha_2.lower()
    except LookupError:
        sys.stderr.write("Unexpected country " + normalized + "\n")
        return normalized

def transform_residence(residence):
    return transform_country(residence)

def transform_tools(tools_string):
    split = utils.splitNormalize(tools_string, ',')
    return split

answer_transformers = {
    'country': transform_country,
    'residence': transform_residence,
    'tools': transform_tools,
}

def transform_answer(answer, question):
    return answer_transformers.get(question, lambda x: x)(answer)


answers = 'artists.json'
questions = 'questions_short.json'
institution_questions = 'questions_institutions_short.json'
jiq = json.load(open(institution_questions))
jq = json.load(open(questions))
ja = json.load(open(answers))

e = {}

for j in ja:
    if len(j['responses']) == 0:
        continue
    respDict = {}
    id = j['id']
    respDict['id'] = id
    branch = j['branch']
    if branch == 'Practitioners and Artists':
        respDict['category'] = 'artist'
        question_names = jq
    elif branch == 'Institutions':
        respDict['category'] = 'institution'
        question_names = jiq
    else:
        continue
    for q in j['responses']:
        question_name = utils.normalize(question_names[q])
        answer = transform_answer(j['responses'][q], question_name)
        respDict[question_name] = answer
    e[id] = respDict

print(json.dumps(e))
