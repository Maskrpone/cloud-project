import streamlit as st
from utils import get_foods_by_nutrient, pick_random_entries

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


# Navigation
pg = st.navigation([prop_page, "app.py"], position="hidden")
pg.run()
