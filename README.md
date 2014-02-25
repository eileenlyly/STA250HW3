


Predicting Closed Questions on StackOverflow with NLTK
=====================

Tags
---------
With the help of [StackExchange queries](http://data.stackexchange.com/stackoverflow/queries), we can explore the properties of tags.

By Feb 2014 (since the statistics of tags only slightly change over time, apply dataset of anytime is fair), there are 36,127 total tags used in 19,814,527 stackoverflow posts. I identify top 100 of them as [popular]() (appear in 46.19% of all posts), top 5,000 of them as [common]() (appear in 92.49% of all posts), others as rare (appear in less than 8% of all posts).

Then I try to categorize tags by its [description]() (to increase efficiency, I only analyze top 5,000 tags). After the inspection of some top tags, I divide tags into 4 categories: [language](), [library](), [application]() and others. 
The rule is to identify keywords in each category:
| Category |  Keywords | 
| :--------: | :------:| 
| language  | "language" | 
| library   |  "library", "framework", "module" | 
| application| "application", "software", "platform", "IDE"| 
A single tag may appear in multiple categories.

We can assume that the topic of the posted questions are determined by the category of their tags. In this way, we categorize the topic of posts.

