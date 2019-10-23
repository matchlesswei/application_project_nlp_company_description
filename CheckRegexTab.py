import os, json
import re

path_to_json = '/Users/weiding/Desktop/vc/sum'
# read all json files from the folder
json_files = [pos_json for pos_json in os.listdir(path_to_json) if pos_json.endswith('.json')]

# enumerate each file
count_empty_file = 0
company_tab_list = []
count_not_regex_tabs = 0
count_wayback_machine = 0
check_file_empty = False
for index, js in enumerate(json_files):
    with open(os.path.join(path_to_json, js)) as json_file:
        json_text = json.load(json_file)
        if not len(json_text) == 0:
            if check_file_empty:
                count_empty_file += 1
            check_file_empty = True
            for key in json_text.keys():
                if (re.match("^[0-9]{8}\_.*\.(html|htm|php|org|asp|aspx)$", key)):
                    count_not_regex_tabs += 1
                    if (len(json_text[key]) != 0) :
                        if ("The Wayback Machine" in json_text[key]):
                            count_wayback_machine += 1


print("tabs not regex: " + str(count_not_regex_tabs))
print("wayback_machine: " + str(count_wayback_machine))

