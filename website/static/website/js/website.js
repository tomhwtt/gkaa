// add Quantity
$(document).on('click', '#addQuantity', function(event){

  var quantity = $('#registrationQuantity').val();
	var new_quantity = parseInt(quantity) + 1;

  $('#registrationQuantity').val(new_quantity);
  $('#quantityText').text(new_quantity);

});

$(document).on('click', '#subtractQuantity', function(event){

  var quantity = $('#registrationQuantity').val();
	var new_quantity = parseInt(quantity) - 1;

  if (new_quantity > 0) {
    $('#registrationQuantity').val(new_quantity);
    $('#quantityText').text(new_quantity);
	}

});

$(document).on('click', '.donation_radio', function(event){

  // show the clear radio button
  $('#clearRadioContainer').removeClass('d-none');

  // set the dues paid tag
  if ($('#dues_paid').length) {
    var dues_paid = $('#dues_paid').val();

  // if donation
  }else{
    var dues_paid = 'true';
  }


  if (dues_paid) {
    var dues_amount = parseInt(0);
  }else{
    var dues_amount = parseInt(50);
  }

  var donation_amount = $(this).val();
  var payment_amount = parseInt(donation_amount) + parseInt(dues_amount);

  $('#payment_amount').val(payment_amount);

  $('#donationOther').val(donation_amount);

  updateDuesPaymentBtn()

});

// Clear Radio Buttons
$(document).on('click', '#clearRadioBtn', function(event){

  $('.donation_radio').prop('checked',false);
  $('#clearRadioContainer').addClass('d-none');
  $('#donationOther').val('');

  // set the dues paid tag
  if ($('#dues_paid').length) {
    var dues_paid = $('#dues_paid').val();

  // if donation
  }else{
    var dues_paid = 'true';
  }

  if (dues_paid) {
    var dues_amount = parseInt(0);
  }else{
    var dues_amount = parseInt(50);
  }

  $('#payment_amount').val(dues_amount);

  updateDuesPaymentBtn()

});

// clear radio buttons and reset amount if donation is typed in
$( "#donationOther" ).keyup(function() {

  $('.donation_radio').prop('checked',false);
  $('#clearRadioContainer').addClass('d-none');

  // set the dues paid tag
  if ($('#dues_paid').length) {
    var dues_paid = $('#dues_paid').val();

  // if donation
  }else{
    var dues_paid = 'true';
  }

  if (dues_paid) {
    var dues_amount = parseInt(0);
  }else{
    var dues_amount = parseInt(50);
  }

  var donation_amount = $(this).val();

  if (donation_amount) {
    var payment_amount = parseInt(donation_amount) + parseInt(dues_amount);
  } else{
    var payment_amount = parseInt(dues_amount);
  }

  $('#payment_amount').val(payment_amount);

  updateDuesPaymentBtn()


});

// Fundraiser
$(document).on('click', '#addFundraiserQty', function(event){

  var current_quantity = $('#fundraiserQty').val();

  if (current_quantity) {
    var new_quantity = parseInt(current_quantity) + 1;
    $('#fundraiserQty').val(new_quantity);
    $('#fundraiserQtyText').text(new_quantity);
  }


});

$(document).on('click', '#subtractFundraiserQty', function(event){

  var current_quantity = $('#fundraiserQty').val();

  if (current_quantity && current_quantity > 1) {
    var new_quantity = parseInt(current_quantity) - 1;
    $('#fundraiserQty').val(new_quantity);
    $('#fundraiserQtyText').text(new_quantity);
  }


});


// FUNCTION: update the dues payment button
function updateDuesPaymentBtn () {

  var payment_amount = $('#payment_amount').val();

  if (parseInt(payment_amount) > 0) {
    $('#paymentBtnAmount').text('($' + payment_amount + ')')
  }else{
    $('#paymentBtnAmount').text('')
  }

}


// Event Registration
$('#registerBtn').on('click', function(event){

  let quantity_array = [];
  let total_attendees = 0;
  let registerType = parseInt($('#registerType').val());
  let registerName = $('#registerName').val();
  let registerEmail = $('#registerEmail').val();

  $('.qty').each(function(index, element) {

    if ($(this).val()) {
      qty = $(this).val();
      total_attendees += parseInt(qty);
    }else{
      qty = 0;
    }

    quantity_array.push({
      'id': $(this).attr('data-id'),
      'qty': qty
    })

  });

  // form checks
  if (registerType == 0){
    $('#registerTypeError').html('Please choose registration type');
  }

  if (!registerName){
    $('#registerNameError').html('Please enter your name');
  }

  if (!registerEmail){
    $('#registerEmailError').html('Please enter your email address');
  }

  if (total_attendees == 0){
    $('#totalError').addClass('form-error');
  }

  if (total_attendees && registerType && registerName && registerEmail){
      newEventRegistration(JSON.stringify(quantity_array))
  }

  //

});


function newEventRegistration(s){

  var csrf_token = $("input[name=csrfmiddlewaretoken]").val();
  var register_type = $('#registerType').val();
  var register_email = $('#registerEmail').val();
  var register_name = $('#registerName').val();
  var register_event = $('#registerEvent').val();

  $.ajax({
   type:"post",
   url:"/event/registration/new/",
   data:{ 'type': register_type,
          'email': register_email,
          'name': register_name,
          'event': register_event,
          'subevent_string': s
   },
   dataType: "json",
   headers: {'X-CSRFToken': csrf_token},
   cache: false,
   success: function(result){

     window.location.href = '/event/registration/' + result.success + '/payment/'

   },
   error: function(error){

   }

  });

}
