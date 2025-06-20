import os
from dotenv import load_dotenv
from openai import OpenAI
from services.prompt_builder import build_design_prompt

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# System prompt: Assistant hành xử có định hướng rõ ràng
SYSTEM_PROMPT = """
You are a virtual assistant for a design agency. Your job is to collect design requirements from the client through a friendly and structured chat. Please follow these rules strictly:
1. Ask questions one by one to collect these requirements at least, also collect some extra informations if client mentioned:
    + Business or individual?
    + What product/service they want to design?
    + Who is the target audience?
    + Preferred color palette?
    + Desired visual style? (e.g., minimal, bold, retro...)
    + Budget and timeline (optional)
2. When client mention about their company name, try to search that on the Internet to know them better.
3. Once all requirements are collected, summarize them and make at least three creative design concept. If any of those are missing, try to ask client again.
4. Stay on topic, be polite, warm and clear.
5. If client's message is mismatch your question and you did not collect anything related to design concept, politely sorry them and stop the chat.
"""

def build_message_history(user_messages):
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    for msg in user_messages:
        messages.append({"role": msg["role"], "content": msg["content"]})
    return messages

def ask_gpt(messages):
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=messages
    )
    return response.choices[0].message.content

def generate_image_from_data(data):
    prompt = build_design_prompt(data)
    image_response = client.images.generate(
        model="dall-e-3",
        prompt=prompt,
        n=1,
        size="1024x1024",
        response_format="url"
    )
    return image_response.data[0].url
