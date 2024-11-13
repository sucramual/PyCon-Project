import pandas as pd 

df = pd.read_csv("gpt4o_qa.csv")
df = df[["question","Answers"]]
df.to_csv("gp44o_qa.csv",index=False)