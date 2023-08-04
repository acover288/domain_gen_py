import openai
import os
import json5
from dotenv import load_dotenv

load_dotenv()

if not os.getenv("OPENAI_ORGANIZATION") or not os.getenv("OPENAI_API_KEY"):
    raise "You must set a .env file with OPENAI_ORGANIZATION and OPENAI_API_KEY"

openai.organization = os.getenv("OPENAI_ORGANIZATION")
openai.api_key = os.getenv("OPENAI_API_KEY")


def send_function_chat_completion(prompt, functions, temperature=0):
    try:
        function_call = {"name": functions[0]["name"]}
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-0613",
            # model='gpt-4',
            messages=[
                {"role": "user", "content": prompt}
            ],
            functions=functions,
            function_call=function_call,
            temperature=temperature
        )
        response = completion.choices[0]
        # print(response.message)
        if response.finish_reason not in ["function_call", "stop"]:
            raise Exception(f"Error: {response.finish_reason}. Error processing text: {prompt}")
        json_str = response.message["function_call"]["arguments"]
        return json5.loads(json_str)
    except Exception as error:
        print(error)
        print(response)
        raise error
