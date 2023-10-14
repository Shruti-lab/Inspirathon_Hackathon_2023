import asyncio
from django.http import HttpResponse
from django.shortcuts import render
import openai
from notesmaker.video_to_text import vidgentext
from notesmaker.pdfgen import generatepdf
openai.api_key = "OPENAI_API_KEY"
userMessage=""
user_input=" "
ai_response = ""

async def get_ai_response(prompt,model="gpt-3.5-turbo"):
    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=0, # this is the degree of randomness of the model's output
    )
    return response.choices[0].message["content"]


def index(requests):
    return render(requests,'index.html')


async def analyze(requests):
    global user_input
    global ai_response
    url=requests.GET.get('urllink','URL not found')
    print(url)
    # Get the AI response for the given URL.
    user_input = vidgentext(url)
    print(user_input)
    prompt = f"""List 7 import topics covered in the text below delimited with triple backticks. Then after little break explain in detailed manner the text below which is delimited with triple backticks in 50 words.
      Text:'''{user_input}''' """
    ai_response = await get_ai_response(prompt)
    print(ai_response)
    generatepdf(ai_response)
    #print(ai_response)
    #params = {'link':url,'sumarized_text':ai_response}
    #send thi url to model and return text
    return render(requests,'analyze.html')

def chatbot(requests):
    return render(requests,'chatbot.html')

async def getResponse(requests):
    global ai_response
    userMessage = requests.GET.get('userMessage')
    userprompt=f"""Your are friendly AI teacher who will read the given text delimited by triple backticks 
and respond to user's text delimited by triple backticks the questions,doubts, or text they ask or send according to the text you read. Also can respond to their greetings in friendly manner (eg hi,hello,goodmorning,goodevening,goodafternoon etc)
text:'''{ai_response}'''
user's text: {userMessage}"""
    chatResponse = str(await get_response(userprompt))
    return HttpResponse(chatResponse)


async def get_response(userprompt,model="gpt-3.5-turbo"):
    messages = [{"role": "user", "content": userprompt}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=0, # this is the degree of randomness of the model's output
    )
    return response.choices[0].message["content"]

    
