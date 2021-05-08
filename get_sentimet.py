import torch
from torchtext.legacy import data
import spacy
from spacy.lang.en import English
nlp = English()
import torch.nn as nn
import torch.optim as optim
from textblob import TextBlob, Word
import regex as re
import dill
import pandas as pd

class RNN(nn.Module):
    def __init__(self, vocab_size, embedding_dim, hidden_dim, output_dim, n_layers, 
                 bidirectional, dropout, pad_idx):
        
        super().__init__()
        
        self.embedding = nn.Embedding(vocab_size, embedding_dim, padding_idx = pad_idx)
        
        self.rnn = nn.LSTM(embedding_dim, 
                           hidden_dim, 
                           num_layers=n_layers, 
                           bidirectional=bidirectional, 
                           dropout=dropout)
        
        self.fc = nn.Linear(hidden_dim * 2, output_dim)
        
        self.dropout = nn.Dropout(dropout)
        
    def forward(self, text, text_lengths):
        
        #text = [sent len, batch size]
        
        embedded = self.dropout(self.embedding(text))
        
        #embedded = [sent len, batch size, emb dim]
        
        #pack sequence
        # lengths need to be on CPU!
        packed_embedded = nn.utils.rnn.pack_padded_sequence(embedded,text_lengths.to('cpu'),enforce_sorted=False)
        
        packed_output, (hidden, cell) = self.rnn(packed_embedded)
        
        #unpack sequence
        output, output_lengths = nn.utils.rnn.pad_packed_sequence(packed_output)

        #output = [sent len, batch size, hid dim * num directions]
        #output over padding tokens are zero tensors
        
        #hidden = [num layers * num directions, batch size, hid dim]
        #cell = [num layers * num directions, batch size, hid dim]
        
        #concat the final forward (hidden[-2,:,:]) and backward (hidden[-1,:,:]) hidden layers
        #and apply dropout
        
        hidden = self.dropout(torch.cat((hidden[-2,:,:], hidden[-1,:,:]), dim = 1))
                
        #hidden = [batch size, hid dim * num directions]
            
        return self.fc(hidden)


def clean_sentiment_data(col):
    '''

    clean sentiment data for analysis
    return : clean tweet list
    '''
    clean_text = []
    for text in col:
        text = re.sub(r'http\S+', '', text)
        text = text.lower()
        #non-word char
        text = re.sub(r"\W", " ", text)
        #digit
        text = re.sub(r"\d", " ", text)
        #post extra space
        text = re.sub(r"\s+", " ", text)
        #single letters
        text = re.sub(r"\s+[a-z]\s+", " ", text)
        #leading extra space
        text = re.sub(r"^\s+", "", text)
        #leading extra space at the end
        text = re.sub(r"\s+$", "", text)
        words = text.split()
        text = " ".join(word for word in words if not nlp.vocab[word].is_stop)
        text = TextBlob(text)
        text = " ".join([word.lemmatize() for word in text.words]) 
        clean_text.append(text)
        
    return clean_text

def vocabulary_generator():
    tweet = data.Field(sequential=True,tokenize = 'spacy',
                  tokenizer_language = 'en_core_web_sm',
                  include_lengths = True)
    target = data.Field(sequential=False, use_vocab=False)
    fields = {
    'Tweets' : ('t',tweet),
    'Target' : ('s', target)
}
    train_data = data.TabularDataset(path = "./clean_train_csv.csv",format = "csv",fields=fields)
    tweet.build_vocab(train_data,max_size=10000,vectors = "glove.6B.100d", unk_init = torch.Tensor.normal_,min_freq=1)
    with open("./TEXT.Field","wb")as f:
     dill.dump(tweet,f)
    with open("./TEST.Field","wb")as f:
     dill.dump(target,f)

# def test_dataloader(test_data):
#     test_df = pd.DataFrame(test_data,columns = ['Tweets'])
#     test_df.to_csv('./test_csv_file.csv')
#     tweet = data.Field(sequential=True,tokenize = 'spacy',
#                   tokenizer_language = 'en_core_web_sm',
#                   include_lengths = True)
#     field = {
#     'Tweets' : ('t', tweet)
#     }   
#     test_dl = data.TabularDataset(path = './test_csv_file.csv',format = "csv",fields=field)
#     return test_dl

# def test_iterators(test_dl):
#     BATCH_SIZE = 1
#     device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
#     test_iterator = data.BucketIterator(
#         (test_dl), 
#         batch_size = BATCH_SIZE,
#         sort_key = lambda x: len(x.t),
#         sort_within_batch = False,
#         device = device)
#     return test_iterator


def load_pretrained_model(TEXT_FIELD):
    INPUT_DIM = 10002
    EMBEDDING_DIM = 100
    HIDDEN_DIM = 256
    OUTPUT_DIM = 1
    N_LAYERS = 2
    BIDIRECTIONAL = True
    DROPOUT = 0.5
    PAD_IDX = TEXT_FIELD.vocab.stoi[TEXT_FIELD.pad_token]

    model = RNN(INPUT_DIM, 
                EMBEDDING_DIM, 
                HIDDEN_DIM, 
                OUTPUT_DIM, 
                N_LAYERS, 
                BIDIRECTIONAL, 
                DROPOUT, 
                PAD_IDX)
    model.load_state_dict(torch.load('./Customer-review-app/trained_model.pt',map_location='cpu'))
    model.eval()
    model.embedding.weight.data.copy_(TEXT_FIELD.vocab.vectors)

    return model 

def predict_sentiment(model, sentence,TEXT):
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model.eval()
    tokenized = [tok.text for tok in nlp.tokenizer(sentence)]
    indexed = [TEXT.vocab.stoi[t] for t in tokenized]
    length = [len(indexed)]
    tensor = torch.LongTensor(indexed).to(device)
    tensor = tensor.unsqueeze(1)
    length_tensor = torch.LongTensor(length)
    try:
        prediction = torch.sigmoid(model(tensor, length_tensor))
        return prediction.item()
    except:
        return 0

def generate_sentiment_predictions(model,test_list,TEXT):
    predictions = []
    for tweet in test_list:
        predictions.append(predict_sentiment(model,tweet,TEXT))
    return predictions


def generate_sentiments(df):
    df = df[df['comment'].notna()]
    X = clean_sentiment_data(df['comment'])
    with open("./Customer-review-app/TEXT.Field","rb")as f:
     TEXT=dill.load(f)
    model = load_pretrained_model(TEXT)
    predictions = generate_sentiment_predictions(model,X,TEXT)
    return predictions

def end_to_end(url):
    pass

if __name__ == '__main__':
    df = pd.read_csv('collected_data.csv')
    predictions = sentiments(df)
