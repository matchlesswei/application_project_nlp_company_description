import pandas as pd

df_sum_all = pd.read_csv("company_tab_content_sum_all_with_label.csv")
df_clean = df_sum_all.drop_duplicates('Web')['Web']

df_industry = pd.read_stata('/Users/weiding/Desktop/industry.dta')

df_sum_all_with_label = pd.merge(df_clean, df_industry, on='Web', how='left')

industry_analysis = df_sum_all_with_label['IndustrySegment'].value_counts()
df_industry_analysis = industry_analysis.to_frame().reset_index()
df_multiple_industry = df_industry_analysis[df_industry_analysis['index'].str.contains(',')]
df_single_industry = df_industry_analysis[~df_industry_analysis['index'].str.contains(',')]
number_of_companies = sum(df_industry_analysis['IndustrySegment'])
number_of_unique_industry_companies = sum(df_single_industry['IndustrySegment'])

print('number of total companies:' + str(number_of_companies))
print('number of companies with unique industry category:' + str(number_of_unique_industry_companies))
print(df_single_industry)

df_large_category = pd.read_excel('/Users/weiding/Desktop/LargeCategory.xlsx', header=None)
df_large_category.columns = ['index', 'category']
df_categroy_analysis = pd.merge(df_single_industry, df_large_category, on='index', how='left')
print("Industry big category and number of companies:")
print(df_categroy_analysis.groupby(['category']).sum())