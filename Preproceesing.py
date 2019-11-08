import os, json
import csv
import pandas as pd
import nltk

# path_to_json = '/Users/weiding/Google Drive/Application Project/100_files'
path_to_json = '/Users/weiding/Desktop/vc/sum_all'
# read all json files from the folder
json_files = [pos_json for pos_json in os.listdir(path_to_json) if pos_json.endswith('.json')]
nltk.download('punkt')

# enumerate each file
count_empty_file = 0
company_tab_list = []
company_tab_content_list = []
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
            for key, value in json_text.items():
                count_total_tabs += 1
                if len(value) == 0:  # remove the empty tab content and tab
                    count_empty_tabs += 1
                elif "The Wayback Machine" in value:
                    continue
                else:
                    check_file_empty = False  # if a tab has useful information, this tab is not empty
                    count_valid_tabs += 1
                    key = key.split('_', 1)[-1]  # remove the date
                    key = key.split('.html', 1)[0]  # remove the .html
                    sub_tabs = key.split('_')
                    for sub_tab in sub_tabs:
                        if len(sub_tab) != 0:
                            company_tab_list.append([js, sub_tab])
                    sentenceList = nltk.sent_tokenize(value)  # split paragraph as sentences
                    for sentence in sentenceList:
                        company_tab_content_list.append([js, key, sentence])

print("Number of empty file: " + str(count_empty_file))
print("Number of total tabs:" + str(count_total_tabs))
print("Number of empty tabs:" + str(count_empty_tabs))
print("Number of valid tabs:" + str(count_valid_tabs))

with open('tabs.csv', 'w') as writeFile:
    writer = csv.writer(writeFile)
    for row in company_tab_list:
        writer.writerow(row)

writeFile.close()

# generate a dataframe: each row with 3 columns - company, tab and content. Each sentence of content as a single row.
company_tab_content_df = pd.DataFrame(company_tab_content_list)
company_tab_content_df.columns = ['company', 'tab', 'content']
company_tab_content_df.drop_duplicates(subset=['company', 'content'], inplace=True)  # remove duplicate sentences
company_tab_unique_content_df = company_tab_content_df.groupby(['company', 'tab'])['content'].\
    apply(lambda x: '.'.join(x)).reset_index()  # gather sentences together with same company and tab

# add industry category to the data
df_industry = pd.read_stata('/Users/weiding/Desktop/industry.dta')
company_tab_unique_content_df = company_tab_unique_content_df.rename(columns = {'company':'Web'})
df_sum_all_with_label = pd.merge(company_tab_unique_content_df, df_industry, on='Web', how='left')
df_sum_all_with_label = df_sum_all_with_label.dropna(subset=['IndustrySegment'])

df_sum_all_with_label.to_csv("company_tab_content_sum_all_with_label.csv", encoding='utf-8', index=False)
