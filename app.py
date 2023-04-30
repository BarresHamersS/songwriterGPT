from flask import Flask, render_template, request
import numpy as np
import pandas as pd

app = Flask(__name__)
df = pd.read_csv('tcc_ceds_music.csv')

def create_dict(genre, sadness_factor):
    genre_df = df.loc[(df['genre'] == genre) & ((df['sadness'] >= sadness_factor[0]) & (df['sadness'] <= sadness_factor[1]))]

    word_index_dict = {}
    index = 0
    for lyric in genre_df['lyrics']:
        words = lyric.split()
        for word in words:
            if word not in word_index_dict:
                word_index_dict[word] = index
                index += 1
    

    counts = np.zeros(len(word_index_dict))
    for lyric in df['lyrics']:
        words = lyric.split()
        for word in words:
            if word.lower() in word_index_dict:
                index = word_index_dict[word.lower()]
                counts[index] += 1
                
    probs = counts / np.sum(counts)
    return word_index_dict, probs



def GENERATE(word_index_dict, probs, max_words):
    returnSTR = ""
    index_word_dict = {v: k for k, v in word_index_dict.items()}
    num_words = 0
    model_type = "unigram"


    if model_type == "unigram":
        while(True):
            wordIndex = np.random.choice(len(word_index_dict), 1, p=list(probs))
            word = index_word_dict[wordIndex[0]]
            returnSTR += word + " "
            num_words +=1
            if word == "</s>" or num_words == max_words:
                break

        return returnSTR


@app.route("/")
def index():
    return render_template('index.html')


@app.route('/lyrics', methods=['POST'])
def lyrics():
    genre = request.form['genre']
    sadness_range = [float(request.form['min_sadness']), float(request.form['max_sadness'])]
    number_sentences= int(request.form['n_sentences'])
    number_words= int(request.form['n_words'])
    word_index_dict, probs = create_dict(genre, sadness_range)
    lyrics = []
    for i in range(number_sentences):
        sent = GENERATE(word_index_dict, probs, number_words)
        lyrics.append(sent)
    return render_template('lyrics.html', genre=genre, lyrics=lyrics)




if __name__ == "__main__":
    app.run(debug=True)
