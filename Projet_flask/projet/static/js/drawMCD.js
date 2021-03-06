 var canvas = document.getElementById("canvas");
 var ctx = canvas.getContext("2d");
 var cw = 1200;
 var ch = 5000;
 var posx;
 var posy;
 var e;
 var a;
 var r;
 var re;
 var ra;
 var liste_entite;
 var liste_atts;
 var liste_relation;
 var liste_relation_entite;
 var liste_relation_entite_attributs;

 function init(){
   // Fonction qui recup les donnees et les instancies
   cw = 1200;
   ch = 5000;
   posx = 10;
   posy = 10;
   e = document.getElementById("entites").innerHTML;
   a = document.getElementById("atts").innerHTML;
   r = document.getElementById("rels").innerHTML;
   re = document.getElementById("relsE").innerHTML;
   ra = document.getElementById("relsA").innerHTML;
   liste_entite = MrPropre(e);
   liste_atts =  MrPropre(a);
   liste_relation =  MrPropre(r);
   liste_relation_entite =  MrPropre(re);
   liste_relation_entite_attributs =  MrPropre(ra);
 }
 function MrPropre(liste_salle){
   // Fonction qui rend propre les donnees recup
   var sans_crochet_droit = liste_salle.replace(/]/g, "");
   var sans_crochet_gauche = sans_crochet_droit.replace(/\[/g, "");
   var sans_espaces = sans_crochet_gauche.replace(/ /g, "");
   var liste_propre = sans_espaces.split(",");
   var liste_finale = [];
   for(var i=0;i<liste_propre.length;++i){
     var to_add = liste_propre[i].split(";");
     liste_finale.push(to_add);
   }
   return liste_finale;
 }
 function drawE(e){
   if(e.length <5){
     if(e[3] == "None"){
       if(posx == 10){
         px = 10;
       }
       else{
         px = posx + 150;
       }
       py = posy;
     }
     else{
       px = e[3][0];
       py = e[3][1];
     }
     var liste_att_entite = [];
     for(var j=0; j <liste_atts.length;++j){
       if(liste_atts[j][2] == e[0]){
         liste_att_entite.push(liste_atts[j]);
       }
     }
     var positionEnt = [];
     positionEnt.push(px,py);
     ctx.beginPath();
     ctx.moveTo(px,py);
     ctx.lineTo(px + e[2].length * 10 ,py);
     ctx.lineTo(px + e[2].length * 10 ,py + 35 +  liste_att_entite.length * 10);
     ctx.lineTo(px,py + 35 +  liste_att_entite.length * 10);
     ctx.lineTo(px,py);
     ctx.moveTo(px,py+20);
     ctx.lineTo(px + e[2].length * 10 ,py + 20 );
     ctx.font = "10px Arial";
     ctx.fillText(e[2], px + 10, py+50/3);
     for(var i=0;i<liste_att_entite.length;++i){
       ctx.fillText(liste_att_entite[i][3], px + 10, py+35);
       py += 10;
     }
     posx = px + e[2].length * 10;
     posy = py +35
     positionEnt.push(posx,posy);
     e[3] = positionEnt;
     posy = 10;
     e.push(true);
     ctx.stroke();
   }
 }
 function getListeRelationEntite(relation){
   var l_r_e = [];
   for(var i=0;i<liste_relation_entite.length;++i){
     if(liste_relation_entite[i][1] == relation[0]){
       l_r_e.push(liste_relation_entite[i]);
     }
   }
   return l_r_e;
 }
 function drawRH(rel,l_r_e){
   var entites = [];
   var posX = posx;
   var posY = posy;
   for(var i=0;i<l_r_e.length;++i){
     for(var j=0;j<liste_entite.length;++j){
       if(l_r_e[i][2] == liste_entite[j][0]){
         entites.push(liste_entite[j])
         if(liste_entite[j].length == 5){
           posX = Math.max(liste_entite[j][3][0],liste_entite[j][3][2]);
           posY = Math.max(liste_entite[j][3][1],liste_entite[j][3][3])/ 2;
         }
       }
     }
   }
   ctx.beginPath();
   ctx.ellipse(posX + 100,posY,20,40,90*Math.PI/180,0,2*Math.PI)
   ctx.fillText(rel[2], posX + 100 - (rel[2].length * 3 / 2), posY - 5);
   for(var k=0; k<entites.length;++k){
     if(k == 0){
       ctx.moveTo(posX + 100,posY);
       ctx.lineTo(posX,posY);
       ctx.fillText(l_r_e[k][3], posX, posY);
       if(entites[k].length != 5){
         var newpos = [];
         newpos.push(posX + 200 ,10);
         entites[k][3] = newpos;
       }
     }
     else if(k == 1){
       ctx.moveTo(posX + 100,posY);
       ctx.lineTo(posX + 200,posY);
       ctx.fillText(l_r_e[k][3], posX + 180, posY);
       if(entites[k].length != 5){
         var newpos = [];
         newpos.push(posX + 200,10);
         entites[k][3] = newpos;
       }
     }
     else{
       ctx.moveTo(posX + 100,posY);
       ctx.lineTo(posX + 100,posY + 100);
       ctx.fillText(l_r_e[k][3], posX + 100, posY + 80);
       if(entites[k].length != 5){
         var newpos = [];
         newpos.push(posX + 100 - (entites[k][2].length * 3 / 2),posY + 100);
         entites[k][3] = newpos;
       }
     }
     ctx.stroke();
     drawE(entites[k]);
   }
   rel.push(true);
 }

 function drawRV(rel,l_r_e){
   var entites = [];
   var posX = posx;
   var posY = posy;
   for(var i=0;i<l_r_e.length;++i){
     for(var j=0;j<liste_entite.length;++j){
       if(l_r_e[i][2] == liste_entite[j][0]){
         entites.push(liste_entite[j])
         if(liste_entite[j].length == 5){
           posX = Math.abs(liste_entite[j][3][0] + liste_entite[j][3][2]) / 2;
           posY = Math.max(liste_entite[j][3][1],liste_entite[j][3][3]);
         }
       }
     }
   }
   ctx.beginPath();
   ctx.ellipse(posX,posY + 50 ,20,40,90*Math.PI/180,0,2*Math.PI)
   ctx.fillText(rel[2], posX - rel[2].length * 3 /2, posY +50);
   for(var k=0; k<entites.length;++k){
     if(k == 0){
       ctx.moveTo(posX,posY+50);
       ctx.lineTo(posX,posY);
       ctx.fillText(l_r_e[k][3], posX, posY + 20);
       if(entites[k].length != 5){
         var newpos = [];
         newpos.push(posX,posY+50);
         entites[k][3] = newpos;
       }
     }
     else{
       ctx.moveTo(posX,posY);
       ctx.lineTo(posX,posY+100);
       ctx.fillText(l_r_e[k][3], posX, posY+80);
       if(entites[k].length != 5){
         var newpos = [];
         newpos.push(posX - (entites[k][2].length * 3 / 2),posY + 100 );
         entites[k][3] = newpos;
       }
     }
     ctx.stroke();
     drawE(entites[k]);
   }
   rel.push(true);
 }

 function drawRsolo(liste_r){
   var entites;
   var posX = posx;
   var posY = posy;
     for(var j=0;j<liste_entite.length;++j){
       if(l_r_e[0][2] == liste_entite[j][0]){
         entites = liste_entite[j];
         if(liste_entite[j].length == 5){
           posX = Math.abs(liste_entite[j][3][0] + liste_entite[j][3][2]) / 2;
           posY = Math.max(liste_entite[j][3][1],liste_entite[j][3][3]);
         }
       }
     }
   ctx.beginPath();
   ctx.ellipse(posX,posY + 50 ,20,40,90*Math.PI/180,0,2*Math.PI)
   ctx.fillText(rel[2], posX - rel[2].length * 3 /2, posY +50);
   for(var k=0; k<entites.length;++k){
     if(k == 0){
       ctx.moveTo(posX,posY+50);
       ctx.lineTo(posX,posY);
       ctx.fillText(l_r_e[0][3], posX, posY + 20);
       if(entites[k].length != 5){
         var newpos = [];
         newpos.push(posX,posY+50);
         entites[3] = newpos;
       }
     }
     else{
       ctx.moveTo(posX,posY);
       ctx.lineTo(posX,posY+100);
       ctx.lineTo(posX + 50,posY+100);
       ctx.lineTo(posX + 50,posY - 20);
       ctx.lineTo(posX + 25,posY - 20);
       ctx.fillText(l_r_e[1][3], posX + 25,posY - 20);
       if(entites[k].length != 5){
         var newpos = [];
         newpos.push(posX - (entites[2].length * 3 / 2),posY + 100 );
         entites[3] = newpos;
       }
     }
     ctx.stroke();
   }
   rel.push(true);
 }

 function drawR(liste_r){
   var verifdraw = [];
   for(var k=0;k<liste_r.length;++k){
     if(liste_r[k].length != 4 ){
       verifdraw.push(liste_r[k]);
     }
   }
   for(var i=0;i<verifdraw.length;++i){
     if(verifdraw[i].length != 4){
       if(i==0){
         rel = verifdraw[i];
         l_r_e = getListeRelationEntite(rel);
         if(l_r_e.length == 2 && l_r_e[0][2] == l_r_e[1][2]){
           drawRsolo(l_r_e);
         }
         else{
           drawRH(rel,l_r_e);
         }
       }
       else{
         rel = verifdraw[i];
         l_r_e = getListeRelationEntite(rel);
         if(l_r_e.length == 2 && l_r_e[0][2] == l_r_e[1][2]){
           drawRsolo(l_r_e);
         }
         else{
           drawRV(rel,l_r_e);
         }
       }
     }
   }
 }
 function draw(){
   console.log("Coucou");
   //Fonction qui lance le dessin du MCD
   init();
   // INFOS AFFICHAGES
   // LISTE_ENTITE :
   // [ [idE,idP,nomEn,positionE{,draw}] ]
   // console.log(liste_entite);
   // LISTE_ATTRIBUTS :
   // [ [idA,idP,idE,nomA,genreA,typeA,actifA] ]
   // console.log(liste_atts);
   // LISTE_RELATION :
   // [ [idR,idP,nomRe,{draw}] ]
   // console.log(liste_relation);
   // LISTE_RELATION_ENTITE :
   // [ [idRE,idR,idE,cardE,cardR] ]
   // console.log(liste_relation_entite);
   // LISTE_RELATION_ENTITE_ATTRIBUTS :
   // [ [idRA,idR,idA] ]
   // console.log(liste_relation_entite_attributs);
   // RECUPERATION DES INFOS GRACE A L ID DU PROJET
   ctx.clearRect(0, 0, canvas.width, canvas.height);
   for(var i=0;i<liste_entite.length;++i){
       // Recupt entite et dessine entite
       var e = liste_entite[i];
       drawE(e);
       // recup relation associe a l entite
       var liste_R = [];
       for(var k=0;k<liste_relation_entite.length;++k){
         if(liste_relation_entite[k][2] == e[0]){
           for(var g=0;g<liste_relation.length;++g){
             if(liste_relation_entite[k][1] == liste_relation[g][0]){
               liste_R.push(liste_relation[g]);
             }
           }
         }
       }
       drawR(liste_R)
   }
 }

 download.addEventListener("click", function() {
   var canvas = document.getElementById("canvas");
   var imgData = canvas.toDataURL("image/png", 1.0);
   var pdf = new jsPDF();
   var name_mcd = document.getElementById("mcd_name").innerHTML;
   var name_mcd_bis = document.getElementById("tmp").innerHTML;

   console.log(name_mcd);
   console.log(name_mcd_bis);

   pdf.addImage(imgData, 'JPEG', 0, 0);
   pdf.save(name_mcd + ".pdf");
 }, false);
