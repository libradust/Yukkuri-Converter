import re
import requests
from bs4 import BeautifulSoup

URL_PIANJIA = "https://www.ltool.net/chinese_simplified_and_traditional_characters_pinyin_to_katakana_converter_in_simplified_chinese.php"
URL_YUKKURI = "https://www.yukumo.net/#/"

def post_to_pianjia(contents):
    """发包给片假名转换网"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
        ' AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        }
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
            print(f"转换结果: {final_result.get_text(strip=True)}")
            return final_result.get_text(strip=True)

def deal_with_result(contents):
    """处理转换结果,删除空格和多余文本"""
    contents_no_space=contents.replace(" ","")  # 删除空格
    pattern=re.compile(r'\(.*?\)')  # 删除所有括号和括号里的内容
    completed_contents=pattern.sub('', contents_no_space)
    print(f"处理后的结果: {completed_contents}")


def main():
    contents=input("请输入要转换的文本：")
    result=post_to_pianjia(contents)
    deal_with_result(result)

if __name__ == "__main__":
    main()