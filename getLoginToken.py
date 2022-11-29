import json
from http.cookiejar import CookieJar
from jsonpath import jsonpath
import requests
from getAES import getAES
from imgReg.ocr_image_ocr import image_reg

basic_headers = {
    "Host": "www.eeagd.edu.cn",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"
}


def checkExamResult(stu):
    kw = {"account": stu["id"],
          "password": getAES(stu["pwd"]),
          "accLogin": "false",
          "Connection": "keep-alive"
          }

    s = requests.Session()
    s.cookies = CookieJar()

    # 1. toLogin
    url_login = 'https://www.eeagd.edu.cn/zkselfec/login/login.jsp'
    r_login = s.get(url_login, headers=basic_headers)
    cookies = r_login.cookies.get_dict()

    # 2. get addcode
    url_loginAddCode = 'https://www.eeagd.edu.cn/zkselfec/login/login.addcode'
    r_url_loginAddCode = s.get(url_loginAddCode, headers=basic_headers, stream=True)
    if r_url_loginAddCode.status_code == 200:
        # 将内容写入图片
        open('./imgReg/easy_img/img_to_reg.jpg', 'wb').write(r_url_loginAddCode.content)
    addCode = image_reg()
    kw["addcode"] = addCode

    # 3. request to login
    url_loginDo = 'https://www.eeagd.edu.cn/zkselfec/login/login.do'
    logindo_response = s.post(url_loginDo, data=kw, headers=basic_headers, verify=False)

    if (logindo_response.text.__contains__("true")):
        # 4.request to main page
        url_main = 'https://www.eeagd.edu.cn/zkselfec/pages/main.jsp'
        main_response = s.get(url_main, headers=basic_headers)

        query_line = [{"page": 1, "rows": 20}, "", ""]
        # 5.查询笔试成绩
        url_queryKmcj = 'https://www.eeagd.edu.cn/zkselfec/gdbk/queryKmcj.jsmeb'
        response_queryKmcj = s.post(url_queryKmcj, json=query_line, headers=basic_headers)
        rsp_json_queryKmcj = json.loads(response_queryKmcj.text)
        if (jsonpath(rsp_json_queryKmcj, "$..total")[0] == "0"):
            bscj_result = f'''笔试成绩已通过|0| 已通过课程名称| 无'''
        else:
            lession_name = jsonpath(rsp_json_queryKmcj, "$..KMMC")
            lession_count = jsonpath(rsp_json_queryKmcj, "$..total")[0]
            bscj_result = f'''笔试成绩已通过|{lession_count}| 已通过课程名称| {lession_name}'''
        # 6.查询实践课成绩
        url_querySjkcj = 'https://www.eeagd.edu.cn/zkselfec/gdbk/querySjkcj.jsmeb'
        response_querySjkcj = s.post(url_querySjkcj, json=query_line, headers=basic_headers)
        rsp_json_querySjkcj = json.loads(response_querySjkcj.text)
        if (jsonpath(rsp_json_querySjkcj, "$..total")[0] == "0"):
            sjkcj_result = f'''实践课成绩已通过|0| 已通过课程名称| 无'''
        else:
            lession_name = jsonpath(rsp_json_querySjkcj, "$..KMMC")
            lession_count = jsonpath(rsp_json_querySjkcj, "$..total")[0]
            sjkcj_result = f'''实践课成绩已通过|{lession_count}| 已通过课程名称| {lession_name}'''

        print(f'''学生编号|{kw["account"]}| {bscj_result}| {sjkcj_result}''')
    else:
        print(f'''学生编号|{kw["account"]}| 密码错误''')
