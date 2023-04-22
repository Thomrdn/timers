from flask import Flask
import requests
from datetime import datetime, timedelta, timezone

app = Flask(__name__)

@app.route("/timers")
def index():
    # Appel de l'API et récupération des données JSON
    response = requests.get("http://dbd-info.com/api/timers")
    data = response.json()

    # Extraction des données nécessaires
    player_count = data["data"]["playerCount"]
    shrine_reset_date_str = data["data"]["timers"]["shrineResetDate"]
    rift_end_date_str = data["data"]["timers"]["riftEndDate"]
    grade_reset_date_str = data["data"]["timers"]["gradeResetDate"]

    # Conversion des chaînes de caractères en objets datetime avec fuseau horaire
    shrine_reset_date = datetime.fromisoformat(shrine_reset_date_str).astimezone(timezone.utc) + timedelta(hours=2)
    rift_end_date = datetime.fromisoformat(rift_end_date_str).astimezone(timezone.utc) + timedelta(hours=2)
    grade_reset_date = datetime.fromisoformat(grade_reset_date_str).astimezone(timezone.utc) + timedelta(hours=2)

    # Calcul des durées restantes avec fuseau horaire
    shrine_reset_delta = shrine_reset_date - datetime.now(tz=shrine_reset_date.tzinfo)
    rift_end_delta = rift_end_date - datetime.now(tz=rift_end_date.tzinfo)
    grade_reset_delta = grade_reset_date - datetime.now(tz=grade_reset_date.tzinfo)

    # Formatage de la chaîne de caractères finale
    result = "Nombre de joueurs Steam en ligne : {} | Raffraichissement du Temple : {} jours, {} heures, {} minutes, {} secondes. | Fermeture de la Faille : {} jours, {} heures, {} minutes, {} secondes. | Réinitialisation des Rangs : {} jours, {} heures, {} minutes, {} secondes. |".format(
        player_count,
        shrine_reset_delta.days,
        shrine_reset_delta.seconds // 3600,
        (shrine_reset_delta.seconds // 60) % 60,
        shrine_reset_delta.seconds % 60,
        rift_end_delta.days,
        rift_end_delta.seconds // 3600,
        (rift_end_delta.seconds // 60) % 60,
        rift_end_delta.seconds % 60,
        grade_reset_delta.days,
        grade_reset_delta.seconds // 3600,
        (grade_reset_delta.seconds // 60) % 60,
        grade_reset_delta.seconds % 60)

    return result

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
