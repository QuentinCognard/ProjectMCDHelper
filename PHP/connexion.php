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
    $file_db = new PDO("sqlite:../BD/BD.sqlite");
    $file_db->setAttribute(PDO::ATTR_ERRMODE,PDO::ERRMODE_EXCEPTION);
    echo "<form method='POST' action='connexion.php'>";
    $html ="<p>Identifiant: ";
    $html.="<input type='text' name='identifiant'><br></p>";
    $html.="<p>Mot de passe: ";
    $html.="<input type='text' name='mdp'><br></p>";
    $html.="<a href='' alt='Mot de passe oublié ?'>";
    $html.="<input type='submit' value='Connexion'><br></p>";
    echo "</form>";
    echo $html;
    echo "<input type='button' value='Créer un compte' OnClick='window.location.href=\'connexion.php'/>";


  if ($_SERVER["REQUEST_METHOD"]=="POST"){
  }
  ?>
  </article>
</body>
</html>
