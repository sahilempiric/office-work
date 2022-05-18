// this is for Ajax CSRF_TOKEN ((((((  DO NOT CHANGE IT/ REMOVE  ))))))

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


document.getElementById("input_reset_1").addEventListener("click", userlist_func);

function userlist_func() {
    document.getElementById("user_start_date").value = "";
    document.getElementById("user_end_date").value = "";
    document.getElementById("user_type_1").value = "";
    location.reload();
}


// Data Searching 
document.getElementById("submit_1").addEventListener("click", userlist_search_func);

function userlist_search_func() {
    var start_date = document.getElementById("user_start_date").value;
    var end_date = document.getElementById("user_end_date").value;
    var select_type = document.getElementById("option_1").value;
    if (select_type == '0'){
        var user_id = document.getElementById("user_type_1").value;
    }
    else if(select_type == '1'){
        var user_name = document.getElementById("user_type_1").value;
    }
}


// Edit User Details
$(document).on('click', '.edit_user', function () {

    var edit_user_id = $(this).attr('id');
    var str_id = edit_user_id.split("_");
    var id = str_id[1];

    $.ajax({
        url: "/unknown/userlist/",
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
                if(data['TotalCoin']){
                  $(".total_coin_hs").show()
                  $("#total_coin").val(data['TotalCoin']);
                  $("#total_coin").prop('required',true);
                }
                else{
                  $(".total_coin_hs").hide()
                }
                $("#user_status").val(data['Status']).change();
                $("#editUser").modal(); 
                sessionStorage.setItem("edit_user_id",id); 

              }
        }
    });
})

// Save 
$(document).on('click', '#save_user', function () {
    
    var edit_user_id = sessionStorage.getItem("edit_user_id");

    if($(".total_coin_hs").is(":visible")){
      var ttl_coins = $('#total_coin').val();
      var status = $('#user_status').val();

      $.ajax({
        url: "/unknown/userlist/",
        type: "post",
        data: {
              id: edit_user_id,
              total_coin: ttl_coins,
              user_status: status,
              edit_form: true,
        },
        success: function(data){
              if(data == 'ID is Required'){
                alert("ID is Required");
              }
              else if(data == 'ID is not Valid'){
                alert("ID is not Valid");
              }
              else if(data == 'Total Coin is Required'){
                alert("Total Coin is Required");
              }
              else if(data == 'Total Coin is not Valid'){
                alert("Total Coin is not Valid");
              }
              else if(data == 'Total Coin Enter in an integer!'){
                alert("Total Coin Enter in an integer!");
              }
              else if(data == 'Enter Valid Total Coin'){
                alert("Enter Valid Total Coin");
              }
              else if(data == 'Status is Required'){
                alert("Status is Required");
              }
              else if(data == 'Status is not Valid'){
                alert("Status is not Valid");
              }
              else{
                alert("Edit Successfully!");
                location.reload();
                sessionStorage.removeItem('edit_user_id');

              }
        }
      });
    }
    else{
    
      var status = $('#user_status').val();

      $.ajax({
          url: "/unknown/userlist/",
          type: "post",
          data: {
                id: edit_user_id,
                user_status: status,
                edit_form: true,
          },
          success: function(data){
                if(data == 'ID is Required'){
                  alert("ID is Required");
                }
                else if(data == 'ID is not Valid'){
                  alert("ID is not Valid");
                }
                else if(data == 'Total Coin is Required'){
                  alert("Total Coin is Required");
                }
                else if(data == 'Total Coin is not Valid'){
                  alert("Total Coin is not Valid");
                }
                else if(data == 'Total Coin Enter in an integer!'){
                  alert("Total Coin Enter in an integer!");
                }
                else if(data == 'Enter Valid Total Coin'){
                  alert("Enter Valid Total Coin");
                }
                else if(data == 'Status is Required'){
                  alert("Status is Required");
                }
                else if(data == 'Status is not Valid'){
                  alert("Status is not Valid");
                }
                else{
                  alert("Edit Successfully!");
                  location.reload();
                  sessionStorage.removeItem('edit_user_id');

                }
          }
      });
    }
})


// Delet Model Open
$(document).on('click', '.dlt_user', function () {

    var dlt_id = $(this).attr('id');
    var str_id = dlt_id.split("_");
    var id = str_id[1];
    
    sessionStorage.setItem("dlt_user_id",id); 
    $("#deleteuser").modal(); 
    
  })
  
  
  // Delete Purchase coin Data
  $(document).on('click', '#dlt_user', function () {
  
    var dlt_user = sessionStorage.getItem("dlt_user_id");
    
  
    $.ajax({
        url: "/unknown/userlist/",
        type: "post",
        data: {
              id: dlt_user,
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
                sessionStorage.removeItem('dlt_user_id');
  
              }
        }
    });
    
  })