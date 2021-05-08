import pandas as pd
from get_sentimet import generate_sentiments

def convert_str(col):
    col = col.astype(str).str.replace(',','').str.replace('\s*M', 'e6').str.replace('\s*K', 'e3').astype(float)
    return col

def preprocess_data():
    data = pd.read_csv('./Customer-review-app/collected_data.csv')
    data = data.fillna('0')
    float_list = ['comment_likes','comment_retweets','comment_replies']
    for x in float_list:
        data[x] = convert_str(data[x])
    data = data[data['comment'].notna()]
    data['sentiments'] = generate_sentiments(data)
    X = data['comment']
    y = data['comment_likes']
    z = data['sentiments']
    small_data = pd.DataFrame(list(zip(X[:5],y[:5],z[:5])),columns = ['Comment','Comment Likes','Comment Sentiment Score'])
    return data, small_data


    


# data, small_data = preprocess_data()
# print(data.head)

preprocess_data()