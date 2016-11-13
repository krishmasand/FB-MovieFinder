#!/usr/bin/python 
from __future__ import print_function

from flask import Flask
from flask import request

import random
import json
import re
import requests
import rake
import operator

app = Flask(__name__)

CATEGORIES = {'Movie Bundles': 4815, 'Sci-Fi': 4747, 'Romantic Comedy': 4742, 'Drama': 3473, 'Fantasy': 4746, 'Animation': 4744, 'Adventure': 4743, 'Action': 3472, 'Comedy': 3474, 'Thriller': 4748, 'Childrens': 3639}

def extractTitleDescription(textDump, limit=5):
    if limit < 0:
        limit = 0
    parsed = json.loads(textDump)
    titleDescs = []
    if limit > len(parsed["Products"]):
        limit = len(parsed["Products"])
    randMovies = random.sample(parsed["Products"], limit)
    #randMovies = parsed["Products"][0:limit]

    if limit == 0:
        app.logger.warning("There were no suggestions")

    for movie in randMovies:
        titleDescs.append({"Title":movie["Name"], "Description": movie["ShortDescription"], "ID": movie["Id"], "Rating": movie["GuidanceRatings"][0]["Name"]})

    return titleDescs 

@app.route("/category", methods = ["POST"])
def category():

    retText = ""

    retCats = {}
    content = request.data
    if content == "":
        retText += "no content received"
    else:
        content = re.sub(r'https:\/\/facebook.com\/[A-Za-z]*', '', content)
        app.logger.info("Content: %s" % (content))
        rake_object = rake.Rake("SmartStoplist.txt", 3, 1, 1)

        keywords = rake_object.run(content)


        retMovies = []

        if keywords:
            keys = []
            for keyword in keywords:
                keys.append(keyword[0])
            keys = keys[:5]
            app.logger.info("Keys: %s" % (str(keys)))
          
            totalTitleDescs = []
            for key in keys:
                r = requests.post(
                        "https://services.sls1.cdops.net/Subscriber/SearchProducts", 
                        data=json.dumps({"SearchString":key, "Categories":[3338]}), 
                        headers={"CD-DistributionChannel":"20389393-b2e4-4f65-968e-75a5227e544c","CD-SystemId":"e5ce3167-4e0b-4867-a8c3-c8f23aec5e71"}
                        )
                titleDescs = extractTitleDescription(r.text, limit=2)
                totalTitleDescs += titleDescs
            retMovies = totalTitleDescs
            



        if not retMovies:
            app.logger.warning("No keywords")
        words = re.findall(r"[\w']+", content)
        newWords = []
        for word in words:
            newWords.append(word.lower())

        for cat in CATEGORIES:
            if cat.lower() in newWords: 
                if cat.lower() not in retCats:
                    retCats[cat] = 0
                retCats[cat] += 1

        catsLeft = len(retCats)
        for cat in retCats:
            retCats[cat] = {"id": CATEGORIES[cat], "count": retCats[cat]}
            r = requests.post(
                    "https://services.sls1.cdops.net/Subscriber/SearchProducts", 
                    data=json.dumps({"Categories":[retCats[cat]["id"]]}), 
                    headers={"CD-DistributionChannel":"20389393-b2e4-4f65-968e-75a5227e544c","CD-SystemId":"e5ce3167-4e0b-4867-a8c3-c8f23aec5e71"}
                    )
            moviesToExtract = min(5, (10 - len(retMovies))//catsLeft)
            catsLeft -= 1
            titleDescs = extractTitleDescription(r.text, limit=moviesToExtract)
            if len(retMovies) + len(titleDescs) <= 10:    
                retMovies = titleDescs + retMovies
    for (i, movie) in enumerate(retMovies):
        escapedTitle=movie["Title"].replace(" ", "+")
        r = requests.get("http://www.omdbapi.com/?t=%s&plot=short&r=json&tomatoes=true" % (escapedTitle))
        parsed = json.loads(r.text)
        if "Error" not in parsed:
            movie["Plot"] = parsed["Plot"]
            movie["Score"] = parsed["tomatoRating"]
        else:
            movie["Plot"] = movie["Description"]
            movie["Score"] = "?"
        r = requests.get("http://metadata.sls1.cdops.net/Product/SystemId/e5ce3167-4e0b-4867-a8c3-c8f23aec5e71/DistributionChannel/20389393-b2e4-4f65-968e-75a5227e544c/Id/%d" % (movie["ID"]))
        parsed = json.loads(r.text)
        if "RelatedMedia" in parsed["Product"] and parsed["Product"]["RelatedMedia"]:
            movie["TrailerUrl"] = parsed["Product"]["RelatedMedia"][0]["MediaUrl"]
        else:
            movie["TrailerUrl"] = ""
        if "AdditionalInformationURL" in parsed["Product"]:
            movie["Website"] = parsed["Product"]["AdditionalInformationURL"]
        else:
            movie["Website"] = ""
        
        retMovies[i] = movie



    if retMovies:
        app.logger.info(retMovies)  
        retText = "Movie suggestions based on your conversation:\n\n"
        for (i, movie) in enumerate(retMovies):
            if movie not in retMovies[0:i]:
                retText += "%d) %s, (%s/10, %s)\n" % (i+1, movie["Title"], movie["Score"], movie["Rating"])

                if movie["Website"]:
                    retText += "Website: %s\n" % (movie["Website"])
                retText += "%s\n\n" % (movie["Plot"])
    else:
        #Never remove the frowny face.  Is used on the front end
        retText = "There are no movie suggestions :("
    return retText


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int("8084"))

