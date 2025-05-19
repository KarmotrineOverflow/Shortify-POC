""" 

We need functions for:

- Splitting the content by sentences
- Limitting captions to 2-3 words displayed

"""

def split_sentences(text_block):

    sentences = text_block.split('.|. |, |?|? ')
    print(sentences)

    if sentences is [None]:
        return [text_block]
    
    return sentences

def split_displayed_captions(text_excerpt):

    words = text_excerpt.split(' ')
    new_combinations = []

    """ for i in range(len(words)):
        if len(words[i]) >= 10 or i + 1 > len(words) - 1:
            new_combinations.append(words[i])
        
        else:
            new_combinations.append(" ".join([words[i], words[i + 1]]))
            i += 1
 """
    word_index = 0

    while word_index <= len(words) - 1:
        if len(words[word_index]) >= 10 or word_index + 1 > len(words) - 1:
            new_combinations.append(words[word_index])
            word_index += 1

        else:
            new_combinations.append(" ".join([words[word_index], words[word_index + 1]]))
            word_index += 2

        print(word_index)

    print(new_combinations)
    return new_combinations

def attach_audio_to_caption(caption, audio, start, end):

    return None