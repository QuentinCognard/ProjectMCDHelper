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
  <article>
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
    echo "<form method='POST' action='connexion.php'>";
    $html ="<p>Identifiant: ";
    $html.="<input type='text' name='login'><br></p>";
    $html.="<p>Mot de passe: ";
    $html.="<input type='text' name='mdp'><br></p>";
    $html.="<a href='' alt='Mot de passe oublié ?'>";
    $html.="<input type='submit' value='Connexion'><br></p>";
    echo $html;
    echo "</form>";
    echo "<input type='button' value='Créer un compte' OnClick='window.location.href=\'connexion.php'/>";
  }
  else{
    verification();
  }
  ?>
  </article>
</body>
</html>
