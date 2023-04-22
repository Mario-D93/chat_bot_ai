import openai
from decouple import config

class ChatBot:
    def __init__(self):
        openai.api_key = config('OPENAI_API_KEY')

    def get_response(self, user_input):
        resp = openai.Completion.create(
            engine="text-davinci-003",
            prompt=user_input,
            max_tokens=3800,
            temperature=0.4
        ).choices[0].text

        return resp

