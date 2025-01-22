import matplotlib.pyplot as plt
import streamlit as st
import pandas as pd
import seaborn as sns
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import StandardScaler

from visualizations import (
    plot_grouped_scatter_plots,
    plot_grouped_barplots,
    plot_grouped_boxplots,
    plot_grouped_histograms,
    plot_grouped_heatmap,
    plot_moyen
)

from data_processing import preprocess_data

# Titre de l'application
st.title("Musical Analysis Dashboard")

# Sélection des options dans la barre latérale
st.sidebar.subheader("Paramètres de visualisation")
chart_type = st.sidebar.selectbox(
    "Choisir le type de graphique",
    ["Scatter Plot", "Bar Chart", "Boxplot", "Histogram", "Heatmap", "KMeans Clustering", "Bar plot"]
)

st.sidebar.subheader("Filtres sur popularité")

# Filtrer par popularité
min_popularity = st.sidebar.slider("Popularité minimale", 0, 100, 50)

# Charger les données
@st.cache_data
def load_data():
    data = pd.read_csv("hf://datasets/maharshipandya/spotify-tracks-dataset/dataset.csv")  # Remplacez par votre chemin de dataset
    return data

data = load_data()
data=preprocess_data(data)


# Sélectionner les colonnes numériques et catégorielles
numerical_columns = data.select_dtypes(include=["float64", "int64"]).columns.tolist()
categorical_columns = data.select_dtypes(include=["object", "category"]).columns.tolist()

# Sélectionner les variables selon le type de graphique
variable_1, variable_2 = None, None
if chart_type in ["Scatter Plot", "Boxplot", "Histogram", "Heatmap"]:
    variable_1 = st.sidebar.selectbox("Variable 1", numerical_columns)
    variable_2 = st.sidebar.selectbox("Variable 2", numerical_columns)
elif chart_type == "Bar Chart":
    variable_1 = st.sidebar.selectbox("Variable catégorielle", categorical_columns)
    
elif chart_type == "Bar plot":
    variable_1 = st.sidebar.selectbox("Variable catégorielle", categorical_columns)
    variable_2 = st.sidebar.selectbox("Variable 2", numerical_columns)

# Paramètres pour le clustering KMeans
if chart_type == "KMeans Clustering":
    variable_1 = st.sidebar.selectbox("Composante 1 graphique", numerical_columns)
    variable_2 = st.sidebar.selectbox("Composante 2 graphique", numerical_columns)
    n_clusters = st.sidebar.slider("Nombre de clusters", min_value=2, max_value=10, value=3)


# Bouton pour générer le graphique
if st.sidebar.button("Générer le graphique"):
    
    filtered_data = data[data['popularity'] >= min_popularity]
    st.write(f"Nombre de morceaux après filtrage : {len(filtered_data)}")
    
    if chart_type == "KMeans Clustering":
        st.subheader(f"Clustering KMeans avec {n_clusters} clusters sur {variable_1} et {variable_2}")
        # Appliquer K-Means avec les deux variables choisies
        kmeans = KMeans(n_clusters=n_clusters)
        clusters = kmeans.fit_predict(filtered_data[[variable_1, variable_2]])

        # Ajouter les clusters au dataset
        filtered_data['Cluster'] = clusters

        # Visualisation des clusters
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.scatterplot(data=filtered_data, x=variable_1, y=variable_2, hue='Cluster', palette="viridis", ax=ax)
        ax.set_xlabel(variable_1)
        ax.set_ylabel(variable_2)
        ax.set_title(f"KMeans Clustering sur {variable_1} et {variable_2}")
        st.pyplot(fig)

    # Les autres graphiques
    elif chart_type == "Scatter Plot":
        st.subheader(f"Scatter Plot de {variable_1} et {variable_2}")
        plot_grouped_scatter_plots(filtered_data, variable_1, variable_2)
    elif chart_type == "Bar Chart":
        st.subheader(f"Bar Chart de {variable_1} ")
        plot_grouped_barplots(filtered_data, variable_1)
    elif chart_type == "Boxplot":
        st.subheader(f"Boxplot de {variable_1}")
        plot_grouped_boxplots(filtered_data, variable_1)
    elif chart_type == "Histogram":
        st.subheader(f"Histogramme de {variable_1}")
        plot_grouped_histograms(filtered_data, variable_1)
    elif chart_type == "Heatmap":
        st.subheader(f"Heatmap de {variable_1} et {variable_2}")
        plot_grouped_heatmap(filtered_data, variable_1, variable_2)
    elif chart_type == "Bar plot":
        st.subheader(f"Bar plot de {variable_2} moyen(ne) par {variable_1}")
        plot_moyen(filtered_data, variable_1, variable_2)