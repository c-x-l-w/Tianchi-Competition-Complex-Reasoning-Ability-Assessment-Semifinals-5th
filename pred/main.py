import subprocess
import time

def run_command(command):
    """运行给定的命令"""
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    if process.returncode != 0:
        print(f"Error executing command: {command}\n{stderr.decode()}")
    else:
        print(f"Command executed successfully: {command}\n{stdout.decode()}")

def find_and_kill_pt_main_thread():
    """查找并终止 pt_main_thread 进程"""
    try:
        # 使用 ps 命令查找包含 "pt_main_thread" 的进程
        ps_output = subprocess.check_output(["ps", "aux"])
        ps_output = ps_output.decode().strip().split('\n')

        pids = []
        for line in ps_output:
            if "pt_main_thread" in line:
                # 提取 PID
                pid = int(line.split()[1])
                pids.append(pid)

        for pid in pids:
            if pid:
                print(f"Terminating pt_main_thread with PID: {pid}")
                subprocess.run(["kill", "-9", str(pid)])  # 使用 SIGKILL 强制终止
            else:
                print(f"No pt_main_thread found")
    except subprocess.CalledProcessError:
        print("No matching pt_main_thread found.")

def main():
    print("开始启动vllm服务器")
    # 启动vllm服务
    vllm_command = (
        "python -m vllm.entrypoints.openai.api_server "
        "--model Qwen1.5-32B-Chat-GPTQ-Int4/ "
        "--served-model-name qwen --max-model-len=2048 "
        "--enable-lora "
        "--enforce-eager "
        "--lora-modules sql-lora=checkpoint-6328 "
        "sql-lora1=checkpoint-3876 "
        "sql-lora2=checkpoint-5498"
    )
    vllm_process = subprocess.Popen(vllm_command, shell=True)
    
    # 等待一段时间让vllm服务启动
    time.sleep(300)

    # 其他命令
    commands = [
        "python vllm_api.py --model_name sql-lora --jsol_output_name model1.jsonl",
        "python vllm_api.py --model_name sql-lora1 --jsol_output_name model2.jsonl",
        "python vllm_api.py --model_name sql-lora2 --jsol_output_name model3.jsonl",
        "python voting_jsonl.py",
    ]

    # 顺序执行其他命令
    for command in commands:
        run_command(command)

    # 终止vllm服务
    find_and_kill_pt_main_thread()

if __name__ == "__main__":
    main()