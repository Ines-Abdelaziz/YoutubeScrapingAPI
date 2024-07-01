from flask import Flask, request, jsonify
from flask_cors import CORS

from dataclasses import asdict


# Assuming ChannelData and VideoData are imported from somewhere
from data_extraction import ChannelData, VideoData, video_data

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/video_data', methods=['get'])
def get_video_data():
    video_id = request.args.get('video_id')
    videoData, channelData = video_data(video_id)

    Vdata = VideoData(
        video_id=videoData.video_id[0],
        published_at=videoData.published_at[0],
        channel_id=videoData.channel_id[0],
        title=videoData.title[0],
        description=videoData.description[0],
        view_count=videoData.view_count[0],
        made_for_kids=videoData.made_for_kids[0],
        like_count=videoData.like_count[0],
        dislike_count=videoData.dislike_count[0],
        comment_count=videoData.comment_count[0],
        topic_categories=videoData.topic_categories[0],

    )

    Chdata = ChannelData(
        id=channelData.id[0],
        title=channelData.title[0],
        description=channelData.description[0],
        keywords=list(channelData.keywords),  # Convert set to list
        view_count=channelData.view_count[0],
        subscriber_count=channelData.subscriber_count[0],
        video_count=channelData.video_count[0]
    )

    # Convert dataclasses to dictionaries
    Vdata_dict = asdict(Vdata)
    Chdata_dict = asdict(Chdata)
    # If any field in the dictionaries is a set, convert it to a list
    for key, value in Vdata_dict.items():
        if isinstance(value, set):
            Vdata_dict[key] = list(value)

    for key, value in Chdata_dict.items():
        if isinstance(value, set):
            Chdata_dict[key] = list(value)

    # Return scraped data as JSON response
    return jsonify({'video_data': Vdata_dict, 'channel_data': Chdata_dict})

if __name__ == "__main__":
    app.run(host="0.0.0.0")