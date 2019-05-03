import requests
import os
import json
import urllib.parse
from PIL import Image
from time import gmtime, strftime
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("term", help="Image search term")
parser.add_argument("count", help="Maximum number of results to return")
parser.add_argument("-r", "--includeRelated", choices=[0, 1], type=int, help="Include related terms")
args = parser.parse_args()

term = urllib.parse.quote_plus(args.term)
includeRelatedTerms = bool(args.includeRelated)
outputPath = "download"
resultsLimit = int(args.count)

API_URL = "https://api.cognitive.microsoft.com/bing/v7.0/images/search"
API_KEY_PATH = "api_keys/bing_search.txt"
IMAGE_TIMEOUT = 10
PAGE_SIZE = 200
STATE_FILE = "state.json"


def bing_api_key():
    key_file = open(API_KEY_PATH, "r")
    return key_file.read()


apiKey = bing_api_key()


def timestamp():
    return strftime("%H:%M:%S", gmtime())


def is_image_broken(file_path):
    try:
        image = Image.open(file_path)
        return False
    except Exception as ex:
        return True


def is_supported_extension(file_extension):
    extension_whitelist = ['.jpg', '.jpeg']
    return file_extension.lower() in extension_whitelist


def get_search_results(query, offset, count):
    params = {"q": query, "count": count, "offset": offset}
    headers = {"Ocp-Apim-Subscription-Key": apiKey}
    search = requests.get(API_URL, headers=headers, params=params)
    bing_results = search.json()
    print(f"{timestamp()} Called Bing api with term: {query} offset: {offset}, returned {len(bing_results['value'])} results")
    print(f"{timestamp()} Estimated matches: {bing_results['totalEstimatedMatches']}")
    return bing_results


def get_image(url, file_name):
    print(f"{timestamp()} Downloading: {url}")
    image_req = requests.get(url, timeout=IMAGE_TIMEOUT)
    extension = url[url.rfind("."):]
    if not is_supported_extension(extension):
        print(f"{timestamp()} ERROR Image not in extension whitelist, skipped {url} ")
        return False
    file_path = os.path.sep.join([outputPath, f"{file_name}{extension}"])
    image_file = open(file_path, "wb")
    image_file.write(image_req.content)
    image_file.close()
    if is_image_broken(file_path):
        print(f"{timestamp()} ERROR Broken image: {file_path}, deleting")
        os.remove(file_path)
        return False

    return True


def save_state(file_path, next_file_number, set_of_links):
    f = open(file_path, "w+")
    list_of_links = list(set_of_links)
    state = {"nextFileNumber": next_file_number, "listOfLinks": list_of_links}
    state_json = json.dumps(state)
    f.write(state_json)
    print(f'{timestamp()} State saved, nextFileNumber: {state["nextFileNumber"]}, listOfLinks count: {len(state["listOfLinks"])}')


def load_state(file_path):
    f = open(file_path, "a+")
    f.seek(0)
    state_json = f.read()
    if state_json == '':
        return 0, set()
    state = json.loads(state_json)
    print(f'{timestamp()} State loaded, nextFileNumber: {state["nextFileNumber"]}, listOfLinks count: {len(state["listOfLinks"])}')
    return state["nextFileNumber"], set(state["listOfLinks"])


def download_images(current_term, results_limit):
    current_offset = 0
    current_count = 0
    current_file_number, visited_urls = load_state(STATE_FILE)
    while (current_offset + current_count) < results_limit:
        bing_results = get_search_results(current_term, current_offset, PAGE_SIZE)
        results_limit = bing_results["totalEstimatedMatches"] if results_limit > bing_results["totalEstimatedMatches"] else results_limit

        for bingResult in bing_results["value"]:
            image_url = bingResult["contentUrl"]
            if image_url in visited_urls:
                print(f"WARNING Image already downloaded {image_url}")
                continue

            try:
                if get_image(image_url, current_file_number):
                    current_count += 1
                    current_file_number += 1
            except Exception as ex:
                print(f"{timestamp()} ERROR Failed to download {image_url}")
            visited_urls.add(image_url)
        current_offset = bing_results["nextOffset"]
        current_count = 0
        save_state(STATE_FILE, current_file_number, visited_urls)


def get_related_search_terms(search_term):
    bing_results = get_search_results(search_term, 0, 0)
    return list(map(lambda q: urllib.parse.quote_plus(q["text"]).lower(), bing_results["queryExpansions"]))


download_images(term, resultsLimit)

if includeRelatedTerms:
    relatedTerms = get_related_search_terms(term)
    for relatedTerm in relatedTerms:
        download_images(relatedTerm, resultsLimit)
