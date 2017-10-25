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
</body>

<?php
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
          <input type='adress' name='mail'>
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
    </form>
    <input type='button' value='Valider'>
  </fieldset>";

echo $html;

}else{
  echo "coucou";
}

?>


</html>
