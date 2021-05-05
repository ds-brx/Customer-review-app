# Customer-review-app
A sentiment analysis application with an inbuilt bot that scrapes the comment section of a twitter post for generating interactive customer review insights.

## Description:
Analysing twitter comments for a company's post is an indispensable resource of honest customer review. The application makes the process interesting and efficient. This app, **Review Beta** scrapes the **comment section** of the twitter post the user wishes to explore. It is inbuilt with a twitter bot, that essentially scrapes the comment section of the required twitter post url, and sends it to a sentiment analyser for sentiment analysis, and delivers beautiful interactive graphs.

## Tools used :
<ul>
  <li> Python </li>
  <li> Selenium </li>
  <li> PyTorch </li>
  <li> Dash </li>
  <li> Flask </li>
</ul>

## Functional Modules :
<ul>
  <li> bot.py : The twitter bot used to scrape a continuous loading twitter page for the comment section of the given post url.</li>
  <li> training.ipynb : Trained a bi-directional recurrent neural network model on 1.6 million labelled tweets. </li>
  <li> get_sentimet.py : Perform sentiment analysis on the scraped tweets by the pretrained model. </li>
  <li> clean_collected_data : Clean the collected data obtained by the bot. </li>
  <li> app.py : A dash server embedded into a flask server to deploy the interactive dashboard.</li>
  </ul>
  
## Working screenshots:
<ul>
  <li> Home page: Paste your desired twitter post url over here. </li>
  <li> Demo: Copy a URL </li>
  <li> Demo : Paste it to the form and click on search button.</li>
  <li> Demo: Insight 1.1: Sentiment analysis of tweets posted by date time sequence.</li>
  <li> Insight 1.2</li>
  <li> Insight 2: Graph depicting reply comment likes, replies, retweets and the tweet for representing popularity of the comment feedbacks.</li>
  <li> Insight 3: Sentiment score of top 5 comments for a popular opinion analysis. </li>
</ul>

![alt text](https://github.com/ds-brx/Customer-review-app/blob/main/images/Home-page.png)
![alt text](https://github.com/ds-brx/Customer-review-app/blob/main/images/Choose_url.png)
![alt text](https://github.com/ds-brx/Customer-review-app/blob/main/images/Home-paste-url.png)
![alt text](https://github.com/ds-brx/Customer-review-app/blob/main/images/insight-1.png)
![alt text](https://github.com/ds-brx/Customer-review-app/blob/main/images/insight-2.png)
![alt text](https://github.com/ds-brx/Customer-review-app/blob/main/images/insight-4.png)
![alt text](https://github.com/ds-brx/Customer-review-app/blob/main/images/insight-5.png)

  ## Further Work:
  <ul>
  <li> Work further to train the model on different languages. </li>
  <li> Feature engineering for better deduced insights. </li>
  <li> Optimise the bot for quicker and more efficient scraping process. </li>
  <li> Analysis of giphys or images posted for added semantic understanding. </li>
  </ul>
  
  
  


