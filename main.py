import requests
from bs4 import BeautifulSoup

URL_PIANJIA = "https://www.ltool.net/chinese_simplified_and_traditional_characters_pinyin_to_katakana_converter_in_simplified_chinese.php"
URL_YUKKURI = "https://www.yukumo.net/#/"

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    }

data={
    "contents": "哈哈哈哈",
}

# 发包
response=requests.post(URL_PIANJIA, headers=headers, data=data)
bs=BeautifulSoup(response.text, "html.parser")

# 检查是否发送成功
textarea=bs.find("textarea")
if textarea.has_attr('name') and textarea['name'] == 'contents':
    print(f"成功发送\"{textarea.get_text(strip=True)}\"到片假名转换器")
    
# 获取结果
result=bs.find('div',class_="resultleft")
if result:
    final_result=result.find('div',class_="finalresult")
    if final_result:
        print(f"转换结果: {final_result.get_text(strip=True)}")