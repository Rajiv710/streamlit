{
  "nbformat": 4,
  "nbformat_minor": 0,
  "metadata": {
    "colab": {
      "name": "Covid_app.ipynb",
      "provenance": [],
      "authorship_tag": "ABX9TyMEo1gwBiyW5JiUinmtrQXC",
      "include_colab_link": true
    },
    "kernelspec": {
      "name": "python3",
      "display_name": "Python 3"
    }
  },
  "cells": [
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "view-in-github",
        "colab_type": "text"
      },
      "source": [
        "<a href=\"https://colab.research.google.com/github/Rajiv710/streamlit/blob/main/Covid_app.py\" target=\"_parent\"><img src=\"https://colab.research.google.com/assets/colab-badge.svg\" alt=\"Open In Colab\"/></a>"
      ]
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "coEB8ZbJ5XHW"
      },
      "source": [
        "import streamlit as st\n",
        "import pandas as pd\n",
        "import datetime\n",
        "import matplotlib.pyplot as plt\n",
        "import seaborn as sns\n",
        "st.title('COVID 19 DATA ANALYSIS')\n",
        " \n",
        "data= 'https://raw.githubusercontent.com/datasets/covid-19/master/data/countries-aggregated.csv'\n",
        "df = pd.read_csv(data)\n",
        " \n",
        "df['Active cases'] = df['Confirmed'] - (df['Recovered'] + df['Deaths'])\n",
        "df['Daily cases'] = df.groupby(['Country'])['Confirmed'].diff().fillna(df['Confirmed'])\n",
        " \n",
        "df['Date'] = pd.to_datetime(df['Date'])\n",
        " \n",
        "a = df.groupby(['Country'])['Confirmed'].max().sort_values(ascending = False).head()\n",
        " \n",
        "highest = None\n",
        " \n",
        " \n",
        "for i in a.index:\n",
        "  if highest is None:\n",
        "    highest =  df[ df['Country']== i ]\n",
        "  else:\n",
        "    x = df[ df['Country']== i ]\n",
        "    highest= highest.merge(x,how='outer')\n",
        " \n",
        "b = highest.groupby(['Country'])['Deaths'].max()\n",
        "c = highest.groupby(['Country'])['Recovered'].max()\n",
        "maxi = pd.DataFrame({'Total cases': a, 'Total Recovered':c,'Total deaths': b })\n",
        "maxi.sort_values(by = ['Total cases'],inplace = True, ascending = False)\n",
        "\n",
        "idx = df.groupby(['Country'])['Confirmed'].transform(max) == df['Confirmed']\n",
        "Latest =df[idx]\n",
        "Latest= Latest.drop_duplicates(subset = 'Confirmed', keep ='last')\n",
        "Latest.reset_index(inplace = True)\n",
        "Latest['Date']= Latest['Date'].dt.date\n",
        "\n",
        "\n",
        "if st.button(' top 5 '):\n",
        "  fig,ax = plt.subplots()\n",
        "  maxi.plot.bar(figsize = (16,7), fontsize = 21, color = {'Total cases':'#FFA500','Total Recovered':'g','Total deaths':'r'} ,ax=ax)\n",
        "  plt.title( 'TOP 5 WROST AFFECTED COUNTRIES\\n(By total cases)',fontsize = 30)\n",
        "  plt.ylabel('No. of people',fontsize = 21)\n",
        "  plt.xlabel('Countries',fontsize = 21)\n",
        "  st.pyplot(fig)\n",
        "\n",
        "if st.checkbox('Check info'):\n",
        "  y = st.selectbox('Select country:',Latest['Country'])\n",
        "  Country = y\n",
        "  if st.button('Go'):\n",
        "    \n",
        "    Latest_date =Latest.loc[Latest['Country']==y]['Date'].values\n",
        "    confirmed =  Latest.loc[Latest['Country']==y]['Confirmed'].values\n",
        "    recovered =Latest.loc[Latest['Country']==y]['Recovered'].values\n",
        "    deaths =Latest.loc[Latest['Country']==y]['Deaths'].values\n",
        "    act_case =Latest.loc[Latest['Country']==y]['Active cases'].values\n",
        "    daily =Latest.loc[Latest['Country']==y]['Daily cases'].values\n",
        "    st.write('Country = ',y,'  \\n''Latest date = ', Latest_date[0],'  \\n''Total Cases = ',+confirmed[0],'  \\n''Total Recovered =',+recovered[0],'  \\n''Total Deaths = ',+deaths[0],'  \\n''Active cases = ',+act_case[0],'  \\n''New cases = ',+daily[0])\n",
        "\n",
        "    fig_dims = (18,6)\n",
        "    fig, ax = plt.subplots(figsize=fig_dims)\n",
        "    sns.lineplot(x = 'Date', y = 'Daily cases', hue = 'Country',data = df[(df.Country == y)],ax=ax)\n",
        "    sns.set_context('talk')\n",
        "    plt.title('Daily cases Timeline  ', fontsize = 24)\n",
        "    st.pyplot(fig)\n",
        "\n",
        "if st.button('Most Active cases'):\n",
        "  fig,ax = plt.subplots()\n",
        "  active = df.groupby(['Country'])['Active cases'].max().sort_values(ascending = False).head(6)\n",
        "  active.plot(figsize =(12,6), kind = 'bar',fontsize = 18,color = {'r','b','y','#FFA500','g'},ax=ax)\n",
        "  plt.title( 'Most Active cases',fontsize = 30)\n",
        "  plt.ylabel('No. of people (in millions)',fontsize = 21)\n",
        "  plt.xlabel('Countries',fontsize = 21)\n",
        "  st.pyplot(fig)\n",
        "\n",
        "if st.button('peak of various countries'):\n",
        "  idx = df.groupby(['Country'])['Daily cases'].transform(max) == df['Daily cases']\n",
        "  Max_daily_cases = df[idx]\n",
        "  M = Max_daily_cases.sort_values(by = ['Daily cases'],ascending =False).head(8)\n",
        "  fig,ax = plt.subplots()\n",
        "  sns.scatterplot(x = 'Date', y = 'Daily cases', hue = 'Country', data = M, s = 190,ax=ax)\n",
        "  sns.set(rc={'figure.figsize':(18,5)})\n",
        "  sns.set_context('paper')\n",
        "  plt.title('Peak of various countries',fontsize = 28)\n",
        "  plt.ylabel('Daily Cases',fontsize = 21)\n",
        "  plt.xlabel('Date',fontsize = 21)\n",
        "  st.pyplot(fig)\n"
      ],
      "execution_count": null,
      "outputs": []
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "Bm6ekcaT9PE8"
      },
      "source": [
        ""
      ],
      "execution_count": null,
      "outputs": []
    }
  ]
}