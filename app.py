from flask import Flask, render_template, request
import numpy as np
import pandas as pd
from sklearn.preprocessing import normalize

app = Flask(__name__)
df = pd.read_csv('tcc_ceds_music_computed.csv')

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
    
    counts = np.zeros((len(word_index_dict), ) * 2)
    for lyric in genre_df['lyrics']:
        words = lyric.split()
        previous_word = '<s>'
        for word in words[1:]:
            if word.lower() in word_index_dict:
                current_word = word.lower()
                prev_idx = word_index_dict[previous_word]
                curr_idx = word_index_dict[current_word]
                counts[prev_idx, curr_idx] += 1
                previous_word = current_word

    ALPHA_SMOOTHING = 0.1
    counts += ALPHA_SMOOTHING
    
    probs = normalize(counts, norm='l1', axis=1)
    return word_index_dict, probs


def GENERATE(word_index_dict, probs, max_words, start_word, temperature):
    returnSTR = ""
    index_word_dict = {v: k for k, v in word_index_dict.items()}
    num_words = 0
    model_type = "bigram"

    if model_type == "bigram":
        returnSTR = start_word + " "
        prevWord = start_word
        while True:
            # Apply temperature scaling
            probs_scaled = np.power(probs[word_index_dict[prevWord]], 1/temperature)
            probs_scaled /= np.sum(probs_scaled)
            wordIndex = np.random.choice(len(word_index_dict), 1, p=probs_scaled)[0]
            word = index_word_dict[wordIndex]
            returnSTR += word + " "
            num_words +=1
            prevWord = word
            if word == "</s>" or num_words == max_words:
                break

    return returnSTR

#def GENERATE(word_index_dict, probs, max_words, start_word):
#    returnSTR = ""
#    index_word_dict = {v: k for k, v in word_index_dict.items()}
#    num_words = 0
#    model_type = "bigram"
#
#
#    if model_type == "bigram":
#        returnSTR = start_word + " "
#        prevWord = start_word
#        while True:
#            wordIndex = np.random.choice(len(word_index_dict), 1, p=list(probs[word_index_dict[prevWord]]))
#            word = index_word_dict[wordIndex[0]]
#            returnSTR += word + " "
#            num_words +=1
#            prevWord = word
#            if word == "</s>" or num_words == max_words:
#                break
#
#    return returnSTR
#

@app.route("/")
def index():
    return render_template('index.html')


@app.route('/lyrics', methods=['POST'])
def lyrics():
    genre = request.form['genre']
    sadness_range = [float(request.form['min_sadness']), float(request.form['max_sadness'])]
    number_sentences = int(request.form['n_sentences'])
    number_words = int(request.form['n_words'])
    temperature = float(request.form['temperature'])
    word_index_dict, probs = create_dict(genre, sadness_range)
    lyrics = []

    for i in range(number_sentences):
        sent = GENERATE(word_index_dict, probs, number_words, '<s>', temperature)
        sent = ' '.join(word for word in sent.split() if word != '<s>')
        if sent:
            lyrics.append(sent)
    return render_template('lyrics.html', genre=genre, lyrics=lyrics)
#def lyrics():
#    genre = request.form['genre']
#    sadness_range = [float(request.form['min_sadness']), float(request.form['max_sadness'])]
#    number_sentences= int(request.form['n_sentences'])
#    number_words= int(request.form['n_words'])
#    word_index_dict, probs = create_dict(genre, sadness_range)
#    lyrics = []
#
#    for i in range(number_sentences):
#        sent = GENERATE(word_index_dict, probs, number_words, '<s>')
#        sent = ' '.join(word for word in sent.split() if word != '<s>')
#        if sent:
#            lyrics.append(sent)
#    return render_template('lyrics.html', genre=genre, lyrics=lyrics)
#


if __name__ == "__main__":
    app.run(debug=True)
