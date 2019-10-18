import os, json
import csv

# path_to_json = '/Users/weiding/Google Drive/Application Project/100_files'
path_to_json = 'C:/Users/kwokp/OneDrive/Desktop/Study/zzz_application project/vc/test'
json_files = [pos_json for pos_json in os.listdir(path_to_json) if pos_json.endswith('.json')]

count = 0
for index, js in enumerate(json_files):
    with open(os.path.join(path_to_json, js)) as json_file:
        json_text = json.load(json_file)
        #print(js)
        #print(json_text.keys())
        for key in json_text.keys():
            print(key)
        if len(json_text) == 0:
            count += 1

print(count)