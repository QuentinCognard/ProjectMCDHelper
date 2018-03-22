rm -rf venv/
source installvenv.sh
rm MCDBD.db
./manage.py syncdb
./manage.py newuser admin admin
./manage.py newuser lukas lukas
./manage.py loaddroit BD/droit.yml
./manage.py loadprojet BD/projet.yml
./manage.py loadgerer BD/gerer.yml
./manage.py loadentite BD/entite.yml
./manage.py loadrelation BD/relation.yml
./manage.py loadattributs BD/att.yml
./manage.py loadrelationentite BD/relentite.yml
./manage.py runserver
