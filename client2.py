from google import genai
import keys

client = genai.Client(api_key="keys.api_key_gemini")
system_role = "You are a female virtual assistant named Sidney skilled in general tasks like Alexa and Google Cloud. You must respond to the following user query"
user_role = "tell me something about python programming language in about 50 words"
response = client.models.generate_content(model="gemini-2.0-flash",
        contents= system_role + user_role)
print(response.text)




# def aiProcess(command): # from client2.py
#     client = genai.Client(api_key=keys.api_key_gemini)
#     system_role = "You are a female virtual assistant named Sidney skilled in general tasks like Alexa and Google Cloud. You must respond to the following user query"
#     user_role = command
#     response = client.models.generate_content(model="gemini-2.0-flash",
#         contents= system_role + user_role)
#     return response.text