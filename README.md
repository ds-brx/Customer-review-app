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
  <li> bot.py : The twitter bot used to scrape the comment section from the given post url.</li>
  <li> training.ipynb : Trained a bi-directional recurrent neural network model on 1.6 million labelled tweets. </li>
  <li> get_sentimet.py : Perform sentiment analysis on the scraped tweets by the pretrained model. </li>
  <li> clean_collected_data : Clean the collected data obtained by the bot. </li>
  <li> app.py : The flask server embedded by a dash server to deploy the interactive dashboard.</li>
  </ul>
  
## Working screenshots:

  
  


