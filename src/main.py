# download html

import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs
import pandas as pd

def main():
    scrap_by_keyword('公主')

def scrap_by_keyword(keyword):
    moreLink = get_app_more_link(keyword)
    # print(moreLink)
    game_links = get_game_list(moreLink)
    df = pd.DataFrame()
    for game_link in game_links:
        game_detail = get_game_detail(game_link)
        print(game_detail)
        df = df.append(game_detail, ignore_index=True)
    df.to_excel('./files/{}.xlsx'.format(keyword))

def get_game_detail(detailLink):
    x = requests.get(detailLink, headers = {'Accept-Language': 'zh-CN,en-US;q=0.7,en;q=0.3'})
    soup = BeautifulSoup(x.text, 'html.parser')

    game_name = soup.select_one('h1.AHFaub > span').text # 游戏名
    tab1 = soup.select('div.ZVWMWc > div > span > a')
    company_name = tab1[0].text # 公司名
    cate_name = ''
    if len(tab1) == 2:
        cate_name = tab1[1].text # 分类名
    
    try:
        star_num = soup.select_one('div.BHMmbe').text # 评分
    except:
        star_num = ''
    
    try:
        people_num = soup.select_one('span.AYi5wd').text # 评分人数
    except:
        people_num = ''
    
    other_infos = soup.select('div.hAyfc > span.htlgb > div.IQ1z0d > span')
    try:
        update_date = other_infos[0].text # 更新日期: '2020年9月9日'
    except:
        update_date = ''

    try:
        size = other_infos[1].text # 大小: 43M
    except:
        size = ''
    
    try:
        install_num = other_infos[2].text # 安装次数: 10,000,000+
    except:
        install_num = ''
    
    try:
        current_version = other_infos[3].text # 当前版本：2.4.2
    except:
        current_version = ''
    
    try:
        android_requirement = other_infos[4].text # Android 系统版本要求：4.1 及更高版本
    except:
        android_requirement = ''
    
    try:
        contact = other_infos[9].select_one('div > a.euBY6b').text
    except:
        contact = ''

    qs = urlparse(detailLink).query
    package_id = parse_qs(qs)['id'][0]
    return {
        '游戏名称': game_name,
        '公司名称': company_name,
        '分类': cate_name,
        '评分': star_num,
        '评分人数': people_num,
        '安装次数': install_num,
        '更新日期': update_date,
        '大小': size,
        '当前版本': current_version,
        '包名': package_id,
        '联系方式': contact,
    }
    

def get_game_list(moreLink):
    x = requests.get(moreLink, headers = {'Accept-Language': 'zh-CN,en-US;q=0.7,en;q=0.3'})
    soup = BeautifulSoup(x.text, 'html.parser')
    game_blocks = soup.select('a.JC71ub')
    prefix = 'https://play.google.com'
    result = []
    for blk in game_blocks:
        result.append(prefix + blk['href'])
    return result

def get_app_more_link(keyword):
    x = requests.get('https://play.google.com/store/search', params = {'q': keyword}, headers = {'Accept-Language': 'zh-CN,en-US;q=0.7,en;q=0.3'})
    soup = BeautifulSoup(x.text, 'html.parser')
    a = soup.select_one('div.W9yFB > a[href]')
    moreLink = 'https://play.google.com' + a['href']
    return moreLink

if __name__ == "__main__":
    main()
