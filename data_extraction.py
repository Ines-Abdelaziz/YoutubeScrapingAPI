
from dataclasses import dataclass
from youtubesearchpython import VideosSearch, ChannelsSearch
from datetime import datetime
from dateutil.relativedelta import relativedelta
import re
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
    timestamp: str
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
    video_data = VideoData(  
        video_id= video.get('id', ''),
        published_at= calculate_datestamp( video.get('publishedTime', '')),
        channel_id= video.get('channel').get('id', ''),
        title= video.get('title', ''),
        description= video.get('descriptionSnippet')[0].get('text', ''),
        view_count= video.get('viewCount').get('text', ''),
        made_for_kids= 'N/A',
        like_count='N/A',
        dislike_count='N/A',
        comment_count='N/A',
        topic_categories={''},
        timestamp= datetime.now().isoformat(),)
    
    
    channel_id=video_data.channel_id
    ChannelSearch = ChannelsSearch(channel_id, limit=1)
    channel=ChannelSearch.result()['result'][0]
    channel_data=ChannelData(
        id=channel_id,
        title=channel.get('title', ''),
        description=channel.get('descriptionSnippet')[0].get('text', ''),
        keywords='',
        view_count='',
        subscriber_count=transform_to_bigint(channel.get('subscribers')),
        #if none type is returned, then the value is set to 0
        video_count=channel.get('videoCount',0),
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
