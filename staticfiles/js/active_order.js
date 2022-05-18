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


document.getElementById("input_reset_3").addEventListener("click", active_order_func);

function active_order_func() {
    document.getElementById("active_order_start_date").value = "";
    document.getElementById("active_order_end_date").value = "";
    document.getElementById("user_type_3").value = "";
    window.location = '/unknown/activeorder/';
    location.reload();
}



// Edit Active Order Details
$(document).on('click', '.edit_active_order', function () {

    var edit_activeoreder_id = $(this).attr('id');
    var str_id = edit_activeoreder_id.split("_");
    var id = str_id[1];

    $.ajax({
        url: "/unknown/activeorder/",
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
                $("#no_like_log").val(data['no_like_log']);
                $("#editactiveorder").modal(); 
                sessionStorage.setItem("edit_active_order_id",id); 

              }
        }
    });
})

// Save 
$(document).on('click', '#save_activeorder', function () {

    var edit_id = sessionStorage.getItem("edit_active_order_id");
    var needactive = $('#needed').val()
    var Receivedactive = $('#received').val()
    var no_like_log = $('#no_like_log').val()

    $.ajax({
        url: "/unknown/activeorder/",
        type: "post",
        data: {
              id: edit_id,
              needed: needactive,
              received: Receivedactive,
              no_like_log: no_like_log,
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
              else if(data == 'Needed is Not Less then 0!'){
                alert("Needed is Not Less then 0!");
              }
              else if(data == 'Received is Required'){
                alert("Received is Required");
              }
              else if(data == 'Received is not Valid'){
                alert("Received is not Valid");
              }
              else if(data == 'Received is Integer'){
                alert("Received is Integer");
              }
              else if(data == 'No_like_log is Required'){
                alert("No_like_log is Required");
              }
              else if(data == 'No_like_log is not Valid'){
                alert("No_like_log is not Valid");
              }
              else if(data == 'No_like_log is Integer'){
                alert("No_like_log is Integer");
              }
              else{
                alert('Edit Successfully!');
                location.reload();
                sessionStorage.removeItem('edit_active_order_id');

              }
        }
    });
    
})

// Delet Model Open
$(document).on('click', '.dlt_active_order', function () {

  var dlt_activeorder_id = $(this).attr('id');
  var str_id = dlt_activeorder_id.split("_");
  var id = str_id[1];
  
  sessionStorage.setItem("dlt_active_order_id",id); 
  $("#deleteactiveorder").modal(); 
  
})


// Delete Purchase coin Data
$(document).on('click', '#dlt_activeorder', function () {

  var dlt_activeorder_id = sessionStorage.getItem("dlt_active_order_id");
  

  $.ajax({
      url: "/unknown/activeorder/",
      type: "post",
      data: {
            id: dlt_activeorder_id,
            delete_form: true,
      },
      success: function(data){
            if(data == 'ID is Required'){
              alert("ID is Required");
            }
            else if(data == 'ID is not Valid'){
              alert("ID is not Valid");
            }
            else{
              alert('Delete Successfully!');
              location.reload();
              sessionStorage.removeItem('dlt_active_order_id');

            }
      }
  });
  
})