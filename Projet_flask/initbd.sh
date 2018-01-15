rm MCDBD.db
./manage.py syncdb
./manage.py loaddroit BD/droit.yml
./manage.py loadprojet BD/projet.yml
./manage.py loadgerer BD/gerer.yml
./manage.py newuser admin admin
./manage.py newuser lukas lukas