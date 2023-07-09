from os import name
#from tkinter.tix import COLUMN
import requests;

from bs4 import BeautifulSoup;
import pandas as pd;
import time;
import datetime;
import string;
import json;
import nltk;

nltk.download('averaged_perceptron_tagger')
nltk.download('stopwards')
nltk.download('wordnet')
nltk.download('punkt')
from nltk import pos_tag
from nltk.corpus import wordnet
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

baseUrl ="https://pureportal.coventry.ac.uk/en/organisations/coventry-university/persons/"
profileUrl ="https://pureportal.coventry.ac.uk/en/persons/"
#first = requests.get(URL)
#soup = BeautifulSoup(first.text,'html.parser')
#print(soup)   
 
def get_maximum_page():
    first = requests.get(baseUrl)
    soup = BeautifulSoup(first.text,'html.parser')
    final_page = soup.select('#main-content > div > section > nav > ul >li:nth-child(12) > a')[0]['href']
    fp = final_page.split('=')[-1]
    print("page is :"+fp)
    return int(fp)
mx = get_maximum_page()

def check_department(researcher):
    l1= researcher.find('div',class_='rendering_person_short')

    for span in l1.find_all('span'):
        #check department 
        print(span.text)

        if span.text == str('Centre for Intelligent Healthcare'):
            name = researcher.find('h3',class_= 'title').find('span').text
            return name;
        else:
            pass

def create_csv():
    database = pd.DataFrame(columns=['Title','Author','Published'])
    database.to_csv('database.csv')

create_csv()
#    file_path = 'E:/InformationRetrivalProject/database.csv'

## Open the file in write mode and create a CSV writer object
#with open(file_path, 'w', newline='') as csvfile:
#    writer = csv.writer(csvfile)

#    # Write the data to the CSV file
#    for row in data:
#        writer.writerow(row)

#print('CSV file saved successfully.')

def update_csv(database):
    current_data = pd.read_csv(database,index_col=False)
    return current_data

def getall_research_publication( researcher,url,df):
    new_url= url + str(researcher).replace(' ','-').lower() + '/publications/'
    page= requests.get(new_url)
    soup = BeautifulSoup(page.content,"html.parser")
    results = soup.find(id="main-content")
    papers = results.find_all("li",class_="list-result-item")

    for paper in papers:
        title = paper.find('h3',class_='title').find('span')
        author = paper.find('a',class_='link person')
        author_text = "";
        if author is not None:
            author = author.find('span');
            if author is not None:
                author_text = author.text;
        
        date = paper.find('span',class_='date')
        link = paper.find('h3',class_='title').find('a',href=True)['href']
        
        opening = pd.read_csv('database.csv',index_col=False)
        new_data = {'Title': [title.text], 'Author': [author_text], 'Published': [date.text], 'Link': [link]}
        new_data_df = pd.DataFrame(new_data)

        opening = pd.concat([opening, new_data_df], ignore_index=True)

        # opening = opening.append({'TItle':title.text,
        #                            'Author':author.text,
        #                            'Published':date.text,
        #                            'Link':link},ignore_index = True)
        opening.to_csv('database.csv', index=False)
        
    # print(opening) 
         
#scrapping

def scrape(mx):
    df = update_csv('database.csv')
    i=0
    while True:
       if i>17:
            break

       if i>0:
            url=baseUrl+'?page='+str(i)
       else:
            url= baseUrl
       i=i+1

         # scapping start here 
       page= requests.get(url)
       soup = BeautifulSoup(page.content, "html.parser")
       results = soup.find(id="main-content")
       researchers = results.find_all("li", class_="grid-result-item")
       
       for researcher in researchers:
             # Check if researcher has any papers\n",
             check = researcher.find('div', class_='stacked-trend-widget')
             if check:
                 name = check_department(researcher)
             if name is None:
                pass
             else:
                getall_research_publication(name,profileUrl , df)
  
scrape(mx)


#Schedul Crawler for every week .
days = 0
interval = 7
while days <= 1:
    scrape(mx)
    print(f"Crawled at {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f'Next crawl scheduled after {interval} days')
    time.sleep(interval)
    days = days + 1

## Indexing Componenet
#    scraped_db = pd.read_csv('database.csv').rename(column={'Unnamed:0':'SN'}).reset_index(drop=True)
#    scraped_db.head()
#    sample_db.head(7)
#    single_row = scraped_db.loc[1,:].copy()
#    single_row
#    print(scraped_db)

##Preprocess Text 

#sw= stopwords.words("enlish")
#lemmatizer = WordNetLemmatizer


#def tp1(text):
#    text = text.lower() #make lowercase
#    text = text.translate(str.maketrans('',
#                                        '',
#                                        string.punctuation)) # Remove punctuation marks

#    text = lematize(text)
#    return text

#def fwpt(word):
#    tag = pos_tag([word][0][1][0]).upper()
#    has_tag ={"V":wordnet.VERB,"R":wordnet.ADV,"N":wordnet.NOUN,"J":wordnet.ADJ}
#    return has_tag.get(tag,wordnet.NOUN)

##def lematize(text):
##         tkns = nltk.word_tokenize(text)
##         ax =""
##         for each tkns:



              





















































































































