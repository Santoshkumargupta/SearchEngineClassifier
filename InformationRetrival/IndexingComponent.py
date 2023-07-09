from typing import Any
import pandas as pd;
import datetime;
import string;
import json;
import nltk;

nltk.download('averaged_perceptron_tagger')
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('punkt')
from nltk import pos_tag
from nltk.corpus import wordnet
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

def IndexingDetailMethod(xtest, q):
    sample_db = pd.read_csv('database.csv').rename(columns={'Unnamed: 0':'SN'})
    sample_db
    print(f'{sample_db.shape[0]} records were scraped')

    scraped_db = pd.read_csv('database.csv')
    scraped_db.rename(columns={'Unnamed: 0':'SN'},inplace=True)

    scraped_db['SN'].fillna(pd.Series(range(1, len(scraped_db) + 1)), inplace=True)
    # scraped_db.head()
    # sample_db:Any
    # sample_db.head(7)
    print(scraped_db)
    single_row = scraped_db.loc[1,:].copy()
    # print(single_row) 


    # print(scraped_db.head())


    #Preprocess Text 

    # Remove stop words
    sw = stopwords.words("english")
    lemmatizer = WordNetLemmatizer()

    def tp1(txt):
        txt = txt.lower()   # Make lowercase
        txt = txt.translate(str.maketrans('',
                                        '',
                                        string.punctuation))   # Remove punctuation marks
        txt = lematize(txt)
        return txt


    def fwpt(word):
        tag = pos_tag([word])[0][1][0].upper()
        hash_tag = {"V": wordnet.VERB, "R": wordnet.ADV,"N": wordnet.NOUN,"J": wordnet.ADJ}         
        return hash_tag.get(tag, wordnet.NOUN)

    def lematize(text):
            tkns = nltk.word_tokenize(text)
            ax = ""
            for each in tkns:
                if each not in sw:
                    ax += lemmatizer.lemmatize(each, fwpt(each)) + " "
            return ax


    # # Sample title
    single_row['Title']

    # # Demonstration of lowercase and punctuation removal
    tp1(single_row['Title'])

    # # Demonstration of lematization
    lematize(tp1(single_row['Title']))
    lematize(single_row['Title'])

    sample_db['Title'].iloc[5]
    scraped_db['Title'].iloc[5]

    processed_db = scraped_db.copy()

    def preprocess_df(df):
        df.Title = df.Title.apply(tp1)
        df.Author = df.Author.str.lower()
        df = df.drop(columns=['Author','Published'], axis=1)
        return df
        
    preprocess_df(processed_db)
    processed_db.head()

    print("Preprocess dataFrame is:----")
    print(processed_db.head())

    #Indexing Construction

    single = processed_db.loc[0,:].copy()
    print(single)
    indexing_trial = {}

    words = single.Title.split()
    SN = single.SN
    word = words[0]
    indexResult = {word: [SN]}

    print('=====================================================================')
    print('Sample index is :')
    print(indexResult)

    ## Indexer Function
    def apply_index(inputs, index):
        words = inputs.Title.split()
        SN = int(inputs.SN)
        for word in words:
            if word in index.keys():
                if SN not in index[word]:
                    index[word].append(SN)
            else:
                index[word] = [SN]
        return index

    indx = apply_index(inputs=single, index= {})
    print(indx)

    def full_index(df, index):
        for x in range(len(df)):
            inpt = df.loc[x,:]
            ind = apply_index(inputs=inpt, index=index)
        return ind

    def construct_index(df, index):
        queue = preprocess_df(df)
        ind = full_index(df=queue, index=index)
        return ind

    indexed = full_index(processed_db, 
                        index = {})

      
    indexes = construct_index(df=scraped_db, 
                            index = {})

    with open('indexes.json', 'w') as new_f:
        json.dump(indexes, new_f, sort_keys=True, indent=4)
        
    with open('indexes.json', 'r') as file:
        data = json.load(file)

    def index_2(df, x_path):
        if len(df) > 0:
            with open(x_path, 'r') as file:
                prior_index = json.load(file)
            new_index = construct_index(df = df, index = prior_index)
            with open(x_path, 'w') as new_f:
                json.dump(new_index, new_f, sort_keys=True, indent=4)
    


    # Query Processor
    def demonstrate_query_processing():
        sample = input('Enter Search Terms: ')
        processed_query = tp1(sample)
        #print(f'User Search Query: {sample}')
        print(f'Processed Search Query: {processed_query}')
        return processed_query
        
    #demonstrate_query_processing()


    #Split Query into individaul term
    def split_query(terms):
        each = tp1(terms)
        return each.split()

    dqp = demonstrate_query_processing()
    dqp
    print(f'Split Query: {split_query(dqp)}')

    #Boolean Functionalities
    def union(lists):
        union = list(set.union(*map(set, lists)))
        union.sort()
        return union

    def intersection(lists):
        intersect = list(set.intersection(*map(set, lists)))
        intersect.sort()
        return intersect

    #SearchEngine Function
    def vertical_search_engine(df, query, index=indexes):
        query_split = split_query(query)
        retrieved = []
        for word in query_split:
            if word in index.keys():
                retrieved.append(index[word])
                
                
        # Ranked Retrieval
        if len(retrieved)>0:
            high_rank_result = intersection(retrieved)
            low_rank_result = union(retrieved) 
            c = [x for x in low_rank_result if x not in high_rank_result]      
            high_rank_result.extend(c)
            result = high_rank_result

            
            final_output = scraped_db[scraped_db.SN.isin(result)].reset_index(drop=True)
        
            #Return result in order of Intersection ----> Union
            dummy = pd.Series(result, name = 'SN').to_frame()
            result = pd.merge(dummy, final_output, on='SN', how = 'left')
            
        else:
            result = 'No result found'
        
        return result

    def test_search_engine():
        xtest = scraped_db.copy()
        query = input("Enter your search query: ")
        return vertical_search_engine(xtest, query, indexed)
        
    # test_search_engine()
    # print(test_search_engine())
   
    def final_engine(results):
        if type(results) != 'list':
            return results
            #print(results)
        else:
            for i in range(len(results)):
                printout = results.loc[i, :]
                #print(printout['Title'])
                #print(printout['Author'])
                #print(printout['Published'])
                #print(printout['Link'])
                #print('')

    scraped_db['Author'].iloc[24]
    final_engine(test_search_engine())
    
    return vertical_search_engine(xtest, q, index=indexes)

#  IndexingDetailMethod()







