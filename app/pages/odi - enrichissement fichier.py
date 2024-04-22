"""
# App with Streamlit https://streamlit.io/ 
Pour enrichir le fichier de réponses au questionnaire
"""
### A.Importation des librairies nécessaires pour le script

#Core Pkgs - Web application
import streamlit as st
from streamlit_option_menu import option_menu

#Other Pkgs
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import re
import requests

import pandas as pd
import numpy as np

import os
import random 


import time

import json

#Export fichier
import pickle
import pyarrow.parquet as pq

######################################
### B.Setup de l'application Streamlit  - Streamlit webpage properties / set up the app with wide view preset and a title
st.set_page_config(page_title="MUBI x TMDB", page_icon="cinema", layout="wide")


if "header_tmdb" not in st.session_state:
	#pour appeler l'API TMDB avec le token
    st.session_state["header_tmdb"] = ''

if "film_choice_MUBI" not in st.session_state:
	#ici on veut conserver le film choisi
    st.session_state["film_choice_MUBI"] = ''
	
if "list_film_choice_MUBI" not in st.session_state:
	# pour générer la iste de films choisis
	st.session_state["list_film_choice_MUBI"] = []

######################################
### C.Chargement des datasets
@st.cache_data
def load_header_tmdb():
	with  open("secret/TMDB.txt", "r") as file:
	    file_lines = file.read().split('\n')
	header_tmdb = [token.split(':') for token in file_lines][0][1].replace('/n','')
	return header_tmdb

st.session_state["header_tmdb"] = {
	    "accept": "application/json",
	    "Authorization": f"Bearer {load_header_tmdb()}"
	}

headers = st.session_state["header_tmdb"]

# C.1.1 Load the data tmdb Movie
@st.cache_data  # 👈 Add the caching decorator # Reading from a Parquet file # #pd.read_csv(file) 
def load_data_tmdb(tmdb):
	df = pd.read_parquet(tmdb)
	return df

file_path_tmdb = 'data/TMDB_movie_dataset_v11.parquet.gzip' #'data/TMDB_movie_dataset_v11.csv'

if "tmdb_data" not in st.session_state:
    st.session_state["tmdb_data"] = load_data_tmdb(file_path_tmdb)
tmdb_df = st.session_state["tmdb_data"][st.session_state["tmdb_data"]['adult']==False]


#C.1.2 Load the data tmdb TV Show
@st.cache_data  # 👈 Add the caching decorator # Reading from a Parquet file # #pd.read_csv(file) 
def load_data_tmdb_tv(tmdb):
	df = pd.read_csv(tmdb, sep=',')
	return df

file_path_tmdb_tv = 'data/TMDB_tv_dataset_v3.csv' #'data/TMDB_movie_dataset_v11.csv'

if "tmdb_data_tv" not in st.session_state:
    st.session_state["tmdb_data_tv"] = load_data_tmdb_tv(file_path_tmdb_tv)
	
tmdb_df_tv = st.session_state["tmdb_data_tv"][st.session_state["tmdb_data_tv"]['adult']==False]

tmdb_df_tv['name'] = tmdb_df_tv['name'].str.upper()
tmdb_df_tv.insert(0,'year_first_air',tmdb_df_tv['first_air_date'].apply(lambda y : int(str(y).split('-')[0]) if str(y)!='nan' else y))
tmdb_df_tv.insert(1,'year_last_air',tmdb_df_tv['last_air_date'].apply(lambda y : int(str(y).split('-')[0]) if str(y)!='nan' else y))


#C.2 Load the data mubi
@st.cache_data  # 👈 Add the caching decorator
def load_data_mubi(mubi):
	df = pd.read_csv(mubi, sep=";", encoding='utf8')
	df = df.sort_values(by='title')
	return df
	
file_path_mubi = 'data/liste_des_films_laureatsrenommee_tmdb_id_ARCHIVES_18_AVRIL_2024.csv'
#'liste_des_films_laureatsrenommee_tmdb_id.csv' 'soup_mubi_avril_2024.csv'


if "mubi_data" not in st.session_state:
    st.session_state["mubi_data"] = load_data_mubi(file_path_mubi)
mubi_df = st.session_state["mubi_data"]


#C.3 Load the data questionnaire ODI
@st.cache_data  # 👈 Add the caching decorator
def load_data(file: str) -> pd.DataFrame:
    df = pd.read_csv(file)
    return df
	
file_path_odi = './data/Etape 1 Identification du film - Feuille 1.csv'

### Colonnes à ajouter
	#Année de sortie - release_year
	#Nationalité -production_countries
	#Genre - genres
	#Entreprise de production - production_companies
	#TMDB User Score - vote_average|popularity ?
	#budget à ajouter ?
	#Box Office - Allociné ?
	

if "odi_data" not in st.session_state:
	st.session_state["odi_data"] = load_data(file_path_odi)
	
	### Enrichissement avec données TMDB : metadonnées du film
	st.session_state["odi_data"] = pd.merge(st.session_state["odi_data"], st.session_state["tmdb_data"][["id", "release_year","production_countries","genres","production_companies", "popularity","vote_average"]], how='left',  left_on="id_tmdb", right_on="id")

	### Enrichissement avec données MUBI : liste des prix
	group_df = mubi_df.groupby('tmbd_id').agg(nb_recompense=('festival','count'),
                          liste_festival=('festival', list)).reset_index()
	
	st.session_state["odi_data"] = pd.merge(st.session_state["odi_data"],group_df , how='left',  left_on="id_tmdb", right_on="tmbd_id")


@st.cache_data
def tmdb_imdb_box_of(id):
    #Je construis un dataframe vide
    box_of_fr = pd.DataFrame(columns=['id_tmdb','Opening','Gross'])
    list=[]
    #Pour un ID TMDB donnée je cherche l'ID IMDB correspondant
    url_tmdb_ext_id = f"https://api.themoviedb.org/3/movie/{id}/external_ids"
    response_ext_id = requests.get(url_tmdb_ext_id, headers=headers)

    if response_ext_id.status_code == 200:
        id_imdb = json_data_ext_id = response_ext_id.json()['imdb_id']

    #Si j'ai un id IMDB, je recherche la liste de box office mondiaux
    url_mojo = f"https://www.boxofficemojo.com/title/{id_imdb}/"
    box_of_fr_temp = pd.concat(pd.read_html(url_mojo),axis=0)

    if len(box_of_fr_temp)>0 and 'Area' in box_of_fr_temp.columns:
        box_of_fr_temp = box_of_fr_temp[box_of_fr_temp['Area'] == "France"]
        box_of_fr_temp["Opening"] = box_of_fr_temp["Opening"].apply(lambda o : int(o.replace("$", "").replace(",", "")))
        box_of_fr_temp["Gross"] = box_of_fr_temp["Gross"].apply(lambda o : int(o.replace("$", "").replace(",", "")))
        box_of_fr_temp['id_tmdb'] = str(id)
        box_of_fr_temp = box_of_fr_temp[['id_tmdb','Opening','Gross']]
        list.append(box_of_fr_temp)
        
    elif len(box_of_fr_temp)>0 and 'EMEA' in box_of_fr_temp.columns:
        box_of_fr_temp = box_of_fr_temp[box_of_fr_temp['EMEA'] == "France"]
        box_of_fr_temp["Lifetime Gross"] = box_of_fr_temp["Lifetime Gross"].apply(lambda o : int(o.replace("$", "").replace(",", "")))
        box_of_fr_temp['id_tmdb'] = str(id)
        box_of_fr_temp["Opening"] = None
        box_of_fr_temp = box_of_fr_temp[['id_tmdb','Opening','Lifetime Gross']].rename(columns={'Lifetime Gross':'Gross'})
        list.append(box_of_fr_temp)  

    return box_of_fr_temp
	
@st.cache_data
def box_of_fr():
	box_of_fr = pd.DataFrame()
	
	for df in st.session_state["odi_data"]["id_tmdb"].apply(lambda i: tmdb_imdb_box_of(i)):
	    box_of_fr = box_of_fr._append(df)

	st.dataframe(box_of_fr)

	return box_of_fr

### Enrichissement avec données IMDB - MOJO  : box office français
st.session_state["odi_data"] = pd.merge(st.session_state["odi_data"], box_of_fr(), how='left',  on="id_tmdb")


odi_df = st.session_state["odi_data"]

######################################
### D. Container du header
header = st.container(border = True)
header.title("Observatoire des Imaginaires")
header.write("""<div class='fixed-header'/>""", unsafe_allow_html=True)
header.subheader("Pour enrichir le fichier d'analyse")

######################################
### E. Container des dataframes
cont_dataframe = st.container(border = True)

with cont_dataframe:
	col_tmdb, col_questionnaire = st.columns(2)

	with col_tmdb.expander("Aperçu des données - Movies") :
		tmdb_df.sort_values('title')
		st.dataframe(tmdb_df.head())

	with col_tmdb.expander("Aperçu des données - Movies") :
		tmdb_df_tv.sort_values('name')
		st.dataframe(tmdb_df_tv.head())
		
	with col_questionnaire.expander("Aperçu des données - Mubi Awards") :
		mubi_df.sort_values('title_utf')
		st.dataframe(mubi_df.head())
		
	with col_questionnaire.expander("Aperçu des données - Réponse Questionaires") :
		st.dataframe(odi_df.head())
				

######################################
### 
award = []
with st.container(border = True):
	group_df = mubi_df.groupby('tmbd_id').agg(nb_recompense=('festival','count'),
                          liste_festival=('festival', list)).reset_index()
	st.write(group_df)

	
