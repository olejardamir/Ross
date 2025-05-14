from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline, StoppingCriteria, StoppingCriteriaList
from langchain_community.llms import HuggingFacePipeline
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import torch
import re


class EndOfSpeechCriteria(StoppingCriteria):
    def __init__(self, tokenizer, stop_phrase):
        self.tokenizer = tokenizer
        self.stop_phrase = stop_phrase
        self.stop_ids = tokenizer.encode(stop_phrase, add_special_tokens=False)

    def __call__(self, input_ids, scores, **kwargs):
        # Check last generated tokens
        generated = self.tokenizer.decode(input_ids[0][-len(self.stop_ids):])
        return self.stop_phrase.lower() in generated.lower()


def load_local_model(model_name="TinyLlama/TinyLlama-1.1B-Chat-v0.3"):
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        device_map="auto",
        torch_dtype=torch.float16
    )

    stop_phrase = "END OF SPEECH"
    stopping_criteria = StoppingCriteriaList([
        EndOfSpeechCriteria(tokenizer, stop_phrase)
    ])

    generate_pipe = pipeline(
        "text-generation",
        model=model,
        tokenizer=tokenizer,
        max_new_tokens=1024,
        stopping_criteria=stopping_criteria,
        temperature=0.7,
        do_sample=True,
    )

    return HuggingFacePipeline(pipeline=generate_pipe)


def generate_speech(topic: str):
    llm = load_local_model()
    prompt_template = """
You are a professional public speaker. Write a clear and compelling speech of around 900 words (~5 minutes long) on the following topic:

Topic: {topic}

Only return the speech that has 900 words approximately. When done, write END OF SPEECH

START OF SPEECH:
"""


    chain = LLMChain(llm=llm, prompt=PromptTemplate(
        template=prompt_template,
        input_variables=["topic"]
    ))

    result = chain.run(topic=topic)

    # Robust extraction using regex
    match = re.search(
        r"START OF SPEECH:(.*?)END OF SPEECH",
        result,
        re.IGNORECASE | re.DOTALL
    )

    if match:
        return match.group(1).strip()
    return f"Failed to generate speech. Full output:\n\n{result}"


if __name__ == "__main__":
    topic = "The importance of digital literacy in the modern world"
    output = generate_speech(topic)
    print(f"\nFinal Speech Output:\n{output}")