import os
import pandas as pd
import anthropic
import streamlit as st
import streamlit.components.v1 as components
from dotenv import load_dotenv

# ── Config ────────────────────────────────────────────────────────────────────
load_dotenv()
CATALOG_PATH = os.path.join(os.path.dirname(__file__), "catalog.csv")
LOGO_PATH = os.path.join(os.path.dirname(__file__), "logo.png")
MODEL = "claude-opus-4-6"

# ── Brand CSS ─────────────────────────────────────────────────────────────────
BRAND_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap');
html, body, [class*="css"] { font-family: 'Inter', sans-serif !important; }
header[data-testid="stHeader"],
[data-testid="stToolbar"],
[data-testid="stDecoration"],
#MainMenu, footer { visibility: hidden !important; height: 0 !important; }
[data-testid="stSidebar"] { padding-top: 0.5rem !important; }
[data-testid="stSidebar"] hr { margin: 0.3rem 0 !important; }
[data-testid="stSidebar"] p { margin-bottom: 0.2rem !important; font-size: 0.82rem !important; }
[data-testid="stSidebar"] li { font-size: 0.82rem !important; }
[data-testid="stSidebar"] strong { font-size: 0.82rem !important; }
</style>
"""

# ── Inline SVG logo (fallback when logo.png not present) ──────────────────────
LOGO_SVG = """
<div style="padding:2px 0 4px 0;">
  <svg viewBox="0 0 320 56" xmlns="http://www.w3.org/2000/svg" style="width:90%;max-height:40px;">
    <polygon points="26,3 50,27 26,51 2,27" fill="#1A1A1A" stroke="#2e2e2e" stroke-width="1.5"/>
    <polyline points="16,37 26,13 36,37" fill="none" stroke="#E8E0D0" stroke-width="3" stroke-linejoin="round" stroke-linecap="round"/>
    <line x1="19" y1="32" x2="33" y2="32" stroke="#E8E0D0" stroke-width="3" stroke-linecap="round"/>
    <line x1="62" y1="10" x2="62" y2="46" stroke="#C84B2A" stroke-width="2"/>
    <text x="74" y="30" font-family="Inter,Arial Black,sans-serif" font-weight="800" font-size="17" letter-spacing="3" fill="#333">TRAILGEAR</text>
    <text x="74" y="44" font-family="Inter,Arial,sans-serif" font-weight="600" font-size="8" letter-spacing="4" fill="#C84B2A">CO.</text>
    <line x1="74" y1="47" x2="100" y2="47" stroke="#C84B2A" stroke-width="1"/>
  </svg>
</div>
"""

# ── Load catalog ──────────────────────────────────────────────────────────────
@st.cache_data
def load_catalog(path: str) -> pd.DataFrame:
    return pd.read_csv(path)


def catalog_to_text(df: pd.DataFrame) -> str:
    lines = []
    for _, row in df.iterrows():
        lines.append(
            f"[{row['id']}] {row['name']} | Category: {row['category']} | "
            f"Price: {row['price_eur']} EUR | Material: {row['material']} | "
            f"Weight: {row['weight_kg']}kg | "
            f"Certifications: {row['certifications'] if pd.notna(row['certifications']) else 'None'} | "
            f"Use case: {row['use_case']} | In stock: {row['in_stock']} | "
            f"Description: {row['description']}"
        )
    return "\n".join(lines)


# ── Claude call ───────────────────────────────────────────────────────────────
def ask_agent(user_question: str, catalog_text: str, history: list[dict]) -> str:
    client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

    system_prompt = f"""You are a knowledgeable outdoor gear assistant for TrailGear Co., an outdoor and hiking equipment retailer.

Answer customer questions using only the products listed in the catalog below.

Formatting rules — follow these exactly:
- Never use emojis of any kind.
- Never use em dashes (the — character). Use commas or short sentences instead.
- When listing multiple products, use a ## heading for each category or section, then plain paragraph text or a simple bullet list underneath.
- Always include the product name and price in euros (e.g. 89.99 EUR) when recommending a product.
- Keep answers helpful, concise and direct.
- If no products match the query, say so clearly. Do not invent products.

--- PRODUCT CATALOG ---
{catalog_text}
--- END CATALOG ---"""

    messages = history + [{"role": "user", "content": user_question}]

    response = client.messages.create(
        model=MODEL,
        max_tokens=1024,
        system=system_prompt,
        messages=messages,
    )
    return response.content[0].text


# ── Streamlit UI ──────────────────────────────────────────────────────────────
def main():
    st.set_page_config(
        page_title="TrailGear Co. Assistant",
        page_icon="🏔️",
        layout="centered",
        initial_sidebar_state="expanded",
    )

    # Inject brand styles
    st.markdown(BRAND_CSS, unsafe_allow_html=True)

    # Load catalog
    df = load_catalog(CATALOG_PATH)
    catalog_text = catalog_to_text(df)

    # ── Sidebar ───────────────────────────────────────────────────────────────
    with st.sidebar:
        # Logo
        if os.path.exists(LOGO_PATH):
            st.image(LOGO_PATH, use_container_width=True)
        else:
            st.markdown(LOGO_SVG, unsafe_allow_html=True)

        st.divider()

        st.markdown("**About**")
        st.markdown(
            "This AI agent reads a structured product catalog and answers natural "
            "language questions. No search bar, no filters needed."
        )

        st.divider()

        st.markdown("**How to use it**")
        st.markdown(
            "Type any question in plain English. You can ask for recommendations, "
            "compare products, filter by price or weight, and more."
        )

        st.divider()

        st.markdown("**Try asking**")
        sample_questions = [
            "What waterproof jackets do you have under 200 EUR?",
            "I need a sleeping bag for -10°C trips.",
            "What is the lightest tent in the range?",
            "Which products have EN certifications?",
            "Recommend a full kit for a 3-day hiking trip.",
        ]
        questions_html = "".join(
            f"<p style='margin:1px 0;font-size:0.8rem;'><em>{q}</em></p>"
            for q in sample_questions
        )
        st.markdown(questions_html, unsafe_allow_html=True)

        st.divider()

        st.markdown("**Author**")
        st.markdown("Dani Baumgarten")
        st.markdown(
            "[LinkedIn](https://www.linkedin.com/in/danibaum8/)  "
            "[GitHub](https://github.com/danibaum8)  "
            "[Kaggle](https://www.kaggle.com/danibaum)"
        )

        st.divider()

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Products", len(df))
        with col2:
            st.metric("Categories", df["category"].nunique())
        with col3:
            st.metric("In stock", int(df["in_stock"].sum()))

        st.divider()

        if st.button("Clear Chat", use_container_width=True):
            st.session_state.messages = []
            st.rerun()

    # Lock sidebar — auto-expand if collapsed, hide collapse button
    components.html("""
    <script>
    (function() {
        function manageSidebar() {
            var doc = window.parent.document;
            // Auto-expand if currently collapsed
            var expandBtn = doc.querySelector('[data-testid="collapsedControl"]');
            if (expandBtn && expandBtn.offsetParent !== null) {
                expandBtn.click();
            }
            // Hide the collapse button inside the sidebar
            var collapseBtn = doc.querySelector('[data-testid="stSidebarCollapseButton"]');
            if (collapseBtn) collapseBtn.style.display = 'none';
            // Hide any sidebar button with collapse/close aria-label
            var sidebarBtns = doc.querySelectorAll('[data-testid="stSidebar"] button');
            sidebarBtns.forEach(function(btn) {
                var label = (btn.getAttribute('aria-label') || '').toLowerCase();
                if (label.includes('collapse') || label.includes('close')) {
                    btn.style.display = 'none';
                }
            });
        }
        // Run immediately, then keep watching for DOM changes
        manageSidebar();
        setInterval(manageSidebar, 400);
    })();
    </script>
    """, height=1)

    # ── Main chat area ────────────────────────────────────────────────────────
    st.markdown("## Ask about our gear")
    st.caption("Get instant answers about products, specs, pricing and recommendations.")

    # Initialise chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Render chat history
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Chat input
    if prompt := st.chat_input("E.g. What is the lightest tent you have?"):
        with st.chat_message("user"):
            st.markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})

        history = st.session_state.messages[:-1]

        with st.chat_message("assistant"):
            with st.spinner("Searching catalog..."):
                reply = ask_agent(prompt, catalog_text, history)
            st.markdown(reply)

        st.session_state.messages.append({"role": "assistant", "content": reply})


if __name__ == "__main__":
    main()
