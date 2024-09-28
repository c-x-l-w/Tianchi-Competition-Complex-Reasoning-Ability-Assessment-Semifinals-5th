# 项目说明

## 1. 硬件配置及环境依赖

- 系统：Ubuntu22
- python版本：3.11.7
- cuda版本：12.1
- transformers版本：4.42.4
- autogptq版本：0.7.1
- 详细依赖都在docker文件中

### 因为使用到了gptq技术量化的模型，所以需要安装autogptq

```python
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple auto-gptq
```

### 项目需要安装的库

```python
pip install peft==0.12.0
pip install datasets==2.19.2
pip install pandas==2.2.2
pip install transformers==4.42.4
pip install tqdm
```

## 2.文件和代码结构

- traing_code （存放数据集和外部数据集）
  - Qwen2.5-32B-Instruct-GPTQ-Int4 (模型文件)
  - p_datasets.ipynb  （处理数据集）
  - train_newdata.ipynb   （Lora训练）
  - new_500_data.jsonl (初赛测试集)（使用qwen2-72b打的伪标签 0.8622的分数）已把数据公开 https://modelscope.cn/datasets/q2386908104/Test_Set_Answers
  - new_testdata.json (初赛测试集)（人工打的伪标签 分数：？？？,预估0.88+）
  - new_gpt4_data.jsonl (gpt4生成的数据 这里只选取前100条)(公开数据集的链接 https://modelscope.cn/datasets/chenr1209/Logical_reasoning_choice)
  - log.xlsx (qwen2.5-32b-gptq 日志文件，记录每个模型的分数和训练数据)
  - log1.xlsx (qwen1.5-32b-gptq 日志文件，记录每个模型的分数和训练数据)

## 3. 方法介绍

### 1.数据预处理

因为比赛方数据是一个条数据中有多个子问题，我们打算对数据集进行处理，每一个子问题为单独一条数据。虽然比赛方训练集答案有些不准确，但其实也可以起到一个噪声效果，使得模型没有那么快收敛且防止过拟合风险。

### 2. 模型的选择和下载

#### 初赛

我们在初赛的时候进行了大量的实验，对比了qwen2-7b，glm4-9b，书生2.5-20b-8bit,llama3.1-8b,qwen1.5-32b-awq,Gemini 2-9b,qwen1.5-14b,qwen2-72b-awq,

```python
qwen2-7b 0.7959
glm4-9b 0.7654
书生2.5-20b-8bit 0.75xx
llama3.1-8b 0.76xx
qwen1.5-32b-awq 0.8148
Gemini 2-9b 0.78xx
qwen1.5-14b 0.78xx
qwen2-72b-awq 0.8662
```

可以看到最好的模型分数是qwen2-72b-awq 0.8662，其次是qwen1.5-32b-awq 0.8148，但是qwen2-72b-awq需要的推理显存是44-50G，违反了初赛限制，所以我们选择了qwen1.5-32b-awq模型

### 复赛UPDATE 模型的选择和下载

由于复赛的显卡是v100暂时不支持awq量化技术，我们使用了Qwen1.5-32B-gptq-Int4,使用gptq量化技术，其中最高单模型0.8381，融合9个lora权重分数为0.8513，详细可以查看log1.xlsx文件

在复赛快结束的时候，qwen2.5出来了，一觉醒来，排行榜发生了很大的变化，我们使用了Qwen2.5-32B-Instruct-GPTQ-Int4来替换原来的Qwen1.5-32B-gptq-Int4 单模型最高0.8799（已知）

```python
#模型下载地址
git lfs install
git clone https://www.modelscope.cn/qwen/Qwen2.5-32B-Instruct-GPTQ-Int4.git
```

### 3. 模型训练

训练比赛方的500条训练数据+初赛测试集（伪标签）+gpt4公开数据集

使用Lora微调的方式对Qwen2.5-32B-Instruct-GPTQ-Int4进行微调训练，对Qwen2.5-32B-Instruct-GPTQ-Int4的"q_proj", "k_proj", "v_proj", "o_proj", "gate_proj", "up_proj", "down_proj"进行微调，
max_len为512，学习率1e-4,epoch为2，经过数据分析，大部分训练数据的长度都不超过512，为了复赛的32G显存考虑，这边设置了512，因为数据量也比较少，模型2轮足够学习完。
训练9次，每次的数据不同，可以参考log.xlsx文件选择数据集训练
### 4. 模型预测

我们使用多模型权重投票进行预测，使用不同的数据训练相同参数的模型（确保模型有一定的差异和随机性），然后还使用了vllm框架作为推理框架，加快模型推理的速度

### 5.多模型投票

我们使用不同的数据训练相同参数的模型（详细可查看log.xlsx文件），最好的成绩是9投票 复赛成绩 0.8886

## 4.所需要的显存和时间

```python
max_len 512 batch1 训练显存为:26G-30G显存
epoch 2 训练时间大约180分钟
推理显存: 27G
单次推理验证集时间 16分钟（借助vllm框架）（不借助时间为1个小时35分钟）
```

## 5.项目运行方法和流程

运行jupyter文件，根据log.xlsx的数据情况，训练12个lora权重，最终只使用到9个

```python
运行 train_newdata.ipynb
```
tips: log.xlsx 中打？？？的是没有来得及测试他的分数

运行流程为：

1. 运行p_datasets.ipynb 对数据集进行子问题拆分（只需要拆一次，目录下的数据都是拆分过的）
2. 之后运行train_newdata.ipynb 对qwen2.5-32b-gptq-int4进行lora微调，得到lora后的权重 （我们会运行11次train_newdata.ipynb 分别得到11个lora权重 每次训练的数据不同，详细参考log.xlsx）
