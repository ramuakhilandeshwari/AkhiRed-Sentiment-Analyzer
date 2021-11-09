from flask import Flask, request, render_template,url_for
from flask_cors import cross_origin
import boto3
import json


app = Flask(__name__)

@app.route("/")
@cross_origin()
def home():
    return render_template("index.html")

@app.route("/sound", methods = ["GET", "POST"])
@cross_origin()
def sound():
    if request.method == "POST":
        text_senti = request.form['textforsenti']          
        # Code to analyse the sentiment of the given text using comprehend
        comprehend = boto3.client(service_name='comprehend', region_name='us-east-1')
        senti_result=json.dumps(comprehend.detect_sentiment(Text=text_senti, LanguageCode='en'), sort_keys=True, indent=4)
        # Code for text to voice conversion using polly
        polly = boto3.client(service_name='polly',region_name='us-east-1')  
        response = polly.synthesize_speech(OutputFormat='mp3', VoiceId='Brian',Text=senti_result)
        file = open('static/speech.mp3', 'wb')
        file.write(response['AudioStream'].read())
        file.close()
        audiospeech=True

    return render_template("index.html",conversion=senti_result,audiospeech=audiospeech)


if __name__ == "__main__":
    app.run(debug=True)
