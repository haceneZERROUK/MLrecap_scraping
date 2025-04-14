

#  Automatiser des projets Scrapy avec Apache Airflow

---

## **Objectif général**
Automatiser **3 projets Scrapy** grâce à **Apache Airflow** installé localement avec Docker, pour exécuter des extractions de données web de façon régulière, maintenable et évolutive.

---

## Module 0 – Introduction à Apache Airflow

### Qu'est-ce qu'Airflow ?
Apache Airflow est un **orchestrateur de workflows** open-source. Il permet d’automatiser des processus métiers sous forme de pipelines de tâches appelés **DAGs** (*Directed Acyclic Graphs*).

Chaque DAG :
- est écrit en Python.
- contient des **tâches** unitaires (appelées operators).
- permet de définir des dépendances logiques entre ces tâches.

### Pourquoi Airflow pour du Scraping ?
- Lancer des spiders automatiquement (par heure, jour, semaine…).
- Gérer les logs, les erreurs, les relances.
- Intégrer d’autres étapes (nettoyage, base de données…).
- Orchestration simple **même entre plusieurs projets Scrapy**.

---

## Module 1 – Préparer tes projets Scrapy

### Structure recommandée :
```
web-scraping/
│
├── scrapy_project_1/
│   └── quotes_scraper/
│       └── spiders/
│           └── quotes.py
├── scrapy_project_2/
│   └── news_scraper/
├── scrapy_project_3/
│   └── jobs_scraper/
└── airflow/
    └── dags/
        └── scraper_dag.py
```

### À vérifier dans chaque projet :
- Tu dois pouvoir **exécuter le spider via une fonction Python** (voir module suivant).
- Chaque projet doit avoir :
  - `scrapy.cfg`
  - Un dossier `spiders/`
  - Un fichier `settings.py`
  - Un fichier `run_spider.py`(Pour lancer le spider automatiquement)

---

## Module 2 – Exécuter Scrapy depuis Python

### Pourquoi ?
Airflow ne peut pas exécuter `scrapy crawl spider_name` en ligne de commande facilement si les projets sont multiples. On encapsule donc l’appel dans une fonction Python.

### Exemple : `quotes_scraper/run_spider.py`
```python
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from quotes_scraper.spiders.quotes import QuotesSpider

def run():
    process = CrawlerProcess(get_project_settings())
    process.crawl(QuotesSpider)
    process.start()
```

Tu fais de même pour les deux autres projets : `news_scraper` et `jobs_scraper`.

---

## ☁️ **Module 3 — Installer Apache Airflow en local avec Docker**

---

### 🎯 Objectif du module

Mettre en place **Apache Airflow sur ton ordinateur** grâce à Docker et Docker Compose, pour qu’il soit prêt à orchestrer tes spiders Scrapy, **comme s’il tournait dans le cloud**.

---

### 🧠 Pourquoi Docker ?

Apache Airflow est composé de plusieurs services qui doivent communiquer entre eux :

Une base de données pour stocker les tâches et l’historique
Un serveur web (interface Airflow)
Un planificateur (scheduler) qui déclenche les DAGs
Éventuellement un worker (si on scale)
Et… des logs, des plugins, etc.
👉 Problème :
Installer tout ça “à la main” peut vite devenir complexe.

✅ Solution :
Docker permet d’avoir un environnement complet et prêt à l’emploi, avec tous les services déjà configurés, que tu peux démarrer/arrêter en une ligne de commande.

---

### 🧪 Étape 0 – Vérifier les prérequis

Tu dois avoir ces outils installés :

| Outil | Vérification |
|-------|--------------|
| Docker Desktop | `docker --version` |
| Docker Compose | `docker-compose --version` |
| Git *(optionnel)* | `git --version` |

> Si tu ne les as pas, installe **[Docker Desktop pour Mac](https://www.docker.com/products/docker-desktop/)** puis redémarre ton ordi.

---

### 🧱 Étape 1 – Créer le dossier de ton projet Airflow

Ouvre ton terminal :

```bash
mkdir airflow-local
cd airflow-local
mkdir dags logs plugins
```

- `dags/` → tes DAGs Airflow
- `logs/` → les fichiers de logs de chaque tâche
- `plugins/` → pour ajouter des extensions plus tard

---

### 🧾 Étape 2 – Créer le fichier `docker-compose.yml`

Toujours dans le dossier `airflow-local`, crée un fichier :
```bash
touch docker-compose.yml
```

Ce fichier décrit les services Docker à démarrer pour exécuter Airflow.

Voici les services que tu as définis :

| Service        | Rôle                                                    |
|----------------|---------------------------------------------------------|
| `postgres`     | La base de données d’Airflow                            |
| `webserver`    | L’interface web (http://localhost:8080)                |
| `scheduler`    | Le moteur qui exécute les DAGs automatiquement         |
| `airflow-init` | Initialise Airflow (migrations + création de l'utilisateur) |


Colle dedans ce contenu :

```yaml
version: '3'
services:
  postgres:
    image: postgres:13
    environment:
      POSTGRES_USER: airflow
      POSTGRES_PASSWORD: airflow
      POSTGRES_DB: airflow
    volumes:
      - postgres-db-volume:/var/lib/postgresql/data

  webserver:
    image: apache/airflow:2.9.1-python3.10
    environment:
      AIRFLOW__CORE__EXECUTOR: LocalExecutor
      AIRFLOW__DATABASE__SQL_ALCHEMY_CONN: postgresql+psycopg2://airflow:airflow@postgres/airflow
      AIRFLOW__CORE__FERNET_KEY: 'fernet_key_dev_123'
      AIRFLOW__CORE__LOAD_EXAMPLES: 'false'
    volumes:
      - ./dags:/opt/airflow/dags
      - ./logs:/opt/airflow/logs
      - ./plugins:/opt/airflow/plugins
    ports:
      - "8080:8080"
    depends_on:
      - postgres
    command: webserver

  scheduler:
    image: apache/airflow:2.9.1-python3.10
    environment:
      AIRFLOW__CORE__EXECUTOR: LocalExecutor
      AIRFLOW__DATABASE__SQL_ALCHEMY_CONN: postgresql+psycopg2://airflow:airflow@postgres/airflow
    volumes:
      - ./dags:/opt/airflow/dags
      - ./logs:/opt/airflow/logs
      - ./plugins:/opt/airflow/plugins
    depends_on:
      - webserver
    command: scheduler

  airflow-init:
    image: apache/airflow:2.9.1-python3.10
    depends_on:
      - postgres
    environment:
      AIRFLOW__CORE__EXECUTOR: LocalExecutor
      AIRFLOW__DATABASE__SQL_ALCHEMY_CONN: postgresql+psycopg2://airflow:airflow@postgres/airflow
      AIRFLOW__CORE__FERNET_KEY: 'fernet_key_dev_123'
      AIRFLOW__CORE__LOAD_EXAMPLES: 'false'
    volumes:
      - ./dags:/opt/airflow/dags
      - ./logs:/opt/airflow/logs
      - ./plugins:/opt/airflow/plugins
    entrypoint: >
      bash -c "
      airflow db migrate &&
      airflow users create --username airflow --password airflow --firstname Khadija --lastname Aassi --role Admin --email khadija@example.com
      "

volumes:
  postgres-db-volume:
```

---

### ⚙️ Étape 3 – Initialiser Airflow

Lance cette commande une fois pour initialiser la base de données interne d’Airflow :

```bash
docker-compose run --rm airflow-init
```
✅ Elle fait deux choses :

airflow db migrate → crée les tables dans la base PostgreSQL (base de données interne d’Airflow)
airflow users create → crée ton compte admin pour te connecter à l’interface

---

### 🚀 Étape 4 – Lancer Airflow

```bash
docker-compose up
```
Cette commande :

démarre le serveur web (webserver)
démarre le planificateur (scheduler)
connecte tout à la base de données PostgreSQL
📍 Tu accèdes à l’interface sur : http://localhost:8080

Tu peux voir :

Tous les DAGs actifs
Leur historique
Les logs
Les exécutions manuelles ou planifiées

### 🧠 Comment Airflow fonctionne-t-il ?

⛓️ Le rôle des composants :

| Composant       | Fonction                                                                 |
|-----------------|--------------------------------------------------------------------------|
| **DAG**         | Script Python qui définit les tâches à exécuter et leur ordre             |
| **Operator**    | Une tâche à exécuter (ex: fonction Python, commande bash, etc.)           |
| **Scheduler**   | Lit les DAGs, planifie et déclenche les exécutions                       |
| **Webserver**   | Affiche les DAGs, permet de les activer, de consulter les logs           |
| **Base de données** | Enregistre les DAGs, les exécutions, les logs, les utilisateurs     |


---

### 🔐 Connexion à l'interface

Identifiants par défaut :
- **Login** : `airflow`
- **Mot de passe** : `airflow`

---

### 🧪 Étape 5 – Tester avec un DAG de base

Crée un fichier `dags/hello_airflow.py` :

```python
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

with DAG("hello_airflow",
         start_date=datetime(2023, 1, 1),
         schedule_interval=None,
         catchup=False) as dag:

    def hello():
        print("Coucou Khadija, Airflow tourne bien !")

    task = PythonOperator(
        task_id="say_hello",
        python_callable=hello
    )
```

Dans l’interface Airflow :
1. Active le DAG "hello_airflow"
2. Clique sur ▶️ pour lancer une exécution
3. Consulte les logs pour vérifier l'exécution

---

### 📌 Résumé de cette mise en place

| Étape | Résultat |
|-------|----------|
| Docker installé | ✅ environnement conteneurisé |
| `docker-compose.yml` | ✅ Airflow prêt à l'emploi |
| `airflow-init` | ✅ Base de données initialisée |
| `localhost:8080` | ✅ Interface Airflow accessible |
| `dags/` | ✅ Prêt à accueillir tes DAGs Scrapy |


### 📌 Résumé visuel du système

                        +--------------------+
                       |    Interface Web   |  ← http://localhost:8080
                       +--------------------+
                                 ↑
                                 |
                                 ↓
    +----------+   →     +-----------+   ←   +-------------+
    |  DAG.py  |         | Scheduler |       | Base de     |
    | (Python) |   →     |           |   →   | Données     |
    +----------+         +-----------+       +-------------+
                                 ↑
                                 ↓
                         +------------------+
                         | PythonOperator   |
                         | BashOperator     |
                         | (et autres)      |
                         +------------------+

📘 Ce schéma illustre comment Airflow fonctionne en interne : chaque composant joue un rôle clé dans l'exécution des DAGs.

---

✅ À ce stade, tu as Airflow local prêt à recevoir tes DAGs.  
➡️ Passons maintenant à l’automatisation de tes spiders Scrapy avec Airflow.

---

## 🪁 Module 4 – Écrire un DAG pour 3 projets Scrapy

```python
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import sys

BASE_PATH = "/opt/airflow"

default_args = {
    "owner": "khadija",
    "retries": 2,
    "retry_delay": timedelta(minutes=5),
}

def add_path(path):
    if path not in sys.path:
        sys.path.append(path)

def run_project(path, spider):
    add_path(path)
    mod = __import__(f"{spider}.run_spider", fromlist=["run"])
    mod.run()

with DAG(
    dag_id="multi_scrapy_dag",
    default_args=default_args,
    start_date=datetime(2024, 4, 1),
    schedule_interval="@daily",
    catchup=False,
) as dag:

    t1 = PythonOperator(
        task_id="scrape_quotes",
        python_callable=run_project,
        op_args=[f"{BASE_PATH}/scrapy_project_1", "quotes_scraper"]
    )

    t2 = PythonOperator(
        task_id="scrape_news",
        python_callable=run_project,
        op_args=[f"{BASE_PATH}/scrapy_project_2", "news_scraper"]
    )

    t3 = PythonOperator(
        task_id="scrape_jobs",
        python_callable=run_project,
        op_args=[f"{BASE_PATH}/scrapy_project_3", "jobs_scraper"]
    )

    t1 >> t2 >> t3
```

---

## Module 5 – Logs & Monitoring

- Tous les logs sont accessibles dans `/opt/airflow/logs/`.
- Tu peux :
  - Stocker ces logs dans **Azure Blob Storage**
  - Intégrer **Grafana ou Prometheus**
  - Ajouter des **notifications Slack ou email**

---

## Module 6 – Bonnes pratiques

- Utilise des **fichiers `.env`** pour les chemins et identifiants.
- Centralise les **exports Scrapy** (JSON, CSV) dans un dossier `/data/`.
- Vérifie tes spiders indépendamment d’Airflow avant l’intégration.
- Utilise un fichier `__init__.py` dans tous tes dossiers pour faciliter l’import Python.

---

## Module 7 – Aller plus loin

- **Capteurs (Sensors)** : lancer un scraping seulement si un fichier est disponible ou une API répond.
- **Paramètres dynamiques** : injecter une URL ou une date dans Scrapy à chaque exécution.
- **Bases de données** : écrire les données dans PostgreSQL, Azure SQL, MongoDB...
- **Tests automatisés** : avec `pytest`, pour chaque spider.
- **Triggers externes** : lancer le DAG via une API ou webhook.

---

## Ressources utiles
- [📘 Scrapy Documentation](https://docs.scrapy.org/en/latest/)
- [📘 Apache Airflow Documentation](https://airflow.apache.org/docs/)
- [📘 Azure Airflow on VM Guide](https://learn.microsoft.com/fr-fr/azure/container-instances/container-instances-airflow)




LAncer le dag:

```bash
docker-compose down --volumes --remove-orphans
docker-compose up --build
```

tester le code dans un shell:

```bash
docker exec -it airflow-webserver-1 bash 
````
```bash
python3 run_spider.py
````
