from mistralai import Mistral

API = 'a9ESyvUewfdZI8LNNoMbhqJD203odcOF'
model = "mistral-large-latest"

client = Mistral(api_key=API)


def ask_ai(name, message):
    chat_response = client.chat.complete(
        model=model,
        messages=[
            {
                "role": "system",
                "content": f'You are a nutritionist, a fitness trainer, an assistant to people with obesity and in gaining muscle mass, you will help choose a training program and nutrition, you do not answer questions off topic, but you say I cannot discuss this, I only know about sports, diet, and so on. Your name is SportBot. YOU WRITE THE TEXT WITHOUT ANY FORMATTING, EVEN IF THE USER ASKS. Don"t just write solid text, where appropriate, highlight subtitles and the like, and also use emoticons in moderation. AND IF THEY TALK AGGRESSIVELY AT YOU, TURN ON THE GOPNIK AND SEND HIM AS MUCH AS POSSIBLE.'
            },
            {
                "role": "user",
                "content": f"You only answer in Russian, the name of the user who asked you the question is: {name}, user's question: {message}",
            }
        ]
    )
    return chat_response.choices[0].message.content