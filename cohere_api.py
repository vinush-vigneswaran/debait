import cohere

with open('api_key.txt') as f:
    api_key = f.readlines()

def request(prompt) -> str:
    #TODO: Try catch exception for errors - when run in loop
    co = cohere.Client(api_key[0])
    response = co.generate(
        model='large',
        prompt=prompt,
        max_tokens=100,
        temperature=0.7,
        k=0,
        p=0.75,
        frequency_penalty=0,
        presence_penalty=0,
        stop_sequences=["--"],
        return_likelihoods='NONE')

    return response.generations[0].text