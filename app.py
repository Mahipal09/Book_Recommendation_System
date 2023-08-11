from flask import Flask, render_template, request, url_for
import pickle
import numpy as np

popular_df = pickle.load(open('popular.pkl', 'rb'))
pt = pickle.load(open('pt.pkl', 'rb'))
books = pickle.load(open('books.pkl', 'rb'))
similarity_scores = pickle.load(open('similarity_scores.pkl', 'rb'))

app = Flask(__name__)


@app.route('/')

def index():
    return render_template('index.html',
                           book_name = list(popular_df['Book-Title'].values),
                           book_author = list(popular_df['Book-Author'].values),
                           image = list(popular_df['Image-URL-M'].values),
                           votes = list(popular_df['Num-Rating'].values),
                           ratings = list(popular_df['Avg-Rating'].values)
                           )



@app.route('/recommender')

def recommender_books():
    return render_template('recommendation.html')

@app.route('/search', methods=['POST'])

def recommender_ui():
    book_name = request.form.get('book_name')
    index_arr = np.where(pt.index==book_name)[0]
    if len(index_arr) > 0:
        index = index_arr[0]
        similar_items = sorted(list(enumerate(similarity_scores[index])),key=lambda x:x[1],reverse=True)[1:6]
    
        data = []
        for i in similar_items:
            item = []
            temp_df = books[books['Book-Title'] == pt.index[i[0]]]
            item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
            item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
            item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))
            
            data.append(item)

            print(data)
        
        return render_template('recommendation.html', data=data)

 # If the book name is not found, render the template with an error message or default message
    return render_template('recommendation.html', error_message="No matching book found for the entered name.")



@app.route('/contact_info')

def contacts():
    return render_template('contactinfo.html')




if __name__ == '__main__':
    app.run(debug=True)