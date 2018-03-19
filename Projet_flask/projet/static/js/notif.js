  function notif(){
    document.getElementById('notif').innerHTML="<sup id='nb'>"+{{nbnotif}}+"</sup><span class='glyphicon glyphicon-bell'></span>Notifications"
    if ({{nbnotif}}>0){
      document.getElementById('nb').style.backgroundColor = "red";
      document.getElementById('nb').style.color = "white";
      document.getElementById('nb').style.borderRadius = "50%";
      document.getElementById('nb').style.padding = "0.2em";

    }
  }
  function sendDemande(){
    document.location.href="/projets/{{current_user.login}}/{{projet.nomProj}}/description/{{master}}/notif"
  }