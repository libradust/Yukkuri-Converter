import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import quote

URL_PIANJIA = "https://www.ltool.net/chinese_simplified_and_traditional_characters_pinyin_to_katakana_converter_in_simplified_chinese.php"
URL_YUKKURI = "https://www.yukumo.net/"
headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
        ' AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        }

def post_to_pianjia(contents):
    """发包给片假名转换网"""
    
    data={"contents": contents,}

    # 发包
    response=requests.post(URL_PIANJIA, headers=headers, data=data)
    if response.status_code == 200:
        bs=BeautifulSoup(response.text, "html.parser")

    # 检查发送内容
    textarea=bs.find("textarea")
    if textarea.has_attr('name') and textarea['name'] == 'contents':
        print(f"成功发送\"{textarea.get_text(strip=True)}\"到片假名转换器")
    
    # 获取结果
    result=bs.find('div',class_="resultleft")
    if result:
        final_result=result.find('div',class_="finalresult")
        if final_result:
            # print(f"转换结果: {final_result.get_text(strip=True)}")
            return final_result.get_text(strip=True)

def deal_with_result(contents):
    """处理转换结果,删除空格和多余文本"""
    contents_no_space=contents.replace(" ","")  # 删除空格
    pattern=re.compile(r'\(.*?\)')  # 删除所有括号和括号里的内容
    completed_contents=pattern.sub('', contents_no_space)
    print(f"处理后的结果: {completed_contents}")
    return completed_contents

def transform_to_yukkuri(ready_content,voice_type,mp3_name):
    """转换为油库里并把音频下载到本地"""

    encoded_text = quote(ready_content)# 对文本进行URL编码

    url = f"{URL_YUKKURI}api/v2/aqtk1/koe.mp3?type={voice_type}&kanji={encoded_text}"
    response = requests.get(url,headers=headers)

    if response.status_code == 200:
        with open(f"{mp3_name}.mp3", "wb") as f:
            f.write(response.content)
        print(f"音频已保存为同文件夹下的-{mp3_name}.mp3")
    else:
        print(f"请求失败，状态码: {response.status_code}")
        print(response.text)


def main():
    contents=input("输入要转换的文本：")
    voice_type=input("输入声音类型,可用的有\n"
                     "dvd, f1, f2, imd1, jgr, m1, m2, r1\n"
                     "不填默认为f1：")
    if not voice_type:
        voice_type="f1"

    result=post_to_pianjia(contents)
    ready_content=deal_with_result(result)
    transform_to_yukkuri(ready_content,voice_type,contents)
    main()

if __name__ == "__main__":
    main()
