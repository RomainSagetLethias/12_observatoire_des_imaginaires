"""
# Application pour l'Observateur des Imaginaires
"""


# Export fichier

# Datavisualisation

import pandas as pd
import plotly.express as px

# O.Importation des librairies nécessaires pour le script
# Core Pkgs - Web application
import streamlit as st

# Other Pkgs

# 3.Setup de l'application Streamlit  - Streamlit webpage properties / set up the app
# with wide view preset and a title
st.set_page_config(
    page_title="Observatoire des Imaginaires",
    page_icon="herb",
    layout="wide",
)


@st.cache_data  # 👈 Add the caching decorator
def load_data(file: str) -> pd.DataFrame:
    df = pd.read_csv(file)
    return df


# Load the data
# TODO connect to Google Sheet and load data 
file_path = "https://raw.githubusercontent.com/dataforgoodfr/12_observatoire_des_imaginaires/analyse/streamlit_app_v2/data/Etape%201%20Identification%20du%20film%20-%20Feuille%201.csv"  
# ne pas lire la première ligne
data = load_data(file_path)

# Renommer les noms de colonnes (utile si le fichier d'entrée change de noms de colonnes)
# Renommer la colonne
data.rename(columns={'title': 'TITRE'}, inplace=True)


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
        (
            "Cette application analyse les données du sondage de **l'Observatoire des Imaginaires**. "
        ),
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
# TODO est-ce encore utile ? 
df = data[~data["TITRE"].str.contains(r"Contenu \d+", na=False)].dropna(how="all")

# ne conserver qu'une ligne sur 4  (ce qui revient à supprimer
# les informations des personnages 2, 3, 4 quand ils existent)
##df_truncated = df.iloc[::4]

# Nettoyage du data set

# mettre les titres en majuscule
df["TITRE"] = df["TITRE"].str.upper()
# mettre les pays en majuscule et supprimer les espaces au début et à la fin
st.dataframe(df)

# TODO    ------    reprendre ce code quand les données sont enrichies avec les informations du film


# df_truncated["PAYS"] = df_truncated["PAYS"].str.strip().str.upper()
# df_truncated["PAYS"] = df_truncated["PAYS"].apply(lambda p: p.replace(" ET ", ";"))
# df_truncated.insert(
#     3,
#     "pays_rework",
#     [
#         pays if len(pays.split(";")) == 1 else "INTERNATIONAL"
#         for pays in df_truncated["PAYS"]
#     ],
# )

### Convertir les types de données correctement ici
# Convertir les années en entier
# annee = "ANNEE"
# df_truncated[annee] = (
#     pd.to_numeric(df_truncated[annee], errors="coerce").fillna(0).astype(int)
# ) 


# with cont_metric:
#     with st.expander("Aperçu des donnéess"):
#         st.dataframe(df_truncated)

#     ### A. Affichage des métriques macro
#     col_nb_livre, col_nb_editeur, col_nb_prem_roman = st.columns([2, 2, 2])
#     with col_nb_livre:
#         # Metric nb Ouvrages
#         st.metric(label="Oeuvres analysées", value=len(set(df_truncated["TITRE"])))
#     with col_nb_editeur:
#         # Metric nb Editeurs
#         st.metric(
#             label="Films",
#             value=len(set(df_truncated[df_truncated.TYPE == "FILM"]["TITRE"])),
#         )
#     with col_nb_prem_roman:
#         # Metric Premier Roman
#         st.metric(
#             label="Séries",
#             value=len(set(df_truncated[df_truncated.TYPE == "SÉRIE"]["TITRE"])),
#         )

#     st.write()
#     st.write(
#         f":blue[{round(100*len(set(df_truncated[df_truncated.TYPE == 'FILM']['TITRE']))/len(set(df_truncated['TITRE'])),2)}%] des contenus renseignés sont des films vs :blue[{round(100*len(set(df_truncated[df_truncated.TYPE == 'SÉRIE']['TITRE']))/len(set(df_truncated['TITRE'])),2)}%] des séries.",  # noqa: E501
#     )

# Trouver les titres qui apparaissent plus de 4 fois dans la colonne "TITRE"
# (car chaque titre a 4 lignes, une pour chaque personnage)


# titles_more_than_once = (
#     df_truncated.groupby(["TITRE", "TYPE"]).agg(compte=("TITRE", "count")).reset_index()
# )
# titles_more_than_once = titles_more_than_once[titles_more_than_once["compte"] > 1]


# Afficher un bar chart des titres les plus fréquents
# Affichage d'un bar chart horizontal


# with st.container(border=True):
#     st.header("Productions les plus fréquentes")
#     col_freq_film_select, col_freq_film_vide, col_freq_film_graph = st.columns(
#         [2, 0.5, 5],
#     )
#     with col_freq_film_select:
#         type_choice = st.selectbox(
#             "Choisir un type",
#             titles_more_than_once["TYPE"].unique(),
#             index=None,
#         )
#     with col_freq_film_graph:
#         if type_choice == "FILM":
#             t = titles_more_than_once.loc[
#                 titles_more_than_once["TYPE"] == "FILM"
#             ].sort_values(
#                 by="compte",
#                 ascending=True,
#             )
#         elif type_choice == "SÉRIE":
#             t = titles_more_than_once.loc[
#                 titles_more_than_once["TYPE"] == "SÉRIE"
#             ].sort_values(
#                 by="compte",
#                 ascending=True,
#             )
#         else:
#             t = titles_more_than_once.sort_values(by="compte", ascending=True)

#         st.bar_chart(t, x="TITRE", y="compte")

# # Types de contenus et pays d'origine
# with st.container(border=True):
#     st.header("Types de contenus")
#     col_contenu_date, col_contenu_vide, col_contenu_graph = st.columns([4, 0.5, 4])

#     with col_contenu_date:
#         date_group_df = (
#             df_truncated.groupby("ANNEE")
#             .count()
#             .reset_index()[["ANNEE", "TITRE"]]
#             .rename(columns={"TITRE": "nb_titre"})
#         )
#         date_group_df["periode_percent"] = 100 * (
#             1 - (date_group_df.nb_titre.cumsum() / date_group_df.nb_titre.sum())
#         )

#         date_min = str(df_truncated.ANNEE.min())
#         date_max = str(df_truncated.ANNEE.max())
#         date_pareto = (
#             date_group_df[date_group_df["periode_percent"] <= 80]["ANNEE"].min()  # noqa: PLR2004
#         )
#         date_value_pareto = int(
#             round(
#                 date_group_df[date_group_df["periode_percent"] <= 80][  # noqa: PLR2004
#                     "periode_percent"
#                 ].max(),
#                 0,
#             ),
#         )

#         st.markdown(
#             (
#                 f"Les contenus datent d'une période qui s'étend de {date_min}"
#                 f" à {date_max}. {date_value_pareto}% des contenus sont postérieurs à"
#                 f" {date_pareto}."
#             ),
#         )

#         st.bar_chart(date_group_df, x="ANNEE", y="nb_titre")

#     with col_contenu_graph:
#         country_group_df = df_truncated
#         country_group_df = (
#             country_group_df.groupby("pays_rework")
#             .count()
#             .reset_index()[["pays_rework", "TITRE"]]
#             .rename(columns={"TITRE": "nb_titre"})
#             .sort_values("nb_titre")
#         )
#         country_group_df["country_percent_cumul"] = round(
#             100
#             * (
#                 1
#                 - (country_group_df.nb_titre.cumsum() / country_group_df.nb_titre.sum())
#             ),
#             0,
#         )
#         country_group_df["country_percent"] = round(
#             100 * (country_group_df.nb_titre / country_group_df.nb_titre.sum()),
#             2,
#         )

#         country_value_pareto = int(
#             round(
#                 country_group_df[country_group_df["country_percent"] >= 10][  # noqa: PLR2004
#                     "country_percent"
#                 ].sum(),
#                 2,
#             ),
#         )
#         country_group_df_pareto = country_group_df[
#             country_group_df["country_percent"] >= 10  # noqa: PLR2004
#         ][["pays_rework", "country_percent"]].sort_values(
#             "country_percent",
#             ascending=False,
#         )

#         st.write(
#             f"A **:blue[{country_value_pareto}%]**, les 2 principaux pays dont les contenus sont les plus visionnés sont : {country_group_df.nlargest(2,'country_percent').reset_index(drop=True)['pays_rework'][0].capitalize()} ({country_group_df.nlargest(2,'country_percent').reset_index(drop=True)['country_percent'][0]}%) et {country_group_df.nlargest(2,'country_percent').reset_index(drop=True)['pays_rework'][1].capitalize()} ({country_group_df.nlargest(2,'country_percent').reset_index(drop=True)['country_percent'][1]}%).",  # noqa: E501
#         )

#         fig_type = px.bar(
#             country_group_df,
#             y="pays_rework",
#             x="nb_titre",
#             orientation="h",
#             text_auto=True,
#         )
#         st.plotly_chart(fig_type, use_container_width=True)

# # LIEUX VISIONNAGE
# with st.container(border=True):
#     canal_group_df = (
#         df_truncated.groupby("CANAL")
#         .count()[["TITRE"]]
#         .rename(columns={"TITRE": "nb_titre"})
#         .sort_values("nb_titre", ascending=False)
#     )
#     canal_group_df["canal_percent"] = 100 * (
#         canal_group_df.nb_titre / canal_group_df.nb_titre.sum()
#     )
#     canal_country_group_df = (
#         df_truncated.groupby(["CANAL", "pays_rework"])
#         .count()[["TITRE"]]
#         .rename(columns={"TITRE": "nb_titre"})
#         .sort_values("nb_titre", ascending=False)
#         .reset_index()
#     )

#     col_text_canal, col_table_canal = st.columns([5, 3])
#     with col_text_canal:
#         canal_visionne1 = canal_group_df.nb_titre.nlargest(2).reset_index()["CANAL"][0]
#         percent_canal_visionne1 = round(canal_group_df.canal_percent.nlargest(2)[0], 2)
#         canal_visionne2 = canal_group_df.nb_titre.nlargest(2).reset_index()["CANAL"][1]
#         percent_canal_visionne2 = round(canal_group_df.canal_percent.nlargest(2)[1], 2)

#         st.markdown(
#             f"Les contenus sont visionnés principalement sur :blue[{canal_visionne1.capitalize()}] (:blue[{percent_canal_visionne1}%]) et :blue[{canal_visionne2.capitalize()}] (:blue[{percent_canal_visionne2}%]).\n\n La majorité des contenus visionnés sur :blue[{canal_visionne1.capitalize()}] ont pour pays d'origine :blue[{canal_country_group_df[canal_country_group_df['CANAL']==canal_visionne1].nlargest(1,'nb_titre').reset_index()['pays_rework'][0]}] (:blue[%]), alors que la majorité des contenus français sont visionnés xxx (xxx%).\n\n :blue[{round(canal_group_df.loc['Autre','canal_percent'],2)}%] des contenus sont visionnés sur un canal `Autre` que la liste proposée (cf ci-contre)",  # noqa: E501
#         )

#         # Les contenus sont visionnés principalement sur Netflix (29.91%) ou dans
#         # une salle de cinéma (28.97%). La majorité des contenus américains sont
#         # visionnés sur Netflix (40.48% des contenus US), alors que la majorité
#         # des contenus français sont visionnés au cinéma (44.19%).
#     # 23.36% des contenus sont visionnés sur un canal `autre`
#     # que la liste proposée (cf ci-dessous)

#     with col_table_canal:
#         st.markdown(set(canal_group_df.reset_index().CANAL))

# st.subheader("EPOQUE DE RECITS")
# st.write(set(df_truncated["EPOQUE DU RECIT"]))

# st.subheader("TYPE DE MONDE")
# st.write(set(df_truncated["TYPE DE MONDE"]))
# st.dataframe(
#     df_truncated[["TITRE", "TRAITEMENT DU RECIT", "TYPE DE MONDE"]]
#     .groupby(["TRAITEMENT DU RECIT", "TYPE DE MONDE"])
#     .count(),
# )


# TODO   FIN  ------    reprendre ce code quand les données sont enrichies avec les informations du film

#
# 				with st.container():

#
# fig.add_trace(go.Pie(labels=gender_viz_crew.gender_text, values=gender_viz_crew.nb_by_genre, name="Equipe tech"),  # noqa: E501
#              1, 2)
#
#
#
#
# fig.update_layout(width = 400,
# 			margin=dict(t=0, b=0, l=0, r=0),)
# 	x=1),
# Add annotations in the center of the donut pies.
# annotations=[dict(text='Casting', x=0.15, y=0.5, font_size=20, showarrow=False),
#             dict(text='Crew', x=0.83, y=0.5, font_size=20, showarrow=False)])
#
#
#    data=[go.Bar(x=country_group_df.pays_rework ,
# 				 y=country_group_df.nb_titre)])
#
# 		with colinfofilm.expander("Table de données"):

def prepare_technology_data(data, colname_id):
    """
    Extracts and prepares technology-related data for analysis from multiple characters.
    
    Parameters:
        data (DataFrame): The original dataset containing technology tools and demographic information for characters.
        colname_id (String): Part of the column name for which we want to do the analysis, e.g. 'gender'.
    
    Returns:
        DataFrame: A long-format DataFrame ready for analysis and visualization.
    """
    # Technology tools as described in the dataset
    tech_tools_suffix = [
        'Smartphone', 'Ordinateur', 'TV', 'Tablette', 'Console de jeux', 
        'Objets connectés', 'Robotique', 'Autre'
    ]


    # Prepare and concatenate data for all characters with accurate column names
    all_characters_data = pd.DataFrame()

    # Loop through each character number
    for i in range(1, 5):
        # Prepare the mapping for each character's technology columns using the correct format
        colnames = {
            f"character{i}_technology_tools [{tool}]": tool for tool in tech_tools_suffix
        }
        colnames[f"character{i}_" + colname_id] = colname_id
        
        # Select and rename the relevant columns for each character
        temp_data = data[list(colnames.keys())].rename(columns=colnames)
        
        # Append to the overall DataFrame
        all_characters_data = pd.concat([all_characters_data, temp_data], ignore_index=True)

    # Melt the DataFrame to long format for easier plotting
    melted_data_all = all_characters_data.melt(id_vars=[colname_id], 
                                               value_vars=tech_tools_suffix, 
                                               var_name='Technology', 
                                               value_name='Frequency')

    # Remove NaN entries for plotting
    melted_data_all.dropna(inplace=True)

    return melted_data_all

# Example usage:
# df = pd.read_csv('your_dataset.csv')
# prepared_data = prepare_technology_data(df)
# print(prepared_data.head())

def prepare_character_data(data, colname_suffixes):
    """
    Extracts and prepares data for analysis from multiple characters.
    
    Parameters:
        data (DataFrame): The original dataset containing technology tools and demographic information for characters.
        colname_id (String): Part of the column name for which we want to do the analysis, e.g. 'gender'.
    
    Returns:
        DataFrame: A long-format DataFrame ready for analysis and visualization.
    """

    # Prepare and concatenate data for all characters with accurate column names
    all_characters_data = pd.DataFrame()

    # Loop through each character number
    for i in range(1, 5):
        # Prepare the mapping for each character's technology columns using the correct format
        colnames = {
            f"character{i}_{suffix}": suffix for suffix in colname_suffixes
        }

        
        # Select and rename the relevant columns for each character
        temp_data = data[list(colnames.keys())].rename(columns=colnames)
        
        # Append to the overall DataFrame
        all_characters_data = pd.concat([all_characters_data, temp_data], ignore_index=True)

    return all_characters_data


###  TODO Analyse de l’échantillon

# Questions
# Quels sont les sous-échantillons statistiquement représentatifs qui peuvent être analysés ?

# Visualisations
# Nombre de films uniques
# Nombre, titre et fréquence des contenus non-uniques
# Répartition des nationalités
# Répartition des producteurs
# Répartition des années de sortie
# Répartition des canaux de diffusion
# Répartition des genres (uniques)
# Répartition des producteurs
# Nombre de films pour chaque type de récompense documentées (Césars, Cannes, Oscars…) / par année de sortie
# Année de sortie en fonction de nationalité
# Genres en fonction de l’année de sortie
# Genres en fonction de la nationalité
# Nationalité en fonction du canal de diffusion
# Genre en fonction du canal de diffusion
# Année en fonction du canal de diffusion

# TODO Analyse des doublons
# Pour chaque contenu présents plusieurs fois:
# visualisation de toutes les réponses divergentes
# visualisation des personnages à la même désignation (nom ou nom d’acteur) et des réponses divergentes pour les mêmes personnages


# TODO Analyse de l’arène

# Questions
# Où se passent les récits ? 
# Est-ce que le lieu du récit est corrélé avec la nationalité du film ?
# Dans quels types de société se déroulent nos récits (réalité vs fantaisie, dystopie vs utopies…) ? Y a t-il une influence du genre ?
# À quelle époque se passent les récits ? Quelle est la proportion de récits qui ne se déroulent pas à l’époque de leur écriture ? Comment est-ce influencé par leur genre ?
# Est-ce que ces tendances évoluent au cours du temps ?

# Visualisations
# Répartitions:
# Pays de l’action
# Nombre de pays par film (1, 2 …)
# Environnement de l’action
# Époque de l’action
# Temporalité de l’action (i.e. temps de l’action par rapport à époque d’écriture du récit)
# Type de société
# Type de mondes
# Corrélations : 
# Pays de l’action vs pays de production
# Type de monde vs année de production
# Type de monde vs genre
# Type de monde vs nationalité du film
# Type de monde vs canal de diffusion
# Type de société vs année de production
# Type de société vs genre
# Type de société vs nationalité du film
# Type de société vs canal de diffusion
# Temporalité du récit vs genre
# Temporalité du récit vs année de production
# Temporalité du récit vs canal de diffusion
# Temporalité du récit vs type de monde
# Temporalité du récit vs type de société
# Nombre de pays de l’action vs genre


# TODO Analyse des personnages renseignés

# Questions: 
# Quelles sont les caractéristiques des personnages ? Qui sont-ils ? Comment vivent-ils ? Quelle est l’influence des caractéristiques du film sur les caractéristiques des personnages ?

# Visualisations:
# Nombre total de personnages renseignés 
# Nombre moyen de personnages par film
# En cas de contenus identiques, identification des désignations identiques et comparaison des divergences dans les répon
# Répartitions:
# Tranches d’âges
# Genre
# Ethnicités
# Gentil ou méchant
# Principal ou secondaire
# Corrélations:
# Possibilité de corréler chacun des 5 paramètres au 4 autres (genre vs âge etc.)
# Possibilité de corréler chacun des 5 paramètres à nationalité du film / date du film / producteur / genre du film

# TODO Analyse des caractéristiques écologiques des personnages

# Questions
# Les personnages de fiction présentent-ils des traits de caractères écologiques ? si oui, qui sont ces personnages ? Est-ce que c’est influencé par les caractéristiques du film (nationalité …) ? Est-ce que ça évolue dans le temps ?

# Visualisations
# Répartition des réponses à la sensibilité écologique du personnage
# Corrélation entre la sensibilité écologique et les caractéristiques du personnage (genre / ethnicité /  âge / gentil-méchant / principal-secondaire)
# Corrélation entre la présence de personnage ayant une sensibilité écolo et les caractéristiques du film (année / nationalité / genre / producteur / canal de diffusion)

# TODO Analyse de la mobilité à l’écran

# Questions
# Comment se déplace-t-on à l’écran ? Est-ce qu’il y a une corrélation entre 
# Visualisation de la proportion de modes de transport représentés à l’écran. Filtres possibles sur les caractéristiques du contenu (ex. que les films français) ou sur la nature des personnages (ex. tranches d’âge).
# Objectif: répondre aux questions suivantes:
# Comment se déplace-t-on à l’écran ?
# Est-ce que ça varie selon le type de personnage et leur sensibilité à l’écologie ?

# TODO Analyse de l’habitat
# Visualisation générale des modes d’habitat à l’écran, avec filtres possibles sur les types de contenu ou sur les caractéristiques des personnages (ex. comment habitent les jeunes ? comment habitent les CSP+ ?). Importance corréler l’habitat à l’emploi exercé (i.e. la catégorie socio-professionnelle).
# Corrélation entre les lieux de vie et les lieux de l’action (dans la catégorie arène). Question posée : les “aventures” se passent-elles forcément loin du lieu de vie des personnages ? Regarder notamment l’influence du genre et l’influence de la nationalité du film

# TODO Analyse de l’emploi
# Visualisation des emplois représentés à l’écran selon le type de contenu.
# Intéressant de regarder qui pratique quel type d’emploi (femmes vs hommes, jeunes…)
# Corrélation entre le métier pratiqué et la sensibilité du personnage à l’écologie

job_data = prepare_character_data(data=data,colname_suffixes={'job_sector'})

# Calculate the frequency of each job sector
job_sector_counts = job_data['job_sector'].value_counts().reset_index()
job_sector_counts.columns = ['Job Sector', 'Frequency']

# Creating a bar chart for job sector distribution
fig = px.bar(job_sector_counts, x='Job Sector', y='Frequency',
             title='Frequency of Job Sectors',
             labels={'Job Sector': 'Job Sector', 'Frequency': 'Frequency'})

# Update layout for better visualization
fig.update_layout(xaxis_title='Job Sector',
                  yaxis_title='Count',
                  xaxis_tickangle=-45)

# Show the plot
st.plotly_chart(fig)


data.replace('Non, il / elle a même des comportements et valeurs explicitement anti-écologiques ','Non, anti-écolo', inplace=True)
job_data = prepare_character_data(data= data, colname_suffixes={'interested_ecology','job_sector'})

# Create a cross-tabulation
ct = pd.crosstab(job_data['job_sector'], job_data['interested_ecology'])

# Generate a heatmap
fig = px.imshow(ct, text_auto=True, aspect="auto",
                labels=dict(x="Interest in Ecology", y="Job Sector", color="Count"),
                title='Heatmap of Job Sectors and Interest in Ecology')

# Update layout for clarity
fig.update_xaxes(side="bottom")

# Display the plot
st.plotly_chart(fig)

job_data = prepare_character_data(data= data, colname_suffixes={'interested_ecology','job'})


# Create a cross-tabulation
ct = pd.crosstab(job_data['job'], job_data['interested_ecology'])

# Generate a heatmap
fig = px.imshow(ct, text_auto=True, aspect="auto",
                labels=dict(x="Interest in Ecology", y="Job", color="Count"),
                title='Heatmap of Job and Interest in Ecology')

# Update layout for clarity
fig.update_xaxes(side="bottom")

# Display the plot
st.plotly_chart(fig)



# Analyse de la technologie
# Visualisation de l’emploi de la technologie à l’écran selon le type de film (regarder en particulier le genre) et le type de personnage (corréler en particulier à l’âge). Question sous-jacente : comment utilise-t-on la technologie à l’écran ? est-ce systématique ? est-ce corrélé à une certaine forme de réalité des usages ?
melted_data_all = prepare_technology_data(data=data, colname_id='gender')

# Custom color mapping 
color_map = { "Pas du tout" : '#98FB98', "Occasionnellement": '#99CCFF', "Souvent": '#3A4EC6', "Systématiquement": '#FF5050'}
category_orders={"Frequency": ["Pas du tout", "Occasionnellement", "Souvent", "Systématiquement"]}

label_nb_characters = 'Nombre de réponses'


fig = px.histogram(melted_data_all, x='Technology', color='Frequency', 
                   barmode='stack', title='Utilisation de la technologie par appareil et fréquence',
                   labels={'count':'Count of Responses'}, 
                   color_discrete_map=color_map,
                   category_orders=category_orders)
fig.update_layout(# xaxis_title='Technology Tool',
                  yaxis_title=label_nb_characters,
                  legend_title='Fréquence',
                  xaxis={'categoryorder':'total descending'},
                  xaxis_tickangle=-45)
st.plotly_chart(fig)


fig = px.histogram(melted_data_all, x='Technology', color='Frequency', 
                   barmode='stack', facet_col='gender', 
                   title='Utilisation de la technologie par genre, type d\'appareil et fréquence',
                   labels={'count':'Count of Responses'}, 
                   color_discrete_map=color_map,
                   category_orders=category_orders)

# Update the x-axis title for each subplot
fig.update_xaxes(title_text='', tickangle=-45)

fig.update_layout(# xaxis_title='Technologie',
                  yaxis_title=label_nb_characters,
                  legend_title='Fréquence'
                  )

st.plotly_chart(fig)

# analysis by ethnic group
melted_data_all = prepare_technology_data(data=data, colname_id='ethnic_origin')
melted_data_all.rename(columns={'ethnic_origin':'Ethnie'}, inplace=True)


fig = px.histogram(melted_data_all, x='Technology', color='Frequency', 
                   barmode='stack', facet_col='Ethnie', 
                   title='Utilisation de la technologie par ethnie, type d\'appareil et fréquence',
                   color_discrete_map=color_map,
                   category_orders=category_orders)

# Update the x-axis title for each subplot
fig.update_xaxes(title_text='', tickangle=-45)

fig.update_layout(yaxis_title=label_nb_characters,
                  legend_title='Fréquence'
                  )


st.plotly_chart(fig)



# TODO Analyse des modes de vie


# TODO L’écologie dans le récit

# TODO 
# Pédagogie?
# Cartographie des contenus qui mentionnent un enjeu écologique et corrélation à leurs caractéristiques (nationalité etc.). Est-ce que ça a évolué au cours du temps ? Est-ce que certains genres s’y prêtent  plus que d’autres ? Quand l’écologie est mentionnée, de quel type de récit s’agit-il ? (dystopie, récit futuriste…)
# Adéquation entre le score calculé et le score proposé par les répondants
# Enjeux écologiques les plus fréquemment montrés / les plus ignorés
# Box office / récompenses obtenues par les films qui parlent d’écologie ou qui ont des scores écologiques élevées (question : ces films sont-ils vus ?)
# A l’inverse, quels scores écologiques pour les films les plus vus au box office ? 

# Pédagogie clandestine ?
# Visualisation et statistiques sur les comportements listés, avec filtres possibles sur la nature des contenus.
# Corrélation au score écologique proposé par les répondants, la question étant : les spectateurs font-ils le lien entre certains comportements montrés à l’écran et l’impact écologique d’un contenu ? 

# Personnage écolo vs récit écolo


# La biodiversité à l’écran


# La perception des répondants


# Influence des caractéristiques des répondants


# La perception des répondants
# Quels types de contenus remportent les meilleurs scores?
# Quels types de contenus remportent les moins bons scores?

# L’influence du profil des répondants
# Sur les scores fournis 
# Sur le nombre de réponses type “je ne sais pas / je ne me souviens plus”


