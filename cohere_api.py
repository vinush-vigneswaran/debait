import cohere
from cohere.classify import Example

def request(prompt,api_key) -> str:
    '''
    Connects to cohere API and returns AI response given a prompt text.
    '''
    num_tries = 0
    out = ""
    while num_tries < 2:
        try:
            co = cohere.Client(api_key)
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
            out = response.generations[0].text
            num_tries = 3
        except Exception as e:
            out = "connection timed out!"
            print("ERROR GENERATE: " + str(type(e)))
            num_tries += 1
    return out

def classify(input, api_key):
    '''
    Connects to cohere API and returns fine-tuned model classification
    '''
    max = 0
    try:
        co = cohere.Client(api_key)
        response = co.classify(
            model='9e2e2d1c-2c28-466c-8302-9c69dad99124-ft',
            inputs=[input])

        confidence = response.classifications[0].confidence
        for data in confidence:
            if data.confidence > max:
                max = data.confidence
                best_label = data.label
    except Exception as e:
        out = "ERROR CLASSIFY: " + str(type(e))
        print(out)
        best_label = "connection timed out!"

    return best_label

# out = classify("high ideals are all well and good, but not when they come at the expense of the present. Our world is marred by war, famine, and poverty; billions of people are struggling simply to live from day to day. Our dreams of exploring space are a luxury they cannot afford!")
# print(out)