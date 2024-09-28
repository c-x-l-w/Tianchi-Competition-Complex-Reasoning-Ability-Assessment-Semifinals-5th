print("----------------------开始查看日志----------------------")

try:
    with open("nohup.out","r",encoding="utf8") as f:
        data=f.read()
        print(data)
except Exception as e:
    print(e)
    print("运行失败")