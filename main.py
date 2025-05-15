""" 

    Shortify POC

    An app to generate short-form videos based on a given content and chosen videogame background

"""

import os
from utils import clip_utils
from math import ceil, floor
from moviepy import VideoFileClip, vfx, TextClip, AudioFileClip, CompositeAudioClip, CompositeVideoClip, concatenate_videoclips

# TODO: Comment the process. It's been a week and I'm already lost in my own code.

# Stick to gathering the video details through CMD for now
video_title = ""
test = video_title
video_content = ""
video_bg = ""

# At this part, we are just retrieving video content information from the user
available_video_bg = ["rdr2", "dark souls", "sekiro", "got1", "got2"]

while (video_title == ""):
    print("==========")
    video_title = input("Enter video title: ")
    print("==========")

    if video_title == "":
        print("\n\nPlease enter a valid video title!\n\n")

while (video_content == ""):
    print("==========")
    video_content = input("Enter video content: ")
    print("==========")

    if video_content == "":
        print("\n\nPlease enter a valid video content!\n\n")

while (video_bg not in available_video_bg):
    print("==========")
    video_bg = input(f"Enter video background (Available: {available_video_bg}): ")
    print("==========")

    if video_bg not in available_video_bg:
        print("\n\nPlease enter a valid video background!\n\n")

# Prepare the captions for each video clip. Split them into words that can fit in a 9:16 aspect ratio (1-3 words based on length)
title_clips = clip_utils.create_caption_and_audio_clips(video_title, 'title')
content_clips = clip_utils.create_caption_and_audio_clips(video_content, 'content')

# Append the caption and speech collection to one big clip
title_captions = clip_utils.convert_caption_collection_to_clip(title_clips, 0)
content_captions = clip_utils.convert_caption_collection_to_clip(content_clips, title_captions.duration)

# Extract subclips from chosen background video
title_bg_clip = clip_utils.extract_short_video_clip(title_captions.duration, video_bg)
content_bg_clip = clip_utils.extract_short_video_clip(content_captions.duration, video_bg)

title_final_clip = CompositeVideoClip([title_bg_clip, title_captions])
content_final_clip = CompositeVideoClip([content_bg_clip, content_captions])

final_clip = concatenate_videoclips([title_final_clip, content_final_clip])
final_clip.write_videofile('./clips/video/full_clip.mp4')

""" 
# Generate the speeches to be used in the short form video
title_dir = speech_utils.generate_to_speech(video_title, "title")
content_dir = speech_utils.generate_to_speech(video_content, "content")

# Import the video and audio clips to manipulate
bg_video = VideoFileClip(f'./clips/video/bg/{video_bg}.mp4')
title_audio = AudioFileClip('./clips/audio/title.mp3')
content_audio = AudioFileClip('./clips/audio/content.mp3')

# Get the duration of the audio clips
title_audio_duration = ceil(title_audio.duration)
content_audio_duration = ceil(content_audio.duration)

# Clip the title and content video clips using the audio duration
title_bg_clip = bg_video.subclipped(0, title_audio_duration)
content_bg_clip = bg_video.subclipped(title_audio_duration, content_audio_duration + title_audio_duration)

# Attach the audio clips to the clipped video parts
title_bg_clip.audio = CompositeAudioClip([title_audio])
content_bg_clip.audio = CompositeAudioClip([content_audio])

title_text = TextClip(
    text=video_title,
    font=caption_font,    
    font_size=50,
    color="#FFFFFF",
    text_align="center"
)

content_text = TextClip(
    font=caption_font,
    text=video_content,
    font_size=50,
    color="#000000",
    text_align="center"
)

# Time the clips to play after another
title_bg_clip = title_bg_clip.with_duration(5)
title_text = title_text.with_duration(title_audio_duration).with_position(("center", "center")).with_fps(20).with_start(0)


content_bg_clip = content_bg_clip.with_start(title_text.end).with_end(content_audio_duration**2)


title_clip = CompositeVideoClip([title_bg_clip, title_text])
content_clip = CompositeVideoClip()
full_clip.write_videofile('./clips/video/full_clip.mp4')



print(f"\n\n{content_audio_duration}\n\n") """
