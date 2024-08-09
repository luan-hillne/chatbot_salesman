from langchain.memory import ConversationBufferWindowMemory, ConversationBufferMemory
from langchain.chains import LLMChain
from langchain.schema import SystemMessage
from langchain.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder,
    AIMessagePromptTemplate
)
from config_app.enum import Variable
from langchain_community.callbacks import get_openai_callback
from utils.llm_manager import get_llm
from config_app.config import get_config
import re
config_app = get_config()
enum = Variable()
memory = ConversationBufferWindowMemory(k = config_app["parameter"]["search_number_messages"],return_messages=True)

def initialize_chat_conversation(human_input, response_elastic, session_id, llm):
    prompt = ChatPromptTemplate.from_messages(
    [
        SystemMessage(
            content=enum.SYSTEM_MESSAGE
        ),
        MessagesPlaceholder(
            variable_name=session_id
        ),
        HumanMessagePromptTemplate.from_template(
            enum.HUMAN_MESSAGE_TEMPLATE
        ),
        AIMessagePromptTemplate.from_template(
           enum.AI_MESSAGE_TEMPLATE
        ),
    ]
    )

    prompt.messages[0].content = prompt.messages[0].content.format(context=response_elastic)
    memory.memory_key = session_id
    total_tokens = ''
    try:
        
        chain = LLMChain(
            llm=llm,
            prompt=prompt,
            # verbose=True,
            memory=memory
        )
        with get_openai_callback() as cb:
            response = chain.predict(human_input=human_input)
            total_tokens = cb.total_tokens
            print('======total_tokens=====\n', cb.total_tokens)
    except Exception as e:
        chain = LLMChain(
            llm=get_llm(),
            prompt=prompt,
            # verbose=True,
            memory=memory
        )
        with get_openai_callback() as cb:
            response = chain.predict(human_input=human_input)
            total_tokens = cb.total_tokens
            print('======total_tokens=====\n', cb.total_tokens)

    return response, memory, total_tokens
