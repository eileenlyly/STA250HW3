import csv
import os

os.chdir('/Users/eileenlyly/courses/STA250/HW3/')

reader = csv.reader( open('tags_description_5000.csv'))

with open('tag_lng.csv','w') as output1, open('tag_lib.csv','w') as output2, open('tag_app.csv','w') as output3:
    for tag in reader:
        if "language" in tag[1]:
            output1.write(tag[0])
            output1.write('\n')
        if "library" in tag[1] or "framework" in tag[1] or "module" in tag[1]:
            output2.write(tag[0])
            output2.write('\n')
        if "application" in tag[1] or "software" in tag[1] or "IDE" in tag[1] or "platform" in tag[1]:
            output3.write(tag[0])
            output3.write('\n')