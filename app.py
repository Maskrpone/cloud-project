import streamlit as st
import datetime
from utils import get_phase_menstruelle

user_config = {}
st.set_page_config(
    page_title="Home", page_icon=":notebook:", initial_sidebar_state="collapsed"
)

all_months = [
    "Janvier",
    "Février",
    "Mars",
    "Avril",
    "Mai",
    "Juin",
    "Juillet",
    "Août",
    "Septembre",
    "Octobre",
    "Novembre",
    "Décembre",
]


def home_page():
    st.logo("images/logo_cloud.png")
    if "user_config" not in st.session_state:
        st.session_state["user_config"] = {}
    st.header("Bonjour, nous avons besoin de vous !")
    st.markdown(
        "**Pourriez-vous répondre à quelques questions afin que nous puissions au mieux vous conseiller ?**"
    )

    with st.expander("**Cycle**", expanded=True):
        phase = st.selectbox(
            "**Dans quelle phase de votre cycle êtes-vous ?**",
            ("Menstruelle", "Folliculaire", "Ovulatoire", "Lutéale", "Je ne sais pas"),
        )

    st.session_state["user_config"]["phase_menstruelle"] = phase.lower()

    if phase == "Je ne sais pas":
        st.text("Pas de problème nous allons essayer de le deviner au mieux !")
        first_day_of_period = st.date_input(
            "Quelle est la date du premier jour de vos dernières règles ?",
            datetime.date.today(),
            max_value=datetime.date.today(),
        )
        duree_cycle = st.number_input(
            "Combien de temps dure votre cycle en moyenne ?", value=28
        )
        st.info(
            "La durée moyenne du cycle menstruelle d'une fille est de 28 jours environ."
        )

        if first_day_of_period and duree_cycle:
            guessed_phase = get_phase_menstruelle(first_day_of_period, duree_cycle)
            st.session_state["user_config"]["phase_menstruelle"] = guessed_phase
            st.success(
                (
                    f"Vous êtes très certainement dans la phase **{guessed_phase}**",
                    "de votre cycle menstruel",
                )
            )

    with st.expander("**Saison**"):
        date = datetime.date.today()
        st.info(f"Nous sommes aujourd'hui en **{all_months[date.month - 1]}**")
        wanted_season = st.selectbox(
            "Selectionnez le mois que vous voulez analyser",
            (month for month in all_months),
            index=(date.month - 1),
        )

        st.session_state["user_config"]["saison"] = wanted_season.lower()

    saved = st.button("Sauvegarder")

    if saved:
        st.switch_page("prop_page.py")


home = st.Page(home_page, title="Home", default=True)
props = st.Page("prop_page.py", title="Properties")

pg = st.navigation([home_page, props], position="hidden")
pg.run()

# TODO : Utiliser l'API data.gouv pour récupérer les légumes et fruits de saison.
