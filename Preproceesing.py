import os, json
import csv
import pandas as pd

# path_to_json = '/Users/weiding/Google Drive/Application Project/100_files'
path_to_json = '/Users/weiding/Desktop/vc/sum_all'
# read all json files from the folder
json_files = [pos_json for pos_json in os.listdir(path_to_json) if pos_json.endswith('.json')]

# enumerate each file
count_empty_file = 0
company_tab_list = []
count_total_tabs = 0
count_empty_tabs = 0
count_valid_tabs = 0
check_file_empty = False
for index, js in enumerate(json_files):
    with open(os.path.join(path_to_json, js)) as json_file:
        json_text = json.load(json_file)
        if len(json_text) == 0:  # find and ignore empty files
            count_empty_file += 1
        else:
            js = js.split('_20', 1)[0]  # only keep the website name or company name

            # processing the tab

            if check_file_empty:
                count_empty_file += 1
            check_file_empty = True
            for key in json_text.keys():
                count_total_tabs += 1
                if len(json_text[key]) == 0:  # remove the empty tab content and tab
                    count_empty_tabs += 1
                elif "The Wayback Machine" in json_text[key]:
                    continue
                else:
                    check_file_empty = False  # if a tab has useful information, this tab is not empty
                    count_valid_tabs += 1
                    key = key.split('_', 1)[-1]  # remove the date
                    key = key.split('.html', 1)[0]  # remove the .html
                    values = key.split('_')
                    for value in values:
                        if len(value) != 0:
                            company_tab_list.append([js, value])

print("Number of empty file: " + str(count_empty_file))
print("Number of total tabs:" + str(count_total_tabs))
print("Number of empty tabs:" + str(count_empty_tabs))
print("Number of valid tabs:" + str(count_valid_tabs))

with open('tabs.csv', 'w') as writeFile:
    writer = csv.writer(writeFile)
    for row in company_tab_list:
        writer.writerow(row)

writeFile.close()

# analyse the tabs and list the unique tabs with their occurences
df = pd.read_csv("tabs.csv")
df.columns = ['Company', 'Tab']
pivoted = pd.pivot_table(df, index=['Company','Tab'], aggfunc='size')
df_aggregation = pivoted.to_frame().reset_index()
df_aggregation.rename(columns={0: 'Occurrences'}, inplace=True)

tab_analyse = df_aggregation['Tab'].value_counts()
df_tab_analyse = tab_analyse.to_frame().reset_index()
df_tab_analyse.to_csv("tab_analyse.csv", sep='\t', encoding='utf-8')