from openai import OpenAI
from tqdm import tqdm
import argparse
import os
import time


def parse_args():
    parser = argparse.ArgumentParser(description="Train a language model with PEFT and LoRA.")
    parser.add_argument("--model_name", type=str, default="sql-lora", help="Directory to save the trained model")
    parser.add_argument("--jsol_output_name", type=str, default="model1.jsonl", help="Directory to save the trained model")
    parser.add_argument("--start_vllm", type=str, default="True", help="Directory to save the trained model")
    return parser.parse_args()

args = parse_args()
if args.start_vllm=="True":
    time.sleep(180)


# Modify OpenAI's API key and API base to use vLLM's API server.
openai_api_key = "sk-xxx"
openai_api_base = "http://localhost:8000/v1"
# openai_api_base='http://127.0.0.1:8000/v1'
client = OpenAI(
    api_key=openai_api_key,
    base_url=openai_api_base,
)
print("----------------------开始查看日志----------------------")

try:
    with open("nohup.out","r",encoding="utf8") as f:
        data=f.read()
        print(data)
except Exception as e:
    print(e)
    print("运行失败")

test_dir=os.path.join("/tcdata","round2_test_data.jsonl")
new_test_json_dir="round2_test_data_new.jsonl"
import pandas as pd
test_texts=pd.read_json(new_test_json_dir, lines=True)
pred_list=[]
try:
    for i in tqdm(test_texts.values):
        instruction = i[0]
        input_value = i[1]
        chat_response = client.chat.completions.create(
        model=args.model_name,
        messages = [
            {"role": "system", "content": f"{instruction}"},
            {"role": "user", "content": f"{input_value}"}
        ]
    )

        pred_list.append(chat_response.choices[0].message.content)

    import json
    data1=[]
    with open(test_dir, "r",encoding="utf8") as file: 
        idx = 0
        for line in file:
            data_line = json.loads(line)
            current_id = data_line["id"]
            questions = data_line["questions"]

            # 添加预测答案到问题列表中
            combined_questions = []
            for question in questions:
                combined_questions.append({'answer': pred_list[idx]})
                idx += 1

            # 添加到结果数据中
            data1.append({'id': current_id, 'questions': combined_questions})
    with open(args.jsol_output_name, 'w', encoding='utf-8') as f:
        for entry in data1:
            f.write(json.dumps(entry, ensure_ascii=False) + '\n')
except:
    pass