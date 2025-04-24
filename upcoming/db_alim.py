import json
import mysql.connector
from datetime import datetime

# Connexion à la base de données MySQL
conn = mysql.connector.connect(
    host='localhost',
    port=3306,
    user='niab_admin',
    password='Admin123456+',
    database='top_movies'
)
cursor = conn.cursor()

# Charger les données du fichier JSON
with open('upcoming/upcomes.json', 'r', encoding='utf-8') as f:

    data = json.load(f)

# Préparer la requête d'insertion
sql = """
INSERT INTO niab_app_movie (
    fr_title, original_title, released_date, casting, director, writer, distribution, country,
    classification, duration, categories, weekly_entrances_pred, synopsis, programmed,
    programmed_room, programmation_start_date, programmation_end_date, allocine_url,
    image_url, trailer_url, creation_date
) VALUES (
    %s, %s, %s, %s, %s, %s, %s, %s,
    %s, %s, %s, %s, %s, %s,
    %s, %s, %s, %s,
    %s, %s, %s
)
"""

for movie in data:
    # Conversion de la date au format YYYY-MM-DD
    try:
        released_date = datetime.strptime(movie.get('released_date', ''), '%d/%m/%Y').date()
    except Exception:
        released_date = None

    # Champs à remplir ou à générer
    casting = ', '.join([a for a in [movie.get('actor_1'), movie.get('actor_2'), movie.get('actor_3')] if a and a != "no_actor"])
    director = movie.get('director') or movie.get('directors') or ''
    categories = ', '.join(movie.get('list_categories', [])) if 'list_categories' in movie else movie.get('category', '')
    synopsis = movie.get('synopsis', None).strip()
    weekly_entrances_pred = 1000  # Valeur arbitraire, à modifier selon besoin

    # Préparer les valeurs dans le même ordre que la requête
    values = (
        movie.get('fr_title', ''),
        movie.get('original_title', ''),
        released_date,
        casting,
        director,
        movie.get('writer', ''),
        movie.get('distribution', ''),
        movie.get('country', ''),
        movie.get('classification', ''),
        movie.get('duration', ''),
        categories,
        weekly_entrances_pred,
        synopsis,
        False,         # programmed
        None,          # programmed_room
        None,          # programmation_start_date
        None,          # programmation_end_date
        movie.get('allocine_url', ''),
        movie.get('image_url', ''),
        None,          # trailer_url
        datetime.now().date()  # creation_date
    )
    cursor.execute(sql, values)

conn.commit()
cursor.close()
conn.close()
