from get_data import *
from ml_utils import *
import time

keywords = ['machine+learning', 'data+science', 'kaggle']

def update_db():
    with open('new_videos.json', 'w+') as data_file:
        for keyword in keywords:
            for page in range(1,4):
                search_page = download_search_page(keyword, page)
                videos_list = parse_search_page(search_page)
                
                for video in videos_list:
                    video_page = download_video_page(video['link'])
                    video_json_data = parse_video_page(video_page)
                    
                    if 'watch-time-text' not in video_json_data: # if the video parsed does not have a title, discard
                        continue
                        
                    p = compute_prediction(video_json_data)
                    
                    video_id = video_json_data.get('og:video:url', '')
                    data_front = {"title": video_json_data['watch-title'], "score": float(p), "video_id": video_id}
                    
                    print(video_id, json.dumps(data_front))
                    data_file.write('{}\n'.format(json.dumps(data_front)))
                    
    return True