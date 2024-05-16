import requests
from bs4 import BeautifulSoup as bs
from tqdm import tqdm

import urllib3

urllib3.disable_warnings()



def jobkorea_scrapper(quote_keyword, pagenum):
    pbar = tqdm(range(1, pagenum))
    jobkorea_jobs = []
    for i in pbar:
        url = f'https://www.jobkorea.co.kr/Search/?stext={quote_keyword}&Page_No={i}'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
        }
        res = requests.get(url, headers=headers, verify=False)        
        soup = bs(res.content, 'html.parser')

        ul = soup.select_one('div.lists ul.clear') #box
        rows = ul.select('li.list-post') #li모두
        for row in rows:
            job_dict = {}
            content = row.select_one('a.title.dev_view')
            company = row.select_one('a.name.dev_view').get_text()    
            title = content.get_text().strip()
            link = 'https://www.jobkorea.co.kr' + content['href']
            master = row.select_one('p.option span.exp')
            if master is None:
                master = ''
            else:
                master = master.get_text()
            grade = row.select_one('p.option span.edu')
            if grade is None:
                grade = ''
            else:
                grade = grade.get_text()
            location = row.select_one('p.option span.loc.long')
            if location is None:
                location = ''
            else:
                location = location.get_text()

            job_dict['company'] = company
            job_dict['title'] = title
            job_dict['link'] = link
            job_dict['master'] = master
            job_dict['grade'] = grade    
            job_dict['location'] = location
            
            jobkorea_jobs.append(job_dict)
    pbar.close()
    return jobkorea_jobs
    
    
    

    



