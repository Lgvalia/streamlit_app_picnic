import streamlit as st
import plotly.express as px
import pandas as pd

st.write('# Which Platform Users Click First')


#Prepare Data
#Main Df
df = pd.read_csv('WhatsgoodlyData-10.csv')

#Pie Chart
data_pie = df.groupby(by='Answer')['Count'].sum().reset_index()

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

#Data for University
data_university = df.loc[df['Segment Type']=='University'].groupby(by=['Segment Description','Answer'])['Count'].sum().reset_index()

#Data for others
data_others = df.loc[~(df['Segment Type'].isin(['University','Custom']))].groupby(by=['Segment Type','Segment Description','Answer'])['Count'].sum().reset_index()



tab1, tab2, = st.tabs(["Summary", "In-Depth"])

with tab1:
    
    st.write( ' Total Number of Respondents: {:,}'.format(df['Count'].sum()))

    #Pie Chart
    fig_pie = px.pie(data_pie, values='Count', names='Answer', hole=0.3)
    fig_pie.update_traces(textposition='inside', textinfo='percent+label')
    fig_pie.update_layout(title="Respondents Percentages by Platform")
    st.plotly_chart(fig_pie)
   
    # Segment Counts
    data = df.groupby(by=['Segment Type','Answer'])['Count'].sum().reset_index()
    fig = px.bar(data, x='Segment Type',y='Count', color='Answer', text_auto=True, barmode='stack')
    fig.show()
    fig.update_layout(title="Platform Count by Segment Types")
    #fig.update_layout(margin = dict(t=0.2, l=0.2, r=0.2, b=0.2))
    # -- Input the Plotly chart to the Streamlit interface
    st.plotly_chart(fig, use_container_width=True)

    #segment percents
    data['Percentage'] = data['Count'] / data.groupby(by=['Segment Type'])['Count'].transform('sum')
    fig_pct = px.bar(data, x='Segment Type',y='Percentage', color='Answer', text_auto=True, barmode='stack')
    fig_pct.layout.yaxis.tickformat = ',.2%'
    fig_pct.update_layout(title="Platform Percents by Segment Types")
    #fig_pct.update_layout(margin = dict(t=0.2, l=0.2, r=0.2, b=0.2))
    st.plotly_chart(fig_pct, use_container_width=True)

with tab2:
    #Custom
    st.write('Custom Segmet Type by Sub Categories')
    category_choice = st.selectbox(
        "Choose Category",
        (['All'] + data_custom['Segment Category'].unique().tolist()),
    ) 
    if category_choice != "All":
        filtered_df = data_custom[data_custom['Segment Category'] == category_choice]
    else: filtered_df = data_custom
    fig_custom = px.treemap(filtered_df, path=[px.Constant("all"),'Segment Category', 'Segment SubCategory', 'Answer'], values='Count')
    fig_custom.data[0].textinfo = 'label+value'
    fig_custom.update_layout(margin = dict(t=30, l=0, r=0, b=0))
    #fig_custom.update_layout(title="Custom Segmet Type by Sub Categories")
    st.plotly_chart(fig_custom, use_container_width=True)
    
    #University     
    st.write('By Universities')
    university_choice = st.multiselect(
        "Choose University",
        (data_university['Segment Description'].unique().tolist()),
    )
    if  len(university_choice) == 0:
        uni_filtered_data = data_university
    else: uni_filtered_data = data_university.loc[data_university['Segment Description'].isin(university_choice)]
    
    fig_university = px.treemap(uni_filtered_data, path=[px.Constant("all"),'Segment Description', 'Answer'], values='Count')
    fig_university.data[0].textinfo = 'label+value'
    fig_university.update_layout(margin = dict(t=30, l=0, r=0, b=0))
    st.plotly_chart(fig_university)

    #Others
    st.write('By Other Segments')
    other_choice = st.selectbox(
        "Choose Category",
        (['All'] + data_others['Segment Type'].unique().tolist()),
    ) 
    if other_choice != "All":
        other_filtered_df = data_others[data_others['Segment Type'] == other_choice]
    else: other_filtered_df = data_others
    
    fig_others = px.treemap(other_filtered_df, path=[px.Constant("all"),'Segment Type','Segment Description', 'Answer'], values='Count')
    fig_others.data[0].textinfo = 'label+value'
    fig_others.update_layout(margin = dict(t=30, l=0, r=0, b=0))
    #fig_custom.layout.values.tickformat = ',.2%'
    st.plotly_chart(fig_others, use_container_width=True)
