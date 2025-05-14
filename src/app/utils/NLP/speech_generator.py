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


def clean_speech_output(text):
    match = re.search(
        r"START OF SPEECH:(.*?)END OF SPEECH",
        text,
        re.IGNORECASE | re.DOTALL
    )
    if match:
        return match.group(1).strip()
    return None


def count_words(text):
    return len(re.findall(r'\b\w+\b', text))


def generate_speech(topic: str, retries=3):
    llm = load_local_model()
    prompt_template = """
You are a professional public speaker. Write a clear and compelling speech of around 900 words, paragraph per ascii line, on the following topic:

Topic: {topic}

Only return the speech that has 900 words approximately. When done, write END OF SPEECH

START OF SPEECH:
"""
    chain = LLMChain(llm=llm, prompt=PromptTemplate(
        template=prompt_template,
        input_variables=["topic"]
    ))

    for attempt in range(retries):
        result = chain.run(topic=topic)
        speech_text = clean_speech_output(result)
        if speech_text:
            return speech_text

    return "Use a different model"


def continue_speech(topic, last_paragraph):
    llm = load_local_model()
    continuation_template = """
You are a professional public speaker. Write a clear and compelling speech of around 900 words, paragraph per ascii line, on the following topic:

Topic: {topic}

Only return the speech that has 900 words approximately. When done, write END OF SPEECH

START OF SPEECH:
{last_paragraph}
"""
    chain = LLMChain(llm=llm, prompt=PromptTemplate(
        template=continuation_template,
        input_variables=["topic", "last_paragraph"]
    ))

    result = chain.run(topic=topic, last_paragraph=last_paragraph)
    speech_text = clean_speech_output(result)
    return speech_text if speech_text else ""


def generate_full_speech(topic):
    final_speech = generate_speech(topic)

    if final_speech == "Use a different model":
        return final_speech

    while count_words(final_speech) < 900:
        lines = final_speech.strip().splitlines()
        if not lines:
            break
        last_paragraph = lines[-1].strip()
        extension = continue_speech(topic, last_paragraph)
        if not extension:
            break
        # Avoid repeating last paragraph
        extension_lines = extension.splitlines()
        if extension_lines and extension_lines[0].strip() == last_paragraph:
            extension_lines = extension_lines[1:]
        final_speech += "\n" + "\n".join(extension_lines)

    return final_speech


if __name__ == "__main__":
    topic = "The importance of digital literacy in the modern world"
    full_output = generate_full_speech(topic)
    print(f"\nFinal Speech Output:\n{full_output}")
