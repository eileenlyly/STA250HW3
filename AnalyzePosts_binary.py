import csv, os
import nltk
from nltk.tokenize import RegexpTokenizer
from nltk.tag import pos_tag
from collections import defaultdict
from itertools import groupby, imap
import numpy as np
from multiprocessing import Pool
from dateutil import parser as dateparser
from datetime import datetime

os.chdir('/Users/eileenlyly/courses/STA250/HW3/')

#read language tags into dictionary, 436 total language tags
lng_reader = csv.reader(open('tag_lng.csv'))
lng_dict = defaultdict(lambda : None)
for lng in lng_reader:
    lng_dict[lng[0]]
 
#read lib tags into dictionary, 690 total library tags
lib_reader = csv.reader(open('tag_lib.csv'))
lib_dict = defaultdict(lambda : None)
for lib in lib_reader:
    lib_dict[lib[0]]
 
#read app tags into dictionary, 1022 total app tags
app_reader = csv.reader(open('tag_app.csv'))
app_dict = defaultdict(lambda : None)
for app in app_reader:
    app_dict[app[0]]
    
#read popular tags into dictionary, 100 total popular tags
pop_reader = csv.reader(open('popular_tags.csv'))
pop_dict = defaultdict(lambda : None)
for pop in pop_reader:
    pop_dict[pop[0]]
    
#read common tags into dictionary, 5000 total common tags
com_reader = csv.reader(open('common_tags.csv'))
com_dict = defaultdict(lambda : None)
for com in com_reader:
    com_dict[com[0]]
 
word_parser = RegexpTokenizer(r'\w+')
        
def norm_tag(string):
    return RE_NONALNUM.sub('', string).lower()

def analyzePosts_binary(row): 
    post_status = '1'
    if row['OpenStatus'] != 'open':
        post_status = '0'  
    
    post_id = row['PostId']
    user_id = row['OwnerUserId']
    post_time = dateparser.parse(row['PostCreationDate'])
    user_time = dateparser.parse(row['OwnerCreationDate'])    
    user_age = (post_time - user_time).days
    user_rep = row['ReputationAtPostCreation']
    post_time = (post_time - datetime(2008,1,1,0,0)).days
    
    output = post_status + ',' + str(post_id) + ',' + str(post_time) + ',' + user_id + ',' + user_rep + ',' + str(user_age)
      
    tags = [row["Tag%d"%i].lower() for i in range(1,6) if row["Tag%d"%i]] 
    tag_num = len(tags)
    
    is_tag_pop = 0
    is_tag_com = 0
    for t in tags:
        if t in pop_dict:
            is_tag_pop = 1
            is_tag_com = 1
            break
        if t in com_dict:
            is_tag_com = 1
    
    tag_cat = 0    
    for t in tags:            
        if t in lng_dict:
            tag_cat = 1
            break
        elif t in lib_dict:
            tag_cat = 2
            break
        elif t in app_dict:
            tag_cat = 3
            break
    output += ',' + str(tag_num) + ',' + str(is_tag_pop) + ',' + str(is_tag_com) + ',' + str(tag_cat)
    
    #parameters about title
    title = row['Title'].lower()
    title_len = len(title)
    title_words = word_parser.tokenize(title)
    title_words_count = len(title_words)
    is_title_qst = title.endswith('?') * 1
    # number of tags mentioned in title
    n_tags_in_title = len(set(title_words).intersection(set(tags)))
    output += ',' + str(title_len) + ',' + str(title_words_count) + ',' + str(is_title_qst) + ',' + str(n_tags_in_title)
    
    #get main body
    body = row['BodyMarkdown'].lower()
    body_len = len(body)    
    
    lines = body.splitlines()
    codes = []
    text = []
    sents = []
    # Divide post into code and text blocks
    for is_code, group in groupby(lines, lambda l: l.startswith('    ')):
        (codes if is_code else text).append('\n'.join(group))
    
    code_seg = len(codes)
    code_lines = 0
    for c in codes:
        code_lines += c.count('\n')
        
    n_tags_in_text = 0
    sent_num = 0
    sent_qst = 0
    
    for seg in text:
        for sent in nltk.sent_tokenize(seg):
            sent_num += 1
            ss = sent.strip()
            if ss.endswith('?'):
                sent_qst += 1   
                
    #sent_qst_rt = round(float(sent_qst) / sent_num, 3)
    
    output += ',' + str(body_len) + ',' + str(code_seg) + ',' + str(code_lines) + ',' + str(n_tags_in_text) + ',' + str(sent_num) + ',' + str(sent_qst)
    
    return output + '\n'
            
                    

if __name__ == "__main__":
        
    # Read csv as dictionary    
    reader = csv.DictReader(open('data/pred-test.csv'))
        
    pool = Pool()     
    with open('data/output_binary.csv', 'w') as outf:
        header = "post_status,post_id,post_time,user_id,user_rep,user_age,tag_num,is_tag_pop,is_tag_com,tag_cat,title_len,title_words,is_title_qst,n_tags_in_title"
        header += ",body_len,code_seg,code_lines,n_tags_in_text,sent_num,sent_qst\n"
        outf.write(header)
        for i,output in enumerate(pool.imap(analyzePosts_binary, reader, chunksize=100)):
            outf.write(output)
