python p_data.py
nohup python -m vllm.entrypoints.openai.api_server \
    --model Qwen2.5-32B-Instruct-GPTQ-Int4/ \
    --served-model-name qwen \
    --max-model-len=2800 \
    --enable-lora \
    --enforce-eager \
    --lora-modules sql-lora=checkpoint1-6328 sql-lora1=checkpoint2-6328 sql-lora2=checkpoint3-5062 sql-lora3=checkpoint4-3672 sql-lora4=checkpoint5-6328 sql-lora5=checkpoint6-6328 sql-lora6=checkpoint7-6328 sql-lora7=checkpoint8-6328 sql-lora8=checkpoint9-5062 sql-lora9=checkpoint10-5062 sql-lora10=checkpoint4-15498 2>&1 &
    
python vllm_api.py --model_name sql-lora --jsol_output_name model1.jsonl --start_vllm True
python vllm_api.py --model_name sql-lora1 --jsol_output_name model2.jsonl --start_vllm False
python vllm_api.py --model_name sql-lora2 --jsol_output_name model3.jsonl --start_vllm False
python vllm_api.py --model_name sql-lora3 --jsol_output_name model4.jsonl --start_vllm False
python vllm_api.py --model_name sql-lora4 --jsol_output_name model5.jsonl --start_vllm False
python vllm_api.py --model_name sql-lora5 --jsol_output_name model6.jsonl --start_vllm False
python vllm_api.py --model_name sql-lora6 --jsol_output_name model7.jsonl --start_vllm False
python vllm_api.py --model_name sql-lora7 --jsol_output_name model8.jsonl --start_vllm False
python vllm_api.py --model_name sql-lora8 --jsol_output_name model9.jsonl --start_vllm False
python vllm_api.py --model_name sql-lora9 --jsol_output_name model10.jsonl --start_vllm False
python vllm_api.py --model_name sql-lora10 --jsol_output_name model11.jsonl --start_vllm False

python voting_jsonl.py 
# python log.py