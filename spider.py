import json
import re
import requests

'''
爬取页面
'''
def get_one_page(url):

    header={
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                     '(KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36'
    }

    response=requests.get(url=url,headers=header)

    return response.text

'''
页面解析函数
'''

def parse_one_page(html):
    pattern=re.compile('<dd>.*?board-index.*?>(.*?)</i>.*?data-src="(.*?)".*?name.*?a.*?>'
                       '(.*?)</a>.*?star.*?>(.*?)</p>.*?releasetime.*?>(.*?)</p>.*?integer.*?>'
                       '(.*?)</i>.*?fraction.*?>(.*?)</i>.*?</dd>',re.S)
    items=re.findall(pattern,html)
    for item in items:
        yield {
            'index':item[0],
            'image':item[1],
            'title':item[2].strip(),
            'actor':item[3].strip()[3:] if len(item[3])>3 else '',
            'time':item[4].strip()[5:] if len(item[4])>5 else '',
            'score':item[5].strip()+item[6].strip(),
        }
    # print(item)

'''
写入文件函数
'''
def write_to_file(content):
    with open('result.txt','a',encoding='utf-8') as f:
        print(type(json.dumps(content)))
        f.write(json.dumps(content,ensure_ascii=False)+'\n')

'''
主函数
'''
def main(offset):
    url='https://maoyan.com/board/4?offset={}'.format(offset)
    html=get_one_page(url=url)
    result=parse_one_page(html)
    # 打印爬取结果
    for item in result:
        print(item)
        write_to_file(item)

if __name__=='__main__':
    for i in range(0,10):
        main(offset=i*10)