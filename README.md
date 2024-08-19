# ranking_algorithms
A website for ranking evolutionary algorithms uploaded by users


# run frontend
cd react-app
npm start

# run backend
cd backend
source .venv/bin/activate
python3 app.py

sudo ./run_app.sh    # teraz tak tylko trzeba stworzyć python venv

# strict cross origin policy
Сan turn it off in Firefox like this in search bar about:config -> security.fileuri.strict_origin_policy -> false

# migracja danych w bazie danych / aktualizacja
flask db init
flask db migrate -m "Synchronize database schema with models"
flask db upgrade

flask db init: raz na początku
flask db migrate: po każdej zmianie w modelach
flask db upgrade: po utworzeniu nowych migracji, aby zaktualizować bazę danych