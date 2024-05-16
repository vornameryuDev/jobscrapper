from inspectors.etcetera import saveExel
from inspectors.jobkorea import jobkorea_scrapper
from inspectors.saramin import saramin_scrapper
from urllib.parse import quote
from flask import Flask, jsonify, redirect, render_template, request, send_file, url_for

import pandas as pd



app = Flask(__name__)

db = {}

@app.route('/export')
def export():
    keyword = request.args.get('keyword')    
    if keyword is None:
        return redirect(url_for('home'))    
    if keyword not in db:
        return redirect(f'/search?keyword={keyword}')
    saveExel(db, keyword)
    return send_file(f"jobscrapper_result_{keyword}.xlsx", as_attachment=True)
    

@app.route('/search')
def search():
    keyword = request.args.get('keyword')
    if keyword is None:
        return redirect(url_for('home'))
    if keyword in db:
        result = db[keyword]
    else:        
        quote_keyword = quote(keyword)
        page_num = 2
        jobkorea_jobs = jobkorea_scrapper(quote_keyword, page_num)
        saramin_jobs = saramin_scrapper(quote_keyword, page_num)
        result = jobkorea_jobs + saramin_jobs
        db[keyword] = result        
    return render_template('search.html', result=result, keyword=keyword)


@app.route('/')
def home():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(host="localhost", port=8080, debug=True)


