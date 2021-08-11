
from dash_bootstrap_components._components.Row import Row
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Output, Input, State
import dash
import dash_bootstrap_components as dbc  # pip install dash-bootstrap-components
import plotly.express as px              # pip install plotly
import pandas as pd                      # pip install pandas
from datetime import datetime, timedelta
from wordcloud import WordCloud          # pip install wordcloud
import sys, os
sys.path.insert(0, os.path.abspath('...'))
from jupyter_dash import JupyterDash 
from twint_lib import get_tweets, get_followers_following, get_replies
from app import app
from datetime import date
import nest_asyncio
# csv oku **************************************
DATA_PATH=os.path.abspath('data')
df_cnt = pd.read_csv(DATA_PATH+"\DiyanetTV.csv")
df_cnt["date"] = pd.to_datetime(df_cnt["date"])
df_cnt["day"] = df_cnt["date"].dt.day
df_cnt["month"] = df_cnt["date"].dt.month
#df_cnt['day'] = df_cnt['day'].apply(lambda x: calendar.day_abbr[x])
app.css.append_css({
    "external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"
})
reply_list=["DiyanetTV","DikenComTr","gazetesozcu", "diyanethbr","memurlarnet", "tgrthabertv", "TwiterSonSakika","vatan","stargazete","timeturk","hurhaber1","habervakti"]
username_list= ["Diyanet","DiyanetTV","DR_FatihKurt"]
filterLayout=dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.Div([
                        dbc.CardImg(src='/assets/logo.png') # 150px by 45px
                    ],className='mb-2')
            
                ])
            ]),
        ], width=2),

        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.Div([
                        html.Div([
                            html.Div('Tarih Aralığı', className='three columns'),
                            html.Div([
                                dcc.DatePickerSingle(
                                    id='basTarih',
                                    date=datetime.today().date() - timedelta(days=15),
                                    className='ml-5'
                                ),dcc.DatePickerSingle(
                                    id='bitTarih',
                                    date=datetime.today().date(),
                                    className='mb-2 ml-2'
                                ),
                            ],className='nine columns' ),
                        ]),
                        html.Div([
                            html.Div('Hashtag', className='three columns'),
                            html.Div(dcc.Input(id="hashtag", type="text", placeholder="",className='ml-5'),className='nine columns')
                        ]),
                    ]),
                ])
            ],  color="light"),
        ], width=3), 
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.Div([
                        # Select Division Dropdown
                        html.Div([
                            html.Div('Kullanıcı Seçin', className='three columns'),
                            html.Div(dcc.Dropdown(id='kullanici-selector',
                                                options=[{'label':opt, 'value':opt} for opt in username_list], value="DiyanetTV"),
                                    className='nine columns')
                        ]),

                        # Select Season Dropdown
                        html.Div([
                            html.Div('Reply Hesap Seçin', className='three columns'),
                            html.Div(dcc.Dropdown(id='reply-selector', 
                            options=[{'label':opt, 'value':opt} for opt in reply_list], placeholder="Seçiniz", multi=True),
                                    className='nine columns')
                        ]),
                    ]),
                ])
            ])
        ], width=4), 
        dbc.Col([
            dbc.Card([
                dbc.CardBody([                    
                        html.Div([                        
                            dbc.Button(
                                ("Tweet'den Çek"),
                                color="primary",
                                block=True,
                                id="btnYenile",
                                className="mr-1"
                            )
                        ], style={'textAlign':'center', 'textSize':'10px'}),
                ])
            ])
        ], width=2),
    ],className='mb-2 mt-2'),

summaryLayout=dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Followers"),
                dbc.CardBody([
                    html.H2(id='followers', children="000")
                ], style={'textAlign':'center'})
            ]),
        ], width=2),
        
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Followings"),
                dbc.CardBody([
                    html.H6('Followings'),
                    html.H2(id='followings', children="000")
                ], style={'textAlign':'center'})
            ]),
        ], width=2),
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Replies"),
                dbc.CardBody([
                    html.H6('Invites received'),
                    html.H2(id='replies', children="000")
                ], style={'textAlign':'center'})
            ]),
        ], width=2),
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Tweets"),
                dbc.CardBody([
                    html.H6('Invites sent'),
                    html.H2(id='tweets', children="000")
                ], style={'textAlign': 'center'})
            ]),
        ], width=2),
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Likes"),
                dbc.CardBody([
                    html.H6('Reactions'),
                    html.H2(id='likes', children="000")
                ], style={'textAlign': 'center'})
            ]),
        ], width=2),
    ],className='mb-2')
layout = html.Div([
    html.Div(filterLayout),
    html.Div(summaryLayout),
    
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dcc.Graph(id='line-chart', figure={}, config={'displayModeBar': False}),
                ])
            ]),
        ], width=6),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dcc.Graph(id='bar-chart', figure={}, config={'displayModeBar': False}),
                ])
            ]),
        ], width=6),
    ],className='mb-2'),
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dcc.Graph(id='TBD', figure={}),
                ])
            ]),
        ], width=4),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dcc.Graph(id='pie-chart', figure={}, config={'displayModeBar': False}),
                ])
            ]),
        ], width=4),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dcc.Graph(id='wordcloud', figure={}, config={'displayModeBar': False}),
                ])
            ]),
        ], width=4),
    ],className='mb-2'),
]#, fluid=True
)

@app.callback(
    
    Output('followers','children'),
    Output('followings','children'),
    Output('replies','children'),
    Output('tweets','children'),
    Output('likes','children'),
    [Input('btnYenile', 'n_clicks')],
    [State('basTarih','date'),
    State('bitTarih','date'),
    State('kullanici-selector', 'value'),
    State('reply-selector', 'value'),
    State('hashtag', 'value')]
)
#,bas_tarih, bit_tarih
def update_dash(n_clicks,bas_tarih, bit_tarih, kullanici, reply, hashtag):
    date_object = date.fromisoformat(bas_tarih)
    date_bas= date_object.strftime('%B %d, %Y')

    date_object = date.fromisoformat(bit_tarih)
    date_bit= date_object.strftime('%B %d, %Y')

    print("yenileye girdim {} - {} - {} / @{}, @{}, H: {}".format(n_clicks,date_bas, date_bit,kullanici, reply, hashtag))
    
    dic_follow=get_followers_following(kullanici)
    (followers_num, followings_num)=(dic_follow["followers"], dic_follow["following"])
    nest_asyncio.apply()
    # replies
    df_replies= get_replies(bas_tarih, bit_tarih,kullanici)
    replies_num = len(df_replies)
    # tweets
    nest_asyncio.apply()
    df_list= get_tweets(bas_tarih, bit_tarih,kullanici)
    tweets_num = len(df_list)

    df_tweets = pd.DataFrame(df_list)
    """
    print(type(df_tweets), df_tweets.head())
    for tw in df_tweets.head():
        print(tw, type(tw))
    """
    #,retweets_count,likes_count
    likes_num = 0# sum(df_tweets[['likes_count']])
    print(followers_num, followings_num, replies_num, tweets_num, likes_num)
    
    return followers_num, followings_num, replies_num, tweets_num, likes_num
    
    #return 'The input "{}" , clicked {} times'.format(value,n_clicks), followers_num, followings_num,5+n_clicks,6+n_clicks,7+n_clicks


"""
@app.callback(
    Output(component_id="number-output", component_property="children"),
    [Input(component_id="input-1", component_property="value"),
    Input(component_id="input-2", component_property="value")]
)
def update_output(input1, input2):
    return u'Input 1 is "{}" and Input 2 is "{}"'.format(input1, input2)
"""
# Line Chart ***********************************************************
