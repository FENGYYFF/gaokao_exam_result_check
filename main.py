import time
from getLoginToken import checkExamResult

stu_data = [{"id": "030120101936", "pwd": "Xh13579."},
            {"id": "030619210466", "pwd": "Yyqx112825@"},
            {"id": "030122212033", "pwd": "Xh13579."},
            {"id": "030122210361", "pwd": "Xh13579."},
            {"id": "030122212327", "pwd": "Xh13579."},
            {"id": "030122212190", "pwd": "Xh13579."},
            {"id": "030122210540", "pwd": "Xh13579."}]


def main():
    # 运行代码
    for stu in stu_data:
        checkExamResult(stu)


if __name__ == '__main__':
    print("登录中......")
    time_a = time.time()
    main()
    timeEnd = (time.time() - time_a).__round__(2)
    print(f'''查询耗时：{timeEnd}秒''')
