from utils import speech_utils, caption_utils
from moviepy import TextClip, AudioFileClip

caption_font = "./resources/font/Roboto-Bold.ttf"

def create_caption_and_audio_clips(text_excerpt):
    captions = caption_utils.split_displayed_captions(text_excerpt)
    caption_speech_dirs = [speech_utils.generate_to_speech(captions[i], i, "title") for i in range(len(captions))]

    caption_text_clips = [
        TextClip(
            text=caption,
            font=caption_font,    
            font_size=50,
            color="#FFFFFF",
            text_align="center"
        ) for caption in captions
    ]

    caption_speech_clips = [
        AudioFileClip(speech_dir) for speech_dir in caption_speech_dirs
    ]

    caption_and_audio_collection = [{"caption": caption_text_clips[i], "speech": caption_speech_clips[i]} for i in range(len(caption_text_clips))] # This is the var to use for handling title captions

    return caption_and_audio_collection