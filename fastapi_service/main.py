# Write hello world in FastAPI
from fastapi import FastAPI
import uvicorn
from .models.dataset import DatasetType
from .models.word_definition import WordDefinition
from .models.word_from_definition import WordFromDefinitionRequest, WordFromDefinitionResponse
from .models.define_word import DefineWordRequest, DefineWordResponse
from .models.generate_word import GenerateWordResponse
from .utils.utils import boot, warmup, gen_word_to_word_definition

word_generator, hyphenator = boot()
warmup(word_generator)
app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/define_word", response_model=DefineWordResponse,
          summary="Define a word, whether it exists or not.",
          description="""
          This endpoint will generate a definition for a word, whether it exists or not.
          The word is passed in the request, and the dataset is optional."""
        )
def define_word(request: DefineWordRequest):
    dataset = request.dataset.name
    # For now don't handle UD datasets
    temperature = request.temperature
    if temperature and temperature > 0:
        do_sample=True
        gen_word = word_generator.generate_word_from_definition(
            request.word, do_sample=do_sample, generation_args=dict(
                top_k=200, max_length=200, do_sample=do_sample,
                temperature=temperature,
                num_return_sequences=5))
    else:
        gen_word = word_generator.generate_definition(request.word, do_sample=request.do_sample)
    return DefineWordResponse(
        word=gen_word_to_word_definition(
            gen_word,
            dataset,
            word_generator,
            hyphenator
        )
    )


@app.post("/word_from_definition", response_model=WordFromDefinitionResponse,
          summary="Generate a word from a definition.",
          description="""
          This endpoint will generate a word from a definition. The definition is passed in the request.
          The dataset is optional (OED by default), and the temperature is optional. If the temperature is set, the word will be generated
          with sampling, and the temperature will be used. If the temperature is not set, the word will be generated
          without sampling.
          """)
def word_from_definition(request: WordFromDefinitionRequest):
    dataset = request.dataset.name
    do_sample = request.do_sample
    temperature = request.temperature
    if temperature and temperature > 0:
        do_sample=True
        gen_word = word_generator.generate_word_from_definition(
            request.definition, do_sample=do_sample, generation_args=dict(
                top_k=200, max_length=200, do_sample=do_sample,
                temperature=temperature,
                num_return_sequences=5))
    else:
        gen_word = word_generator.generate_word_from_definition(request.definition, do_sample=do_sample)
    return WordFromDefinitionResponse(
        word=gen_word_to_word_definition(
            gen_word,
            dataset=dataset,
            generator=word_generator,
            hyphenator=hyphenator
        )
    )

@app.get("/generate_word", response_model=GenerateWordResponse,
         summary="Generate a word.",
         description="""
         This endpoint will generate a word. The word is generated from scratch.
         """)
def generate_word():
    gen_word = word_generator.generate_word()
    return GenerateWordResponse(
        word=gen_word_to_word_definition(
            gen_word,
            dataset="OED",
            generator=word_generator,
            hyphenator=hyphenator
        )
    )

# Health check
@app.get("/health")
def health():
    return {"status": "ok"}

def main():
    uvicorn.run(
        app=app,
        host="127.0.0.1",
        port=8000,
        log_level="debug",
        reload=True
    )

if __name__ =="__main__":
    main()
