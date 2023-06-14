const formulario= document.getElementById('form1');
formulario.addEventListener('submit',function(e){
      
      e.preventDefault();
    var usuario=document.getElementById('usuario').value;
    var password=document.getElementById('pass').value;
    
      console.log(usuario);
      if(usuario ==""){
           const input=document.getElementById('usuario').style.border='2px solid red'; 
           alert("Faltan campos");
           return false;
      }else if(password==""){
	 
           alert("Faltan campos");
           return false;
   }
            
      alert("Formulario enviado");
            return true;
});
