from utils import speech_utils, caption_utils
from moviepy import TextClip, AudioFileClip, VideoFileClip, CompositeVideoClip, CompositeAudioClip

caption_font = "./resources/font/Roboto-Bold.ttf"

def create_caption_and_audio_clips(text_excerpt:str, excerpt_type:str):
    """ 
        Creates captions and generates speech for the given text excerpt.

        Returns a list that contains the collection of generated captions and speeches

        :param str text_excerpt: the block of text that will be used as basis for generating captions and speeches
        :param str excerpt_type: determines which part of the video the text block is. Can be 'title' or 'content'
        :return: a list of collections for the generated captions/speeches
    """

    try:
        if excerpt_type not in ['title', 'content']:
            raise ValueError("excerpt_type can only be either 'title' or 'content'")
  
        sentences = caption_utils.split_sentences(text_excerpt)
        captions = [caption_utils.split_displayed_captions(sentence) for sentence in sentences]
        caption_speech_dirs = [speech_utils.generate_to_speech(sentences[i], i, excerpt_type) for i in range(len(sentences))]

        caption_clips = []

        for collection in captions:
            caption_text_clips = [
                TextClip(
                    text=caption,
                    font=caption_font,    
                    font_size=50,
                    color="#FFFFFF",
                    text_align="center"
                ) for caption in collection
            ]

            caption_clips.append(caption_text_clips)

        caption_speech_clips = [
            AudioFileClip(speech_dir) for speech_dir in caption_speech_dirs
        ]

        caption_and_audio_collection = [{
            "sentence": sentences[i], 
            "captions": caption_clips[i], 
            "speech": caption_speech_clips[i]
            }     
            
            for i in range(len(sentences))] # This is the var to use for handling title captions

        return caption_and_audio_collection
    
    except Exception as e:
        print(str(e))

def extract_short_video_clip(length:float, selected_bg:str):
    """ 
        Extracts a random part from the selected background video based on the given length

        Returns a `VideoClip` with the length of the total duration of the captions

        :param float length: the total length of the captions that will be used as basis for the background clip length
        :param str selected_bg: the name of the selected MP4 background clip
        :return: the extracted `VideoClip` from the chosen background video clip

    """
    import random

    bg_video = VideoFileClip(f'../clips/video/bg/{selected_bg}.mp4')
    rand_clip_start = random.randint(0, int((bg_video.duration - length)))
    clip_end = rand_clip_start + length

    extracted_clip:VideoFileClip = bg_video.subclipped(rand_clip_start, clip_end)

    return extracted_clip

def convert_caption_collection_to_clip(collection:list, start:float):

    total_duration = start
    caption_clip_collection = []

    for obj in collection:

        current_captions = obj["captions"]
        current_speech = obj["speech"]        

        speech_duration = current_speech.duration
        caption_duration = speech_duration / len(current_captions)

        for i in range(len(current_captions)):
            current_captions[i] = current_captions[i].with_start(total_duration).with_duration(caption_duration).with_position(("center", "center"))        

        # Combine the modified caption clips and set the speech as the audio of the resulting clip 
        appended_caption_clips = CompositeVideoClip(current_captions)
        current_speech = current_speech.with_start(appended_caption_clips.start).with_duration(appended_caption_clips.duration)
        appended_caption_clips.audio = current_speech
        
        caption_clip_collection.append(appended_caption_clips)

        total_duration = appended_caption_clips + total_duration

    resulting_clip = CompositeVideoClip(caption_clip_collection)

    return resulting_clip