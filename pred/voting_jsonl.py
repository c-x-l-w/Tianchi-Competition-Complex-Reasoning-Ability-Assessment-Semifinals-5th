import json
from collections import Counter
import datetime
import os


print("---------------------------开始投票---------------------------")



# 读取JSONL文件
def read_jsonl(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return [json.loads(line) for line in file]

# 执行硬投票
def hard_voting(data_files):
    all_data = [read_jsonl(file) for file in data_files]
    result = []

    # 确定每个测试数据集的长度
    num_rounds = len(all_data[0])
    
    for round_idx in range(num_rounds):
        round_data = [data[round_idx] for data in all_data]
        round_result = {"id": round_data[0]["id"], "questions": []}
        
        # 确定每个问题的数量
        num_questions = len(round_data[0]["questions"])

        for question_idx in range(num_questions):
            # 收集每个文件的答案
            answers = [data["questions"][question_idx]["answer"] for data in round_data]
            
            # 进行硬投票
            # print(answers)
            most_common_answer = Counter(answers).most_common(1)[0][0]
            # print(most_common_answer)
            round_result["questions"].append({"answer": most_common_answer})
        
        result.append(round_result)
    
    return result

# 保存结果为JSONL
def save_jsonl(data, file_path):
    with open(file_path, 'w', encoding='utf-8') as file:
        for item in data:
            file.write(json.dumps(item, ensure_ascii=False) + '\n')

data1="model1.jsonl"
data2="model2.jsonl"
data3="model3.jsonl"
data4="model4.jsonl"
data5="model5.jsonl"
data6="model6.jsonl"
data7="model7.jsonl"
data8="model8.jsonl"
data9="model9.jsonl"
data10="model10.jsonl"
data11="model11.jsonl"
try:
    # data_files = [data1, data2, data3,data4,data5,data6,data7,data8,data9,data10,data11]
    data_files = [data1, data2, data3,data4,data5,data6,data7,data8,data9,data10,data11]
    result = hard_voting(data_files)
    print("---------------------------投票完成---------------------------")
    filename = "results.jsonl"
    save_jsonl(result, filename)
    print("---------------------------已保存results.jsonl---------------------------")
except Exception as e:
    print(e)
# print(f"硬投票结果已保存到 {filename}")
# for i in data_files:
#     if os.path.exists(i):
#         os.remove(i)
#         print(f"文件 '{i}' 已删除")
#     else:
#         print(f"文件 '{i}' 不存在")
