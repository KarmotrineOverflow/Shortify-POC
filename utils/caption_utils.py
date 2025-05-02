""" 

We need functions for:

- Splitting the content by sentences
- Limitting captions to 2-3 words displayed

"""

def split_sentences(text_block):

    sentences = text_block.split('.')
    print(sentences)

    if sentences is [None]:
        return [text_block]
    
    return sentences

def split_displayed_captions(text_excerpt):

    words = text_excerpt.split(' ')
    new_combinations = []

    for i in range(len(words)):
        if len(words[i]) >= 10 or i + 1 > len(words) - 1:
            new_combinations.append(words[i])
        
        else:
            new_combinations.append(" ".join([words[i], words[i + 1]]))

    print(new_combinations)
    return new_combinations
