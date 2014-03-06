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

- OpenStatus: binary- open(1), close(0) / multiple- open(1), not a real question(2), not constructive(3), off topic(4), too localized(5)
- post\_id, post\_time(relative time from 2008), user\_id, user\_rep, user\_age(user's registration age when created the post)
- tag\_num, is\_tag\_pop(popular tag?), is\_tag\_com(common tag?), tag\_cat(category of the primaty(first) tag)
- title\_len, title\_words, is\_title\_qst(is title a question), n\_tags\_in\_title(number of tags contained in the title)
- body\_len, code\_seg(number of segments of code), code\_lines, n\_tags\_in\_text, sent\_num, sent\_qst(how mant sentences are question)

I take advantage of multi-threading to increase efficiency. It takes about 50s to analyze the train-sample.csv


Train the Data
------------

- k-Nearest Neighbor

	I tries several different machine learning methods and found k-nearest neighbor gives the best results.
	[Sklearn's k-nearest neighbor classifier](http://scikit-learn.org/stable/modules/generated/sklearn.neighbors.KNeighborsClassifier.html) has two options for the weight function. By experienment, "distance"(weight points by the inverse of their distance) and select no less than 0.1% of the total train samples as the neighbors, seems to predict the data extremely good. 

- Ada Boosting

	Sklearn has its [AdaBoosting function](http://scikit-learn.org/stable/modules/ensemble.html#adaboost). I select 0.01% of total sample as weak learners.

- My Ada Boosting

	I implemented the classic AdaBoosting algorithm described in its [wiki page](http://en.wikipedia.org/wiki/AdaBoost). For each iteration, I select 0.01% of total sample to train a Naive Bayes classifier. The threshold to stop the iterations is to have 80% of correctly predicted samples, or the boosting will stop after 100 iterations.

- Spearman's Correlation Coefficient

	Binary Classification
		
	[-0.18186737348940374, -0.18192166162337667, -0.2347649593652551, 0.17953603535891882, 0.16060628937212476, 0.10662357681215597, 0.069033489608542636, 0.076689624469826537, 0.11374890904311763, 0.128818635336367, 0.077106168352071014, -0.070986993363882742, 0.044947796618716764, 0.28232767490441391, 0.30683020982976916, 0.27414583558042682, 0.038387226078081663, 0.2217674176039682, 0.063698404530265276]
		
	Multiple Classification
		
	[0.15474436799406391, 0.15477260668853404, 0.18140611150452385, -0.12615523197452411, -0.1128094624090137, -0.078243265055053621, -0.11531104445749948, -0.093584935920177179, -0.11273764946206317, -0.10579877985176953, -0.06468919494077148, 0.08346185752649983, -0.030609430542116005, -0.21291021890610909, -0.27526857859324994, -0.24543297648129761, -0.005078182628876533, -0.15300345767563306, -0.017508570421120095]

	According to the matrix above, significant predictors are: 
		post\_id, post\_time, user\_id, user\_rep, user\_age, tag\_cat, title\_len, body\_len, code\_seg, code\_lines, sent\_num


Prediction Results
-----------
I randomly select 10,000 posts(not exist in the train sample) for prediction.
*Estimated average

Binary Classification Accuracy and Precision

| KNN |  AdaBoosting | My Ada |
| :--------: | :------:| :------:| 
|0.8422 | 0.7207 | *0.60 |
|0.9208 | 0.7088|*0.53 |


Multiple Classification Accuracy and Precision

| KNN |  AdaBoosting | My Ada |
| :--------: | :------:| :------:| 
|0.8138 | 0.5566 | *0.48|
|0.8441 | 0.4950|*0.40 |

K-nearest neighbors beats others! And it runs much faster, which only takes 5 seconds to train the sample and predict.