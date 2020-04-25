import os.path
from flask import Flask, render_template
import os
import json
import run_backend
import time
#import sqlite3 as sql

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
    
    videos_unique = [i for n, i in enumerate(videos) if i not in videos[n + 1:]] # erase duplicates

    predictions = []
    for video in videos_unique:
        print(video)
        predictions.append(
            {"video_link": video['video_id'], 
            "video_title": video['title'], 
            "video_score": float(video['score'])})
        
    predictions = sorted(predictions, key=lambda x: x['video_score'], reverse=True)[:30]
    
    return predictions

@app.route('/')
def main():
    predictions = get_predictions()
    return render_template('index.html', predictions=predictions)
    
if __name__ == '__main__':
    #app.run(debug=True)
    app.run(debug=True, host='0.0.0.0')