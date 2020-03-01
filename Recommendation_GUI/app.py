#Import Relevant Libraries
from flask import Flask, flash, redirect, request, jsonify, render_template, url_for
import numpy as np
import scipy.sparse
from sklearn.metrics.pairwise import cosine_similarity

X_vector = scipy.sparse.load_npz('X_word2vec.npz')
y_vector = np.load('y_word2vec.npy', allow_pickle=True)
Website = np.load('Website_word2vec.npy', allow_pickle=True)


app = Flask(__name__)
app.secret_key = 'secret key'

# home route
@app.route('/')
def home():
    return render_template('recommendation.html')

# recommend route which are used in the recommendation function to recommend 5 music files
@app.route('/recommendation',methods=['GET', 'POST'])
def recommendation():

    #number of companies
    top_k = int(request.values.get("select_number"))
    Input_Company = request.values.get("Input company website")
    #Word2vec Similarity
    Input=X_vector[np.where(Website==Input_Company)[0][0]]
    Similarity = np.zeros((X_vector.shape)[0])
    for index, vector in enumerate(X_vector):
        Similarity[index]=np.round(cosine_similarity(Input, vector), 2)
    output=np.flipud(Similarity.argsort()[(-1-top_k):-1])
    company=["" for x in range(len(output))]
    company_cat=["" for x in range(len(output))]
    for index, i in enumerate(output):
        company[index] = Website[i]
        company_cat[index] = y_vector[i]
        #similarity[index] =Similarity[i]
    wrap = list(zip(company, company_cat))
    #return render_template('recommendation.html', companies = company, company_category = company_cat)
    return render_template('recommendation.html', combine=wrap)


# run the app
if __name__ == "__main__":
    app.jinja_env.cache = {}
    #app.run(host='0.0.0.0', debug=False, threaded=True,port=5000)
    app.run(host='0.0.0.0', debug=True, threaded=True,port=5000)