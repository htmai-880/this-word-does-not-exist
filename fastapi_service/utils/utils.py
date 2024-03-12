from title_maker_pro.word_generator import WordGenerator
from title_maker_pro.datasets import GeneratedWord
from hyphen import Hyphenator
import torch
from ..models.word_definition import WordDefinition
from ..models.dataset import DatasetType
import logging


def boot():
    word_generator = WordGenerator(
        device="cuda:0" if torch.cuda.is_available() else "cpu",
        forward_model_path="./forward-dictionary-model-v1",
        inverse_model_path="./inverse-dictionary-model-v1",
        blacklist_path="blacklist.pickle",
        quantize=False,
    )
    hyphenator = Hyphenator("en_US")
    return word_generator, hyphenator

def warmup(word_generator: WordGenerator):
    logging.info(f"Warming up with word generation")
    gen_word = word_generator.generate_word()
    logging.info(f"Warmup word: {gen_word}")


def gen_word_to_word_definition(gen_word : GeneratedWord,
                                dataset: str,
                                generator: WordGenerator,
                                hyphenator: Hyphenator):
    return WordDefinition(
        word=gen_word.word,
        definition=gen_word.definition,
        pos=gen_word.pos,
        examples=[gen_word.example],
        syllables=hyphenator.syllables(gen_word.word),
        probablyExists=generator.probably_real_word(gen_word.word),
        dataset=DatasetType(name=dataset)
    )

