import streamlit as st
import time
from pathlib import Path
import matplotlib.pyplot as plt

from src.parser import parse_cordeau_mdvrp
from src.distance import create_distance_matrix
from src.baseline import solve_nearest_neighbor
from src.model import solve_with_ortools
from src.visualization import plot_solution

# -- PAGE SETUP --
st.set_page_config(page_title="MDVRP Optimizer", page_icon="🚚", layout="wide")
st.title("🚚 Multi-Depot Vehicle Routing Optimizer")
st.markdown("An end-to-end supply chain analytics project solving the Multi-Depot Vehicle Routing Problem.")

# -- LOAD DATA --
# (Using st.cache_data so the web app doesn't recalculate the math every time you click a button)
@st.cache_data
def load_and_prep_data():
    base_dir = Path(__file__).resolve().parent
    file_path = base_dir / "data" / "raw" / "cordeau" / "p01.txt"
    data = parse_cordeau_mdvrp(file_path)
    locations, dist_matrix = create_distance_matrix(data)
    return data, locations, dist_matrix

data, locations, dist_matrix = load_and_prep_data()

# -- SIDEBAR CONTROLS --
st.sidebar.header("Optimization Controls")
time_limit = st.sidebar.slider("AI Thinking Time (seconds)", min_value=1, max_value=30, value=5)

if st.sidebar.button("🚀 Run Optimization"):
    
    # Create two columns side-by-side for our results
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Baseline (Human Heuristic)")
        with st.spinner("Running Nearest Neighbor..."):
            base_sol = solve_nearest_neighbor(data, dist_matrix)
            
            st.metric(label="Total Distance", value=f"{base_sol['total_distance']:.2f}")
            st.metric(label="Vehicles Used", value=len(base_sol['routes']))
            
            # Draw Baseline Map
            fig_base = plot_solution(data, base_sol, title="Baseline Routes")
            st.pyplot(fig_base)

    with col2:
        st.subheader("OR-Tools (AI Optimizer)")
        with st.spinner(f"Running Google OR-Tools for {time_limit} seconds..."):
            or_sol = solve_with_ortools(data, dist_matrix, time_limit_seconds=time_limit)
            
            # Calculate savings
            savings = base_sol['total_distance'] - or_sol['total_distance']
            
            st.metric(label="Total Distance", value=f"{or_sol['total_distance']:.2f}", delta=f"-{savings:.2f} distance saved", delta_color="inverse")
            st.metric(label="Vehicles Used", value=or_sol['vehicles_used'])
            
            # Draw AI Map
            fig_or = plot_solution(data, or_sol, title="AI Optimized Routes")
            st.pyplot(fig_or)

    st.success("Optimization Complete! 🎉")
else:
    st.info("👈 Click 'Run Optimization' in the sidebar to start!")