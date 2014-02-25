import argparse
import csv
import nltk
from nltk.tokenize import RegexpTokenizer
from collections import Counter, Mapping, Sequence, defaultdict
from itertools import groupby
import re
import numpy as np
from multiprocessing import Pool
from dateutil import parser as dateparser

import os

CLASSES = [ 'not a real question', 'not constructive', 'off topic', 'open', 'too localized']
status = dict( (k, str(i+1)) for i,k in enumerate(CLASSES))
def norm_tag(string):
    return RE_NONALNUM.sub('', string).lower()

def analyzeEntries(row):
    word_counter = RegexpTokenizer(r'\w+')
    post_id = row['PostId']
    try:
      post_status = status[row['OpenStatus']]
    except KeyError:
      # no OpenStatus, must be a test file
      post_status = '0'
    
    usr_rep = row['ReputationAtPostCreation']
      
    tags = [row["Tag%d"%i].lower() for i in range(1,6) if row["Tag%d"%i]] 
    tags_num = len(tags)
    
    #parameters about title
    title = row['Title'].lower()
    title_len = len(title)
    title_words = word_counter.tokenize(title)
    title_words_count = len(title_words)
    is_title_qst = title.endswith('?')
    # number of tags mentioned in title
    n_tags_in_title = len(set(words).intersection(set(tags)))
    
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
                
    

if __name__ == "__main__":

  # Read csv as dictionary
    reader = csv.DictReader( open('/Users/eileenlyly/courses/STA250/HW3/data/test.csv') )
    pool = Pool()
      
    with open('/Users/eileenlyly/courses/STA250/HW3/data/output.csv', 'w') as outf:
        with Timer() as t:
            for i,output in enumerate(pool.imap(analyzeEntries, reader, chunksize=100)):
                outf.write( output )
