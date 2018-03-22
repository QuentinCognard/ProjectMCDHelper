#! /bin/bash

# Pour lancer une install simple dans le répértoire courant
# qui contient le requirements.txt : 'source installvenv.sh'
# Plusieurs paramètres sont disponibles pour ce script version 1 :
# 'source installvenv.sh rm' -> par défaut si un venv existe il 
# n'est pas recréer. Avec l'option 'rm' si un venv existe il est supprimer.
# 'source installvenv.sh CheminVersDossierDuVenv/' -> install le venv
# dans le dossier voulu.
# 'source installvenv.sh rm CheminVersDossierDuVenv/' -> supprime puis
# install le venv dans le dossier choisi

if [ -z $1 ]
then
  if [ -d "venv" ]
  then
     echo "Il existe déjà un venv"
  else
     virtualenv -p python3 venv
     echo "virtualenv fait"; sleep 1
     source venv/bin/activate
     echo "Lancement de l'installation des packages"; sleep 2
     python3 -m pip install -r requirements.txt
     echo "Fin de l'installation du venv et des packages"
  fi
else
  if [ -z $2 ]
  then
    if [ $1 == "rm" ]
    then
      rm -r venv
      virtualenv -p python3 venv
      echo "virtualenv fait"; sleep 1
      source venv/bin/activate
      echo "Lancement de l'installation des packages"; sleep 2
      python3 -m pip install -r requirements.txt
      echo "Fin de l'installation du venv et des packages"
    elif [ $1 == "help" ]
    then
      echo "
# Pour lancer une install simple dans le répértoire courant
# qui contient le requirements.txt : 'source installvenv.sh'
# Plusieurs paramètres sont disponibles pour ce script version 1 :
# 'source installvenv.sh rm' -> par défaut si un venv existe il 
# n'est pas recréer. Avec l'option 'rm' si un venv existe il est supprimer.
# 'source installvenv.sh CheminVersDossierDuVenv/' -> install le venv
# dans le dossier voulu.
# 'source installvenv.sh rm CheminVersDossierDuVenv/' -> supprime puis
# install le venv dans le dossier choisi
";
    else
      virtualenv -p python3 $1venv
      echo "virtualenv fait"; sleep 1
      source $1venv/bin/activate
      echo "Lancement de l'installation des packages"; sleep 2
      python3 -m pip install -r requirements.txt
      echo "Fin de l'installation du venv et des packages"
    fi
  else
    if [ $1 == "rm" ]
    then
      rm -r $2venv
      virtualenv -p python3 $2venv
      echo "virtualenv fait"; sleep 1
      source $2venv/bin/activate
      echo "Lancement de l'installation des packages"; sleep 2
      python3 -m pip install -r requirements.txt
      echo "Fin de l'installation du venv et des packages"
    fi
  fi
fi
