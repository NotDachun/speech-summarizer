import json
import urllib.request, urllib.error, urllib.parse
from background_listen import SpeechToText

APPLICATION_ID = 'beb572e2'
APPLICATION_KEY = '764be5de1aeb9b450180db631545135e'

#function that calls api
def call_api(endpoint, parameters):
  url = 'https://api.aylien.com/api/v1/' + endpoint
  headers = {
      "Accept":                             "application/json",
      "Content-type":                       "application/x-www-form-urlencoded",
      "X-AYLIEN-TextAPI-Application-ID":    APPLICATION_ID,
      "X-AYLIEN-TextAPI-Application-Key":   APPLICATION_KEY
  }
  opener = urllib.request.build_opener()
  request = urllib.request.Request(url,
    urllib.parse.urlencode(parameters).encode('utf-8'), headers)
  response = opener.open(request)
  return json.loads(response.read().decode())

#api wrapper function that summarizes the inputted text
def summarize_string(title):
  speech = SpeechToText()
  speech.run()
  sentence_count = speech.text.count('.')
  parameters = {"text": speech.text, "sentences_number": sentence_count//10, "title": title, "language": "en"}
  return call_api("summarize", parameters)

def summarize_text(filename, title):
  file = open(filename, 'r')
  text = file.read()
  text = text.replace('\n', ' ')
  text = text.replace('\t', ' ')
  file.close()
  sentence_count = text.count('.')
  print("Original sentence count: " + str(sentence_count))
  parameters = {"text": text, "sentences_number": 10, "title": title, "language": "en"}
  return call_api("summarize", parameters)

test = "Hello my name is Jeremy. I am 19 years old. I like to play soccer. I go to Harvey Mudd College in California. Currently I am at home in Bellevue, Washington. Test over. Lol this is just filler. Can you accurately summarize this. I wonder. This is a test. I am sitting next to Daniel Zhu. Daniel Zhu goes to the University of Washington."

