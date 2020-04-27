import get_data
from ml_utils import compute_prediction
import time
import json
import sqlite3 as sql

keywords = ['machine+learning', 'data+science', 'kaggle']
db_name = 'videos.db'

def update_db():
    with sql.connect(db_name) as conn:
        for keyword in keywords:
            for page in range(1,4):
                search_page = get_data.download_search_page(keyword, page)
                videos_list = get_data.parse_search_page(search_page)
                
                for video in videos_list:
                    video_page = get_data.download_video_page(video['link'])
                    video_json_data = get_data.parse_video_page(video_page)
                    
                    if 'watch-time-text' not in video_json_data: # if the video parsed does not have a title, discard
                        continue
                        
                    p = compute_prediction(video_json_data)
                    
                    video_id = video_json_data.get('og:video:url', '')
                    video_title = video_json_data['watch-title'].replace("'", "''")
                    data_front = {"title": video_title, "score": float(p), "video_id": video_id}
                    
                    print(video_id, json.dumps(data_front))
                    cursor = conn.cursor()
                    cursor.execute("INSERT INTO videos VALUES ('{title}', '{video_id}', {score})".format(**data_front))
                    conn.commit()
                    
    return True