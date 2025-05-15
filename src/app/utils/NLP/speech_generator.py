import re

import torch
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain_community.llms import HuggingFacePipeline
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline, StoppingCriteria, StoppingCriteriaList

from Ross_git.logs.log_manager import setup_logger
from Ross_git.src.app.config.app_config import get_section

# Initialize logging using the log manager
logger = setup_logger()

# Load configurations
logger.info("Loading configurations...")
model_config = get_section("model")
speech_config = get_section("speech")

# Cast types (configparser loads values as strings)
model_name = model_config.get("name", "TinyLlama/TinyLlama-1.1B-Chat-v0.3")
max_new_tokens = int(model_config.get("max_new_tokens", 1024))
temperature = float(model_config.get("temperature", 0.7))
stop_phrase = model_config.get("stop_phrase", "END OF SPEECH")

word_count = int(speech_config.get("word_count", 900))
retries = int(speech_config.get("retries", 3))

logger.info(f"Model: {model_name}, max_new_tokens: {max_new_tokens}, temperature: {temperature}")
logger.info(f"Speech target word count: {word_count}, retries: {retries}, stop_phrase: '{stop_phrase}'")


class EndOfSpeechCriteria(StoppingCriteria):
    def __init__(self, tokenizer, stop_phrase):
        self.tokenizer = tokenizer
        self.stop_phrase = stop_phrase
        self.stop_ids = tokenizer.encode(stop_phrase, add_special_tokens=False)

    def __call__(self, input_ids, scores, **kwargs):
        generated = self.tokenizer.decode(input_ids[0][-len(self.stop_ids):])
        return self.stop_phrase.lower() in generated.lower()


def load_local_model():
    logger.info(f"Loading model and tokenizer: {model_name}")
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        device_map="auto",
        torch_dtype=torch.float16
    )

    stopping_criteria = StoppingCriteriaList([
        EndOfSpeechCriteria(tokenizer, stop_phrase)
    ])

    generate_pipe = pipeline(
        "text-generation",
        model=model,
        tokenizer=tokenizer,
        max_new_tokens=max_new_tokens,
        stopping_criteria=stopping_criteria,
        temperature=temperature,
        do_sample=True,
    )

    logger.info("Model pipeline initialized.")
    return HuggingFacePipeline(pipeline=generate_pipe)


def clean_speech_output(text):
    match = re.search(
        r"START OF SPEECH:(.*?)END OF SPEECH",
        text,
        re.IGNORECASE | re.DOTALL
    )
    if match:
        return match.group(1).strip()
    logger.warning("Speech boundaries not found in output.")
    return None


def count_words(text):
    return len(re.findall(r'\b\w+\b', text))


def generate_speech(topic: str):
    logger.info(f"Generating initial speech for topic: '{topic}'")
    llm = load_local_model()

    prompt_template = f"""
You are a professional public speaker. Write a clear and compelling speech of around {word_count} words, paragraph per ascii line, on the following topic:

Topic: {{topic}}

Only return the speech that has {word_count} words approximately. When done, write {stop_phrase}

START OF SPEECH:
"""
    chain = LLMChain(llm=llm, prompt=PromptTemplate(
        template=prompt_template,
        input_variables=["topic"]
    ))

    for attempt in range(1, retries + 1):
        logger.info(f"Speech generation attempt {attempt}/{retries}")
        result = chain.run(topic=topic)
        speech_text = clean_speech_output(result)
        if speech_text:
            logger.info("Initial speech generation successful.")
            return speech_text
        else:
            logger.warning("Speech generation failed to extract valid content.")

    logger.error("All retries failed. Returning fallback response.")
    return "Try again or use a different model."


def continue_speech(topic, last_paragraph):
    logger.info("Attempting to continue speech...")
    llm = load_local_model()

    continuation_template = f"""
You are a professional public speaker. Write a clear and compelling speech of around {word_count} words, paragraph per ascii line, on the following topic:

Topic: {{topic}}

Only return the speech that has {word_count} words approximately. When done, write {stop_phrase}

START OF SPEECH:
{{last_paragraph}}
"""
    chain = LLMChain(llm=llm, prompt=PromptTemplate(
        template=continuation_template,
        input_variables=["topic", "last_paragraph"]
    ))

    result = chain.run(topic=topic, last_paragraph=last_paragraph)
    speech_text = clean_speech_output(result)
    if speech_text:
        logger.info("Continuation successful.")
    else:
        logger.warning("Failed to continue speech.")
    return speech_text if speech_text else ""


def generate_full_speech(topic):
    logger.info(f"Generating full speech for topic: '{topic}'")
    final_speech = generate_speech(topic)

    if final_speech == "Use a different model":
        return final_speech

    while count_words(final_speech) < word_count:
        current_word_count = count_words(final_speech)
        logger.info(f"Current word count: {current_word_count}/{word_count}")
        lines = final_speech.strip().splitlines()
        if not lines:
            logger.warning("Speech is empty or malformed.")
            break
        last_paragraph = lines[-1].strip()
        extension = continue_speech(topic, last_paragraph)
        if not extension:
            logger.warning("No extension received, stopping.")
            break
        extension_lines = extension.splitlines()
        if extension_lines and extension_lines[0].strip() == last_paragraph:
            extension_lines = extension_lines[1:]
        final_speech += "\n" + "\n".join(extension_lines)

    logger.info(f"Final word count: {count_words(final_speech)}")
    return final_speech


# if __name__ == "__main__":
#     topic = "The importance of digital literacy in the modern world"
#     full_output = generate_full_speech(topic)
#     logger.info(f"\nFinal Speech Output:\n{full_output}")
#     print(f"\nFinal Speech Output:\n{full_output}")
