import pandas as pd

# analyse the tabs and list the unique tabs with their occurences
df = pd.read_csv("tabs.csv")
df.columns = ['Company', 'Tab']
pivoted = pd.pivot_table(df, index=['Company','Tab'], aggfunc='size')
df_aggregation = pivoted.to_frame().reset_index()
df_aggregation.rename(columns={0: 'Occurrences'}, inplace=True)

tab_analyse = df_aggregation['Tab'].value_counts()
df_tab_analyse = tab_analyse.to_frame().reset_index()
df_tab_analyse.to_csv("tab_analyse.csv", sep='\t', encoding='utf-8')