import streamlit as st
import plotly.express as px
import pandas as pd

st.write('# Which Platform Users Click First')

# -- Read in the data
df = pd.read_csv('WhatsgoodlyData-10.csv')


# -- Create the figure in Plotly
data = df.groupby(by=['Segment Type','Answer'])['Count'].sum().reset_index()
fig = px.bar(data, x='Segment Type',y='Count', color='Answer', text_auto=True, barmode='stack')
fig.show()
fig.update_layout(title="Platform Count by Segment Types")
# -- Input the Plotly chart to the Streamlit interface
st.plotly_chart(fig, use_container_width=True)