// Create a Stripe client.
var stripe_pk = $('#stripe_pk').val()
var stripe = Stripe(stripe_pk);

// Create an instance of Elements.
var elements = stripe.elements();

// Custom styling can be passed to options when creating an Element.
// (Note that this demo uses a wider set of styles than the guide below.)
var style = {
  base: {
    color: '#32325d',
    fontFamily: '"Helvetica Neue", Helvetica, sans-serif',
    fontSmoothing: 'antialiased',
    fontSize: '16px',
    '::placeholder': {
      color: '#aaa'
    }
  },
  invalid: {
    color: '#fa755a',
    iconColor: '#fa755a'
  }
};

// Create an instance of the card Element.
var card = elements.create('card', {style: style});

// Add an instance of the card Element into the `card-element` <div>.
card.mount('#card-element');

// Handle real-time validation errors from the card Element.
card.addEventListener('change', function(event) {
  var displayError = document.getElementById('card-errors');
  if (event.error) {
    displayError.textContent = event.error.message;
  } else {
    displayError.textContent = '';
  }
});


$(document).on('click', '#paymentBtn', function(event){

  // check payment amount
  var payment_amount = parseInt($('#payment_amount').val());
  var payment_type = $('#payment_type').val();

  if (payment_type == 'donation' || 'dues') {
    var amount_error_text = 'Please choose or enter a donation amount'
  }

  if (payment_amount == 0) {
    $('#amount_error').text(amount_error_text).addClass('mb-2');

  }else {

    // if email exists, validate it
    if ($('#payment_email').length) {
      validatePaymentEmail($('#payment_email').val())
    }else{
      getStripeToken()
    }

  }

});

function validatePaymentEmail(e) {

  var csrf_token = $("input[name=csrfmiddlewaretoken]").val();

  $.ajax({
    type:"post",
    url:"/api/validate/email/",
    data:{'email': e
    },
    dataType: "json",
    headers: {'X-CSRFToken': csrf_token},
    cache: false,
    success: function(result){

      if (result.is_valid) {
        getStripeToken()
      }else{
        $('#payment_email_error').removeClass('d-none');
      }

    }

  });

}

function getStripeToken() {

  // disable the button and gray out the screen right away
  $('#paymentBtn').addClass('disabled');
  $('#cover-spin').removeClass('invisible');

  // create the stripe token
  stripe.createToken(card).then(function(result) {

    // if there is an error
    if (result.error) {

      // display the error
      var errorElement = document.getElementById('card-errors');

      errorElement.textContent = result.error.message;

      // if there is an error, they will need the button and screen restored
      $('#paymentBtn').removeClass('disabled');
      $('#cover-spin').addClass('invisible');

    } else {


      // if the result object exists and is valid
      if (typeof result == 'object' && result.token.id != undefined) {

        chargeStripe(result.token.id)

      }else{

        chargeStripe('')

      }

    }

  });

}

function chargeStripe(token_id){

  var csrf_token = $("input[name=csrfmiddlewaretoken]").val();
  var payment_type = $('#payment_type').val();
  var payment_type_id = $('#payment_type_id').val();
  var payment_amount= $('#payment_amount').val();
  var payment_email = $('#payment_email').val();

  if ($('#payment_name').length) {
    var payment_name = $('#payment_name').val();
  }else {
    var payment_name = '';
  }

  if ($('#payment_note').length) {
    var payment_note = $('#payment_note').val();
  }else {
    var payment_note = '';
  }

  if (!payment_amount) {
    var payment_amount = '0'
  }

  if (!payment_email) {
    var payment_email = ''
  }

  $.ajax({
    type:"post",
    url:"/api/stripe/charge/new/",
    data:{'token_id': token_id,
          'payment_type': payment_type,
          'payment_type_id': payment_type_id,
          'payment_amount': payment_amount,
          'payment_email': payment_email,
          'payment_name': payment_name,
          'payment_note': payment_note
    },
    dataType: "json",
    headers: {'X-CSRFToken': csrf_token},
    cache: false,
    success: function(result){

        if (result.return_url) {
            window.location.href = result.return_url
        }

    },
    error: function(error){


    }

  });

};

// disable PayPal Button while creating order
$(document).on('click', '.paypal-btn', function(event){

  $(this).addClass('disabled');
  $('#cover-spin').removeClass('invisible');

});
