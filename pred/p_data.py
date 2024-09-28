from tqdm import tqdm
import json
import pandas as pd
import os
print("开始处理数据集")
test_dir=os.path.join("/tcdata","round2_test_data.jsonl")
new_test_dir="round2_test_data_new.jsonl"

def p_dataset(origin_path, new_path):
    messages = []
    with open(origin_path, "r") as file:
        for line in tqdm(file):
            data = json.loads(line)
            problem = data["problem"]
            for question in data['questions']:
                # print("题目:{}\n问题:\n{}\n选项:\n{}".format(problem,question['question'],'\n'.join(f"{'ABCDEFG'[i]}. {o}" for i, o in enumerate(question['options']))))
                prompt = {"instruction":"""你是一个逻辑推理专家，擅长解决逻辑推理问题。以下是一个逻辑推理的题目，形式为单项选择题。所有的问题都是（close-world assumption）闭世界假设，即未观测事实都为假。请逐步分析问题并在最后一行输出答案，最后一行的格式为:答案是：A""",
                          "input": "题目:{}\n问题:\n{}\n选项:\n{}".format(problem,question['question'],'\n'.join(f"{'ABCDEFG'[i]}. {o}" for i, o in enumerate(question['options']))),}
                                    
                messages.append(prompt)
    with open(new_path, "w", encoding="utf-8") as file:
        for message in messages:
            file.write(json.dumps(message, ensure_ascii=False) + "\n")
p_dataset(test_dir,new_test_dir)
