import openai

def check_apiKey(api_key) :
    openai.api_key = api_key

    # api key 맞는지 확인
    try :
        openai.Engine.list()
        return True
    except openai.error.AuthenticationError :
        return False