from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
from langchain.llms import HuggingFacePipeline
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_community.llms import HuggingFacePipeline


def load_local_model(model_name="TinyLlama/TinyLlama-1.1B-Chat-v0.3"):
    print(f"Loading model: {model_name}")
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        device_map="auto",
        torch_dtype="auto"
    )

    generate_pipe = pipeline(
        "text-generation",
        model=model,
        tokenizer=tokenizer,
        max_new_tokens=1000,
        temperature=0.7,
        top_p=0.9,
        do_sample=True,
        repetition_penalty=1.1
    )

    return HuggingFacePipeline(pipeline=generate_pipe)


def create_prompt():
    template = """
You are a professional public speaker. Write a clear and compelling speech of around 900 words (~5 minutes long) on the following topic:

Topic: {topic}

Instructions:
- Begin with a captivating introduction
- Divide the speech into 3 to 5 logically flowing sections
- Maintain an engaging and educational tone
- End with a memorable conclusion or reflection
- Use simple language and avoid overly technical jargon

Only return the speech.

Speech:
"""
    return PromptTemplate(template=template, input_variables=["topic"])


def create_speech_chain(llm):
    prompt = create_prompt()
    return LLMChain(llm=llm, prompt=prompt)


def generate_speech(topic: str):
    llm = load_local_model()
    chain = create_speech_chain(llm)
    speech = chain.run(topic=topic)
    return speech


if __name__ == "__main__":
    # Hardcoded topic
    topic = "The importance of digital literacy in the modern world"
    print(f"\nGenerating speech on topic: {topic}\n")
    output = generate_speech(topic)
    print(output)
