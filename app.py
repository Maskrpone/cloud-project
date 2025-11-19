import streamlit as st
import datetime

user_config = {}

def get_phase_menstruelle(jour_debut: datetime.date, duree_cycle: int):
    """
    This method should help targeting the phase which the user is currently in.
    """
    jour_actuel = datetime.date.today()
    jour_cycle = (jour_actuel - jour_debut).days + 1

    jour_ovulation = duree_cycle - 14

    if jour_cycle <= 5:
        return "menstruelle"
    elif jour_cycle < jour_ovulation:
        return "folliculaire"
    elif jour_cycle == jour_ovulation:
        return "ovulation"
    else:
        return "lutéale"


# st.set_page_config(layout="wide", page_title="Cycle & Saison")

# with st.sidebar:
st.header("Formulaire de personnalisation")

with st.expander("Menstruation", expanded=True):
    phase = st.selectbox(
        "**Dans quelle phase de votre cycle êtes-vous ?**",
        ("Menstruation", "Folliculaire", "Ovulation", "Lutéale", "Je ne sais pas"),
    )

    user_config["phase_menstruelle"] = phase.lower()

    if phase == "Je ne sais pas":
        st.text("Pas de problème nous allons essayer de le deviner au mieux !")
        first_day_of_period = st.date_input(
            "Quelle est la date du premier jour de vos dernières règles ?",
            datetime.date.today(), max_value=datetime.date.today()
        )
        duree_cycle = st.number_input(
            "Combien de temps dure votre cycle en moyenne ?", value=28
        )
        st.info(
            "La durée moyenne du cycle menstruelle d'une fille est de 28 jours environ."
        )

        if first_day_of_period and duree_cycle:
            guessed_phase = get_phase_menstruelle(first_day_of_period, duree_cycle)
            user_config["phase_menstruelle"] = guessed_phase
            st.success(
                f"Vous êtes très certainement dans la phase **{guessed_phase}** de votre cycle menstruel"
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

with st.expander("Saison"):
    # st.text("Questionnaire saison")
    date = datetime.date.today()
    st.info(f"Nous sommes aujourd'hui en **{all_months[date.month - 1]}**")
    wanted_season = st.selectbox(
        "Selectionnez le mois que vous voulez analyser",
        (month for month in all_months),
        index=(date.month - 1),
    )

    user_config["saison"] = wanted_season.lower()

saved = st.button("Sauvegarder")

if saved:
    st.success("Configuration sauvegardée !")


# TODO : Utiliser l'API data.gouv pour récupérer les légumes et fruits de saison.

st.json(user_config)

# st.title("Smart Planner")
# st.info(
#     "Smart Planner est une application vous permettant de déterminer quels aliments seraient à privilégier pour vous, selon plusieurs facteur. Ce n'est pas un dispositif médical. \n"
# )
# st.markdown(" ---")
#
# # Symptômes
# symptomes = st.multiselect(
#     "**Quels symptômes souhaitez-vous soulager ?**",
#     [
#         "Crampes",
#         "Fatigue",
#         "Ballonnements/Rétention d'eau",
#         "Fringales de sucre",
#         "Sautes d'humeur",
#     ],
# )
#
# # Restrictions
# regime = st.radio(
#     "**Suivez-vous un régime alimentaire particulier ?**",
#     ("Classique", "Végétarien", "Végétalien", "Sans Gluten"),
# )
#
# st.json("{'test': 'ezd'}")
#
# st.markdown("## Recommandations")
# st.info(
#     f"En tant que personne en phase **{phase}** en **{saison}**, voici les aliments à privilégier :"
# )
#
#
# # Exemple de fonction de recommandation simple (à développer)
# def get_reco(phase, saison, symptomes, regime):
#     recommandations = []
#
#     # Logique basée sur la phase
#     if phase == "Menstruation":
#         recommandations.append(
#             "Fer : Viande rouge, Épinards (printemps), Lentilles, Graines de sésame."
#         )
#     elif phase == "Lutéale" and "Ballonnements/Rétention d'eau" in symptomes:
#         recommandations.append(
#             "Potassium et Magnésium : Bananes, Légumes-feuilles (si disponibles en saison)."
#         )
#
#     # Logique basée sur la saison
#     if saison == "Hiver":
#         recommandations.append(
#             "Racines chaudes : Patates douces, carottes, soupes. Vitamine C (oranges/citrons)."
#         )
#
#     # Logique basée sur les restrictions
#     if regime == "Végétalien" and "Fer" in recommandations[0]:
#         recommandations = [r.replace("Viande rouge, ", "") for r in recommandations]
#
#     return recommandations
#
#
# recommandations_finales = get_reco(phase, saison, symptomes, regime)
#
# for reco in recommandations_finales:
#     st.success(f"* {reco}")
