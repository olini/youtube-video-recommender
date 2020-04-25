import os.path
from flask import Flask
import os
import json
import run_backend
import time
import sqlite3 as sql

app = Flask(__name__)

def get_predictions():
    videos = []
    
    new_videos_json = 'new_videos.json'
    if not os.path.exists(new_videos_json):
        run_backend.update_db()
        
    with open(new_videos_json, 'r') as data_file:
        for line in data_file:
            line_json = json.loads(line)
            videos.append(line_json)
    
    predictions = []
    for video in videos:
        print(video)
        predictions.append((video['video_id'], video['title'], float(video['score'])))
        
    predictions = sorted(predictions, key=lambda x: x[2], reverse=True)[:30]
    
    predictions_formatted = []
    for prediction in predictions:
        print(prediction)
        predictions_formatted.append('<tr><th><a href=\'{link}\'>{title}</a></th><th>{score}</th></tr>'. format(link=prediction[0], title=prediction[1], score=prediction[2]))
        
    return '\n'.join(predictions_formatted)

@app.route('/')
def main():
    predictions = get_predictions()
    return '''
    <head>
        <h1>YouTube Video Recommender</h1>
    </head>
    <body>
        <table>{predictions}</table>
    </body>
    '''.format(predictions=predictions)
    
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')