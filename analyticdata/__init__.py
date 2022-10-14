import logging

import azure.functions as func
import json
import math


def main(req: func.HttpRequest) -> func.HttpResponse:
    req_body_bytes = req.get_body()
    req_body = req_body_bytes.decode("utf-8")
    
    name = json.loads(req_body)
    
    speaker1_text = []
    speaker2_text = []
    speaker1_duration = []
    speaker2_duration = []
    questions = []

    total_duration = name["durationInTicks"]
    combinedPhrases = name["combinedRecognizedPhrases"]
    combined_text = combinedPhrases[0]["display"]
    phrase_data = name["recognizedPhrases"]
    
    for p in phrase_data:
        if p["speaker"] == 1 :
            # for s in re.findall(r'-?\d+\.?\d*', p["duration"]):
            #     speaker1_duration.append(s)
            speaker1_duration.append(p["durationInTicks"])
            nBest = p["nBest"]
            for n in nBest:
                speaker1_text.append(n["display"])
        elif p["speaker"] == 2 :
            speaker2_duration.append(p["durationInTicks"])
            nBest = p["nBest"]
            for n in nBest:
                speaker2_text.append(n["display"])
 
    list_of_floats_1 = list(map(float, speaker1_duration))
    sp1_duration = math.fsum(list_of_floats_1) 
    list_of_floats_2= list(map(float, speaker2_duration))
    sp2_duration = math.fsum(list_of_floats_2) 
    combined_sp1_text = ''.join(speaker1_text)
    combined_sp2_text = ''.join(speaker2_text)
    
    for sq in speaker2_text:
        sq = sq.strip()
        if '?' in sq:
            quest = sq.split('?')
            questions.append(quest[0]+"?")
        
    speaker1_data = {"text":combined_sp1_text,"sentences":speaker1_text,"duration":sp1_duration}
    speaker2_data = {"text":combined_sp2_text,"sentences":speaker2_text,"duration":sp2_duration,"questions":questions}
    response_data = {"speaker1_data":speaker1_data,"speaker2_data":speaker2_data,"combined_text":combined_text,"total_duration":total_duration}
    
    return json.dumps(response_data)
