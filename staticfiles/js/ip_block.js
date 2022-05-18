// this is for Ajax CSRF_TOKEN ((((((  DO NOT CHANGE IT  ))))))

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');
function csrfSafeMethod(method) {
  // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});
  
// END AJAX CSRF_TOKEN 


// Delet Model Open
$(document).on('click', '.dlt_ip_block', function () {

  var dlt_ip_block_id = $(this).attr('id');
  var str_id = dlt_ip_block_id.split("_");
  var id = str_id[1];
  
  sessionStorage.setItem("dlt_ip_block_id",id); 
  $("#deleteipblock").modal(); 
  
})


// Delete Purchase coin Data
$(document).on('click', '#dlt_ipblock', function () {

  var dlt_ip_block_id = sessionStorage.getItem("dlt_ip_block_id");
  console.log(dlt_ip_block_id)
  

  $.ajax({
      url: "/unknown/ip_block/",
      type: "post",
      data: {
            id: dlt_ip_block_id,
            delete_form: true,
      },
      
      success: function(data){
            if(data == 'ID is Required'){
              alert("ID is Required")
            }
            else if(data == 'ID is not Valid'){
              alert("ID is not Valid")
            }
            else{
              alert('Delete Successfully!');
              location.reload();
              sessionStorage.removeItem('dlt_ip_block_id');

            }
      }
  });
  
})