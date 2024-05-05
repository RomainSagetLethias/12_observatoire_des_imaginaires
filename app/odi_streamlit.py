"""
# Application pour l'Observateur des Imaginaires
"""

# Core Pkgs
import pandas as pd
import plotly.express as px
import streamlit as st

# Other Pkgs
from odi_functions import (
    extract_text_between_brackets,
    prepare_character_data,
    prepare_technology_data,
)

# Set to True if debug information should appear in Streamlit app
debug = False

# Colors #E44F43",“#0B5773”,“#7BC0AC”,“#D3C922”
# gradient colors: #86B4B4, #0B5773, #58949F, #0A3555 #101727

# 3. Setup de l'application Streamlit  - Streamlit webpage properties / set up the app
# with wide view preset and a title
st.set_page_config(
    page_title="Observatoire des Imaginaires",
    page_icon="herb",
    layout="wide",
)

# Load the data
@st.cache_data  # 👈 Add the caching decorator
def load_data(file: str) -> pd.DataFrame:
    df = pd.read_csv(file, sep=";", encoding="utf-8")
    return df

# TODO connect to Google Sheet and load data
file_path = ("https://raw.githubusercontent.com/dataforgoodfr/12_observatoire_des_imaginaires/"
    "main/data/Etape%201%20Identification%20du%20film%20-%20Feuille%201%20-%20enrichi.csv")


if "data" not in st.session_state:
    st.session_state["data"] = load_data(file_path)

data = st.session_state["data"]

# Renommer les noms de colonnes (utile si le fichier d'entrée change de noms de colonnes)
# Renommer la colonne title -> TITRE
data.rename(columns={"title": "TITRE"}, inplace=True)

logo= ("https://media.licdn.com/dms/image/D4E0BAQEZHVBxFn3OXQ/company-logo_200_200/"
         "0/1697116934909/cercle_thmatique_culture_the_shifters_logo?e=1718841600&v=beta"
         "&t=_2DWaEBrblIgXhgVASUipHTcJesOL6s1Sk2uH73Kx58")

### A. Sidebar
with st.sidebar:
    st.image(
        logo,
        use_column_width=True,
    )  # width=50

    st.title("Fait par la dream team _Analyse de données_")
    st.write(
        "Cette application analyse les données du sondage "
         "de **l'Observatoire des Imaginaires**. ",
    )


### B. Container du header
header = st.container()
header.title("Observatoire des Imaginaires")
header.write("""<div class='fixed-header'/>""", unsafe_allow_html=True)

### C. Container des métriques
cont_metric = st.container()

# Et Supprimer les lignes où toutes les valeurs sont NaN
df = data.dropna(how="all")

# Nettoyage du data set

# mettre les titres en majuscule
df["TITRE"] = df["TITRE"].str.upper()
# Convertir les années en entier
annee = "release_year"
df[annee] = pd.to_numeric(df[annee], errors="coerce").fillna(0).astype(int)

with cont_metric:
    with st.expander("Aperçu des données"):
        st.dataframe(df)
        if (debug):
            st.write(list(df.columns))


    ### A. Affichage des métriques macro
    col_nb_oeuvre_analyse, col_nb_film, col_nb_tvshow = st.columns([2, 2, 2])
    with col_nb_oeuvre_analyse:
        # Metric nb Oeuvres analysées
        st.metric(label="Oeuvres analysées", value=len(set(df["TITRE"])))
    with col_nb_film:
        # Metric nb Films
        st.metric(
            label="Films",
            value=len(set(df[df.TYPE == "FILM"]["TITRE"])),
        )
    with col_nb_tvshow:
        # Metric Séries
        st.metric(
            label="Séries",
            value=len(set(df[df.TYPE == "SÉRIE"]["TITRE"])),
        )

    film_titles = set(df[df.TYPE == "FILM"]["TITRE"])
    all_titles = set(df["TITRE"])
    film_ratio = round(100 * len(film_titles) / len(all_titles), 2)

    serie_titles = set(df[df.TYPE == "SÉRIE"]["TITRE"])
    serie_ratio = round(100 * len(serie_titles) / len(all_titles), 2)

    st.write(
        f":blue[{film_ratio}%] des contenus renseignés sont des films vs "
        f":blue[{serie_ratio}%] des séries.",
    )


titles_more_than_once = (
    df.groupby(["TITRE", "TYPE"]).agg(compte=("TITRE", "count")).reset_index()
)
titles_more_than_once = titles_more_than_once[titles_more_than_once["compte"] > 1]

# Afficher un bar chart des titres les plus fréquents
# Affichage d'un bar chart horizontal

with st.container():
    st.subheader("Productions les plus fréquentes")
    col_freq_film_select, col_freq_film_vide, col_freq_film_graph = st.columns(
        [2, 0.5, 5],
    )
    with col_freq_film_select:
        type_choice = st.selectbox(
            "Choisir un type",
            titles_more_than_once["TYPE"].unique(),
            index=None,
        )
    with col_freq_film_graph:
        if type_choice == "FILM":
            t = titles_more_than_once.loc[
                titles_more_than_once["TYPE"] == "FILM"
            ].sort_values(
                by="compte",
                ascending=True,
            )
        elif type_choice == "SÉRIE":
            t = titles_more_than_once.loc[
                titles_more_than_once["TYPE"] == "SÉRIE"
            ].sort_values(
                by="compte",
                ascending=True,
            )
        else:
            t = titles_more_than_once.sort_values(by="compte", ascending=True)

        st.bar_chart(t, x="TITRE", y="compte")

# Types de contenus et pays d'origine
with st.container():
    st.subheader("Types de contenus")

    date_group_df = (
        df.groupby("release_year")
        .count()
        .reset_index()[["release_year", "TITRE"]]
        .rename(columns={"TITRE": "nb_titre"})
        )
    date_group_df["periode_percent"] = 100 * (
        1 - (date_group_df.nb_titre.cumsum() / date_group_df.nb_titre.sum())
        )

    date_min = str(df.release_year.min())
    date_max = str(df.release_year.max())
    date_pareto = date_group_df[date_group_df["periode_percent"] <= 80][ # noqa: PLR2004
                                                                        "release_year"].min()

    date_value_pareto = int(
        round(
            date_group_df[date_group_df["periode_percent"] <= 80][  # noqa: PLR2004
                                                                  "periode_percent"
                                                                  ].max(),0),
        )

    st.markdown(
        (f"Les contenus datent d'une période qui s'étend de **:blue[{date_min}]**"
         f" à **:blue[{date_max}]**. **:blue[{date_value_pareto}%]** des contenus \
             sont postérieurs à"
         f" **:blue[{date_pareto}]**."
         ),
        )

st.bar_chart(date_group_df, x="release_year", y="nb_titre")

with st.container(border=True):
    st.subheader("Nationalité des contenus")
    col_pays, col_contenu_vide, col_pays_annee = st.columns([4, 0.5, 4])

    country_group_df = df
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
        100 * (country_group_df.nb_titre / country_group_df.nb_titre.sum()),
        2,
        )

    country_value_pareto = int(
        round(
            country_group_df[
                country_group_df["country_percent"] >= 10 # noqa: PLR2004
                ][
                    "country_percent"
                    ].sum(),
                2,
                ),
        )
    country_group_df_pareto = country_group_df[
        country_group_df["country_percent"] >= 10  # noqa: PLR2004
        ][["pays_rework", "country_percent"]].sort_values(
            "country_percent",
            ascending=False,
            )

    # Pre-calculate the two largest values
    top_countries_df = country_group_df.nlargest(2,"country_percent").reset_index(drop=True)

    # Extract country names and percentages for readability
    country1_name = top_countries_df["pays_rework"][0].capitalize()
    country1_percent = top_countries_df["country_percent"][0]
    country2_name = top_countries_df["pays_rework"][1].capitalize()
    country2_percent = top_countries_df["country_percent"][1]

    # Format the output string
    output_string = (
        f"A **:blue[{country_value_pareto}%]**, les 2 principaux pays dont les contenus "
        f"sont les plus visionnés sont : {country1_name} ({country1_percent}%) et "
        f"{country2_name} ({country2_percent}%)."
        )

    st.write(output_string)

    with col_pays :
        fig_pays = px.bar(
            country_group_df,
            y="pays_rework",
            x="nb_titre",
            orientation="h",
            text_auto=True,
            )
        st.plotly_chart(fig_pays, use_container_width=True)

    with col_pays_annee:
        country_group_df_rework = df.groupby(["pays_rework",
                    "production_countries",
                    "release_year"]).count().reset_index()[["pays_rework",
                    "production_countries",
                    "release_year",
                    "TITRE"]].rename(columns={"TITRE": "Nb_titres",
                                              "production_countries": "Pays",
                                              "release_year":"Année de sortie" })

        country_group_df_rework["Année de sortie"] = \
            country_group_df_rework["Année de sortie"].astype("str")

        fig_pays_annee = px.bar(country_group_df_rework.sort_values(["Année de sortie"]),
                                y="pays_rework",
                                x="Nb_titres",
                                color="Année de sortie",
                                orientation="h",
                                color_discrete_map={
                                    "1997": "#E44F43",
                                    "2024": "#0B5773",
                                    "2022": "#7BC0AC",
                                    "2023": "#D3C922"},
                                text_auto=True,
                                hover_data={"pays_rework":False,
                                            "Année de sortie":True, "Pays":True})
        st.plotly_chart(fig_pays_annee, use_container_width=True)

# LIEUX VISIONNAGE
with st.container():
    st.subheader("Canaux de diffusion")
    canal_group_df = (
        df.groupby("channel")
        .count()[["TITRE"]]
        .rename(columns={"TITRE": "nb_titre"})
        .sort_values("nb_titre", ascending=False)
    )
    canal_group_df["canal_percent"] = 100 * (
        canal_group_df.nb_titre / canal_group_df.nb_titre.sum()
    )
    canal_country_group_df = (
        df.groupby(["channel", "pays_rework"])
        .count()[["TITRE"]]
        .rename(columns={"TITRE": "nb_titre"})
        .sort_values("nb_titre", ascending=False)
        .reset_index()
    )

    col_text_canal, col_table_canal = st.columns([5, 3])
    with col_text_canal:
        canal_visionne1 = canal_group_df.nb_titre.nlargest(2).reset_index()["channel"][
            0
        ]
        percent_canal_visionne1 = round(canal_group_df.canal_percent.nlargest(2)[0], 2)
        canal_visionne2 = canal_group_df.nb_titre.nlargest(2).reset_index()["channel"][
            1
        ]
        percent_canal_visionne2 = round(canal_group_df.canal_percent.nlargest(2)[1], 2)

        # Pre-calculate and capitalize channel names
        channel1 = canal_visionne1.capitalize()
        channel2 = canal_visionne2.capitalize()

        # Prepare the first part of the message
        part1 = (
            f"Les contenus sont visionnés principalement sur :blue[{channel1}] "
            f"(:blue[{percent_canal_visionne1}%]) et :blue[{channel2}] "
            f"(:blue[{percent_canal_visionne2}%])."
        )

        # Calculate country of origin for the most watched content on channel1
        cntr_df = canal_country_group_df[canal_country_group_df["channel"] == canal_visionne1]
        top_country = cntr_df.nlargest(1, "nb_titre").reset_index()["pays_rework"][0]

        # Prepare the second part of the message
        part2 = (
            f"\n\nLa majorité des contenus visionnés sur :blue[{channel1}] ont pour "
            f"pays d'origine :blue[{top_country}] (:blue[%]), alors que la  "
            f"majorité des contenus français sont visionnés xxx (xxx%)."
        )


        # Combine all parts and use markdown
        st.markdown(part1 + part2)

        # Les contenus sont visionnés principalement sur Netflix (29.91%) ou dans
        # une salle de cinéma (28.97%). La majorité des contenus américains sont
        # visionnés sur Netflix (40.48% des contenus US), alors que la majorité
        # des contenus français sont visionnés au cinéma (44.19%).
    # 23.36% des contenus sont visionnés sur un canal `autre`
    # que la liste proposée (cf ci-dessous)

    # with col_table_canal:
    # 	st.markdown(set(canal_group_df.reset_index().channel))

st.divider()
with st.container():
    st.subheader("Genres Cinématographiques")
    # Fonction pour créer le treemap
    @st.cache_data
    def get_chart_82052330(df: pd.DataFrame, liste: list[str], titre: str) -> None:
        fig = px.treemap(
            df,
            path=[px.Constant("all"), liste],
            values="total_film",  # color='TYPE',
            title=titre,
        )
        fig.update_layout(margin={"t":50, "l":25, "r":25, "b":25})

        st.plotly_chart(fig, theme="streamlit")

    # Préparation du dataframe pour les films
    genre_group_df = df[["id_tmdb", "genres", "TITRE", "TYPE"]].drop_duplicates()

    # je crée une liste de genres uniques
    liste_genre_cine = list({g for genre in genre_group_df["genres"] for g in genre.split(",")})

    # je compte le nombre de films avec au moins le genre pris en compte
    genre_group_df = pd.concat([genre_group_df, pd.DataFrame(columns=liste_genre_cine)])
    for col in liste_genre_cine:
        genre_group_df[col] = [
            1 if col in o.split(",") else 0 for o in genre_group_df["genres"]
        ]

    # j'ajoute une colonne qui fait la somme des films pour un genre donné
    # et ajoute le type pour cette nouvelle ligne
    total_film = dict(
        genre_group_df.loc[genre_group_df["TYPE"] == "FILM"][liste_genre_cine].sum(),
    )

    total_film = (
        pd.DataFrame.from_dict(total_film, orient="index")
        .reset_index()
        .rename(columns={0: "total_film", "index": "genres"})
    )
    total_film.insert(2, "TYPE", "FILM")

    get_chart_82052330(total_film, liste_genre_cine, "Répartition des genres (uniques)")

with st.container():
    # Préparation du dataframe pour les films
    productions_df = df[
        ["id_tmdb", "TITRE", "TYPE", "production_companies"]
    ].drop_duplicates()
    # je crée une liste de genres uniques
    liste_production_cine = list({p
        for prod in productions_df["production_companies"]
        for p in prod.split(",")
    })


    # je compte le nombre de films par producteur
    productions_df = pd.concat(
        [productions_df, pd.DataFrame(columns=liste_production_cine)],
    )
    for col in liste_production_cine:
        productions_df[col] = [
            1 if col in o.split(",") else 0
            for o in productions_df["production_companies"]
        ]

    # j'ajoute une colonne qui fait la somme des films pour un genre donné
    # et ajoute le type pour cette nouvelle ligne
    total_film_prod = dict(
        productions_df.loc[productions_df["TYPE"] == "FILM"][
            liste_production_cine
        ].sum(),
    )

    total_film_prod = (
        pd.DataFrame.from_dict(total_film_prod, orient="index")
        .reset_index()
        .rename(columns={0: "total_film", "index": "production_companies"})
    )
    total_film_prod.insert(2, "TYPE", "FILM")

    get_chart_82052330(
        total_film_prod, liste_production_cine, "Répartition des producteurs",
    )

with st.container():
    st.subheader("Récompenses")

    col_choix_annee, col_award_graph = st.columns([4, 6])

    # Préparation du dataframe pour les films
    award_df = df[
        ["id_tmdb", "TITRE", "TYPE", "nb_recompense", "liste_festival","release_year"]
    ].drop_duplicates()

    liste_award_cine = list({p
        for prod in award_df["liste_festival"] for p in str(prod).split(",")
    })
    if (debug):
        st.write(liste_award_cine)

    list_year = award_df["release_year"].sort_values().unique()

    with col_choix_annee :
        start_clr, end_clr = st.select_slider("Choisir la/les date(s) d'analyse",
                        options=list_year, value=(min(list_year), max(list_year)))


    # je conmpte le nombre de films par récompense
    award_df = pd.concat([award_df, pd.DataFrame(columns=liste_award_cine)])
    for col in liste_award_cine:
        award_df[col] = [1 if col in str(a).split(",")\
            else 0 for a in award_df["liste_festival"]]

    # j'ajoute une colonne qui fait la somme des films pour une récompense donnés
    # et ajoute le type pour cette nouvelle ligne
    total_film_award = dict(
        award_df.loc[(award_df["TYPE"] == "FILM")&\
            (award_df.release_year >= start_clr) & \
                (award_df.release_year <= end_clr)][liste_award_cine].sum(),
    )

    total_film_award = (
        pd.DataFrame.from_dict(total_film_award, orient="index")
        .reset_index()
        .rename(columns={0: "total_film", "index": "liste_festival"})
    )
    total_film_award.insert(2, "TYPE", "FILM")

    with col_award_graph :
        get_chart_82052330(
            total_film_award, liste_award_cine,
            f"Répartition des récompenses de {start_clr} à {end_clr}")

st.divider()


###  TODO Analyse de l’échantillon

# Questions
# Quels sont les sous-échantillons statistiquement représentatifs qui peuvent être analysés ?

# Visualisations
# TODO Nombre de réponses au questionnaire
# Nombre de films uniques - ok
# Nombre, titre et fréquence des contenus non-uniques - ok
# Répartition des nationalités - ok
# Répartition des producteurs - ok
# Répartition des années de sortie
# Répartition des canaux de diffusion
# Répartition des genres (uniques) - ok
# Répartition des producteurs - déjà ok
# Nombre de films pour chaque type de récompense documentées
#                      (Césars, Cannes, Oscars…) / par année de sortie
# Année de sortie en fonction de nationalité
# Genres en fonction de l’année de sortie
# Genres en fonction de la nationalité
# Nationalité en fonction du canal de diffusion
# Genre en fonction du canal de diffusion
# Année en fonction du canal de diffusion

# TODO Analyse des doublons
# Pour chaque contenu présents plusieurs fois:
# visualisation de toutes les réponses divergentes
# visualisation des personnages à la même désignation (nom ou nom d’acteur)
#            et des réponses divergentes pour les mêmes personnages


# TODO Analyse de l’arène

# Questions
# Où se passent les récits ?
# Est-ce que le lieu du récit est corrélé avec la nationalité du film ?
# Dans quels types de société se déroulent nos récits (réalité vs fantaisie, dystopie
#              vs utopies…) ? Y a t-il une influence du genre ?
# À quelle époque se passent les récits ? Quelle est la proportion de récits qui ne se
#        déroulent pas à l’époque de leur écriture ? Comment est-ce influencé par leur genre ?
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
# Quelles sont les caractéristiques des personnages ? Qui sont-ils ? Comment vivent-ils ?
# Quelle est l’influence des caractéristiques du film sur les caractéristiques des personnages ?

# Visualisations:
# Nombre total de personnages renseignés
# Nombre moyen de personnages par film
# En cas de contenus identiques, identification des désignations identiques et
#       comparaison des divergences dans les répon
# Répartitions:
# Tranches d’âges
# Genre
# Ethnicités
# Gentil ou méchant
# Principal ou secondaire
# Corrélations:
# Possibilité de corréler chacun des 5 paramètres au 4 autres (genre vs âge etc.)
# Possibilité de corréler chacun des 5 paramètres
#        à nationalité du film / date du film / producteur / genre du film

# TODO Analyse des caractéristiques écologiques des personnages

# Questions
# Les personnages de fiction présentent-ils des traits de caractères écologiques ?
#   si oui, qui sont ces personnages ? Est-ce que c’est influencé par les caractéristiques
#   du film (nationalité …) ? Est-ce que ça évolue dans le temps ?

# Visualisations
# Répartition des réponses à la sensibilité écologique du personnage
# Corrélation entre la sensibilité écologique et les caractéristiques
#    du personnage (genre / ethnicité /  âge / gentil-méchant / principal-secondaire)
# Corrélation entre la présence de personnage ayant une sensibilité écolo et les
#   caractéristiques du film (année / nationalité / genre / producteur / canal de diffusion)

# TODO Analyse de la mobilité à l’écran

# Questions
# Comment se déplace-t-on à l’écran ? Est-ce qu’il y a une corrélation entre
# Visualisation de la proportion de modes de transport représentés à l’écran. Filtres
#    possibles sur les caractéristiques du contenu (ex. que les films français)
#    ou sur la nature des personnages (ex. tranches d’âge).
# Objectif: répondre aux questions suivantes:
# Comment se déplace-t-on à l’écran ?
# Est-ce que ça varie selon le type de personnage et leur sensibilité à l’écologie ?

# TODO Analyse de l’habitat
# Visualisation générale des modes d’habitat à l’écran, avec filtres possibles sur les
#     types de contenu ou sur les caractéristiques des personnages (ex. comment habitent les
#     jeunes ? comment habitent les CSP+ ?). Importance corréler l’habitat à l’emploi exercé
#     (i.e. la catégorie socio-professionnelle).
# Corrélation entre les lieux de vie et les lieux de l’action (dans la catégorie arène).
#     Question posée : les “aventures” se passent-elles forcément loin du lieu de vie des
#     personnages ? Regarder notamment l’influence du genre et l’influence de la nationalité
#     du film

# TODO Analyse de l’emploi
# Visualisation des emplois représentés à l’écran selon le type de contenu.
# Intéressant de regarder qui pratique quel type d’emploi (femmes vs hommes, jeunes…)
# Corrélation entre le métier pratiqué et la sensibilité du personnage à l’écologie

with st.container():
    st.subheader("Analyse des métiers")
    job_data = prepare_character_data(data=df, colname_suffixes={"job_sector"})

    # Calculate the frequency of each job sector
    job_sector_counts = job_data["job_sector"].value_counts().reset_index()
    job_sector_counts.columns = ["Job Sector", "Frequency"]

    # Creating a bar chart for job sector distribution
    fig = px.bar(
        job_sector_counts,
        x="Job Sector",
        y="Frequency",
        title="Frequency of Job Sectors",
        labels={"Job Sector": "Job Sector", "Frequency": "Frequency"},
    )

    # Update layout for better visualization
    fig.update_layout(xaxis_title="Job Sector", yaxis_title="Count", xaxis_tickangle=-45)

    # Show the plot
    st.plotly_chart(fig)

    # Replace long values to shorter values
    df.replace(
        "Non, il / elle a même des comportements et valeurs explicitement anti-écologiques ",
        "Non, anti-écolo",
        inplace=True,
    )
    job_data = prepare_character_data(
        data=df, colname_suffixes={"interested_ecology", "job_sector"},
    )

    # Create a cross-tabulation
    ct = pd.crosstab(job_data["job_sector"], job_data["interested_ecology"])

    # Generate a heatmap
    fig = px.imshow(
        ct,
        text_auto=True,
        aspect="auto",
        labels={"x":"Interest in Ecology", "y":"Job Sector", "color":"Count"},
        title="Heatmap of Job Sectors and Interest in Ecology",
    )

    # Update layout for clarity
    fig.update_xaxes(side="bottom")

    # Display the plot
    st.plotly_chart(fig)

    job_data = prepare_character_data(
        data=df, colname_suffixes={"interested_ecology", "job"},
    )


    # Create a cross-tabulation
    ct = pd.crosstab(job_data["job"], job_data["interested_ecology"])

    # Generate a heatmap
    fig = px.imshow(
        ct,
        text_auto=True,
        aspect="auto",
        labels={"x":"Interest in Ecology", "y":"Job", "color":"Count"},
        title="Heatmap of Job and Interest in Ecology",
    )

    # Update layout for clarity
    fig.update_xaxes(side="bottom")

    # Display the plot
    st.plotly_chart(fig)


# Analyse de la technologie
# Visualisation de l’emploi de la technologie à l’écran selon le type de film (regarder en
#  particulier le genre) et le type de personnage (corréler en particulier à l’âge).
#  Question sous-jacente : comment utilise-t-on la technologie à l’écran ? est-ce
#  systématique ? est-ce corrélé à une certaine forme de réalité des usages ?
with st.container():
    st.subheader("Analyse de la technologie")

    melted_data_all = prepare_technology_data(data=df, colname_id="gender")

    # Custom color mapping
    color_map = {
        "Pas du tout": "#98FB98",
        "Occasionnellement": "#99CCFF",
        "Souvent": "#3A4EC6",
        "Systématiquement": "#FF5050",
    }
    category_orders = {
        "Frequency": ["Pas du tout", "Occasionnellement", "Souvent", "Systématiquement"],
    }

    label_nb_characters = "Nombre de réponses"


    fig = px.histogram(
        melted_data_all,
        x="Technology",
        color="Frequency",
        barmode="stack",
        title="Utilisation de la technologie par appareil et fréquence",
        labels={"count": "Count of Responses"},
        color_discrete_map=color_map,
        category_orders=category_orders,
    )
    fig.update_layout(  # xaxis_title='Technology Tool',
        yaxis_title=label_nb_characters,
        legend_title="Fréquence",
        xaxis={"categoryorder": "total descending"},
        xaxis_tickangle=-45,
    )
    st.plotly_chart(fig)


    fig = px.histogram(
        melted_data_all,
        x="Technology",
        color="Frequency",
        barmode="stack",
        facet_col="gender",
        title="Utilisation de la technologie par genre, type d'appareil et fréquence",
        labels={"count": "Count of Responses"},
        color_discrete_map=color_map,
        category_orders=category_orders,
    )

    # Update the x-axis title for each subplot
    fig.update_xaxes(title_text="", tickangle=-45)

    fig.update_layout(  # xaxis_title='Technologie',
        yaxis_title=label_nb_characters, legend_title="Fréquence",
    )

    st.plotly_chart(fig)

    # analysis by ethnic group
    melted_data_all = prepare_technology_data(data=df, colname_id="ethnic_origin")
    melted_data_all.rename(columns={"ethnic_origin": "Ethnie"}, inplace=True)


    fig = px.histogram(
        melted_data_all,
        x="Technology",
        color="Frequency",
        barmode="stack",
        facet_col="Ethnie",
        title="Utilisation de la technologie par ethnie, type d'appareil et fréquence",
        color_discrete_map=color_map,
        category_orders=category_orders,
    )

    # Update the x-axis title for each subplot
    fig.update_xaxes(title_text="", tickangle=-45)

    fig.update_layout(yaxis_title=label_nb_characters, legend_title="Fréquence")


    st.plotly_chart(fig)

    melted_data_all = prepare_technology_data(data=df, colname_id="age_group")
    melted_data_all.rename(columns={"age_group": "Catégorie d'âge"}, inplace=True)

    fig = px.histogram(
        melted_data_all,
        x="Technology",
        color="Frequency",
        barmode="group",
        pattern_shape="Catégorie d'âge",
        title="Utilisation de la technologie par catégorie d'âge, type d'appareil et fréquence",
        color_discrete_map=color_map,
        category_orders=category_orders,
    )

    # Update the x-axis title for each subplot
    fig.update_xaxes(title_text="", tickangle=-45)

    fig.update_layout(yaxis_title=label_nb_characters, legend_title="Fréquence")


    st.plotly_chart(fig)

# TODO Analyse des modes de vie


# TODO L’écologie dans le récit

# TODO
# Pédagogie?
# Cartographie des contenus qui mentionnent un enjeu écologique et corrélation à leurs
#    caractéristiques (nationalité etc.). Est-ce que ça a évolué au cours du temps ? Est-ce
#    que certains genres s’y prêtent  plus que d’autres ? Quand l’écologie est mentionnée,
#    de quel type de récit s’agit-il ? (dystopie, récit futuriste…)
# Adéquation entre le score calculé et le score proposé par les répondants
# Enjeux écologiques les plus fréquemment montrés / les plus ignorés


# Des enjeux écologiques et environnementaux sont-ils mentionnés au cours du récit,
#      même brièvement ?
with st.container():
    st.subheader("Enjeux écologiques et environnementaux")
    response_counts = df["environmental_issues"].value_counts().reset_index()
    response_counts.columns = ["environmental_issues", "Count"]
    fig = px.pie(
        response_counts,
        names="environmental_issues",
        values="Count",
        title=("Des enjeux écologiques et environnementaux sont-ils "
            "mentionnés au cours du récit, même brièvement ?"),
    )
    st.plotly_chart(fig)


    # Filter columns that start with 'environmental_issues'
    env_columns = df[
        [col for col in df.columns if col.startswith("environmental_issues")]
    ]
    enjeux = env_columns[env_columns["environmental_issues"] == "Oui"].drop(
        axis=1, labels="environmental_issues",
    )

    # rename columns with shorter names
    colnames = {
        colname: extract_text_between_brackets(colname) for colname in enjeux.columns
    }
    enjeux.rename(columns=colnames, inplace=True)

    # Melt the DataFrame to long format
    long_format_data = enjeux.melt(var_name="Column", value_name="Value")

    # Count the frequency of each value in each column
    value_counts = (
        long_format_data.groupby(["Column", "Value"]).size().reset_index(name="Counts")
    )

    # Pivot the data for heatmap
    heatmap_data = value_counts.pivot(
        index="Value", columns="Column", values="Counts",
    ).fillna(0)

    # Create the heatmap using Plotly Express
    fig = px.imshow(
        heatmap_data,
        labels={"x":"Column", "y":"Value", "color":"Frequency"},
        x=heatmap_data.columns,
        y=heatmap_data.index,
        title="Fréquence des mentions des enjeux écologiques selon le type d'enjeu",
    )
    fig.update_xaxes(side="bottom")  # Ensuring the x-axis labels are at the bottom
    st.plotly_chart(fig)


# Box office / récompenses obtenues par les films qui parlent d’écologie ou qui ont
#         des scores écologiques élevées (question : ces films sont-ils vus ?)
# A l’inverse, quels scores écologiques pour les films les plus vus au box office ?

# Pédagogie clandestine ?
# Visualisation et statistiques sur les comportements listés, avec filtres possibles
#      sur la nature des contenus.
# Corrélation au score écologique proposé par les répondants, la question étant : les
#   spectateurs font-ils le lien entre certains comportements montrés à l’écran et
#   l’impact écologique d’un contenu ?

# Personnage écolo vs récit écolo


# La biodiversité à l’écran


# La perception des répondants
# Quels types de contenus remportent les meilleurs scores?
# Quels types de contenus remportent les moins bons scores?

# L’influence du profil des répondants
# Sur les scores fournis
# Sur le nombre de réponses type “je ne sais pas / je ne me souviens plus”

# TODO Analyse des personnages renseignés

# Questions:
# Quelles sont les caractéristiques des personnages ? Qui sont-ils ? Comment vivent-ils ?
# Quelle est l’influence des caractéristiques du film sur les caractéristiques des personnages ?

# Visualisations:
# Nombre total de personnages renseignés
non_null_count_1 = data["character1_name"].notnull().sum()
non_null_count_2 = data["character2_name"].notnull().sum()
non_null_count_3 = data["character3_name"].notnull().sum()
non_null_count_4 = data["character4_name"].notnull().sum()
total_number_of_characters = non_null_count_1 ++ non_null_count_2\
    ++ non_null_count_3 ++ non_null_count_4
st.write("Le nombre total des peronnage s'agit de",total_number_of_characters)

# Nombre moyen de personnages par film
# En cas de contenus identiques, identification des désignations identiques et
#       comparaison des divergences dans les répon
# Répartitions:

# Tranches d’âges
# Melanger les differentes characteres
blended_column = [val for pair in zip(data["character2_age_group"],
                data["character4_age_group"], strict=False) for val in pair]
data["Age"] = pd.DataFrame(blended_column)
st.write(data["Age"])

#creer une treemap
st.plotly_chart(fig)

fig = px.treemap(data, path=[data["Age"]],hover_data=[data["Age"]],
                 color= data["Age"],color_discrete_map = {
    "Adolescent": "#86b4b4",
    "Jeune adulte (moins de 30 ans)":"0b5773",
    "Adulte (30 - 50 ans)": "#58949f",
    "Senior (plus de 50 ans)": "0a3555",
    "Plus de 70 ans": "#101727",
},
                 title="Répartition de l'age des personnages",
                 )
fig.update_traces(marker={"cornerradius": 5})

fig.update_layout(
    margin = {"t": 50, "l": 25, "r": 25, "b": 25},
    title_font={"size": 30},
    title_x=0.04, title_y=0.95,
)

#mettre en commenteire pour voir les infos comme "count" en hover
fig.data[0].hovertemplate="<b></b>%{label}"

st.plotly_chart(fig)

# Genre
# Melanger les differentes characteres
blended_column = [val for quad in zip(data["character1_gender"],
                    data["character2_gender"],data["character3_gender"],
                    data["character4_gender"], strict=False) for val in quad]
data["Gender"] = pd.DataFrame(blended_column)
st.write(data["Gender"])

# Remplacer NaN avec None pour data["Ethnicites"]
data["Gender"]= data["Gender"].fillna(value=None, method="ffill")

st.plotly_chart(fig)

fig = px.treemap(data, path=["Gender"],
                 title="Répartition du genre des personnages",
                 color_discrete_sequence=["#e44f43","#0b5773","#7bc0ac","#d3c922"],
                 )
fig.update_traces(marker={"cornerradius": 5})

fig.update_layout(
    margin = {"t": 50, "l": 25, "r": 25, "b": 25},
    title_font={"size": 30},
    title_x=0.04, title_y=0.95,
)
#mettre en commenteire pour voir les infos comme "count" en hover
fig.data[0].hovertemplate="<b></b>%{label}"


# Corrélations:
# Possibilité de corréler chacun des 5 paramètres au 4 autres (genre vs âge etc.)
# Create a cross-tabulation
ct = pd.crosstab(data["Age"], data["Gender"])

# Generate a heatmap
fig = px.imshow(
    ct,
    text_auto=True,
    aspect="auto",
    labels={"x": "", "y": "", "color": ""},
    title="Age vs Gendre",
    color_continuous_scale="Bluyl",
)

# Update layout for clarity
fig.update_layout(
    margin = {"t": 50, "l": 25, "r": 25, "b": 50},
    title_font={"size": 30},
    title_x=0.4, title_y=0.97,
)

# Display the plot
st.plotly_chart(fig)

# Ethnicités
# Melanger les differentes characteres
blended_column = [val for quad in zip(data["character1_ethnic_origin"],
                                data["character2_ethnic_origin"],
                                data["character3_ethnic_origin"],
                                data["character4_ethnic_origin"],
                                strict=False) for val in quad]
data["Ethnicites"] = pd.DataFrame(blended_column)
st.write(data["Ethnicites"])
# Remplacer NaN avec None pour data["Ethnicites"]
data["Ethnicites"]= data["Ethnicites"].fillna(value=None, method="ffill")

#creer treemap
st.plotly_chart(fig)

fig = px.treemap(data, path=[data["Ethnicites"]],
                 title="Répartition de l'ethnicités des personnages",
                 color_discrete_sequence=["#e44f43","#0b5773",
                     ],
                 )
fig.update_traces(marker={"cornerradius": 5})

fig.update_layout(
    margin = {"t": 50, "l": 25, "r": 25, "b": 25},
    title_font={"size": 30},
    title_x=0.04, title_y=0.95,
)
#mettre en commenteire pour voir les infos comme "count" en hover
fig.data[0].hovertemplate="<b></b>%{label}"

st.plotly_chart(fig)

# Gentil ou méchant
# Melanger les differentes characteres
blended_column = [val for quad in zip(data["character1_sentiment"],
                        data["character2_sentiment"],
                        data["character3_sentiment"],
                        data["character1_sentiment"], strict=False) for val in quad]
data["Sentiment"] = pd.DataFrame(blended_column)
st.write(data["Sentiment"])

# Remplacer NaN avec None pour data["Ethnicites"]
data["Sentiment"]= data["Sentiment"].fillna(value=None, method="ffill")

#creer treemap
st.plotly_chart(fig)

fig = px.treemap(data, path=["Sentiment"],color= data["Sentiment"], color_discrete_map = {
    "Positive": "#0b5773",
    "Négative":"#d35a4b",
    "Neutre": "#7bc0ac",
    "C'est compliqué": "#d3c922",
},
                 title="Répartition des sentiments envers les personnages",
                 )
fig.update_traces(marker={"cornerradius": 5})

fig.update_layout(
    margin = {"t": 50, "l": 25, "r": 25, "b": 25},
    title_font={"size": 30},
    title_x=0.04, title_y=0.95,
)
#mettre en commenteire pour voir les infos comme "count" en hover
fig.data[0].hovertemplate="<b></b>%{label}"

st.plotly_chart(fig)


# Principal ou secondaire
# Melanger les differentes characteres
blended_column = [val for quad in zip(data["character1_importance"],
                        data["character2_importance"],data["character3_importance"],
                        data["character1_importance"], strict=False) for val in quad]
data["Importance"] = pd.DataFrame(blended_column)
st.write(data["Importance"])

# Remplacer NaN avec None pour data["Ethnicites"]
data["Importance"]= data["Importance"].fillna(value=None, method="ffill")

st.plotly_chart(fig)

fig = px.treemap(data, path=["Importance"],
                 color_discrete_sequence = ["#0b5773","#0a3555","#101727"],
                 title="Importance des personnages",
                 )
fig.update_traces(marker={"cornerradius": 5})

fig.update_layout(
    margin = {"t": 50, "l": 25, "r": 25, "b": 25},
    title_font=dict(size=30),
    title_x=0.04, title_y=0.95,
)
#mettre en commenteire pour voir les infos comme "count" en hover
fig.data[0].hovertemplate="<b></b>%{label}"

st.plotly_chart(fig)


# Possibilité de corréler chacun des 5 paramètres
#        à nationalité du film / date du film / producteur / genre du film
