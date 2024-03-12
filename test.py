from title_maker_pro.word_generator import WordGenerator
import torch

word_generator = WordGenerator(
  device="cuda:0" if torch.cuda.is_available() else "cpu",
  forward_model_path="./forward-dictionary-model-v1",
  inverse_model_path="./inverse-dictionary-model-v1",
  blacklist_path="blacklist.pickle",
  quantize=False,
)

# a word from scratch:
print("============== Word from scratch ==============")
print(word_generator.generate_word())

# definition for a word you make up
print("============== Definition for a word ==============")
print(word_generator.generate_definition("glooberyblipboop", do_sample=False)) 

# new word made up from a definition
print("============== New word from definition ==============")
gen_word = word_generator.generate_word_from_definition("a word that does not exist", do_sample=False)
print(gen_word)
# It may also be a good idea to check if the word already exists.
print("Word exists: ", word_generator.probably_real_word(gen_word.word))


# Try again with sampling (this will take longer)
print("================ Sampling ================")
gen_word = word_generator.generate_word_from_definition("a word that does not exist", do_sample=True)
print(gen_word)
# It may also be a good idea to check if the word already exists.
print("Word exists: ", word_generator.probably_real_word(gen_word.word))


# Try again with a higher temperature (this will take longer)
print("================ Higher temperature ================")
gen_word = word_generator.generate_word_from_definition(
    "a word that does not exist", do_sample=True,
    generation_args=dict(top_k=200,
                        max_length=200,
                        do_sample=True,
                        num_return_sequences=5,
                        temperature=0.7))
print(gen_word)
# It may also be a good idea to check if the word already exists.
print("Word exists: ", word_generator.probably_real_word(gen_word.word))