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

    // UTILISATEURS
    $user = array(
      array(1,"FILLEUL","Lucas","lukas","lukas","lucas.filleul@gmail.com"),
      array(2,"BELHEN","Louis","louis","louis","louis@gmail.com"),
      array(3,"AUTRE","autre","autre","autre","autre@gmail.com")
    );
    $insert = "INSERT INTO USER (idUser,nomUser,prenomUser, login,mdp,adresseMail)
    VALUES (:idUser,:nomUser,:prenomUser,:login,:mdp,:adresseMail)";
    $stmt = $file_db->prepare($insert);
    $stmt->bindParam(':idUser', $idUser);
    $stmt->bindParam(':nomUser', $nomUser);
    $stmt->bindParam(':prenomUser', $prenomUser);
    $stmt->bindParam(':login', $login);
    $stmt->bindParam(':mdp', $mdp);
    $stmt->bindParam(':adresseMail', $adresseMail);


    foreach($user as $u){
      $idUser = $u[0];
      $nomUser = $u[1];
      $prenomUser = $u[2];
      $login = $u[3];
      $mdp = $u[4];
      $adresseMail = $u[5];
      $stmt->execute();
    }
    echo "Users rentrées<br>";

    // DROITS
    $droits = array(
      array(1,"master","permet tout les roles plus ajout membre / supprimer projet / supprimer membre"),
      array(2,"developpeur","permet de travailler sur le mcd"),
      array(3,"visiteur","permet seulement de consulter")
    );
    $insert2 = "INSERT INTO DROIT (idDroit, nomDroit,DescDroit)
    VALUES (:idDroit,:nomDroit,:DescDroit)";
    $stmt = $file_db->prepare($insert2);
    $stmt->bindParam(':idDroit', $idDroit);
    $stmt->bindParam(':nomDroit', $nomDroit);
    $stmt->bindParam(':DescDroit', $DescDroit);


    foreach($droits as $d){
      $idDroit = $d[0];
      $nomDroit = $d[1];
      $DescDroit = $d[2];
      $stmt->execute();
    }
    echo "Droits rentrées<br>";



    // PROJET
    $projet = array(
      array(1,"TESTPROJET","McdTEST","test d'un projet")
    );
    $insert3 = "INSERT INTO PROJET (idProjet, nomProjet,nomMCD,DescProjet)
    VALUES (:idProjet,:nomProjet,:nomMCD,:DescProjet)";
    $stmt = $file_db->prepare($insert3);
    $stmt->bindParam(':idProjet', $idProjet);
    $stmt->bindParam(':nomProjet', $nomProjet);
    $stmt->bindParam(':nomMCD', $nomMCD);
    $stmt->bindParam(':DescProjet', $DescProjet);


    foreach($projet as $p){
      $idProjet = $p[0];
      $nomProjet = $p[1];
      $nomMCD = $p[2];
      $DescProjet = $p[3];
      $stmt->execute();
    }
    echo "Projets rentrées<br>";


    // GERER
    $gerer = array(
      array(1,1,1),
      array(1,2,2),
      array(1,3,3)
    );
    $insert4 = "INSERT INTO GERER (idProjet, idUser,idDroit)
    VALUES (:idProjet,:idUser,:idDroit)";
    $stmt = $file_db->prepare($insert4);
    $stmt->bindParam(':idProjet', $idProjet);
    $stmt->bindParam(':idUser', $idUser);
    $stmt->bindParam(':idDroit', $idDroit);


    foreach($gerer as $g){
      $idProjet = $g[0];
      $idUser = $g[1];
      $idDroit = $g[2];
      $stmt->execute();
    }
    echo "GERER rentrées<br>";




    }
    catch(PDOException $e){
      echo $e->getMessage();
    }
  ?>
</body>
</html>
