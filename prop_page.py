import streamlit as st
import requests
from bs4 import BeautifulSoup
from utils import get_foods_by_nutrient, pick_random_entries, get_recipes

# st.set_page_config(
#     page_title="Propositions", page_icon=":stew:", initial_sidebar_state="collapsed"
# )

saison = st.session_state["user_config"].get("saison", None)

phase = st.session_state["user_config"].get("phase_menstruelle", None)


def get_user_info(saison, phase):
    if saison and phase:
        return f"Au mois de **{saison.capitalize()}** et vous êtes dans la phase **{phase}** de votre cycle !"
    else:
        return "ERROR"


def recipe_card(title: str, link: str) -> None:
    url = f"https://www.marmiton.org{link}"
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        image = soup.find("img", id="recipe-media-viewer-main-picture")
        image_alt = soup.find("img", id="recipe-media-viewer-thumbnail-0")
        print(image)
        if image:
            st.image(image.get("data-src"))
        elif image_alt:
            st.image(image_alt.get("data-src"))
        else:
            st.image(
                "https://assets.afcdn.com/recipe/20100101/recipe_default_img_placeholder_w500h500c1.jpg"
            )
        # col1, col2, col3 = st.columns(3)
        # with col1, col2:
        st.link_button(f"{title}", url, use_container_width=True)


def prop_page():
    st.logo("images/logo_cloud.png", size="large")
    st.header("Vous êtes donc...")

    # Infos de la session utilisateur
    user_info = get_user_info(saison, phase)

    if user_info != "ERROR":
        st.markdown(user_info)
        if st.button("Pas vraiment"):
            st.switch_page("app.py")
    else:
        st.error("Les informations nécessaires ne sont pas disponibles")

    # Liste des aliments
    with st.expander("Aliments conseillés 🥕", expanded=True):
        with st.spinner("Fetching data..."):
            data = get_foods_by_nutrient(
                st.session_state["user_config"].get("phase_menstruelle")
            )
            entries = pick_random_entries(data[0])
            render_md = ""
            for entry in entries:
                render_md += f"- {entry}\n"
            st.markdown(render_md)

    # Liste des plats
    with st.expander("Plats conseillés 🍲", expanded=True):
        st.write("""liste de plats""")
        if entries and len(entries) > 0:
            recipes = get_recipes(entries)
            cols = st.columns(3, width="stretch")
            for i, (title, link) in enumerate(recipes.items()):
                col = cols[i % 3]
                with col:
                    recipe_card(title, link)
        else:
            st.write("Pas de recettes pour le moment.")


# Navigation
pg = st.navigation([prop_page, "app.py"], position="hidden")
pg.run()
