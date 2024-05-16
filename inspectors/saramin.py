from urllib.parse import quote
from bs4 import BeautifulSoup as bs
from tqdm import tqdm
import urllib3
import requests

urllib3.disable_warnings()


# keyword = "스포츠"
# quote_keyword = quote(keyword)

def saramin_scrapper(quote_keyword, num):
    pbar = tqdm(range(1, num))
    saramin_jobs = []
    for i in pbar:
        url = f'https://www.saramin.co.kr/zf_user/search/recruit?searchword={quote_keyword}&recruitPage={i}'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
        }
        res = requests.get(url, headers=headers, verify=False)
        soup = bs(res.content, 'html.parser')

        box = soup.select_one("div#recruit_info_list>div.content")        
        rows = box.select('div.item_recruit')
        for row in rows:
            job_dict = {}
            content = row.select_one('div.area_job')
            company = row.select_one('div.area_corp strong.corp_name>a').get_text().strip()
            
            title = content.select_one('h2.job_tit span').get_text().strip()
            link =  'https://www.saramin.co.kr' + content.select_one('h2.job_tit a')['href']
            conditions = row.select('div.job_condition span')
            master = conditions[1].get_text()            
            grade = conditions[2].get_text()            
            location = conditions[0].get_text()

            job_dict['company'] = company
            job_dict['title'] = title
            job_dict['link'] = link
            job_dict['master'] = master
            job_dict['grade'] = grade    
            job_dict['location'] = location
            
            saramin_jobs.append(job_dict)
    pbar.close()
    return saramin_jobs
    


