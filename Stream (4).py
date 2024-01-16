#!/usr/bin/env python
# coding: utf-8

# In[12]:


import streamlit as st
import pandas as pd
import plotly.express as px


# In[13]:


# Read the CSV file with a different encoding

data = pd.read_csv(r"C:\Users\Admin\OneDrive\Desktop\Olympic 1976-2008.csv", encoding='latin-1')


# In[33]:


import pandas as pd
import streamlit as st
import plotly.express as px

# Read the CSV file with a different encoding
file_path = r"C:\Users\Admin\OneDrive\Desktop\Olympic 1976-2008.csv"
data = pd.read_csv(file_path, encoding='latin-1')

# Remove null values from the 'City' column
cities_without_null = data['City'].dropna().unique()

# Streamlit app
st.title("Olympic Dashboard")

# Dropdown for selecting Olympic City
selected_city = st.selectbox("Select Olympic City:", cities_without_null)

# Dropdown for selecting Country
selected_country = st.selectbox("Select Country:", data['Country'].unique())

# Dropdown for selecting Medal Type
selected_medal = st.selectbox("Select Medal Type:", data['Medal'].unique())

# Slider for setting minimum medal count threshold
medal_threshold = st.slider("Select Medal Threshold:", min_value=1, max_value=20, value=5, step=1)

# Filter data based on user selections
filtered_data = data[(data['City'] == selected_city) &
                     (data['Country'] == selected_country) &
                     (data['Medal'] == selected_medal) &
                     (data.groupby('Athlete')['Medal'].transform('count') >= medal_threshold)]

# Pie chart to display discipline distribution
discipline_pie_chart = px.pie(
    filtered_data,
    names='Discipline',
    title=f"Discipline Distribution in {selected_city}",
    template='plotly_dark'
)

# Bar chart showing the distribution of medals by sport
sport_bar_chart = px.bar(
    filtered_data['Sport'].value_counts().reset_index(),
    x='index',
    y='Sport',
    title=f'Distribution of Medals by Sport in {selected_city}',
    labels={'index': 'Sport', 'Sport': 'Count'},
    height=400,
    color='Sport',  # Set color scale to 'Sport' for gradient colors
    color_continuous_scale='Viridis',  # Use Viridis color scale for gradient colors
    template='plotly_dark'
)

# Bar chart showing the distribution of medals by medal type
medal_bar_chart = px.bar(
    filtered_data['Medal'].value_counts().reset_index(),
    x='index',
    y='Medal',
    title=f'Distribution of Medals by Medal Type in {selected_city}',
    labels={'index': 'Medal Type', 'Medal': 'Count'},
    height=400,
    color='Medal',  # Set color scale to 'Medal' for gradient colors
    color_continuous_scale='Viridis',  # Use Viridis color scale for gradient colors
    template='plotly_dark'
)

# Histogram showing the distribution of medals won by athletes
athlete_histogram = px.histogram(
    filtered_data,
    x='Athlete',
    title=f'Distribution of Medals Won by Athletes in {selected_city}',
    labels={'Athlete': 'Athlete', 'count': 'Medal Count'},
    height=400,
    color_discrete_sequence=px.colors.qualitative.Set3,  # Set color scheme for athlete
    template='plotly_dark'
)

# Pie chart showing the distribution of medals by medal, country, and gender
medal_country_pie_chart = px.pie(
    filtered_data,
    names='Gender',
    title=f'Distribution of {selected_medal} Medals by Gender in {selected_country}',
    template='plotly_dark'
)

# Bar chart showing the most successful athletes
successful_athletes_bar_chart = px.bar(
    filtered_data.groupby('Athlete')['Medal'].count().reset_index().nlargest(10, 'Medal'),
    x='Medal',
    y='Athlete',
    title=f'Top 10 Most Successful Athletes in {selected_city} ({selected_medal} Medals)',
    labels={'Athlete': 'Athlete', 'Medal': 'Medal Count'},
    height=400,
    color_discrete_sequence=px.colors.qualitative.Set1,  # Use Set1 color scheme
    template='plotly_dark'
)

# Scatter plot showing the correlation between the number of athletes and medals
athletes_vs_medals_scatter_plot = px.scatter(
    filtered_data.groupby('Country').agg({'Athlete': 'nunique', 'Medal': 'count'}).reset_index(),
    x='Athlete',
    y='Medal',
    title=f'Correlation between Number of Athletes and Medals in {selected_country}',
    labels={'Athlete': 'Number of Athletes', 'Medal': 'Number of Medals'},
    template='plotly_dark',
    color_discrete_sequence=['#1f77b4'],  # Set color
    hover_name='Country'  # Show country names on hover
)

# Bubble chart showing the most successful athlete in each discipline
most_successful_athletes = data.groupby('Discipline')['Athlete'].agg(lambda x: x.value_counts().idxmax()).reset_index()
medal_counts = data.groupby(['Discipline', 'Athlete']).size().reset_index(name='Medal Count')
most_successful_athletes = pd.merge(most_successful_athletes, medal_counts, on=['Discipline', 'Athlete'], how='left')

bubble_chart = px.scatter(
    most_successful_athletes,
    x='Discipline',
    y='Athlete',
    size='Medal Count',
    color='Medal Count',
    hover_data=['Medal Count'],
    title=f'Most Successful Athlete in Each Discipline ({selected_city})',
    labels={'Athlete': 'Athlete', 'Discipline': 'Discipline'},
    template='plotly_dark'
)

# Bar chart for discipline vs number of medals
discipline_vs_medals_bar_chart = px.bar(
    filtered_data.groupby('Discipline')['Medal'].count().reset_index(),
    x='Discipline',
    y='Medal',
    title=f'Discipline vs Number of Medals in {selected_city}',
    labels={'Discipline': 'Discipline', 'Medal': 'Number of Medals'},
    height=400,
    color='Medal',  # Set color scale to 'Medal' for gradient colors
    color_continuous_scale='Viridis',  # Use Viridis color scale for gradient colors
    template='plotly_dark'
)

# Additional information
additional_info = f"Selected City: {selected_city}, Selected Country: {selected_country}, Selected Medal: {selected_medal}, Medal Threshold: {medal_threshold}"

# Display charts and additional information
st.plotly_chart(discipline_pie_chart)
st.plotly_chart(sport_bar_chart)
st.plotly_chart(medal_bar_chart)
st.plotly_chart(athlete_histogram)
st.plotly_chart(medal_country_pie_chart)
st.plotly_chart(successful_athletes_bar_chart)
st.plotly_chart(athletes_vs_medals_scatter_plot)
st.plotly_chart(bubble_chart)
st.plotly_chart(discipline_vs_medals_bar_chart)
st.write(additional_info)

Objective: 

The objective of our comprehensive study of Olympic data from 1976 to 2008 was to gain insights into global sports performance dynamics. Our analysis focused on athlete, team, and national performance patterns, aiming to identify success factors and challenges. Additionally, we explored changes in training, technology, and socio-political impacts, providing valuable information for national and international sports policies. The project contributes to strategic planning for future Olympics by predicting growth areas and optimizing resource allocation. Talent identification trends assist in refining processes and guiding athlete development programs.

Key Findings:

1.	Most Successful Country (Chart 1):

•	The application allows for a detailed evaluation of the historical performance of countries in specific medal categories.
•	Decision: Tailoring resource allocation based on historical performance trends will enhance strategic planning and 
performance optimization.

2.	Discipline-wise Most Successful Athlete (Chart 2):

•	The visualization aids in identifying key athletes who consistently excel in specific disciplines across different cities.
•	Decision: Focusing talent development programs and strategic planning efforts on these athletes will likely yield positive outcomes.

3.	Medal Count and Gender Distribution (Chart 3):

•	The analysis of medal count by sport and gender distribution provides valuable insights for performance analysis and gender equality initiatives.
•	Decision: Optimize resource allocation, support gender diversity, and strategically plan for upcoming events based on historical performance.

4.	Medal Count vs Sport Discipline (Chart 4):

•	Sports managers can strategically plan for future events by focusing efforts on sports with consistent medal-winning performances.
•	Decision: Allocate resources and develop targeted strategies for sports with proven success, fostering overall performance improvement.

5.	Most Successful Athletes (Chart 5):

•	The histogram helps identify elite athletes based on historical medal counts, aiding in talent development and strategic planning.
•	Decision: Recognize and support elite athletes through sponsorships, endorsements, and targeted training programs.

6.	Discipline vs Number of Medals (Chart 6):

•	Identifying disciplines where countries excel provides valuable information for training programs, talent development, and strategic planning.
•	Decision: Allocate resources strategically, focusing on disciplines with high potential for success.

7.	Most Successful Female Athletes (Chart 7):

•	The application provides insights into successful female athletes, aiding in talent recognition, development, and gender equality initiatives.

•	Decision: Develop targeted programs and partnerships to empower and support successful female athletes.

8.	Medal Distribution Sportwise (Chart 8):

•	The pie chart reveals the popularity of different sports disciplines in terms of medal achievements.
•	Decision: Leverage insights to promote and sponsor disciplines with higher impact and audience engagement.


Conclusion: 

The Dash web application serves as a powerful tool for sports researchers and management companies, offering an interactive and dynamic platform to explore and analyze historical Olympic data. Decision-making based on these analyses can lead to enhanced strategic planning, optimized resource allocation, and targeted development programs. Leveraging historical performance trends provides a competitive advantage, contributing to the overall success of athletes, teams, and nations in future Olympic events. The rich dataset contributes not only to strategic planning but also to academic research, furthering our understanding of sports trends and performance analytics. Embracing data-driven decision-making in the sports industry is essential for creating a lasting legacy and inspiring future generations through the rich history of Olympic competition.


# In[ ]:




