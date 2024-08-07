
from dataclasses import dataclass
from youtubesearchpython import VideosSearch, ChannelsSearch
from datetime import datetime
from dateutil.relativedelta import relativedelta
import re

from pytube import Channel

def get_youtube_channel_title(channel_url):
    try:
        # Create a Channel object
        channel = Channel(channel_url)
        
        # Return the channel title
        return channel.channel_name
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
# Define the video ID
@dataclass
class VideoData:
    video_id: str
    published_at: str
    channel_id: str
    title: str
    description: str
    view_count: str
    made_for_kids: str
    like_count: str
    dislike_count: str
    comment_count: str
    topic_categories: set
@dataclass
class ChannelData:
    id: str
    title: str
    description: str
    keywords: str
    view_count: str
    subscriber_count: int
    video_count: int

def video_data(video_id):
    # Perform a search using the video ID
    videosSearch = VideosSearch(video_id, limit=1)
    result = videosSearch.result()

    # Extract video details
    video = result['result'][0]
    video_id= video.get('id'),
    published_at= calculate_datestamp( video.get('publishedTime')),
    if video.get('channel') is not None:
        channel_id= video.get('channel').get('id'),
    title= video.get('title'),
    if video.get('descriptionSnippet') is not None:  
        description= video.get('descriptionSnippet')[0].get('text'),
    if video.get('viewCount') is not None:
        view_count= video.get('viewCount').get('text'),
    made_for_kids= 'N/A',
    like_count='N/A',
    dislike_count='N/A',
    comment_count='N/A',
    topic_categories={''},
    video_data = VideoData(  
        video_id=video_id,
        published_at=published_at,
        channel_id=channel_id,
        title=title,
        description=description,
        view_count=view_count,
        made_for_kids=made_for_kids,
        like_count=like_count,
        dislike_count=dislike_count,
        comment_count=comment_count,
        topic_categories=topic_categories,
       )
    channel_url = 'https://www.youtube.com/channel/'+channel_id[0]
    channel_title = get_youtube_channel_title(channel_url)
    print(channel_title)
    ChannelSearch = ChannelsSearch(channel_title, limit=1)
    channel=ChannelSearch.result()['result'][0]
    print(channel)
    id=channel_id[0],
    title=channel.get('title'),
    if channel.get('descriptionSnippet') is not None:
        description=channel.get('descriptionSnippet')[0].get('text'),
    keywords='',
    view_count='',
    subscriber_count=transform_to_bigint(channel.get('subscribers')),
    video_count=channel.get('videoCount',0),
    channel_data=ChannelData(
        id=id,
        title=title,
        description=description,
        keywords=keywords,
        view_count=view_count,
        subscriber_count=subscriber_count,
        video_count=video_count
    )
   
    return video_data,channel_data

def calculate_datestamp(relative_time):
    # Extracting the number and the time unit from the input string
    match = re.search(r'(\d+)\s*(seconds?|minutes?|hours?|days?|weeks?|months?|years?)\s*ago', relative_time)
    if not match:
        raise ValueError("Input string is not in a recognized format")

    # Get the amount and the time units from the regex match
    amount = int(match.group(1))
    unit = match.group(2)

    # Mapping singular units to their corresponding relativedelta arguments
    unit_mapping = {
        'second': 'seconds',
        'minute': 'minutes',
        'hour': 'hours',
        'day': 'days',
        'week': 'weeks',
        'month': 'months',
        'year': 'years'
    }

    # Handling plural forms by removing the ending 's' if present
    unit = unit_mapping.get(unit.rstrip('s'), unit)

    # Calculating the new datetime
    delta_kwargs = {unit: -amount}
    new_date = datetime.now() + relativedelta(**delta_kwargs)

    return new_date
def transform_to_bigint(value: str) -> int:
    try:
        # Define suffix multipliers
        suffixes = {'K': 1_000, 'M': 1_000_000, 'B': 1_000_000_000, 'T': 1_000_000_000_000}
        value=value.split(' ')[0]
        # Extract the numeric part and the suffix
        if value[-1] in suffixes:
            multiplier = suffixes[value[-1]]
            numeric_part = float(value[:-1])
        else:
            multiplier = 1
            numeric_part = float(value)
        
        # Convert to bigint
        bigint_value = int(numeric_part * multiplier)
        return bigint_value
    except Exception as e:
        return 0
