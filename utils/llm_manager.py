import logging, time
from langchain_community.chat_models import ChatOpenAI
from config_app.config import get_config
from langchain_groq import ChatGroq
from openai import OpenAI
import openai
import requests
# Cấu hình logging
import logging
import os
from groq import Groq

config_app = get_config()

# Danh sách các API key
api_keys = config_app['parameter']['grog_api_keys']
# open_api_keys = config_app['parameter']['openai_api_keys']
# Chỉ số hiện tại của API key
current_key_index = 0
      
def get_llm():
    global current_key_index
    try:
        api_key = api_keys[current_key_index]
        if "gsk" in api_key:
            print('---- grog ----')
            print("key:", api_key)
            client = Groq(
            api_key=api_key,
            )

            response = client.chat.completions.create(
                messages=[
                    {
                        "role": "user",
                        "content": "Hello World",
                    }
                ],
                model="llama3-8b-8192",
            )
            if response:
                return ChatGroq(model=config_app['parameter']['grog_model_to_use'], api_key=api_key)
        else:
            print('----openai----')
            print("key:", api_key)
            client = OpenAI(api_key=api_key)
            response = client.chat.completions.create(
                        model="gpt-3.5-turbo-0125",
                        messages=[
                            {"role": "user","content": "Hello World"},
                        ]
                        )
            if response:
                return ChatOpenAI(model_name=config_app["parameter"]["gpt_model_to_use"], temperature=config_app["parameter"]["temperature"], openai_api_key=api_key)
    except Exception as e:
        logging.error(f"API returned an API Error: {e}")
        current_key_index = (current_key_index + 1) % len(api_keys)
        time.sleep(1)
        return get_llm()
    
def open_api_keys(api_keys):
    for api_key in api_keys:
        try:
            client = OpenAI(api_key=api_key)
            response = client.chat.completions.create(
                        model="gpt-3.5-turbo-0125",
                        messages=[
                            {"role": "user","content": "Hello World"},
                        ]
                        )
            if response:
                return api_key
        except openai.APIError as e:
            print(f"OpenAI API returned an API Error: {e}")
            
# print(get_llm())