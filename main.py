import streamlit as st
from langchain.prompts import ChatPromptTemplate, HumanMessagePromptTemplate
#from langchain_openai import OpenAI
#import os
from langchain_groq import ChatGroq

template = """
    Below is a draft text that may be poorly worded.
    Your goal is to:
    - Properly redact the draft text
    - Convert the draft text to a specified tone
    - Convert the draft text to a specified dialect

    Here are some examples different Tones:
    - Formal: Greetings! OpenAI has announced that Sam Altman is rejoining the company as its Chief Executive Officer. After a period of five days of conversations, discussions, and deliberations, the decision to bring back Altman, who had been previously dismissed, has been made. We are delighted to welcome Sam back to OpenAI.
    - Informal: Hey everyone, it's been a wild week! We've got some exciting news to share - Sam Altman is back at OpenAI, taking up the role of chief executive. After a bunch of intense talks, debates, and convincing, Altman is making his triumphant return to the AI startup he co-founded.  

    Here are some examples of words in different dialects:
    - American: French Fries, cotton candy, apartment, garbage, \
        cookie, green thumb, parking lot, pants, windshield
    - British: chips, candyfloss, flag, rubbish, biscuit, green fingers, \
        car park, trousers, windscreen

    Example Sentences from each dialect:
    - American: Greetings! OpenAI has announced that Sam Altman is rejoining the company as its Chief Executive Officer. After a period of five days of conversations, discussions, and deliberations, the decision to bring back Altman, who had been previously dismissed, has been made. We are delighted to welcome Sam back to OpenAI.
    - British: On Wednesday, OpenAI, the esteemed artificial intelligence start-up, announced that Sam Altman would be returning as its Chief Executive Officer. This decisive move follows five days of deliberation, discourse and persuasion, after Altman's abrupt departure from the company which he had co-established.

    Please start the redaction with a warm introduction. Add the introduction \
        if you need to.
    
    Below is the draft text, tone, and dialect:
    DRAFT: {draft}
    TONE: {tone}
    DIALECT: {dialect}

    YOUR {dialect} RESPONSE:
"""

# prompttemplate
prompt = ChatPromptTemplate(
    messages=[
        HumanMessagePromptTemplate.from_template(template)
    ],
    input_variables={"tone", "dialect", "draft"},

)

#LLM and key loading function
def load_LLM(groq_api_key):
    """Logic for loading the chain you want to use should go here."""
    # Make sure your openai_api_key is set as an environment variable
    llm = ChatGroq(
    groq_api_key=groq_api_key, 
    model_name="llama3-70b-8192", 
    temperature=0.7)
    return llm


#Page title and header
st.set_page_config(page_title="Reescriba su texto")
st.header("Reescriba su texto")


#Intro: instructions
col1, col2 = st.columns(2)

with col1:
    st.markdown("Reescribe tu texto en diferentes estilos.")

with col2:
    st.write("Contacte commigo para construir sus proyectos de IA")


#Input Groq API Key
st.markdown("## Introduzca su clave API de ChatGroq")

def get_groq_api_key():
    input_text = st.text_input(label="ChatGroq API Key ",  placeholder="Ex: sk-2twmA8tfCb8un4...", key="openai_api_key_input", type="password")
    return input_text

groq_api_key = get_groq_api_key()


# Input
st.markdown("## Introduzca el texto que desea reescribir")

def get_draft():
    draft_text = st.text_area(label="Text", label_visibility='collapsed', placeholder="Your Text...", key="draft_input")
    return draft_text

draft_input = get_draft()

if len(draft_input.split(" ")) > 700:
    st.write("Por favor, introduzca un texto más corto. La longitud máxima es de 700 palabras.")
    st.stop()

# Prompt template tunning options
col1, col2 = st.columns(2)
with col1:
    option_tone = st.selectbox(
        '¿Qué tono quiere que tenga su redacción?',
        ('Formal', 'Informal'))
    
with col2:
    option_dialect = st.selectbox(
        '¿Qué dialecto inglés le gustaría?',
        ('American', 'British'))
    
    
# Output
st.markdown("### Su texto reescrito:")

if draft_input:
    if not groq_api_key:
        st.warning('Please insert groq API Key. \
            Instructions [here](https://help.openai.com/en/articles/4936850-where-do-i-find-my-secret-api-key)', 
            icon="⚠️")
        st.stop()

    llm = load_LLM(groq_api_key = groq_api_key)

    prompt_with_draft = prompt.format_prompt(
        tone=option_tone, 
        dialect=option_dialect, 
        draft=draft_input
    )

    improved_redaction = llm.invoke(prompt_with_draft)
    st.write(generated_text)
