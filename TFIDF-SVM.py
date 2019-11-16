import pandas as pd
import numpy as np
from sklearn import svm
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
import seaborn as sn
import matplotlib.pyplot as plt

# load data, merge with the upper category
df_sum_all = pd.read_csv(
    "/Users/weiding/projects/application_project_nlp_company_description/company_tab_content_sum_all_with_label.csv")
df_upper_category = pd.read_excel('/Users/weiding/Desktop/LargeCategory.xlsx', header=None)
df_upper_category.columns = ['IndustrySegment', 'Category']
df_category_analysis = pd.merge(df_sum_all, df_upper_category, on='IndustrySegment', how='left')
df_category_analysis = df_category_analysis.dropna(subset=['Category'])

# select same number of labels, each 1113, small categories combined to one
df_category_analysis_combined = df_category_analysis.groupby(['Web', 'Category'])['content'].apply(
    ','.join).reset_index()
df_healthcare_group = df_category_analysis_combined[df_category_analysis_combined['Category'] == 'HEALTHCARE GROUP']
df_business_financial_services = df_category_analysis_combined[
    df_category_analysis_combined['Category'] == 'BUSINESS & FINANCIAL SERVICES'].sample(n=1113, replace=False)
df_consumer_service_group = df_category_analysis_combined[
    df_category_analysis_combined['Category'] == 'CONSUMER SERVICES GROUP'].sample(n=1113, replace=False)
df_information_technology_group = df_category_analysis_combined[
    df_category_analysis_combined['Category'] == 'INFORMATION TECHNOLOGY GROUP'].sample(n=1113, replace=False)
df_rest = df_category_analysis_combined[(df_category_analysis_combined['Category'] == 'CONSUMER GOODS GROUP') |
                                        (df_category_analysis_combined['Category'] == 'ENERGY & UTILITIES GROUP') |
                                        (df_category_analysis_combined[
                                             'Category'] == 'INDUSTRIAL GOODS & MATERIALS GROUP')].sample(n=1113,
                                                                                                          replace=False)
df_rest = df_rest.replace(np.array(df_rest['Category']), 'Others')
df_clean = pd.concat(
    [df_healthcare_group, df_business_financial_services, df_consumer_service_group, df_information_technology_group,
     df_rest])

data = df_clean.sample(frac=1)

# generate TF-IDF
feature_extraction = TfidfVectorizer()
X = feature_extraction.fit_transform(data['content'].values)

num_training = 4452
X_train = X[:num_training]
X_test = X[num_training:]
y_train = data['Category'].values[:num_training]
y_test = data['Category'].values[num_training:]

# SVM Classifier
classifier_svm = svm.LinearSVC(verbose=1)
# classifier_svm = svm.SVC(kernel='linear')
classifier_svm.fit(X_train, y_train)
predictions = classifier_svm.predict(X_test)

print(confusion_matrix(y_test, predictions))
print(classification_report(y_test, predictions))
print(accuracy_score(y_test, predictions))

# Plot the confusion matrix
array = confusion_matrix(y_test, predictions)
y_true = ["BUSINESS & FINANCIAL SERVICES", "CONSUMER SERVICES GROUP", "HEALTHCARE GROUP",
          "INFORMATION TECHNOLOGY GROUP", "OTHERS"]
y_pred = ["BUSINESS & FINANCIAL SERVICES", "CONSUMER SERVICES GROUP", "HEALTHCARE GROUP",
          "INFORMATION TECHNOLOGY GROUP", "OTHERS"]
df_cm = pd.DataFrame(array, y_true, y_pred)
df_cm.index.name = 'Actual'
df_cm.columns.name = 'Predicted'
plt.figure(figsize=(10, 7))
# sn.set(font_scale=1.4)#for label size
ax = sn.heatmap(df_cm, cmap="Blues", annot=True, fmt='d', annot_kws={"size": 16})  # font size
bottom, top = ax.get_ylim()
ax.set_ylim(bottom + 0.5, top - 0.5)
ax.tick_params(labelsize=10)
ax.set_xticklabels(y_pred, rotation=45)
plt.show()
