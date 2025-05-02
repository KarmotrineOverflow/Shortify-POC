import pyttsx3, os

engine = pyttsx3.init()
engine.setProperty('rate', 140)

def generate_to_speech(text:str, file_name:str, dir:str):
    """ 

    Generates the given text into an MP3 speech file with the given name

    Properties:

    - `text`: (str) - The text that the generative speech will base on
    - `title`: (str) - The file name that will be given to the generated MP3

    Returns:

    - `path`: (str) - The file directory of the generated MP3 file
      
    """

    generated_mp3_dir = f"{file_name}.mp3"

    # TODO: Try separating each clip to their own dirs using the title
    try:
        os.makedirs(f'{os.getcwd()}\\clips\\audio\\{dir}')

    except FileExistsError:
        print("Audio clip dir already exists.")
    
    finally:
        os.chdir(f'{os.getcwd()}\\clips\\audio\\{dir}')

        engine.save_to_file(text, generated_mp3_dir)
        engine.runAndWait()

        os.chdir(f'{os.getcwd()}\\..\\..\\..\\')

    return f'{os.getcwd()}/clips/audio/{dir}/{generated_mp3_dir}'