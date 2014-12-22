function set_param(el){
     var elem = document.getElementById("param");
     if (el == 1)
     {
        elem.value = 'rdy';
        document.forms["main_form"].submit();
     }
     else
     {
        elem.value = 'load';
        document.forms["main_form"].submit();
     }


}