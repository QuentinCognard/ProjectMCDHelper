<!doctype html>
<html>
<head>
  <title>Exerciseur MCD</title>
  <link rel='stylesheet' href='../CSS/connexion.css'/>
</head>
<body>
  <header>
    <h1>Exerciseur MCD</h1>
  </header>
  <article id='connexion'>
    <?php
    function verification(){
      $file_db = new PDO("sqlite:../BD/BD.sqlite");
      $file_db->setAttribute(PDO::ATTR_ERRMODE,PDO::ERRMODE_EXCEPTION);
      $requetelogin = $file_db->query("SELECT mdp FROM USER where login ='$_POST[login]'");
      $donnees = $requetelogin->fetch();
      if($donnees[0] == $_POST['mdp']){
        echo "BIENVENU !!!!!!!!!! :D";
      }
      else{
        echo "PAS DE USER BRO";
      }
      $file_db = null;
    }
  if ($_SERVER["REQUEST_METHOD"]=="GET"){
    echo "<fieldset><legend>Connexion</legend><form method='POST' action='connexion.php'>";
    $html ="<p>Identifiant: ";
    $html.="<input type='text' name='login' required><br></p>";
    $html.="<p>Mot de passe: ";
    $html.="<input type='password' name='mdp' required><br></p>";
    $html.="<a href=''>Mot de passe oublié ?</a></p>";
    $html.="<section id='boutons'><input id='co' type='submit' value='Connexion'></form><br>";
    $html.="<a href='ajout_user.php'><input id='compte' type='button' value='Créer un compte'></a></section>";
    echo $html;
    echo "</fieldset>";
  }
  else{
    verification();
  }
  ?>
  </article>
</body>
</html>
