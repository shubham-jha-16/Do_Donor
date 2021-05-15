function quant(a){
	
  var mode=document.getElementById("mode");
  var time=document.getElementById("time");
  if(a>20)
  {
    mode.style.display="block";
	document.getElementById("messages").innerHTML = " ";
	return false ;
  }
  else
  
   mode.style.display="none";
   time.style.display="none";
   document.getElementById("messages").innerHTML="**you are only eligible for doorstep"
   return false ;
}
function goto(path)
{
  window.location=path;
}
function radio()
{
  var a=document.getElementById("time");
  a.style.display="block";
}
function radio1()
{
  var a=document.getElementById("time");
   a.style.display="none";
   document.getElementById("time1").value="";
}
