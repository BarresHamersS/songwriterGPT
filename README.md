# songwriterGPT

This repo contains the code for songwriter GPT.

A simple unigram model is build and trained on the tcc_ceds_music dataset which contains over 25 mb of lyrics and the corresponding metadata.

The app is build with a simple Flask application.

The user can choose what kind of text should be generated this is done by accessing the corresponding data of the tcc_ceds_music dataset with the help of pandas.


The app_figures show several figures of the app in process

How to run:
- create a new virtual environment
    python -m venv myenv  
- activate the virtual environment
    source myenv/bin/activate
-  install the required packa  
    pip install -r requirements.txt 

Then in the directory run:
- flask run

Have fun!

