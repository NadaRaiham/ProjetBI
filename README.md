Ce projet a pour objectif de mettre en pratique des concepts de Business Intelligence (BI) en utilisant la base de données Northwind sur SQL Server. Il permet d’explorer, d’analyser et de visualiser les données relatives aux ventes, clients, produits et fournisseurs, afin de faciliter la prise de décision.

Le projet inclut notamment :

L’extraction et la transformation des données via des requêtes SQL.

La création de rapports et de tableaux de bord pour analyser les performances commerciales.

Exécution

Après l’installation de SQL Server et de la base Northwind, exécuter les scripts dans l’ordre suivant :

python .\scripts\extract_sqlserver.py

python .\scripts\extract.py
python .\scripts\transform.py

python .\scripts\load.py

streamlit run .\scripts\dashboard.py
(ou & "C:\Program Files\Python39\python.exe" -m streamlit run .\scripts\dashboard.py sur Windows)

Dans SQL Management Studio, exécuter le script schema.sql

python .\scripts\to_sql.py

Justification des choix techniques

os : manipulation des fichiers système.

pandas : traitement et manipulation de fichiers CSV, XLS et Parquet.

pyodbc : connexion à SQL Server via ODBC.

numpy : gestion des types numériques et des valeurs manquantes.

Streamlit : création et déploiement rapide d’un dashboard BI interactif directement en Python, sans technologies web complexes.

Plotly Express :
Création de graphiques interactifs en une seule ligne

Syntaxe claire et lisible

Visualisations riches : graphiques linéaires, barres, cercles relatifs, scatter 3D

Intégration parfaite avec Streamlit, sans configuration complexe

Résumé : Streamlit et Plotly Express ont été choisis pour leur simplicité, leur rapidité de développement et leur compatibilité avec Pandas, permettant de créer des dashboards interactifs et dynamiques adaptés à l’analyse décisionnelle.

Conclusion

Ce projet BI avec SQL Server et la base Northwind illustre comment exploiter efficacement les données pour soutenir la prise de décision.
Grâce à l’analyse des ventes, des clients et des produits, il est possible d’identifier des tendances, d’optimiser les performances et de mieux comprendre le fonctionnement d’une entreprise.

Ce travail constitue une base solide pour approfondir ses compétences en Business Intelligence et en manipulation de bases de données relationnelles.
