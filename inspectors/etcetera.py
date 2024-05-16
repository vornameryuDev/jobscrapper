import pandas as pd
import numpy as np


def saveExel(db, keyword):
    df_list = []
    for dict in db[keyword]:
        df = pd.DataFrame(
            {
                "회사명": [dict['company']],
                "제목": [dict["title"]],
                "경력": [dict["master"]],
                "학력": [dict["grade"]],
                "지역": [dict["location"]],
                "링크": [dict["link"]],
            }
        )
        df_list.append(df)
    result = pd.concat(df_list, axis=0)
    print(result.head())
    result.to_excel(f"jobscrapper_result_{keyword}.xlsx", index=False)
    
    




