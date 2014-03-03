Predicting Closed Questions on StackOverflow with NLP and ML
=====================

Packages
---------
I am using Python 2.7. Several essential packages are needed:

- [NLTK](http://www.nltk.org/) a natual language processing toolkit for Python
- [scikit-learn](http://scikit-learn.org/stable/) open source data mining tool, this package also require some other dependencies
- [numpy, Scipy, matpoltlib](http://www.scipy.org/) maths packages

Tags
---------
With the help of [StackExchange queries](http://data.stackexchange.com/stackoverflow/queries), we can explore the properties of tags.

By Feb 2014 (since the statistics of tags only slightly change over time, apply dataset of anytime is fair), there are 36,127 total tags used in 19,814,527 stackoverflow posts. I identify top 100 of them as [popular](data/popular_tags.csv) (appear in 46.19% of all posts), top 5,000 of them as [common](data/common_tags.csv) (appear in 92.49% of all posts), others as rare (appear in less than 8% of all posts).

Then I try to categorize tags by their [descriptions](data/tag_description_5000.csv) (to increase efficiency, I only analyze top 5,000 tags). After the inspection of the data, I divide tags into 4 categories: [languages](data/tag_lng.csv), [libraries](data/tag_lib.csv), [applications](data/tag_app.csv) and others. 
The rule is to identify keywords in tag's description:

| Category |  Keywords | 
| :--------: | :------:| 
| languages  | "language" | 
| libraries   |  "library", "framework", "module" | 
| applications| "application", "software", "platform", "IDE"|
 
A single tag may appear in multiple categories.

As a result, 436 tags are grabbed as language, 609 tags are grabbed as library, 1022 tags are grabbed as application. From this [wikipedia list](http://en.wikipedia.org/wiki/List_of_programming_languages), there are about 700 programming lanuages (some of them are really rare though). The data size should be close. 

We can assume that the topic of the one posted question are determined by the category of its first tags. In this way, we categorize the topic of posts. Intuitively, if a post is about programming language, we can expect an appropriate post should have some code segments in the body; if a post is on application, there should be a longer length of texts describing the detailed problems, etc.

Analyze Posts
------------
I extracted the following variable for each entry of post:

- OpenStatus: open(1), close(0)/open(1), not a real question(2), not constructive(3), off topic(4), too localized(5)
- post\_id, post\_time(relative time from 2008), user\_id, user\_rep, user\_age(user's registration age when created the post)
- tag\_num, is\_tag\_pop(popular tag?), is\_tag\_com(common tag?), tag\_cat(category of the primaty(first) tag)
- title\_len, title\_words, is\_title\_qst(is title a question), n\_tags\_in\_title(number of tags contained in the title)
- body\_len, code\_seg(number of segments of code), code\_lines, n\_tags\_in\_text, sent\_num, sent\_qst(how mant sentences are question)

I take advantage of multi-threading to increase efficiency. It takes about 50s to analyze the train-sample.csv

Train the Data
------------
- k-Nearest Neighbor
- Ada Boosting
- My Ada Boosting

Prediction
-----------
