import datetime
import random
import requests
import os
import unicodedata
from bs4 import BeautifulSoup
import re


def get_phase_menstruelle(jour_debut: datetime.date, duree_cycle: int) -> str:
    """
    This method should help targeting the phase which the user is currently in.
    """
    jour_actuel = datetime.date.today()
    jour_cycle = (jour_actuel - jour_debut).days + 1

    jour_ovulation = duree_cycle - 14

    if jour_cycle <= 5:
        return "Menstruelle"
    elif jour_cycle < jour_ovulation:
        return "Folliculaire"
    elif jour_cycle == jour_ovulation:
        return "Ovulatoire"
    else:
        return "Lutéale"


def remove_accents(text):
    normalized_text = unicodedata.normalize("NFKD", text)
    return normalized_text.encode("ascii", "ignore").decode("utf-8")


def get_foods_by_nutrient(phase: str, percentage: float = 0.05):
    phase_cleaned = remove_accents(phase).lower()
    API_URL = os.getenv("API_URL")
    FULL_URL = f"{API_URL}/food-by-phase/"
    params = {"phase": phase_cleaned, "percentage": percentage}
    try:
        response = requests.get(FULL_URL, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error connection to API : {e}")
        return None


def pick_random_entries(entries):
    random_food_table = []
    for key, value in entries.items():
        if not value or len(value) == 0 or key == "*":
            continue
        sample = min(5, len(value))  # we take all of the table if it is too short

        if sample > 0:
            food_picked = random.sample(value, k=sample)
            for i in range(len(food_picked)):
                food_picked[i] = food_picked[i].split(",")[0].split("(")[0]
            random_food_table.extend(food_picked)

    return random_food_table


def get_recipes(entries: list[str]):
    search_url = "https://www.marmiton.org/recettes/recherche.aspx?aqt=plat+"
    sample = min(12, len(entries))
    food_picked = random.sample(entries, k=sample)

    recipes = {}
    for food in food_picked:
        food = food.replace(" ", "+").lower()
        response = requests.get(f"{search_url}{food}")
        if response.status_code == 200:
            html_content = response.text
            soup = BeautifulSoup(html_content, "html.parser")
            pattern = re.compile(r"^/recettes/")
            recipe = soup.find("a", attrs={"href": pattern})
            if recipe:
                recipes[recipe.get_text(strip=True)] = recipe.get("href")

        else:
            print(f"Response was : {response.status_code}")

    return recipes
