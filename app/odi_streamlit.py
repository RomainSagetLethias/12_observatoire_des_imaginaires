"""
# My first app with Streamlit https://streamlit.io/
Here's our first attempt at using data to create a table:
"""

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt


# O.Importation des librairies nécessaires pour le script
# Core Pkgs - Web application
import streamlit as st
from streamlit_option_menu import option_menu

# Other Pkgs
from PIL import Image
import os
import random

# Datavisualisation
import altair as alt
import plotly.graph_objects as go
import plotly.express as px
import matplotlib.pyplot as plt
from plotly.subplots import make_subplots

import pandas as pd
import numpy as np

import time
import re

import json

# Export fichier
import pickle

# 3.Setup de l'application Streamlit  - Streamlit webpage properties / set up the app with wide view preset and a title
st.set_page_config(
    page_title="Observatoire des Imaginaires", page_icon="herb", layout="wide"
)


@st.cache_data  # 👈 Add the caching decorator
def load_data(file):
    df = pd.read_csv(file, skiprows=1)
    return df


# Load the data
file_path = "../data/AnalyseReponsesTreatedData.csv"  #'../data/Analyse réponses.xlsx - Treated data.csv'
# ne pas lire la première ligne
data = load_data(file_path)


# if 'df' not in st.session_state:
# if 'dico' not in st.session_state:
# if 'liste_ean' not in st.session_state:
# if 'select_editeur' not in st.session_state:
# if 'liste_ouvrage' not in st.session_state:
#
## 1. Classe lancée si choix de "rentrée littéraire" dans le menu en sidebar
# class InfoRentreeLitt():
# 	def get_data(df,dico):


### A. Sidebar
with st.sidebar:
    st.image(
        "https://media.licdn.com/dms/image/D4E0BAQEZHVBxFn3OXQ/company-logo_200_200/0/1697116934909/cercle_thmatique_culture_the_shifters_logo?e=1718841600&v=beta&t=_2DWaEBrblIgXhgVASUipHTcJesOL6s1Sk2uH73Kx58",
        use_column_width=True,
    )  # width=50

    st.title("Fait par la dream team _Analyse de données_")
    st.write(
        "Cette application analyse les données du PoC. On peut se faire plaisir en y ajoutant tous les graphiques nécessaires. "
        + "Le code est à nettoyer pour une meilleure maintenance ;-) "
    )


### B. Container du header
header = st.container()
header.title("Observatoire des Imaginaires")
header.write("""<div class='fixed-header'/>""", unsafe_allow_html=True)

### Custom CSS for the sticky header #74d1b4
# st.markdown(
#    """
# <style>
#    div[data-testid="stVerticalBlock"] div:has(div.fixed-header) {
#        top: 2.875rem;
#    .fixed-header {
#        border-bottom: 1px solid white;
# </style>
#    """,

### C. Container des métriques
cont_metric = st.container(border=True)  # border = True


# Supprimer les lignes où la première colonne contient "Contenu XXX"
# XXX est un nombre
# Et Supprimer les lignes où toutes les valeurs sont NaN
df = data[~data["TITRE"].str.contains(r"Contenu \d+", na=False)].dropna(how="all")

# ne conserver qu'une ligne sur 4  (ce qui revient à supprimer les informations des personnages 2, 3, 4 quand ils existent)
df_truncated = df.iloc[::4]

# Nettoyage du data set

# mettre les titres en majuscule
df_truncated["TITRE"] = df_truncated["TITRE"].str.upper()
# mettre les pays en majuscule et supprimer les espaces au début et à la fin
df_truncated["PAYS"] = df_truncated["PAYS"].str.strip().str.upper()
df_truncated["PAYS"] = df_truncated["PAYS"].apply(lambda p: p.replace(" ET ", ";"))
df_truncated.insert(
    3,
    "pays_rework",
    [
        pays if len(pays.split(";")) == 1 else "INTERNATIONAL"
        for pays in df_truncated["PAYS"]
    ],
)

### Convertir les types de données correctement ici
# Convertir les années en entier
annee = "ANNEE"
df_truncated[annee] = (
    pd.to_numeric(df_truncated[annee], errors="coerce").fillna(0).astype(int)
)

with cont_metric:
    with st.expander("Aperçu des donnéess"):
        st.dataframe(df_truncated)

    ### A. Affichage des métriques macro
    col_nb_livre, col_nb_editeur, col_nb_prem_roman = st.columns([2, 2, 2])
    with col_nb_livre:
        # Metric nb Ouvrages
        st.metric(label="Oeuvres analysées", value=len(set(df_truncated["TITRE"])))
    with col_nb_editeur:
        # Metric nb Editeurs
        st.metric(
            label="Films",
            value=len(set(df_truncated[df_truncated.TYPE == "FILM"]["TITRE"])),
        )
    with col_nb_prem_roman:
        # Metric Premier Roman
        st.metric(
            label="Séries",
            value=len(set(df_truncated[df_truncated.TYPE == "SÉRIE"]["TITRE"])),
        )

    st.write()
    st.write(
        f":blue[{round(100*len(set(df_truncated[df_truncated.TYPE == 'FILM']['TITRE']))/len(set(df_truncated['TITRE'])),2)}%] des contenus renseignés sont des films vs :blue[{round(100*len(set(df_truncated[df_truncated.TYPE == 'SÉRIE']['TITRE']))/len(set(df_truncated['TITRE'])),2)}%] des séries."
    )

# Trouver les titres qui apparaissent plus de 4 fois dans la colonne "TITRE" (car chaque titre a 4 lignes, une pour chaque personnage)


titles_more_than_once = (
    df_truncated.groupby(["TITRE", "TYPE"]).agg(compte=("TITRE", "count")).reset_index()
)
titles_more_than_once = titles_more_than_once[titles_more_than_once["compte"] > 1]


# Afficher un bar chart des titres les plus fréquents
# Affichage d'un bar chart horizontal

with st.container(border=True):
    st.header("Films les plus fréquents")
    col_freq_film_select, col_freq_film_vide, col_freq_film_graph = st.columns(
        [2, 0.5, 5]
    )
    with col_freq_film_select:
        type_choice = st.selectbox(
            "Choisir un type", titles_more_than_once["TYPE"].unique(), index=None
        )
    with col_freq_film_graph:
        if type_choice == "FILM":
            t = titles_more_than_once.loc[
                titles_more_than_once["TYPE"] == "FILM"
            ].sort_values(by="compte", ascending=True)
        elif type_choice == "SÉRIE":
            t = titles_more_than_once.loc[
                titles_more_than_once["TYPE"] == "SÉRIE"
            ].sort_values(by="compte", ascending=True)
        else:
            t = titles_more_than_once.sort_values(by="compte", ascending=True)

        st.bar_chart(t, x="TITRE", y="compte")

# Types de contenus et pays d'origine
with st.container(border=True):
    st.header("Types de contenus")
    col_contenu_date, col_contenu_vide, col_contenu_graph = st.columns([4, 0.5, 4])

    with col_contenu_date:
        date_group_df = (
            df_truncated.groupby("ANNEE")
            .count()
            .reset_index()[["ANNEE", "TITRE"]]
            .rename(columns={"TITRE": "nb_titre"})
        )
        date_group_df["periode_percent"] = 100 * (
            1 - (date_group_df.nb_titre.cumsum() / date_group_df.nb_titre.sum())
        )

        date_min = str(df_truncated.ANNEE.min())
        date_max = str(df_truncated.ANNEE.max())
        date_pareto = date_group_df[date_group_df["periode_percent"] <= 80][
            "ANNEE"
        ].min()
        date_value_pareto = int(
            round(
                date_group_df[date_group_df["periode_percent"] <= 80][
                    "periode_percent"
                ].max(),
                0,
            )
        )

        st.markdown(
            f"Les contenus datent d`une période qui s`étend de {date_min} à {date_max}. {date_value_pareto}% des contenus sont postérieurs à {date_pareto}."
        )

        st.bar_chart(date_group_df, x="ANNEE", y="nb_titre")

    with col_contenu_graph:
        country_group_df = df_truncated
        country_group_df = (
            country_group_df.groupby("pays_rework")
            .count()
            .reset_index()[["pays_rework", "TITRE"]]
            .rename(columns={"TITRE": "nb_titre"})
            .sort_values("nb_titre")
        )
        country_group_df["country_percent_cumul"] = round(
            100
            * (
                1
                - (country_group_df.nb_titre.cumsum() / country_group_df.nb_titre.sum())
            ),
            0,
        )
        country_group_df["country_percent"] = round(
            100 * (country_group_df.nb_titre / country_group_df.nb_titre.sum()), 2
        )

        country_value_pareto = int(
            round(
                country_group_df[country_group_df["country_percent"] >= 10][
                    "country_percent"
                ].sum(),
                2,
            )
        )
        country_group_df_pareto = country_group_df[
            country_group_df["country_percent"] >= 10
        ][["pays_rework", "country_percent"]].sort_values(
            "country_percent", ascending=False
        )

        st.write(
            f"A **:blue[{country_value_pareto}%]**, les 2 principaux pays dont les contenus sont les plus visionnés sont : {country_group_df.nlargest(2,'country_percent').reset_index(drop=True)['pays_rework'][0].capitalize()} ({country_group_df.nlargest(2,'country_percent').reset_index(drop=True)['country_percent'][0]}%) et {country_group_df.nlargest(2,'country_percent').reset_index(drop=True)['pays_rework'][1].capitalize()} ({country_group_df.nlargest(2,'country_percent').reset_index(drop=True)['country_percent'][1]}%)."
        )

        fig_type = px.bar(
            country_group_df,
            y="pays_rework",
            x="nb_titre",
            orientation="h",
            text_auto=True,
        )
        st.plotly_chart(fig_type, use_container_width=True)

# LIEUX VISIONNAGE
with st.container(border=True):
    canal_group_df = (
        df_truncated.groupby("CANAL")
        .count()[["TITRE"]]
        .rename(columns={"TITRE": "nb_titre"})
        .sort_values("nb_titre", ascending=False)
    )
    canal_group_df["canal_percent"] = 100 * (
        canal_group_df.nb_titre / canal_group_df.nb_titre.sum()
    )
    canal_country_group_df = (
        df_truncated.groupby(["CANAL", "pays_rework"])
        .count()[["TITRE"]]
        .rename(columns={"TITRE": "nb_titre"})
        .sort_values("nb_titre", ascending=False)
        .reset_index()
    )

    col_text_canal, col_table_canal = st.columns([5, 3])
    with col_text_canal:
        canal_visionne1 = canal_group_df.nb_titre.nlargest(2).reset_index()["CANAL"][0]
        percent_canal_visionne1 = round(canal_group_df.canal_percent.nlargest(2)[0], 2)
        canal_visionne2 = canal_group_df.nb_titre.nlargest(2).reset_index()["CANAL"][1]
        percent_canal_visionne2 = round(canal_group_df.canal_percent.nlargest(2)[1], 2)

        st.markdown(
            f"Les contenus sont visionnés principalement sur :blue[{canal_visionne1.capitalize()}] (:blue[{percent_canal_visionne1}%]) et :blue[{canal_visionne2.capitalize()}] (:blue[{percent_canal_visionne2}%]).\n\n La majorité des contenus visionnés sur :blue[{canal_visionne1.capitalize()}] ont pour pays d'origine :blue[{canal_country_group_df[canal_country_group_df['CANAL']==canal_visionne1].nlargest(1,'nb_titre').reset_index()['pays_rework'][0]}] (:blue[%]), alors que la majorité des contenus français sont visionnés xxx (xxx%).\n\n :blue[{round(canal_group_df.loc['Autre','canal_percent'],2)}%] des contenus sont visionnés sur un canal `Autre` que la liste proposée (cf ci-contre)"
        )

        # Les contenus sont visionnés principalement sur Netflix (29.91%) ou dans une salle de cinéma (28.97%). La majorité des contenus américains sont visionnés sur Netflix (40.48% des contenus US), alors que la majorité des contenus français sont visionnés au cinéma (44.19%).
    # 23.36% des contenus sont visionnés sur un canal `autre` que la liste proposée (cf ci-dessous)

    with col_table_canal:
        st.markdown(set(canal_group_df.reset_index().CANAL))

st.subheader("EPOQUE DE RECITS")
st.write(set(df_truncated["EPOQUE DU RECIT"]))

st.subheader("TYPE DE MONDE")
st.write(set(df_truncated["TYPE DE MONDE"]))
st.dataframe(
    df_truncated[["TITRE", "TRAITEMENT DU RECIT", "TYPE DE MONDE"]]
    .groupby(["TRAITEMENT DU RECIT", "TYPE DE MONDE"])
    .count()
)

# 				st.write(f"Parmi les ouvrages parus et écrits par des autrices, **:blue[{int(round(st.session_state['roman_francais'][st.session_state['roman_francais']['Genre']==selection]['Nb ouvrages'].sum()/len(liste_ean)*100,0))}%]** sont des romans français, **:blue[{int(round(st.session_state['roman_etranger'][st.session_state['roman_etranger']['Genre']==selection]['Nb ouvrages'].sum()/len(liste_ean)*100,0))}%]** des romans étrangers et **:blue[{int(round(st.session_state['essais'][st.session_state['essais']['Genre']==selection]['Nb ouvrages'].sum()/len(liste_ean)*100,0))}%]** des essais.")
#
# 				with st.container():

# fig = plt.subplot()
#
# fig.add_trace(go.Pie(labels=country_group_df.pays_rework, values=country_group_df.nb_titre, name="Countries"))
# fig.add_trace(go.Pie(labels=gender_viz_crew.gender_text, values=gender_viz_crew.nb_by_genre, name="Equipe tech"),
#              1, 2)
#
# colors0 = ['red' if x == 1 else 'blue' if x == 2 else 'green' if x == 0 else 'grey' for x in gender_viz_cast['gender']]
# colors1 = ['red' if x == 1 else 'blue' if x == 2 else 'green' if x == 0 else 'grey' for x in gender_viz_crew['gender']]
#
# fig.update_traces(hole=.4, hoverinfo="label+value+name",marker=dict(colors=colors0)) # Use `hole` to create a donut-like pie chart&
#
# fig.update_traces(hole=.4, hoverinfo="label+value+name")#,marker=dict(colors=colors1), col=2)
#
# fig.update_layout(width = 400,
# 			margin=dict(t=0, b=0, l=0, r=0),)
# legend=dict(
# 	orientation="h",
# 	yanchor="bottom",
# 	y=0.05,
# 	xanchor="right",
# 	x=1),
# title=dict(text="Répartition par genre",y=0.9,),
# Add annotations in the center of the donut pies.
# annotations=[dict(text='Casting', x=0.15, y=0.5, font_size=20, showarrow=False),
#             dict(text='Crew', x=0.83, y=0.5, font_size=20, showarrow=False)])
#
# 		st.plotly_chart(fig)
#
# 		fig1 = go.Figure(
#    data=[go.Bar(x=country_group_df.pays_rework ,
# 				 y=country_group_df.nb_titre)])
#
# 		#colinfofilm.write("Répartition par genre de l'équipe technique")
# 		with colinfofilm.expander("Table de données"):
# 			st.write("Casting")
# 			st.dataframe(gender_viz_cast)
# 			st.write("Equipe technique")
# 			st.dataframe(gender_viz_crew)
# 	placeholderviz.empty()
