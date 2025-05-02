# Extraction de données


Ce dépôt contient le module **MLrecap\_scraping**, responsable de l’extraction des données nécessaires à l’entraînement du modèle prédictif du projet MLRecap. Ainsi que de l'extraction automatisé des sorties de la semaine. 

---

## ➤ Description

Ce module utilise **Scrapy** (Allociné, Jpbox, etc.) pour constituer un jeu de données riche, en récupérant :

* Informations générales (titre, synopsis, genre, nationalité)
* Données sur les acteurs et réalisateurs
* Chiffres prévisionnels (si disponibles)

Ces données sont nettoyées, transformées et exportées au format exploitable par le module **MLrecap\_Model**.

---

## ➤ Comment exécuter le scrapping hebdo

### Avec Docker

```bash
cd airflow_scrapping
docker-compose up
```

### Sans Docker (local)

```bash
python -m venv venv
source venv/bin/activate  # sous Windows : venv\Scripts\activate
pip install -r requirements.txt
cd airflow_scrapping/upcoming
python local_runner.py
```


---

## ➤ Auteur(e)s

* **Hacene Zerrouk**: [GitHub](https://github.com/haceneZERROUK)
* **Malek Boumedine**: [GitHub](https://github.com/Malek-Boumedine)
* **Khadija Abdelmalek**: [GitHub](https://github.com/khadmalek)
* **Khadija Aassi**: [GitHub](https://github.com/Khadaassi)


Pour plus de détails sur le projet: [ML_recap](https://github.com/Khadaassi/Simplon_ML-Recap)

Pour toute question ou amélioration, merci d’ouvrir une issue sur ce dépôt.
