import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import pandas as pd

# Fonction de visualisation : Scatter Plot
def plot_grouped_scatter_plots(data, variable_1, variable_2):
    
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.scatterplot(data=data, x=variable_1, y=variable_2, ax=ax, palette='Blues')
    ax.set_title(f"Nuage de points entre {variable_1} et {variable_2} ")
    ax.set_xlabel(variable_1)
    ax.set_ylabel(variable_2)
    st.pyplot(fig)

# Fonction de visualisation : Bar Plot
def plot_grouped_barplots(data, variable):
    
    counts = data[variable].value_counts().sort_values(ascending=False)
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(x=counts.index, y=counts.values, ax=ax, palette="Blues")
    ax.set_xlabel(variable, fontsize=14)
    ax.set_ylabel("Fréquence", fontsize=14)
    ax.tick_params(axis='x', rotation=45)
    st.pyplot(fig)

# Fonction de visualisation : Box Plot
def plot_grouped_boxplots(data, variable):
    
    
    quantiles = data[variable].quantile([0.25, 0.5, 0.75]) 
    
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.boxplot(data=data,  y=variable, ax=ax, palette="Blues")
    ax.set_xlabel('Filtered data')
    ax.set_ylabel(variable)
    st.pyplot(fig)
    
    st.subheader("Interprétation :")
    st.write(f"Les quantiles sont : (Q1): {quantiles[0.25]},\
        (Q2): {quantiles[0.5]} et (Q3): {quantiles[0.75]}  sur ces \
        morceaux sélectionnés", fontsize=16)

# Fonction de visualisation : Histogram
def plot_grouped_histograms(data, variable):
    
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.histplot(data[variable], ax=ax, color='skyblue', kde=True, bins=30)
    ax.set_xlabel(variable)
    ax.set_ylabel("Fréquence")
    st.pyplot(fig)

# Fonction de visualisation : Heatmap
def plot_grouped_heatmap(data, variable_1, variable_2):
    
    fig, ax = plt.subplots(figsize=(8, 6))
    corr_matrix = data[[variable_1, variable_2]].corr()
    sns.heatmap(corr_matrix, annot=True, cmap="Blues", ax=ax)
    ax.set_title(f"Heatmap de {variable_1} et {variable_2}")
    st.pyplot(fig)

# Fonction de visualisation des clusters K-means
def plot_kmeans_clusters(data, clusters):
    data['Cluster'] = clusters
    fig, ax = plt.subplots(figsize=(10, 8))
    sns.scatterplot(data=data, x='duration_ms', y='popularity', hue='Cluster', palette="viridis")
    ax.set_xlabel('Duration')
    ax.set_ylabel('Popularity')
    st.pyplot(fig)

# Fonction de visualisation des clusters K-NN
def plot_knn_clusters(data, clusters):
    data['Cluster'] = clusters
    fig, ax = plt.subplots(figsize=(10, 8))
    sns.scatterplot(data=data, x='duration_ms', y='popularity', hue='Cluster', palette="magma")
    ax.set_xlabel('Duration')
    ax.set_ylabel('Popularity')
    st.pyplot(fig)

# Fonction de visualisation : PCA
def plot_pca_clusters(data, pca_result):
    pca_df = pd.DataFrame(data=pca_result, columns=[f'PCA {i+1}' for i in range(pca_result.shape[1])])
    pca_df['genre_group'] = data['genre_group'].values
    fig, ax = plt.subplots(figsize=(10, 8))
    sns.scatterplot(data=pca_df, x='PCA 1', y='PCA 2',  palette="Set2", ax=ax)
    ax.set_title("PCA Clusters")
    ax.set_xlabel("PCA 1")
    ax.set_ylabel("PCA 2")
    st.pyplot(fig)



def plot_moyen(data, variable_1, variable_2):
    
    # Calcul des ventes moyennes par genre
    dt = data.groupby(variable_1)[variable_2].mean().reset_index()
    dt = dt.sort_values(by=variable_2, ascending=False)
    
    # Composante avec la plus grande moyenne
    max_component = dt.iloc[0]  # La ligne avec la plus grande moyenne
    max_value = max_component[variable_1]  # La composante correspondante
    max_mean = max_component[variable_2]  # La moyenne correspondante

    # Création du graphique combiné
    fig, ax = plt.subplots(figsize=(12, 7))
    
    # Barplot : Ventes moyennes par genre
    sns.barplot(data=dt, x=variable_1, y=variable_2, palette='Blues_d', alpha=0.7, ax=ax)
    
    # Lineplot : Ajout d'une courbe pour mieux visualiser les tendances
    sns.lineplot(data=dt, x=variable_1, y=variable_2, color='darkblue', marker='o', ax=ax)
    
    # Personnalisation du graphique
    ax.set_title(f" {variable_2} moyen(ne) par {variable_1}", fontsize=16)
    ax.set_xlabel(variable_1, fontsize=14)
    ax.set_ylabel(f"moyenne {variable_2}", fontsize=14)
    ax.tick_params(axis='x', rotation=45)
    ax.grid(axis='y', linestyle='--', alpha=0.7)
    
    # Affichage dans Streamlit
    st.pyplot(fig)
    st.subheader("Interprétation :")
    st.write(f"{max_value} a en moyenne {variable_2} le plus élevé sur ces \
        morceaux sélectionnés", fontsize=16)