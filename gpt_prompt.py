from openai import OpenAI
import pandas as pd
import time
from datetime import datetime

client = OpenAI()

qb = pd.read_csv("testset_questions_only.csv")
qb_list = qb['question'].to_list()
test_question = qb_list[1]

def API_call(client, prompt):
    try:
        completion = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a helpful assistant. Please provide your answer in Cantonese"},
                {
                    "role": "user",
                    "content": f"{prompt}"
                }
            ],
            max_tokens = 500,
            temperature = 0.7
        )
        return completion.choices[0].message.content
    except Exception as e:
        print(f"Error processing prompt: {prompt[:50]}...")
        print(f"Error: {str(e)}")
        raise

qa = qb.copy()
answers = []
total = len(qb_list)

for i, question in enumerate(qb_list):
    try:
        answer = API_call(client,question)
        answers.append(answer)
        print(f"Process {i+1}/{total} questions")
        time.sleep(0.5)
    except Exception as e:
        answers.append(f"Error: {str(e)}")
        print(f"Failed to process question {i+1}")

qa["Answers"] = answers

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
qa.to_csv(f"OpenAI_qa_{timestamp}.csv", index=False)