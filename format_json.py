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
jq = json.load(open(questions))
ja = json.load(open(answers))

e = {}

for j in ja:
    personDict = {}
    id = j['id']
    personDict['id'] = id

    if j['branch'] == 'Practitioners and Artists':

        if len(j['responses']) > 0:

            for q in j['responses']:
                question_name = utils.normalize(jq[q])
                answer = transform_answer(j['responses'][q], question_name)
                personDict[question_name] = answer

        e[id] = personDict

print(json.dumps(e))
