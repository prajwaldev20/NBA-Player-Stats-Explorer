import streamlit as st
import pandas as pd
import base64
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np


st.title("NBA Player Stats Explorer")

st.markdown("""
            This app performs simple webscrapping of NBA players stats data!
            * **Python libraries:** base64, pandas , streamlit
            * **Data Source:** [Basketball-reference.com](https://www.basketball-reference.com/).
            """)

st.sidebar.header("User Input Features")
selected_year = st.sidebar.selectbox('Year', list(reversed(range(2000,2025))))

# Web scraping of NBA player Stats
@st.cache_data
def load_data(year):
    #url = "https://www.basketball-reference.com/leagues/NBA_{year}_advanced.html"
    url = "https://www.basketball-reference.com/leagues/NBA_" + str(year) + "_advanced.html"

    html = pd.read_html(url, header = 0)
    df =html[0]
    raw = df.drop(df[df.Age == 'Age'].index)
    raw = raw.fillna(0)
    playerstats = raw.drop(['Rk'], axis =1)
    return playerstats
playerstats = load_data(selected_year)

# Sidebar - Team Selection
sorted_unique_team = sorted(playerstats.Team.unique(), key=str)
selected_team = st.sidebar.multiselect('Team', sorted_unique_team, sorted_unique_team)

# Sidebar - Position selection
unique_pos = ['C','PF','SF','PG','SG']
selected_pos = st.sidebar.multiselect('Position', unique_pos, unique_pos)

# Filtering data
df_selected_team = playerstats[(playerstats.Team.isin(selected_team)) & (playerstats.Pos.isin(selected_pos))]

st.header('Display Player Stats of Selected Team(s)')
st.write('Data Dimension: ' + str(df_selected_team.shape[0]) + ' rows and ' + str(df_selected_team.shape[1]) + ' columns.')
st.dataframe(df_selected_team)

def filedownload(df):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # strings <-> bytes conversions
    href = f'<a href="data:file/csv;base64,{b64}" download="playerstats.csv">Download CSV File</a>'
    return href

st.markdown(filedownload(df_selected_team), unsafe_allow_html=True)

# Heatmap
if st.button('Intercorrelation Heatmap'):
    st.header('Intercorrelation Matrix Heatmap')

    # Select only numeric columns
    numeric_df = df_selected_team.select_dtypes(include=[np.number])

    # Compute the correlation matrix
    corr = numeric_df.corr()

    # Create a mask for the upper triangle
    mask = np.triu(np.ones_like(corr, dtype=bool))

    # Set up the matplotlib figure
    f, ax = plt.subplots(figsize=(10, 8))  # Adjust figure size for better readability

    # Draw the heatmap
    sns.heatmap(
        corr,
        mask=mask,
        cmap="coolwarm",
        vmax=1,
        vmin=-1,
        center=0,
        square=True,
        annot=True,  # Display correlation values
        fmt=".2f",  # Format correlation values to 2 decimal places
        linewidths=0.5,  # Add gridlines for better separation
        cbar_kws={"shrink": 0.75},  # Shrink color bar size
    )

    # Display the heatmap
    st.pyplot(f)

