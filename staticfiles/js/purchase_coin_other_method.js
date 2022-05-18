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

// Edit Purchase Coin Details
$(document).on('click', '.edit_pc_other', function () {

    var edit_id = $(this).attr('id');
    var str_id = edit_id.split("_");
    var id = str_id[1];

    $.ajax({
        url: "/unknown/purchasecoin_other_method_list/",
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
                $("#purchased_coin").val(data['PurchaseCoin']);
                $("#country_code").val(data['CountryCode']);
                $("#exampleModal").modal(); 
                sessionStorage.setItem("edit_pc_other_id",id); 

              }
        }
    });
})

// Save 
$(document).on('click', '#save_pc', function () {

    var edit_id = sessionStorage.getItem("edit_pc_other_id");
    var pur_co = $('#purchased_coin').val()
    var cou_co = $('#country_code').val()

    $.ajax({
        url: "/unknown/purchasecoin_other_method_list/",
        type: "post",
        data: {
              id: edit_id,
              purchase_co: pur_co,
              country_co: cou_co,
              edit_form: true,
        },
        success: function(data){
              if(data == 'ID is Required'){
                alert("ID is Required")
              }
              else if(data == 'ID is not Valid'){
                alert("ID is not Valid")
              }
              else if(data == 'Purchase Coin is Required'){
                alert("Purchase Coin is Required")
              }
              else if(data == 'Purchase Coin is Empty!'){
                alert("Purchase Coin is Empty!")
              }
              else if(data == 'Purchase Coin is not Valid'){
                alert("Purchase Coin is not Valid")
              }
              else if(data == 'Country Code is Required'){
                alert("Country Code is Required")
              }
              else if(data == 'Country Code is not Valid'){
                alert("Country Code is not Valid")
              }
              else{
                alert('Edit Successfully!');
                location.reload();
                sessionStorage.removeItem('edit_pc_other_id');

              }
        }
    });
    
})

// Delet Model Open
$(document).on('click', '.dlt_pc_other', function () {

  var dlt_id = $(this).attr('id');
  var str_id = dlt_id.split("_");
  var id = str_id[1];
  
  sessionStorage.setItem("dlt_pc_other_id",id); 
  $("#deleteModal").modal(); 
  
})


// Delete Purchase coin Data
$(document).on('click', '#dlt_pc_other', function () {

  var dlt_id = sessionStorage.getItem("dlt_pc_other_id");
  

  $.ajax({
      url: "/unknown/purchasecoin_other_method_list/",
      type: "post",
      data: {
            id: dlt_id,
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
              sessionStorage.removeItem('dlt_pc_other_id');

            }
      }
  });
  
})