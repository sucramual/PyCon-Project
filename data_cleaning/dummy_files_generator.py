import pandas as pd

df = pd.read_csv("testset_questions_only.csv")

df = df.copy()

for i in range(len(df)):
    df.loc[i,"Answers"] = f"dummy_answers_{i}"

for i in range(1,4):
    df.to_csv(f"small_model_{i}_output.csv",index=False)