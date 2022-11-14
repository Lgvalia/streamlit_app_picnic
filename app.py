import streamlit as st
import plotly.express as px
import pandas as pd

st.write('# Which Platform Users Click First')

#Prepare Data
#Main Df
df = pd.read_csv('WhatsgoodlyData-10.csv')

#Df for Custom Segment
d1 = df.loc[df['Segment Type']=='Custom']
d2 = d1.loc[d1['Segment Description'].str.split(' ').str.get(0)=='Graduation']
d2['Segment Category'] = d2['Segment Description'].str.split(' ').str.get(0) + ' ' + d2['Segment Description'].str.split(' ').str.get(1)
d2['Segment SubCategory'] = d2['Segment Description'].str.split(' ').str.get(-1)

d3 = d1.loc[d1['Segment Description'].str.split(' ').str.get(0)!='Graduation']
d3['Segment Category'] = d3['Segment Description'].str.split('?').str.get(0)
d3['Segment SubCategory'] = d3['Segment Description'].str.split('?').str.get(1)

df_custom = pd.concat([d1,d3])
data_custom = df_custom.groupby(by=['Segment Category','Segment SubCategory','Answer'])['Count'].sum().reset_index()



tab1, tab2, = st.tabs(["Summary", "Details"])

with tab1:
   
    # -- Create the figure in Plotly
    data = df.groupby(by=['Segment Type','Answer'])['Count'].sum().reset_index()
    fig = px.bar(data, x='Segment Type',y='Count', color='Answer', text_auto=True, barmode='stack')
    fig.show()
    fig.update_layout(title="Platform Count by Segment Types")
    # -- Input the Plotly chart to the Streamlit interface
    st.plotly_chart(fig, use_container_width=True)


    data['Percentage'] = data['Count'] / data.groupby(by=['Segment Type'])['Count'].transform('sum')
    fig_pct = px.bar(data, x='Segment Type',y='Percentage', color='Answer', text_auto=True, barmode='stack')
    fig_pct.layout.yaxis.tickformat = ',.2%'
    fig_pct.update_layout(title="Platform Percents by Segment Types")
    st.plotly_chart(fig_pct, use_container_width=True)

with tab2:
   st.write('Custom Segmet Type by Sub Categories')
   category_choice = st.selectbox(
        "Choose Category",
        (['All'] + df_custom['Segment Category'].unique().tolist()),
    ) 
   if category_choice != "All":
        filtered_df = data_custom[data_custom['Segment Category'] == category_choice]
   else: filtered_df = data_custom
   fig_custom = px.treemap(filtered_df, path=['Segment Category', 'Segment SubCategory', 'Answer'], values='Count')
   fig_custom.data[0].textinfo = 'label+value'
   #fig_custom.update_layout(title="Custom Segmet Type by Sub Categories")
   st.plotly_chart(fig_custom, use_container_width=True)