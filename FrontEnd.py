import numpy as np
import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import time  # Pour simuler le chargement
from BackEnd import create_combined_plot, run_optimization

# Configuration de la page
def set_page_config():
    st.set_page_config(page_title="Optimisation de Bellman", layout="wide")
    st.markdown("""
        <style>
        .background {
            background-color: #f0f0f5;
            padding: 20px;
            border-radius: 10px;
        }
        .title {
            color: #4CAF50;
            font-size: 36px;
        }
        </style>
    """, unsafe_allow_html=True)

# Page d'accueil
def home_page():
    set_page_config()
    st.markdown("<div class='background'>", unsafe_allow_html=True)

    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.image("ENEAM.jpg", use_column_width='auto')
    with col2:
        st.image("ISE.png", use_column_width='auto')

    st.title("PROJET ACADEMIQUE : OPTIMISATION DYNAMIQUE", anchor="title")
    st.write("Réalisé par :")
    st.write("1. AKINDELE Féridia")
    st.write("2. CHALLA Emmanuel")
    st.write("3. HOUNSOU Jacquelin")
    st.write("4. ZOUNTCHEME Ulrich")
    
    if st.button("Suivant"):
        st.session_state.page = "methodology"

    st.markdown("<footer style='text-align: center;'><small>&copy; ISE2-ENEAM</small></footer>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# Page de méthodologie
def methodology_page():
    set_page_config()
    st.markdown("<div class='background'>", unsafe_allow_html=True)
    
    st.title("Résolution d'un problème d'optimisation dynamique en horizon fini")
    st.markdown(r"""
        ### Méthodologie utilisée
        Nous considérons ici le problème en horizon fini :
        $$ 
        \min_{u \in U} \sum_{n=0}^{N-1} L_n(x_n, u_n) + g(x_N) 
        $$

        Le principe de la programmation dynamique montre que le problème initial peut s'exprimer de deux façons :
        $$ 
        V(0, \mathbf{x}) = \inf_{u \in U} \sum_{n=0}^{N-1} L_n(x_n, u_n) + g(x_N)
        = \inf_{u \in U_0} \{ L_0(\mathbf{x}, u) + V(1, f_0(\mathbf{x}, u)) \}
        $$

        Le problème dans la deuxième égalité est "plus simple" à résoudre puisqu'il s'agit d'une minimisation standard.

        Pour calculer \( V(0, \mathbf{x}) \), on résout par induction rétrograde :
        $$ 
        V(N - 1, x) = \inf_{u \in U_{N-1}} \{ L_{N-1}(x, u) + g(f_{N-1}(x, u)) \}.
        $$
    """)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        if st.button("Précédent"):
            st.session_state.page = "home"
    
    with col2:
        if st.button("Suivant"):
            st.session_state.page = "problem"
    
    st.markdown("</div>", unsafe_allow_html=True)

# Page de problème
def problem_page():
    set_page_config()
    st.markdown("<div class='background'>", unsafe_allow_html=True)
    
    st.title("Problème à résoudre")
    st.write("On considère le problème suivant :")
    st.markdown(r"""
    Minimiser la fonction suivante :
    $$
    \min \sum_{n=0}^{N} (u_n^2 - x_n - 1) 
    $$
    
    sous les contraintes :
    $$
    x_{n+1} = x_n + u_n.
    $$""")
    
    st.write("Pour un horizon N fixé et un état initial donné, vous avez la possibilité de connaître la suite des états optimaux et la suite des contrôles optimaux.")

    x0 = st.number_input("Veuillez entrer l'état initial x0:", value=0.0)
    N = st.number_input("Veuillez insérer l'horizon du problème (ex: 10)", min_value=1, value=10)

    if st.button("Valider"):
        # Affichage de la jauge et message d'attente
        progress_bar = st.progress(0)
        status_text = st.empty()
        status_text.text("Veuillez patienter !!!")

        # Simulation de chargement
        for i in range(100):
            time.sleep(0.05)  # Simule un temps de traitement
            progress_bar.progress(i + 1)

        # Calcul des résultats de l'optimisation
        df_results = run_optimization(x0, N)

        status_text.text("Calcul terminé.")
        st.write("Résultats de l'optimisation :")
        st.dataframe(df_results)

        # Appel à la fonction de graphique combiné
        create_combined_plot(df_results)

    if st.button("Précédent"):
        st.session_state.page = "methodology"

    st.markdown("</div>", unsafe_allow_html=True)


# Main
if 'page' not in st.session_state:
    st.session_state.page = "home"

if st.session_state.page == "home":
    home_page()
elif st.session_state.page == "methodology":
    methodology_page()
elif st.session_state.page == "problem":
    problem_page()
