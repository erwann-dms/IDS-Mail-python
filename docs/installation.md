# Installation

## Prérequis

- Python 3.8 ou supérieur installé.
- pip installé.

## Installation des dépendances

```bash
pip install -r requirements.txt
```

## Lancement de l'application

```bash
python src/qui.py
```
L'interface graphique s'ouvrira et vous pourrez utiliser l'outil

---

# 10. docs/usage.md

```markdown
# Utilisation

## Générer des emails

- Entrez un domaine valide (ex: example.com).
- Spécifiez le nombre d'emails à générer.
- Cliquez sur **Générer**.

## Gérer les emails

- Les emails générés s'affichent dans la liste.
- Utilisez la barre de recherche pour filtrer les emails.
- Sélectionnez un email et cliquez sur **Supprimer** pour le retirer.

## Stockage

Les emails sont stockés dans une base SQLite `emails.db` dans le dossier courant.

---
```
