from flask import Flask, request, jsonify
from dataclasses import asdict

# Assuming ChannelData and VideoData are imported from somewhere
from data_extraction import ChannelData, VideoData, video_data

app = Flask(__name__)

@app.route('/video_data', methods=['get'])
def get_video_data():
    video_id = request.args.get('video_id')
    videoData, channelData = video_data(video_id)

    Vdata = VideoData(
        video_id=videoData.video_id,
        published_at=videoData.published_at,
        channel_id=videoData.channel_id,
        title=videoData.title,
        description=videoData.description,
        view_count=videoData.view_count,
        made_for_kids=videoData.made_for_kids,
        like_count=videoData.like_count,
        dislike_count=videoData.dislike_count,
        comment_count=videoData.comment_count,
        topic_categories=videoData.topic_categories,

    )

    Chdata = ChannelData(
        id=channelData.id,
        title=channelData.title,
        description=channelData.description,
        keywords=list(channelData.keywords),  # Convert set to list
        view_count=channelData.view_count,
        subscriber_count=channelData.subscriber_count,
        video_count=channelData.video_count
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