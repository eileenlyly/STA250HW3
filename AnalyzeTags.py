import csv

reader = csv.reader( open('/Users/eileenlyly/courses/STA250/HW3/tags_description_10000.csv'))

with open('/Users/eileenlyly/courses/STA250/HW3/tag_app.csv','w') as output:
    for tag in reader:
        if "application" in tag[1] or "software" in tag[1] or "IDE" in tag[1] or "platform" in tag[1]:
            output.write(tag[0])
            output.write('\n')