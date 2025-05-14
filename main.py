""" 

    Shortify POC

    An app to generate short-form videos based on a given content and chosen videogame background

"""

import os
from math import ceil, floor
from utils import speech_utils, caption_utils
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
caption_font = "./resources/font/Roboto-Bold.ttf"

""" title_sentences = caption_utils.split_sentences(video_title) """
title_captions = caption_utils.split_displayed_captions(video_title)
title_caption_speech_dir = [speech_utils.generate_to_speech(title_captions[i], i, "title") for i in range(len(title_captions))]

title_caption_clips = [
    TextClip(
        text=caption,
        font=caption_font,    
        font_size=50,
        color="#FFFFFF",
        text_align="center"
    ) for caption in title_captions
]

title_caption_speech = [
    AudioFileClip(speech_dir) for speech_dir in title_caption_speech_dir
]

""" content_sentences = caption_utils.split_sentences(video_content) """
content_captions = caption_utils.split_displayed_captions(video_content)
content_caption_speech_dir = [speech_utils.generate_to_speech(content_captions[i], i, "content") for i in range(len(content_captions))]

content_caption_clips = [
        TextClip(
        text=caption,
        font=caption_font,    
        font_size=50,
        color="#FFFFFF",
        text_align="center"
    ) for caption in content_captions
]

content_caption_speech = [
    AudioFileClip(speech_dir) for speech_dir in content_caption_speech_dir
]

# Put the captions and their respective audio in an object for easy iteration
title_caption_collection = [{"caption": title_caption_clips[i], "speech": title_caption_speech[i]} for i in range(len(title_caption_clips))] # This is the var to use for handling title captions
content_caption_collection = [{"caption": content_caption_clips[i], "speech": content_caption_speech[i]} for i in range(len(content_caption_clips))] # This is the var to use for handling content captions

# Load the background video file
bg_video = VideoFileClip(f'./clips/video/bg/{video_bg}.mp4')

title_duration = sum([floor(speech.duration) for speech in title_caption_speech])
content_duration = sum([floor(speech.duration) for speech in content_caption_speech])

title_bg_clip = bg_video.subclipped(0, title_duration)
content_bg_clip = bg_video.subclipped(title_duration, content_duration + title_duration)

total_duration = 0
title_caption_clip_collection = []

for pair in title_caption_collection:

    current_caption = pair["caption"]
    current_speech = pair["speech"]

    caption_duration = current_speech.duration

    current_caption = current_caption.with_start(total_duration).with_duration(caption_duration - 1).with_position(("center", "center"))
    current_speech = current_speech.with_start(total_duration).with_duration(caption_duration - 1)
    current_caption.audio = CompositeAudioClip([current_speech])

    total_duration = (caption_duration - 1) + total_duration
    print("Total Duration: ", total_duration)
    print("Video clip start: ", current_caption.start)

    title_caption_clip_collection.append(current_caption)

content_caption_clip_collection = []

for pair in content_caption_collection:

    current_caption = pair["caption"]
    current_speech = pair["speech"]

    caption_duration = current_speech.duration

    current_caption = current_caption.with_start(total_duration).with_duration(caption_duration - 1).with_position(("center", "center"))
    current_speech = current_speech.with_start(total_duration).with_duration(caption_duration - 1)
    current_caption.audio = CompositeAudioClip([current_speech])

    total_duration = (caption_duration - 1) + total_duration

    content_caption_clip_collection.append(current_caption)

title_final_clip = CompositeVideoClip([title_bg_clip] + title_caption_clip_collection)
content_final_clip = CompositeVideoClip([content_bg_clip] + content_caption_clip_collection)

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
