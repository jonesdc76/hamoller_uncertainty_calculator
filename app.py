import streamlit as st
import numpy as np

st.set_page_config(page_title="Asymmetry Calculator", page_icon="📊")
st.title("📊 Asymmetry Uncertainty & Time Calculator")
st.markdown("This app calculates statistical metrics for the rate asymmetry: $A = \\frac{N_1 - N_2}{N_1 + N_2}$")

st.sidebar.header("⏱️ Rate Settings")
use_rate = st.sidebar.checkbox("Translate Counts (N) to Time?", value=True)
if use_rate:
    rate = st.sidebar.number_input("Total Event Rate (R1 + R2) per second", min_value=1e-3, value=100.0, format="%f")

mode = st.radio(
    "Choose your calculation mode:",
    ("Calculate Relative Uncertainty (given N and A)", "Calculate Required Counts (given A and Relative Uncertainty)")
)

st.divider()

if mode == "Calculate Relative Uncertainty (given N and A)":
    st.subheader("Compute $\\sigma_A / A$")
    col1, col2 = st.columns(2)
    with col1:
        A = st.number_input("Asymmetry (A)", min_value=0.0, max_value=1.0, value=0.05, step=0.01, format="%f")
    with col2:
        N = st.number_input("Total Events (N)", min_value=1, value=10000, step=1000)
    
    if A == 0:
        st.error("Asymmetry (A) cannot be 0 for relative uncertainty.")
    else:
        sigma_A = np.sqrt((1 - A**2) / N)
        rel_uncertainty = sigma_A / A
        st.metric(label="Relative Uncertainty (σ_A / A)", value=f"{rel_uncertainty:.4f} ({rel_uncertainty*100:.2f}%)")
        st.write(f"**Absolute Uncertainty (σ_A):** {sigma_A:.5f}")
        if use_rate:
            st.info(f"⏱️ **Time required:** {N / rate:.2f} seconds")

else:
    st.subheader("Compute Required $N$")
    col1, col2 = st.columns(2)
    with col1:
        A = st.number_input("Expected Asymmetry (A)", min_value=1e-6, max_value=1.0, value=0.05, step=0.01, format="%f")
    with col2:
        target_rel = st.number_input("Target Relative Uncertainty (σ_A / A)", min_value=1e-6, value=0.02, step=0.005, format="%f")
    
    N_required = int(np.ceil((1 - A**2) / (A**2 * target_rel**2)))
    st.metric(label="Required Total Events (N)", value=f"{N_required:,}")
    if use_rate:
        st.info(f"⏱️ **Required time:** {N_required / rate:.2f} seconds")
