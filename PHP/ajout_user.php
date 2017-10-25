<!doctype html>
<html>
<head>
  <title>Exerciseur MCD</title>
  <link rel='stylesheet' href='../CSS/newcompte.css'/>
</head>
<body>
  <header>
    <h1>Créer un compte</h1>
  </header>
<?php
  function ajout(){
    $file_db = new PDO("sqlite:../BD/BD.sqlite");
    $file_db->setAttribute(PDO::ATTR_ERRMODE,PDO::ERRMODE_EXCEPTION);
    $requeteid = $file_db->query("SELECT max(idUser) FROM USER");
    $maxid = $requeteid->fetch();

    $insert = "INSERT INTO USER (idUser,nomUser,prenomUser, login,mdp,adresseMail)
    VALUES (:idUser,:nomUser,:prenomUser,:login,:mdp,:adresseMail)";

    $stmt = $file_db->prepare($insert);
    $stmt->bindValue(':idUser', $maxid[0] + 1);
    $stmt->bindParam(':nomUser', $_POST['nom']);
    $stmt->bindParam(':prenomUser', $_POST['prenom']);
    $stmt->bindParam(':login', $_POST['id']);
    $stmt->bindParam(':mdp', $_POST['pass']);
    $stmt->bindParam(':adresseMail', $_POST['mail']);
    $stmt->execute();
    $file_db = null;
  }
  if ($_SERVER["REQUEST_METHOD"]=="GET"){
    $html ="
      <fieldset>
          <form method='POST' action='ajout_user.php'>
            <ul>
              <li>
                <label for 'identifiant'>Identifiant : </label>
                <input type='text' name='id'>
              </li>

              <li>
                <label for 'nom'>Nom : </label>
                <input type='text' name='nom'>
              </li>

              <li>
                <label for 'prenom'>Prenom : </label>
                <input type='text' name='prenom'>
              </li>

              <li>
                <label for 'mail'>Email: </label>
                <input type='email' name='mail'>
              </li>

              <li>
                <label for 'pass'>Mot de passe : </label>
                <input type='password' name='pass'>
              </li>

              <li>
                <label for 'confirm'>Confirmation mot de passe : </label>
                <input type='password' name='confirm'>
              </li>
            </ul>
            <input type='submit' value='Valider'>
          </form>
        </fieldset>";
    echo $html;
  }
  else{
    ajout();
  }
?>
</body>
</html>
