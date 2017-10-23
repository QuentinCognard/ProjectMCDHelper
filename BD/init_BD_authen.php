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
    $file_db = new PDO('sqlite:base_de_donnes_PROJET.sqlite');
    $file_db->setAttribute(PDO::ATTR_ERRMODE,PDO::ERRMODE_EXCEPTION);
    $file_db->exec("CREATE TABLE IF NOT EXISTS films(
      code_film INTEGER,
      titre TEXT,
      pays TEXT,
      date INTEGER,
      duree INTEGER,
      couleur TEXT,
      image TEXT
    )");

        $insert = "INSERT INTO films (code_film,titre,pays,date, duree,couleur, image)
        VALUES (:code_film,:titre,:pays,:date, :duree,:couleur, :image)";
        $stmt = $file_db->prepare($insert);
        $stmt->bindParam(':code_film', $code_film);
        $stmt->bindParam(':titre', $titre);
        $stmt->bindParam(':pays', $pays);
        $stmt->bindParam(':date', $date);
        $stmt->bindParam(':duree', $duree);
        $stmt->bindParam(':couleur', $couleur);
        $stmt->bindParam(':image', $image);

        foreach($films as $f){
          $code_film = $f[0];
          $titre = $f[1];
          $pays = $f[2];
          $date = $f[3];
          $duree = $f[4];
          $couleur = $f[5];
          $image = $f[6];
          $stmt->execute();
        }
        $file_db = null;
        echo "BD initialisée";
        // foreach($films as $f){
        //   echo $f;
        // }
      }
      catch(PDOException $e){
        echo $e->getMessage();
      }
      ?>
    </body>
    </html>
