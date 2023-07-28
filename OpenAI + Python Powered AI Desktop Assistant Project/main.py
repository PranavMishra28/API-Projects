# Importing required libraries
import speech_recognition as sr
import os
import webbrowser
import openai
import datetime
import random
import numpy as np
import pyttsx3
import requests
from config import apikey  # Import the OpenAI API key from a separate configuration file

# Global variable to store the conversation history with the AI
chatStr = ""

# Function to chat with the AI using OpenAI's GPT-3 model
def chat(query):
    global chatStr
    print(chatStr)
    openai.api_key = apikey
    chatStr += f"Pranav: {query}\n Chacha Choudhary: "
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=chatStr,
        temperature=0.7,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    say(response["choices"][0]["text"])
    chatStr += f"{response['choices'][0]['text']}\n"
    return response["choices"][0]["text"]

# Function to use the AI to respond to a given prompt
def ai(prompt):
    openai.api_key = apikey
    text = f"OpenAI response for Prompt: {prompt} \n *************************\n\n"

    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        temperature=0.7,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    text += response["choices"][0]["text"]
    if not os.path.exists("Openai"):
        os.mkdir("Openai")

    with open(f"Openai/{''.join(prompt.split('intelligence')[1:]).strip()}.txt", "w") as f:
        f.write(text)

# Function to convert text to speech and play it
def say(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

# Function to send an email using Gmail SMTP
def send_email(recipient, subject, body):
    import smtplib
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart

    # Replace these variables with your email credentials
    sender_email = 'mishrapranav82@gmail.com'
    sender_password = '123456789'

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, recipient, msg.as_string())
        print("Email sent successfully!")
        return True
    except Exception as e:
        print("Failed to send email:", str(e))
        return False
    
# Function to listen to user's voice command using the microphone
def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.pause_threshold = 1
        audio = r.listen(source)
        try:
            query = r.recognize_google(audio, language="en-in")
            print(f"User said: {query}")
            return query
        except sr.UnknownValueError:
            print("Sorry, I didn't understand what you said.")
            return ""
        except sr.RequestError:
            print("Sorry, I am having trouble accessing the Google API. Please check your internet connection.")
            return ""

# Main part of the script
if __name__ == '__main__':
    print('')
    print("Chacha Choudhary - Your personal AI Desktop Assistant")
    say("Greetings! I am Chacha Choudhary, your personal AI Desktop Assistant. I can do a lot of stuff, just ask away!")
    while True:
        print("Listening...")
        query = takeCommand()
        sites = [["youtube", "https://www.youtube.com"], ["wikipedia", "https://www.wikipedia.org"], ["google", "https://www.google.com"]]
        for site in sites:
            if f"Open {site[0]}".lower() in query.lower():
                say(f"Opening {site[0]}")
                webbrowser.open(site[1])
            elif "play music" in query:
                webbrowser.open("https://www.youtube.com/watch?v=1XzY2ij_vL4")
            elif "the time" in query:
                time = datetime.datetime.now().strftime("%H:%M:%S")
                print("The time is: ", time)
                say(f"The time is {time}")
            elif "open zoom" in query.lower():
                zoom_path = r'"C:\Program Files (x86)\Zoom\bin\Zoom.exe"'
                os.system(zoom_path)
            elif "Using AI".lower() in query.lower():
                ai(prompt=query)
            elif "Jarvis Quit".lower() in query.lower():
                exit()
            elif "Reset chat".lower() in query.lower():
                chatStr = ""
            elif "send email" in query.lower():
                say("Sure, please provide the recipient's email address.")
                recipient_email = takeCommand()
                say("Please provide the subject of the email.")
                email_subject = takeCommand()
                say("What would you like to write in the email?")
                email_body = takeCommand()
                if send_email(recipient_email, email_subject, email_body):
                    say("Email sent successfully!")
                else:
                    say("Failed to send the email. Please check your email credentials.")
            else:
                print("Quitting")
                chat(query)
