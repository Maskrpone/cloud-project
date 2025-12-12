from streamlit.testing.v1 import AppTest
from app import get_phase_menstruelle
import datetime

# Vérifications de la page app.py


def test_app_page_selection_manuelle():
    at = AppTest.from_file("app.py")
    at.run()

    # simulation du choix de l'utilisateur
    at.selectbox[0].select("Ovulatoire").run()

    # enregistrement de la valeur fonctionnel
    assert at.session_state["user_config"]["phase_menstruelle"] == "ovulatoire"

    # Vérification de protentiels problèmes avec le bouton sauvegarder
    # at.button[0].click().run()
    # assert not at.exception


def test_app_page_calcul_auto():
    at = AppTest.from_file("app.py")
    at.run()

    # utilisateur selectionne "je ne sais pas"
    at.selectbox[0].select("Je ne sais pas").run()

    # vérifier que les nouveaux champs apparaissent
    assert len(at.date_input) > 0
    assert len(at.number_input) > 0

    # remplir les données
    today = datetime.date.today()
    start_date = today - datetime.timedelta(days=1)

    at.date_input[0].set_value(start_date).run()
    at.number_input[0].set_value(28).run()

    # vérif la logique

    assert "menstruelle" in at.success[0].value.lower()
    assert at.session_state["user_config"]["phase_menstruelle"] == "Menstruelle"


def test_phases_logiques():
    duree_cycle = 28
    today = datetime.date.today()

    # Doit être menstruelle
    debut_regles = today - datetime.timedelta(days=1)  # 1 jour écoulé
    assert get_phase_menstruelle(debut_regles, duree_cycle) == "Menstruelle"

    # Doit être folliculaire
    debut_regles = today - datetime.timedelta(days=9)
    assert get_phase_menstruelle(debut_regles, duree_cycle) == "Folliculaire"

    # Doit être ovulation pour un cycle de 28
    debut_regles = today - datetime.timedelta(days=13)
    assert get_phase_menstruelle(debut_regles, duree_cycle) == "Ovulatoire"

    # Doit être lutéale
    debut_regles = today - datetime.timedelta(days=19)
    assert get_phase_menstruelle(debut_regles, duree_cycle) == "Lutéale"


# Vérifications de la page prop_app.py


def test_prop_page_affichage_correct():
    at = AppTest.from_file("prop_page.py")

    # on test avec des données que l'utilisateur aurait testé
    at.session_state["user_config"] = {
        "saison": "juillet",
        "phase_menstruelle": "ovulation",
    }
    at.run()

    # vérification du text généré
    expected_text = "Au mois de **Juillet** et vous êtes dans la phase **ovulation** de votre cycle !"

    # revoie la liste de tous les texts markdown affichés
    markdown_content = [md.value for md in at.markdown]

    # le texte affiché
    assert any(expected_text in content for content in markdown_content)
    assert len(at.error) == 0  # vérification erreur


def test_prop_page_erreur_donnees_manquantes():
    at = AppTest.from_file("prop_page.py")

    at.session_state["user_config"] = {}  # on ne met rien dans la session
    at.run()

    # message d'erreur :
    assert len(at.error) > 0
    assert "Les informations nécessaires ne sont pas disponibles" in at.error[0].value
