import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import random

st.set_page_config(page_title="Ruth’s Wizard", layout="centered")

st.title("🧙 Ruth’s Wizard")
st.caption("Educational Mines probability visualizer")

# Sidebar controls
st.sidebar.header("Game Settings")
rows = st.sidebar.slider("Rows", 5, 10, 8)
cols = st.sidebar.slider("Columns", 5, 10, 8)
mines = st.sidebar.slider("Mines", 1, rows * cols - 1, 10)
simulations = st.sidebar.slider("Simulations", 100, 2000, 500)

st.sidebar.markdown("---")
st.sidebar.info("This tool is for **educational purposes only**.\n\nIt does NOT predict real game outcomes.")

def generate_heatmap(rows, cols, mines, simulations):
    mine_counts = np.zeros((rows, cols))

    for _ in range(simulations):
        cells = [(r, c) for r in range(rows) for c in range(cols)]
        mine_positions = random.sample(cells, mines)

        for r, c in mine_positions:
            mine_counts[r, c] += 1

    return mine_counts / simulations

if st.button("✨ Generate Instant Probability Map"):
    heatmap = generate_heatmap(rows, cols, mines, simulations)

    fig, ax = plt.subplots(figsize=(6, 6))
    im = ax.imshow(heatmap, cmap="coolwarm")
    plt.colorbar(im, ax=ax, label="Mine Probability")
    ax.set_title("Ruth’s Wizard — Instant Probability Map")

    st.pyplot(fig)

    safest = np.unravel_index(np.argmin(heatmap), heatmap.shape)
    st.success(f"Safest cell (lowest probability): Row {safest[0]}, Column {safest[1]}")
