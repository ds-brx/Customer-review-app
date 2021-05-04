import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import clean_collected_data
from bot import main
from get_sentimet import generate_sentiments
from clean_collected_data import preprocess_data

import plotly.graph_objects as go
URL = 'https://twitter.com/elonmusk/status/1388693126206918658'
usr = "breenda.das@gmail.com"
pwd = "Bree@1807"
file_path = 'collected_data.csv'

def get_data(url):
    main(usr, pwd,file_path,url)
    data, small_data = preprocess_data()
    return data, small_data
dash_app = dash.Dash(__name__)

dash_app.layout = html.Div([
    dcc.Input(id="input-url", type="url", value=URL),
    dcc.Graph(id="sentiment-time-series-chart"),
    dcc.Graph(id="user-comment-insights"),
    dcc.Graph(id = "Top-Tweets-Insights")
])

@dash_app.callback(
    Output('sentiment-time-series-chart', 'figure'),
    Output('user-comment-insights', 'figure'),
    Output('Top-Tweets-Insights', 'figure'),
    Input('input-url', 'value'))
def update_insights(url):
    df,small_df = get_data(url)
    fig1 = go.Figure(data=go.Scatter(x=df['datetime'],
                                    y=df['sentiments'],
                                    mode='markers',
                                    marker_color=df['sentiments'],
                                    text=df['username']))
    fig1.update_layout(title = 'Sentiment analysis with Tweet Replies Date Time',
                    xaxis= dict(title= 'Date Time',gridcolor='lightgrey'),
                    yaxis= dict(title= 'Sentiment Score',showgrid=False),
                    plot_bgcolor='rgba(0,0,0,0)')

    fig2 = px.scatter(df, x="comment_likes", y="comment_retweets", size="comment_replies", color="sentiments",
            hover_name="comment",log_x = True)
    fig2.update_layout(title = 'Reply Statistics Table: Reply Retweets, Reply Likes, Reply Comment Count',plot_bgcolor='rgba(0,0,0,0.1)',yaxis= dict(showgrid=False))
    colors = ['rgb(239, 243, 255)', 'rgb(189, 215, 231)', 'rgb(107, 174, 214)',
            'rgb(49, 130, 189)', 'rgb(8, 81, 156)']
    small_df['Color'] = colors 

    fig3 = go.Figure(data=[go.Table(
    header=dict(
        values=["comment", "comment_likes","comment_sentiment"],
        line_color='white', fill_color='white',
        align='center', font=dict(color='black', size=12)
    ),
    cells=dict(
        values=[small_df['Comment'], small_df['Comment Likes'],small_df['Comment Sentiment Score']],
        line_color=[small_df.Color], fill_color=[small_df.Color],
        align='center', font=dict(color='black', size=11)
    ))
    ])
    fig3.update_layout(title = 'Popular User Statistics')

    return fig1, fig2, fig3


# fig1 = go.Figure(data=go.Scatter(x=df['datetime'],
#                                 y=df['sentiments'],
#                                 mode='markers',
#                                 marker_color=df['sentiments'],
#                                 text=df['username']))
# fig1.update_layout(title = 'Sentiment analysis with Tweet Replies Date Time',
#                   xaxis= dict(title= 'Date Time',gridcolor='lightgrey'),
#                   yaxis= dict(title= 'Sentiment Score',showgrid=False),
#                   plot_bgcolor='rgba(0,0,0,0)')


# ## scatter plot comment likes, comment retweets, place

# fig2 = px.scatter(df, x="comment_likes", y="comment_retweets", size="comment_replies", color="sentiments",
#            hover_name="comment",log_x = True)
# fig2.update_layout(title = 'Reply Statistics Table: Reply Retweets, Reply Likes, Reply Comment Count',plot_bgcolor='rgba(0,0,0,0.1)',yaxis= dict(showgrid=False))
# colors = ['rgb(239, 243, 255)', 'rgb(189, 215, 231)', 'rgb(107, 174, 214)',
#           'rgb(49, 130, 189)', 'rgb(8, 81, 156)']
# small_df['Color'] = colors 

# fig3 = go.Figure(data=[go.Table(
#   header=dict(
#     values=["comment", "comment_likes","comment_sentiment"],
#     line_color='white', fill_color='white',
#     align='center', font=dict(color='black', size=12)
#   ),
#   cells=dict(
#     values=[small_df['Comment'], small_df['Comment Likes'],small_df['Comment Sentiment Score']],
#     line_color=[small_df.Color], fill_color=[small_df.Color],
#     align='center', font=dict(color='black', size=11)
#   ))
# ])
# fig3.update_layout(title = 'Popular User Statistics')

# markdown_text1 = '''
# # Insights on your Twitter Post

# The dashboard presents visuals on the analysis conducted on the user response data on your twitter post. 
# The dashboard gives an overview of the sentiment analysis of the tweet replies recorded over the span of posting date and today.

# ## Sentiment Analysis
# The first graph depicts **Sentiment Analysis of Replies** on your twitter post.This graph shows how the sentiments 
# of reaction of users on your post have changed or evolved over time. This graph is useful to understand the twitter post popularity
# over time and general reaction over time.
# '''

# markdown_text2 = '''
# ## User Comment Insights
# The second graph depicts **User Data Statistics** on your twitter post. This graph shows the popular reply stats on your post
# that may prove useful as an important customer review feedback. The graph plots 3 useful features, the reply user likes, comment and retweets, 
# hovered by the reply comment for reference.
# This is a very valuable customer review graph.
# '''

# markdown_text3 = '''
# ## Popular Reply  Sentiments
# The third graph shows a tabular representation of the **Sentiments of the five most popular by likes user comments** on your tweet. These statistics give 
# an insight of the general impression of your post. A very good popular post makes a good about your twitter post, while a 
# negetive feed back may prove useful to your company.

# '''




# app.layout = html.Div([
#     dcc.Markdown(children=markdown_text1),
#     dcc.Graph(id="sentiment-time-series-chart",figure=fig1),
#     dcc.Markdown(children=markdown_text2),
#     dcc.Graph(id="user comment insights",figure=fig2),
#     dcc.Markdown(children=markdown_text3),
#     dcc.Graph(id = "Top Tweets Insights", figure = fig3)
# ])



dash_app.run_server(debug=True)
