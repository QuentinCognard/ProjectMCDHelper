<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8" />
  <link rel="stylesheet" href="../CSS/films.css" />
  <title> Films </title>
</head>
<body>
  <?php
  try{
    $file_db = new PDO('sqlite:../BD.db');
    $file_db->setAttribute(PDO::ATTR_ERRMODE,PDO::ERRMODE_EXCEPTION);
    $file_db->exec("CREATE TABLE IF NOT EXISTS USER(
      idUser INTEGER PRIMARY KEY,
      nomUser TEXT,
      prenomUser TEXT,
      login TEXT,
      mdp TEXT,
      adresseMail TEXT
    )");
    echo "BD USER initialisée<br>";

    $file_db->exec("CREATE TABLE IF NOT EXISTS DROIT(
      idDroit INTEGER PRIMARY KEY,
      nomDroit TEXT,
      DescDroit TEXT
    )");
    echo "BD Droits initialisée<br>";

    $file_db->exec("CREATE TABLE IF NOT EXISTS PROJET(
      idProjet INTEGER PRIMARY KEY,
      nomProjet TEXT,
      nomMCD TEXT,
      DescProjet TEXT
    )");
    echo "BD Projet initialisée<br>";

    $file_db->exec("CREATE TABLE IF NOT EXISTS GERER(
      idProjet INTEGER,
      idUser INTEGER,
      idDroit INTEGER,
      PRIMARY KEY (idProjet, idUser)
    )");
    echo "BD GERER initialisée<br>";

    $file_db->exec("CREATE TABLE IF NOT EXISTS ATTRIBUTS(
      idAttribut INTEGER PRIMARY KEY,
      idProjet INTEGER,
      idConteneur INTEGER,
      nomAttribut TEXT,
      genreAttribut TEXT,
      typeAttribut TEXT,
      valeurAttribut TEXT,
      Actif INTEGER
    )");
    echo "BD Attributs initialisée<br>";

    $file_db->exec("CREATE TABLE IF NOT EXISTS ENTITE(
      idEntite INTEGER PRIMARY KEY,
      idProjet INTEGER,
      nomEntite TEXT,
      positionEntite TEXT
    )");
    echo "BD Entite initialisée<br>";

    $file_db->exec("CREATE TABLE IF NOT EXISTS RELATION(
      idRelation INTEGER PRIMARY KEY,
      idProjet INTEGER,
      nomRelation TEXT,
      positionRelation TEXT
    )");
    echo "BD Entite initialisée<br>";

    $file_db->exec("CREATE TABLE IF NOT EXISTS RELATIONCONCERNE(
      idRelation INTEGER,
      idEntite INTEGER,
      cardinalite TEXT,
      PRIMARY KEY (idRelation, idEntite)
    )");
    echo "BD relations concerne tels entites initialisée<br>";

    }
    catch(PDOException $e){
      echo $e->getMessage();
    }
  ?>
</body>
</html>
