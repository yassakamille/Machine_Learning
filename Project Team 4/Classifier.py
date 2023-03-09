import requests
import streamlit as st
import math
import joblib
from streamlit_lottie import st_lottie
import plotly.graph_objects as go

data = joblib.load(open("Customer_Segmentation_model", 'rb'))

def load_lottie(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

def min_dist(x,y):
    p = [x,y]
    dists = []
    
    for i in data[0]:
        dists.append(math.dist(p, i))
    
    c = dists.index(min(dists))
    d = min(dists)
    
    x = [p[0], data[0][c][0]]
    y = [p[1], data[0][c][1]]
    
    r = data[2].add_trace(go.Scatter(x=x, y=y, mode="lines", line=go.scatter.Line(color="white"), showlegend=False))
    
    cluster = [c,d,r]
    return cluster


st.set_page_config(page_title='Cluster Specifier')

st.write('# Cluster Specifier Deployment')

lottie_link = "https://assets1.lottiefiles.com/packages/lf20_cuffvo8q.json"
animation = load_lottie(lottie_link)

st.write('---')
st.subheader('Fill out the forms to view your cluster')

with st.container():
    left_column, right_column = st.columns(2)
    
    with left_column:
        age    = st.number_input('Enter your age', 0, 100)
        
        gender = st.radio('Gender: ', ['Female', 'Male'])
        
        annual = st.number_input('Enter your Annual Income', 0, 200)
        
        spending = st.number_input('Enter your Spending Score, varies from 1-->100', 1, 100)
    
    with right_column:
        st_lottie(animation, speed=1, height=400, key="initial")
    
    if st.button('Specify'):
        cluster = min_dist(spending, annual)
        st.write('## Your Cluster is ', cluster[0])
        st.write('# Your distance from the center of the cluster is ', round(cluster[1], 2))
        st.write(data[1])
        st.write(data[2])
        
    
    
    
    
        