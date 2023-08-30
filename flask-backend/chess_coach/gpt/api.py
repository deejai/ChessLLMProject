import openai

def ask_gpt(prompt):
    model_engine = "gpt-3.5-turbo"
    conversation = [
        {"role": "user", "content": prompt}
    ]
    openai_response = openai.ChatCompletion.create(
        model=model_engine,
        messages=conversation
    )
    gpt_response = openai_response['choices'][0]['message']['content']

    return gpt_response
