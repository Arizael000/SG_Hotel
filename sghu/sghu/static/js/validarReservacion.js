const formulario= document.getElementById('form1');
formulario.addEventListener('submit',function(e){
      
      e.preventDefault();
    var usuario=document.getElementById('usuario').value;
    var ci=document.getElementById('CI').value;
    var edad=document.getElementById('edad').value;
    var habitacion=document.getElementById('habitacion').value;
    var fechaini=document.getElementById('fechaIni').value;
    var fechafin=document.getElementById('fechaFin').value;
    var metPago=document.getElementById('metodoDePago').value;
    
    
      
      if(usuario ==""){
           const input=document.getElementById('usuario').style.border='2px solid red'; 
           alert("Faltan campos");
           return false;
      }else if(ci==""){
	const input=document.getElementById('CI').style.border='2px solid red'; 
           alert("Faltan campos");
           return false;
		} else if(edad==""){
	const input=document.getElementById('edad').style.border='2px solid red'; 
           alert("Faltan campos");
           return false;

		} else if(habitacion==""){
        const input=document.getElementById('habitacion').style.border='2px solid red'; 
           alert("Faltan campos");
           return false;

}      else if(fechaini==""){
          const input=document.getElementById('fechaIni').style.border='2px solid red'; 
           alert("Faltan campos");

           return false;

}       else  if(fechafin==""){

		const input=document.getElementById('fechaFin').style.border='2px solid red'; 
           alert("Faltan campos");
          	 return false;

}         else if(metPago=="None"){
const input=document.getElementById('metodoDePago').style.border='2px solid red'; 
           alert("Seleccione un método de pago");
          	 return false;

} else

	 
    
            
      alert("Formulario enviado");
            return true;
});
