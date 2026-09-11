import streamlit as st
import time
from pathlib import Path
import matplotlib.pyplot as plt

from src.parser import parse_cordeau_mdvrp
from src.distance import create_distance_matrix
from src.baseline import solve_nearest_neighbor
from src.model import solve_with_ortools
from src.visualization import plot_solution

# -- PAGE SETUP (Must be first) --
st.set_page_config(page_title="OptiRoute | Logistics Engine", page_icon="🧭", layout="wide")

# -- CUSTOM CSS HACKS --
st.markdown("""
<style>
    .main-header { font-size: 2.5rem; font-weight: 700; color: #1E3A8A; margin-bottom: 0;}
    .sub-header { font-size: 1.2rem; color: #6B7280; margin-bottom: 2rem;}
    .stButton>button { width: 100%; border-radius: 8px; font-weight: bold; }
    div[data-testid="stMetricValue"] { font-size: 2rem; color: #047857; }
</style>
""", unsafe_allow_html=True)

# -- HEADER --
st.markdown('<p class="main-header">🧭 OptiRoute Dispatch Engine</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Intelligent Multi-Depot Fleet Routing & Load Balancing</p>', unsafe_allow_html=True)

# -- LOAD DATA --
@st.cache_data
def load_and_prep_data():
    base_dir = Path(__file__).resolve().parent
    file_path = base_dir / "data" / "raw" / "cordeau" / "p01.txt"
    data = parse_cordeau_mdvrp(file_path)
    locations, dist_matrix = create_distance_matrix(data)
    return data, locations, dist_matrix

data, locations, dist_matrix = load_and_prep_data()

# -- SIDEBAR CONTROLS --
with st.sidebar:
    st.header("⚙️ Dispatch Parameters")
    time_limit = st.slider("AI Compute Time (seconds)", min_value=1, max_value=60, value=10, 
                           help="Longer compute times yield tighter routing efficiencies.")
    run_button = st.button("🚀 Optimize Routes", type="primary")
    
    st.divider()
    st.caption("Active Dataset: Cordeau p01")
    st.caption(f"Network: {len(data['depots'])} Depots | {len(data['customers'])} Customers")

# -- MAIN DASHBOARD --
if run_button:
    # Use Tabs for a cleaner layout instead of cramming everything onto one page
    tab1, tab2 = st.tabs(["📊 AI Optimizer (OR-Tools)", "📉 Baseline Comparison"])
    
    with tab1:
        with st.spinner("Crunching permutations..."):
            or_sol = solve_with_ortools(data, dist_matrix, time_limit_seconds=time_limit)
            
            col1, col2, col3 = st.columns(3)
            col1.metric("Total Route Distance", f"{or_sol['total_distance']:.2f} km")
            col2.metric("Active Fleet", f"{or_sol['vehicles_used']} Trucks")
            col3.metric("Compute Time", f"{time_limit} sec")
            
            st.markdown("### Optimized Route Map")
            fig_or = plot_solution(data, or_sol, title="")
            st.pyplot(fig_or)

    with tab2:
        with st.spinner("Running heuristic baseline..."):
            base_sol = solve_nearest_neighbor(data, dist_matrix)
            savings = base_sol['total_distance'] - or_sol['total_distance']
            
            col1, col2 = st.columns(2)
            col1.metric("Baseline Distance", f"{base_sol['total_distance']:.2f} km")
            col2.metric("AI Savings", f"{savings:.2f} km", delta=f"-{(savings/base_sol['total_distance'])*100:.1f}% vs baseline", delta_color="inverse")
            
            fig_base = plot_solution(data, base_sol, title="Inefficient Heuristic Routing")
            st.pyplot(fig_base)
else:
    st.info("Configure your parameters in the sidebar and click **Optimize Routes** to generate a dispatch plan.")