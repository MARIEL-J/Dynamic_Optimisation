import numpy as np
from scipy.optimize import minimize
import pandas as pd
import plotly.graph_objects as go
import streamlit as st  # For graph display within Streamlit

# Fonction de coût courant Ln(x, u)
def L(n, x, u):
    return u ** 2 - x - 1

# Fonction de récurrence fn(x, u)
def f(n, x, u):
    return x + u

def g(x):
    return 0

def optimize_continuous(L_func, f_func, V_next, n, x):
    def objective(u):
        return L_func(n, x, u) + V_next(f_func(n, x, u))[0]
    
    result = minimize(objective, x0=0)
    optimal_u = result.x[0]
    optimal_cost = result.fun
    return optimal_cost, optimal_u

def backward_induction(x0, time_horizon):
    V = {}
    policy = {}
    
    def V_n(n, x):
        if n == time_horizon:
            return g(x), None
        else:
            return optimize_continuous(L, f, lambda x: V_n(n+1, x), n, x)
    
    for n in range(time_horizon, -1, -1):
        V[n] = lambda x, n=n: V_n(n, x)
        policy[n] = V[n](x0)[1]
        
    return V, policy

def compute_states(x0, policy, time_horizon):
    x_values = [x0]
    for t in range(time_horizon):
        next_x = f(t, x_values[-1], policy[t])
        x_values.append(next_x)
    return x_values

# Updated graph plotting logic
def create_combined_plot(df):
    
    # Ajout d'une nouvelle colonne 
    df['col5'] = df.iloc[:, 2]*2 - df.iloc[:, 3]*2

    # Extraire les colonnes
    x_values = df.iloc[:, 0]  # 1ère colonne
    y_values1 = df.iloc[:, 1]  # 2ème colonne pour le premier diagramme en bâtons
    y_values2 = df['col5']  # Nouvelle colonne pour le deuxième diagramme en bâtons
    
    # Définir la largeur des bâtons
    width = 0.1
    # Créer la figure
    fig = go.Figure()

    # Premier diagramme en bâtons
    fig.add_trace(go.Bar(x=x_values, y=y_values1, name='Fonction valeur', width=width, offset=-width/2, marker_color='purple', opacity=0.8))

    # Deuxième diagramme en bâtons
    fig.add_trace(go.Bar(x=x_values, y=y_values2, name='Coût courant', width=width, offset=width/2, opacity=0.6))

    # Mettre à jour la mise en page
    fig.update_layout(
        title='Evolution du coût courant et de la fonction valeur',
        xaxis_title='Etape',
        yaxis_title='Coût courant et fonction valeur',
        barmode='group',
        yaxis=dict(autorange='reversed')  # Inverser l'axe Y
    )

    st.plotly_chart(fig)  # Display within Streamlit

def run_optimization(x0, time_horizon):
    V, policy = backward_induction(x0, time_horizon)

    df_results = pd.DataFrame({
        'Étape': list(range(time_horizon + 1)),
        'Fonction Valeur': [V[t](x0)[0] for t in range(time_horizon + 1)],
        'u Optimal': [policy[t] for t in range(time_horizon + 1)],
    })

    x_values = compute_states(x0, policy, time_horizon)
    df_results['État Optimal'] = x_values

    return df_results

# Exécution pour les tests
if __name__ == "__main__":
    x0 = int(input("Entrez l'état initial : "))
    time_horizon = int(input("Entrez l'horizon temporel : "))
    df_results = run_optimization(x0, time_horizon)
    create_combined_plot(df_results)
