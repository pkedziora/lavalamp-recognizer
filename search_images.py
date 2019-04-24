import requests
import os
import json
import urllib.parse
from PIL import Image, ImageFilter
from time import gmtime, strftime

term = "lava+lamp"
includeRelatedTerms = False
outputPath = "data/temp"
resultsLimit = 1000

API_URL = "https://api.cognitive.microsoft.com/bing/v7.0/images/search"
API_KEY_PATH = "api_keys/bing_search.txt"
IMAGE_TIMEOUT = 10
PAGE_SIZE = 200
STATE_FILE = "state.json"

def bingApiKey():
    keyFile = open(API_KEY_PATH, "r")
    return keyFile.read()

apiKey = bingApiKey()

def timestamp():
    return strftime("%H:%M:%S", gmtime())

def is_image_broken(filePath):
    try:
        image = Image.open(filePath)
        return False
    except Exception as ex:
        return True


def is_supported_extension(fileExtension):
    extensionWhitelist = ['.jpg', '.jpeg'];
    return fileExtension.lower() in extensionWhitelist


def get_search_results(query, offset, count):
    params = {"q": query, "count": count, "offset": offset}
    headers = {"Ocp-Apim-Subscription-Key" : apiKey}
    search = requests.get(API_URL, headers=headers, params=params)
    bingResults = search.json()
    print(f"{timestamp()} Called Bing api with term: {query} offset: {offset}, returned {len(bingResults['value'])} results");
    print(f"{timestamp()} Estimated matches: {bingResults['totalEstimatedMatches']}")
    return bingResults


def get_image(url, fileName):
        print(f"{timestamp()} Downloading: {url}")
        imageReq = requests.get(url, timeout=IMAGE_TIMEOUT)
        extension = url[url.rfind("."):]
        if not is_supported_extension(extension):
            print(f"{timestamp()} ERROR Image not in extension whitelist, skipped {url} ")
            return False
        filePath = os.path.sep.join([outputPath, f"{fileName}{extension}"])
        imageFile = open(filePath, "wb")
        imageFile.write(imageReq.content)
        imageFile.close()
        if  is_image_broken(filePath):
            print(f"{timestamp()} ERROR Broken image: {filePath}, deleting")
            os.remove(filePath)
            return False
            
        return True


def save_state(filePath, nextFileNumber, setOfLinks):
    f = open(filePath, "w+")
    listOfLinks = list(setOfLinks)
    state = {"nextFileNumber": nextFileNumber, "listOfLinks": listOfLinks}
    stateJson = json.dumps(state)
    f.write(stateJson)
    print(f'{timestamp()} State saved, nextFileNumber: {state["nextFileNumber"]}, listOfLinks count: {len(state["listOfLinks"])}')


def load_state(filePath):
    f = open(filePath, "a+")
    f.seek(0)
    stateJson = f.read()
    if stateJson == '':
        return 0, set()
    state = json.loads(stateJson)
    print(f'{timestamp()} State loaded, nextFileNumber: {state["nextFileNumber"]}, listOfLinks count: {len(state["listOfLinks"])}')
    return state["nextFileNumber"], set(state["listOfLinks"])


def download_images(currentTerm, resultsLimit):
    currentOffset = 0
    currentCount = 0
    currentFileNumber, visitedUrls = load_state(STATE_FILE)
    while (currentOffset + currentCount) < resultsLimit:
        bingResults = get_search_results(currentTerm, currentOffset, PAGE_SIZE)
        resultsLimit = bingResults["totalEstimatedMatches"] if resultsLimit > bingResults["totalEstimatedMatches"] else resultsLimit;
        
        for bingResult in bingResults["value"]:
            imageUrl = bingResult["contentUrl"]
            if imageUrl in visitedUrls:
                print(f"WARNING Image already downloaded {imageUrl}")
                continue

            try:
                if get_image(imageUrl, currentFileNumber):
                    currentCount += 1
                    currentFileNumber += 1
            except Exception as ex:
                print(f"{timestamp()} ERROR Failed to download {imageUrl}")
            visitedUrls.add(imageUrl)
        currentOffset = bingResults["nextOffset"]
        currentCount = 0
        save_state(STATE_FILE,currentFileNumber, visitedUrls)


def get_related_search_terms(term):
    bingResults = get_search_results(term, 0, 0)
    return list(map(lambda q: urllib.parse.quote_plus(q["text"]).lower(), bingResults["queryExpansions"]))


download_images(term, resultsLimit)

if includeRelatedTerms:
    relatedTerms = get_related_search_terms(term)
    for relatedTerm in relatedTerms:
        download_images(relatedTerm, resultsLimit)
