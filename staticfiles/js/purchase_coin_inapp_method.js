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
$(document).on('click', '.dlt_pc_inapp', function () {

    var deletpcinapp_id = $(this).attr('id');
    var str_id = deletpcinapp_id.split("_");
    var id = str_id[1];
    
    sessionStorage.setItem("dlt_pc_inapp_id",id); 
    $("#deleteModalinapp").modal(); 
    
  })
  
  
  // Delete Purchase coin Data
  $(document).on('click', '#dlt_pc_inapp', function () {
  
    var deletpcinapp_id = sessionStorage.getItem("dlt_pc_inapp_id");

    $.ajax({
        url: "/unknown/purchasecoin_inapp_method_list/",
        type: "post",
        data: {
              id: deletpcinapp_id,
              delete_form_inapp: true,
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
                sessionStorage.removeItem('dlt_pc_inapp_id');
  
              }
        }
    });
    
  })