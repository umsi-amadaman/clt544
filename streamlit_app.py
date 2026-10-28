import io
from pathlib import Path
import streamlit as st
import matplotlib.pyplot as plt
from clt_core import simulate,plot_rows,NAMES
st.set_page_config(page_title='SI 544 · Central Limit Theorem',layout='wide')
st.title('Visualizing the Central Limit Theorem')
st.write('Compare four populations, their samples, the sample means, and the pooled observations. Change one setting at a time and predict what will change.')
with st.sidebar:
    st.header('Sampling settings')
    n=st.slider('Observations per sample (n)',1,500,25)
    reps=st.select_slider('Number of repetitions',options=[20,100,300,1000,3000,5000],value=1000)
    mu=st.number_input('Population mean',value=68.)
    sd=st.number_input('Base standard deviation',min_value=.1,value=3.)
    sep=st.slider('Bimodal separation (base SD units)',0.,3.,1.2,.05)
    seed=st.number_input('Random seed',min_value=0,max_value=1000000,value=1,step=1)
    overlay=st.checkbox('Show normal approximation for means',value=True)
    st.caption('The bimodal mixture has SD = √[(separation × base SD)² + (base SD / 2)²]. Its overlay uses that SD.')
r=simulate(n,reps,mu,sd,sep,int(seed))
view=st.radio('Display', ['Walk through the rows','Full original panel'],horizontal=True)
if view=='Full original panel':
    fig=plot_rows(r,overlay=overlay);st.pyplot(fig);plt.close(fig)
else:
    sections=[('1. Population','population','Normal is bell-shaped; uniform gives equal probability to equal-width intervals; gamma is right-skewed; the mixture can have two peaks.'),('2. Repeated samples','samples','Each horizontal row is one sample. Orange marks its mean. We show the first 12 samples so individual observations remain visible.'),('3. Sampling distribution of the mean','means','Each entry is one sample mean. Increasing n generally makes these distributions narrower and, for nonnormal populations, closer to normal.'),('4. Pooled individual observations','pooled','These are the original observations combined across samples. Their distribution resembles the population. Pooling does not make a bimodal population normal.')]
    for title,row,explanation in sections:
        st.subheader(title);st.write(explanation)
        fig=plot_rows(r,rows=[row],overlay=overlay);st.pyplot(fig);plt.close(fig)
with st.expander('Compare the standard errors'):
    st.dataframe(r['summary'].round(4),hide_index=True)
    st.write('Expected SE = population SD / √n. More repetitions stabilize the observed distribution; larger n changes the distribution of the means itself.')
st.subheader('Try these comparisons')
st.markdown('1. Hold repetitions at 1,000. Compare **n = 1, 5, 25, and 100**.\n2. Hold **n = 25**. Compare 20 and 3,000 repetitions. Does the expected SE change?\n3. Watch the bimodal column: why can the mean lie between the two population peaks?\n4. Compare the means row with the pooled row. Which one should retain the population’s two peaks?')
st.caption('Adapted from Bobby Madamanchi’s SI 544 W2Lecture544.pdf and CLT_ShinyApp.R. These are illustrative mathematical populations, not measured playground ages. The CLT statement assumes independent samples from a common population with finite variance; n = 30 is not a universal guarantee.')
st.download_button('Download numerical summary',r['summary'].to_csv(index=False),file_name='clt_summary.csv',mime='text/csv')
