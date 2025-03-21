import os
import json
from PIL import Image
import re

def short_answer(answer):
    answer = answer.split('\n')[0]
    answer = answer.split('. ')[0]
    answer = answer.split('\"')[0]
    answer = answer.split(', ')[0]
    answer = answer.strip()
    answer = answer.lower()
    answer = answer if len(answer) == 0 or answer[-1] != '.' else answer[:-1]
    answer = answer.replace('it is ', '', 1) if answer.startswith('it is ') else answer
    answer = answer.replace('it\'s ', '', 1) if answer.startswith('it\'s ') else answer
    answer = answer.replace('a ', '', 1) if answer.startswith('a ') else answer
    answer = answer.replace('an ', '', 1) if answer.startswith('an ') else answer
    answer = answer.replace('the ', '', 1) if answer.startswith('the ') else answer
    return answer




def make_prompt(question, image_token='', labed_answer = '', choices = [], Reasoning = False):
    #prompt = f'\nBased on the picture: {image_token}, {question} Short answer: {labed_answer}'

    #prompt = f'\n{image_token}Question: {question} Answer: {labed_answer}'
    # "Image:<image>Question: {question} Answer: {answer}\n",
    # if len(labed_answer) > 0:
    #     prompt = prompt + "###"
    if len(choices) > 0:
        question = question + ' Choices:' + ' '.join(choices)
    if len(labed_answer) > 0: 
        #prompt = f'{image_token}Question: {question} Answer: {labed_answer}\n'
        prompt_hf = f'Image:{image_token}Question: {question} Answer: {labed_answer}\n'
        #prompt4 = f'\nBased on the picture: {image_token}, {question} Short answer: {labed_answer}###'
    elif Reasoning:
        prompt_hf = f'Image:{image_token}Question: {question} Let us think step by step:'
        #prompt4 = f'Based on the picture: {image_token}, {question} Let us think step by step:'
    else:
        prompt_hf = f'Image:{image_token}Question: {question} Answer:'
        #prompt4 = f'Based on the picture: {image_token}, {question} Short answer:'
    return prompt_hf



def make_prompt_debug(question, image_token='', labed_answer = '', choices = [], Reasoning = False):
    #prompt = f'\nBased on the picture: {image_token}, {question} Short answer: {labed_answer}'

    #prompt = f'\n{image_token}Question: {question} Answer: {labed_answer}'
    # "Image:<image>Question: {question} Answer: {answer}\n",
    # if len(labed_answer) > 0:
    #     prompt = prompt + "###"
    if len(choices) > 0:
        question = question + ' Choices:' + ' '.join(choices)
    if len(labed_answer) > 0: 
        #prompt = f'{image_token}Question: {question} Answer: {labed_answer}\n'
        #prompt_hf = f'Image:{image_token}Question: {question} Answer: {labed_answer}\n'
        prompt4 = f'Based on the image: {image_token}, {question} Short answer: {labed_answer}###\n'
        #prompt5 = f'{image_token}, {question} We can see these words from the image and calculate the final answer: {labed_answer}###\n'
        #prompt6 = f'Image: {image_token}, Question:{question} \nThe answer: {labed_answer}###\n'
        #prompt7 = f'Image: {image_token}, Question:{question} The answer: {labed_answer}###\n'
        #prompt8 = f'Image: {image_token}, Question:{question} Short answer: {labed_answer}###\n'
        prompt9 = f'Image: {image_token}, {question} Short answer: {labed_answer}###\n'
        prompt10 = f'Based on the image: {image_token}, The question: {question} Short answer: {labed_answer}###\n'
    elif Reasoning:
        #prompt_hf = f'Image:{image_token}Question: {question} Let us think step by step:'
        prompt4 = f'Based on the image: {image_token}, {question} Let us think step by step:'
        prompt8 = f'Image: {image_token}, Question:{question} Let us think step by step:'
    else:
        #prompt_hf = f'Image:{image_token}Question: {question} Answer:'
        prompt4 = f'Based on the image: {image_token}, {question} Short answer:'
        prompt5 = f'{image_token}, {question} We can see these words from the image and calculate the final answer:'
        prompt6 = f'Image: {image_token}, Question:{question} \nThe answer: '
        prompt7 = f'Image: {image_token}, Question:{question} The answer: '
        prompt8 = f'Image: {image_token}, Question:{question} Short answer: '
        prompt9 = f'Image: {image_token}, {question} Short answer: '
        prompt10 = f'Based on the image: {image_token}, The question: {question} Short answer: '
        
    return prompt4


def read_image(image_id, prefix, image_path): 

    image_id = str(image_id)
    if prefix.startswith('COCO'):
        image_id = prefix  + '0' * (12-len(image_id)) + image_id + '.jpg'
    elif not image_id.endswith('.jpg') and not image_id.endswith('.png'):
        image_id = prefix + image_id + '.jpg'
        
    image_path = os.path.join(image_path, image_id)
    return Image.open(image_path).convert('RGB')



class EvalAIAnswerProcessor:
    """
    Processes an answer similar to Eval AI
        copied from
        https://github.com/facebookresearch/mmf/blob/c46b3b3391275b4181567db80943473a89ab98ab/pythia/tasks/processors.py#L897
    """

    CONTRACTIONS = {
        "aint": "ain't",
        "arent": "aren't",
        "cant": "can't",
        "couldve": "could've",
        "couldnt": "couldn't",
        "couldn'tve": "couldn't've",
        "couldnt've": "couldn't've",
        "didnt": "didn't",
        "doesnt": "doesn't",
        "dont": "don't",
        "hadnt": "hadn't",
        "hadnt've": "hadn't've",
        "hadn'tve": "hadn't've",
        "hasnt": "hasn't",
        "havent": "haven't",
        "hed": "he'd",
        "hed've": "he'd've",
        "he'dve": "he'd've",
        "hes": "he's",
        "howd": "how'd",
        "howll": "how'll",
        "hows": "how's",
        "Id've": "I'd've",
        "I'dve": "I'd've",
        "Im": "I'm",
        "Ive": "I've",
        "isnt": "isn't",
        "itd": "it'd",
        "itd've": "it'd've",
        "it'dve": "it'd've",
        "itll": "it'll",
        "let's": "let's",
        "maam": "ma'am",
        "mightnt": "mightn't",
        "mightnt've": "mightn't've",
        "mightn'tve": "mightn't've",
        "mightve": "might've",
        "mustnt": "mustn't",
        "mustve": "must've",
        "neednt": "needn't",
        "notve": "not've",
        "oclock": "o'clock",
        "oughtnt": "oughtn't",
        "ow's'at": "'ow's'at",
        "'ows'at": "'ow's'at",
        "'ow'sat": "'ow's'at",
        "shant": "shan't",
        "shed've": "she'd've",
        "she'dve": "she'd've",
        "she's": "she's",
        "shouldve": "should've",
        "shouldnt": "shouldn't",
        "shouldnt've": "shouldn't've",
        "shouldn'tve": "shouldn't've",
        "somebody'd": "somebodyd",
        "somebodyd've": "somebody'd've",
        "somebody'dve": "somebody'd've",
        "somebodyll": "somebody'll",
        "somebodys": "somebody's",
        "someoned": "someone'd",
        "someoned've": "someone'd've",
        "someone'dve": "someone'd've",
        "someonell": "someone'll",
        "someones": "someone's",
        "somethingd": "something'd",
        "somethingd've": "something'd've",
        "something'dve": "something'd've",
        "somethingll": "something'll",
        "thats": "that's",
        "thered": "there'd",
        "thered've": "there'd've",
        "there'dve": "there'd've",
        "therere": "there're",
        "theres": "there's",
        "theyd": "they'd",
        "theyd've": "they'd've",
        "they'dve": "they'd've",
        "theyll": "they'll",
        "theyre": "they're",
        "theyve": "they've",
        "twas": "'twas",
        "wasnt": "wasn't",
        "wed've": "we'd've",
        "we'dve": "we'd've",
        "weve": "we've",
        "werent": "weren't",
        "whatll": "what'll",
        "whatre": "what're",
        "whats": "what's",
        "whatve": "what've",
        "whens": "when's",
        "whered": "where'd",
        "wheres": "where's",
        "whereve": "where've",
        "whod": "who'd",
        "whod've": "who'd've",
        "who'dve": "who'd've",
        "wholl": "who'll",
        "whos": "who's",
        "whove": "who've",
        "whyll": "why'll",
        "whyre": "why're",
        "whys": "why's",
        "wont": "won't",
        "wouldve": "would've",
        "wouldnt": "wouldn't",
        "wouldnt've": "wouldn't've",
        "wouldn'tve": "wouldn't've",
        "yall": "y'all",
        "yall'll": "y'all'll",
        "y'allll": "y'all'll",
        "yall'd've": "y'all'd've",
        "y'alld've": "y'all'd've",
        "y'all'dve": "y'all'd've",
        "youd": "you'd",
        "youd've": "you'd've",
        "you'dve": "you'd've",
        "youll": "you'll",
        "youre": "you're",
        "youve": "you've",
    }

    NUMBER_MAP = {
        "none": "0",
        "zero": "0",
        "one": "1",
        "two": "2",
        "three": "3",
        "four": "4",
        "five": "5",
        "six": "6",
        "seven": "7",
        "eight": "8",
        "nine": "9",
        "ten": "10",
    }
    ARTICLES = ["a", "an", "the"]
    PERIOD_STRIP = re.compile(r"(?!<=\d)(\.)(?!\d)")
    COMMA_STRIP = re.compile(r"(?<=\d)(\,)+(?=\d)")
    PUNCTUATIONS = [
        ";",
        r"/",
        "[",
        "]",
        '"',
        "{",
        "}",
        "(",
        ")",
        "=",
        "+",
        "\\",
        "_",
        "-",
        ">",
        "<",
        "@",
        "`",
        ",",
        "?",
        "!",
    ]

    def __init__(self, *args, **kwargs):
        pass

    def word_tokenize(self, word):
        word = word.lower()
        word = word.replace(",", "").replace("?", "").replace("'s", " 's")
        return word.strip()

    def process_punctuation(self, in_text):
        out_text = in_text
        for p in self.PUNCTUATIONS:
            if (p + " " in in_text or " " + p in in_text) or (
                re.search(self.COMMA_STRIP, in_text) is not None
            ):
                out_text = out_text.replace(p, "")
            else:
                out_text = out_text.replace(p, " ")
        out_text = self.PERIOD_STRIP.sub("", out_text, re.UNICODE)
        return out_text

    def process_digit_article(self, in_text):
        out_text = []
        temp_text = in_text.lower().split()
        for word in temp_text:
            word = self.NUMBER_MAP.setdefault(word, word)
            if word not in self.ARTICLES:
                out_text.append(word)
            else:
                pass
        for word_id, word in enumerate(out_text):
            if word in self.CONTRACTIONS:
                out_text[word_id] = self.CONTRACTIONS[word]
        out_text = " ".join(out_text)
        return out_text

    def __call__(self, item):
        item = self.word_tokenize(item)
        item = item.replace("\n", " ").replace("\t", " ").strip()
        item = self.process_punctuation(item)
        item = self.process_digit_article(item)
        return item


