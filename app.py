import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import random

st.set_page_config(page_title="Ruth’s Wizard", layout="centered")

st.title("🧙 Ruth’s Wizard")
st.caption("Educational Mines probability simulator")

st.warning(
    "Educational tool only.\n"
    "This does NOT predict real gambling outcomes.",
    icon="⚠️"
)

# Sidebar
st.sidebar.header("Game Settings")
ROWS = st.sidebar.slider("Rows", 5, 10, 8)
COLS = st.sidebar.slider("Columns", 5, 10, 8)
MINES = st.sidebar.slider("Mines", 1, ROWS * COLS - 1, 10)
SIMS = st.sidebar.slider("Simulations", 100, 3000, 1000)

# Initialize state
if "revealed" not in st.session_state:
    st.session_state.revealed = set()

def generate_probabilities(rows, cols, mines, sims):
    counts = np.zeros((rows, cols))
    cells = [(r, c) for r in range(rows) for c in range(cols)]

    for _ in range(sims):
        mine_cells = random.sample(cells, mines)
        for r, c in mine_cells:
            counts[r, c] += 1

    return counts / sims

if st.button("✨ Generate Instant Probability Map"):
    st.session_state.probs = generate_probabilities(ROWS, COLS, MINES, SIMS)
    st.session_state.revealed = set()

# Show heatmap
if "probs" in st.session_state:
    probs = st.session_state.probs

    fig, ax = plt.subplots(figsize=(6, 6))
    im = ax.imshow(probs, cmap="coolwarm")
    plt.colorbar(im, ax=ax, label="Mine Probability")
    ax.set_title("Probability Heatmap")

    st.pyplot(fig)

    safest = np.unravel_index(np.argmin(probs), probs.shape)
    st.success(f"Safest cell: Row {safest[0]}, Column {safest[1]}")

    st.markdown("### 🎯 Clickable Board (Simulation)")
    for r in range(ROWS):
        cols_ui = st.columns(COLS)
        for c in range(COLS):
            key = f"{r}-{c}"
            if (r, c) in st.session_state.revealed:
                cols_ui[c].button(
                    f"{probs[r, c]:.2f}",
                    key=key,
                    disabled=True
                )
            else:
                if cols_ui[c].button("?", key=key):
                    st.session_state.revealed.add((r, c))
                    st.rerun()
