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


document.getElementById("input_reset_2").addEventListener("click", all_order_func);

function all_order_func() {
    document.getElementById("all_order_start_date").value = "";
    document.getElementById("all_order_end_date").value = "";
    document.getElementById("user_type_2").value = "";
    location.reload();
}



// Edit All Order Details
$(document).on('click', '.edit_all_order', function () {

    var edit_alloreder_id = $(this).attr('id');
    var str_id = edit_alloreder_id.split("_");
    var id = str_id[1];
    
    $.ajax({
        url: "/unknown/allorder/",
        type: "post",
        data: {
              id: id,
              type:'edit',
        },
        success: function(data){
              if(data == 'No id!'){
                location.reload();
              }
              else{
                $("#needed").val(data['Needed']);
                $("#received").val(data['Recieved']);
                $("#editallorder").modal(); 
                sessionStorage.setItem("edit_all_order_id",id); 

              }
        }
    });
})

// Save 
$(document).on('click', '#saveallorder', function () {

    var edit_id = sessionStorage.getItem("edit_all_order_id");
    var need = $('#needed').val()
    var Received = $('#received').val()

    $.ajax({
        url: "/unknown/allorder/",
        type: "post",
        data: {
              id: edit_id,
              needed: need,
              received: Received,
              edit_form: true,
        },
        success: function(data){
              if(data == 'ID is Required'){
                alert("ID is Required");
              }
              else if(data == 'ID is not Valid'){
                alert("ID is not Valid");
              }
              else if(data == 'Needed is Required'){
                alert("Needed is Required");
              }
              else if(data == 'Needed is not Valid'){
                alert("Needed is not Valid");
              }
              else if(data == 'Enter needed in an integer'){
                alert("Enter needed in an integer");
              }
              else if(data == 'Enter Valid an integer'){
                alert("Enter Valid an integer");
              }
              else if(data == 'Received is Required'){
                alert("Received is Required");
              }
              else if(data == 'Received is not Valid'){
                alert("Received is not Valid");
              }
              else if(data == 'Received is in Integer'){
                alert("Received is in Integer");
              }
              else{
                alert('Edit Successfully!');
                location.reload();
                sessionStorage.removeItem('edit_all_order_id');

              }
        }
    });
    
})

// Delet Model Open
$(document).on('click', '.dlt_all_order', function () {

  var dlt_all_order_id = $(this).attr('id');
  var str_id = dlt_all_order_id.split("_");
  var id = str_id[1];
  
  sessionStorage.setItem('dlt_all_order_id',id); 
  $("#deleteallorder").modal(); 
  
})


// Delete Purchase coin Data
$(document).on('click', '#dlt_allorder', function () {

  var dlt_all_order_id = sessionStorage.getItem("dlt_all_order_id");
  

  $.ajax({
      url: "/unknown/allorder/",
      type: "post",
      data: {
            id: dlt_all_order_id,
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
              sessionStorage.removeItem('dlt_all_order_id');

            }
      }
  });
  
})



