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


// Edit complete Order Details
$(document).on('click', '.edit_coin_detail', function () {

    var edit_coindetail_id = $(this).attr('id');
    var str_id = edit_coindetail_id.split("_");
    var id = str_id[1];

    $.ajax({
        url: "/unknown/coin_details/",
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
                  console.log(data['Quantity_Coin'])
                $("#quantity_coin").val(data['Quantity_Coin']);
                $("#indian_rate_coin").val(data['IndianRate_Coin']);
                $("#other_rate_coin").val(data['OtherRate_Coin']);
                $("#notes_coin").val(data['Notes_Coin']);
                if(data['IsPopular_Coin'] == '1'){
                    $("#customSwitch_coin").prop('checked', true);
                }
                else{
                    $("#customSwitch_coin").prop('checked', false);
                }
                $("#coin_status_coin").val(data['Status_Coin']).change();
                $("#editcoindetail").modal();        
                sessionStorage.setItem("edit_coin_detail_id",id); 

              }
        }
    });
})

// Save 
$(document).on('click', '#save_coindetail', function () {

    var edit_id = sessionStorage.getItem("edit_coin_detail_id");
    var Quantity_coin = $('#quantity_coin').val()                                   
    var Indianrate_coin = $('#indian_rate_coin').val()                             
    var Otherrate_coin = $('#other_rate_coin').val()                             
    var Notes_coin = $('#notes_coin').val()                             
    var Ispopular_coin = $('#customSwitch_coin').prop('checked')                             
    console.log(Ispopular_coin)
    var coin_status = $('#coin_status_coin').val()                             

    $.ajax({
        url: "/unknown/coin_details/",
        type: "post",
        data: {
              id: edit_id,
              quantity: Quantity_coin,                                         
              indian_rate: Indianrate_coin,                                   
              other_rate: Otherrate_coin,                                   
              notes: Notes_coin,                                   
              is_popular: Ispopular_coin,                                   
              coin_status: coin_status,                                   
              edit_form: true,
        },
        success: function(data){
            if(data == 'ID is Required'){
              alert("ID is Required");
            }
            else if(data == 'ID is not Valid'){
              alert("ID is not Valid");
            }
            else if(data == 'Quantity is Required'){
              alert("Quantity is Required");
            }
            else if(data == 'Quantity is Empty'){
              alert("Quantity is Empty");
            }
            else if(data == 'Quantity is not Valid'){
              alert("Quantity is not Valid");
            }
            else if(data == 'Indian Rate is Required'){
              alert("Indian Rate is Required");
            }
            else if(data == 'Indian Rate is Empty'){
              alert("Indian Rate is Empty");
            }
            else if(data == 'Other Rate is Required'){
              alert("Other Rate is Required");
            }
            else if(data == 'Other Rate is Empty'){
              alert("Other Rate is Empty");
            }
            else if(data == 'Notes is Required'){
              alert("Notes is Required");
            }
            else if(data == 'Notes is Empty'){
              alert("Notes is Empty");
            }
            else if(data == 'Popular is Required'){
              alert("Popular is Required");
            }
            else if(data == 'Popular is not Valid'){
              alert("Popular is not Valid");
            }
            else if(data == 'Coin Status is Required'){
              alert("Coin Status is Required");
            }
            else if(data == 'Coin Status is not Valid'){
              alert("Coin Status is not Valid");
            }
            else{
              alert('Edit Successfully!');
              location.reload();
              sessionStorage.removeItem('edit_coin_detail_id');
            }
        }
    });
    
})

// Delet Model Open
$(document).on('click', '.dlt_coin_detail', function () {

  var dlt_coin_detail_id = $(this).attr('id');
  var str_id = dlt_coin_detail_id.split("_");
  var id = str_id[1];
  
  sessionStorage.setItem("dlt_coin_detail_id",id); 
  $("#deletecoindetail").modal(); 
  
})


// Delete Purchase coin Data
$(document).on('click', '#dlt_coindetail', function () {

  var dlt_coin_id = sessionStorage.getItem("dlt_coin_detail_id");
  

  $.ajax({
      url: "/unknown/coin_details/",
      type: "post",
      data: {
            id: dlt_coin_id,
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
              sessionStorage.removeItem('dlt_coin_detail_id');

            }
      }
  });
  
})