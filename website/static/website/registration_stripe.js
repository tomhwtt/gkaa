// Create a Stripe client.
var stripe_pk = $('#stripePK').val()
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
      color: '#ccc'
    }
  },
  invalid: {
    color: '#fa755a',
    iconColor: '#fa755a'
  }
};

// Create an instance of the card Element.
var cardNumber = elements.create('cardNumber', {style: style});
var cardExpiry = elements.create('cardExpiry', {style: style});
var cardCvc = elements.create('cardCvc', {style: style});
var postalCode = elements.create('postalCode', {style: style});

// Add an instance of the card Element into the `card-element` <div>.
cardNumber.mount('#card-element');
cardExpiry.mount('#card-expiry');
cardCvc.mount('#card-cvc');
postalCode.mount('#postal-code');

// Handle real-time validation errors from the card Element.
cardNumber.addEventListener('change', function(event) {
  var displayError = document.getElementById('card-number-errors');
  if (event.error) {
    displayError.textContent = event.error.message;
  } else {
    displayError.textContent = '';
  }
});

// Handle real-time validation errors from the card Element.
cardExpiry.addEventListener('change', function(event) {
  var displayError = document.getElementById('card-expiry-errors');
  if (event.error) {
    displayError.textContent = event.error.message;
  } else {
    displayError.textContent = '';
  }
});

// Handle real-time validation errors from the card Element.
cardCvc.addEventListener('change', function(event) {
  var displayError = document.getElementById('card-cvc-errors');
  if (event.error) {
    displayError.textContent = event.error.message;
  } else {
    displayError.textContent = '';
  }
});

// Handle real-time validation errors from the card Element.
postalCode.addEventListener('change', function(event) {
  var displayError = document.getElementById('postal-code-errors');
  if (event.error) {
    displayError.textContent = event.error.message;
  } else {
    displayError.textContent = '';
  }
});

// Handle form submission.
var form = document.getElementById('payment-form');

form.addEventListener('submit', function(event) {
  event.preventDefault();

  stripe.createToken(cardNumber).then(function(result) {
    if (result.error) {
      // Inform the user if there was an error.
      var errorElement = document.getElementById('card-errors');
      errorElement.textContent = result.error.message;
    } else {

      // disable the payment button
      $('#paymentBtn').prop("disabled",true).text('Processing Payment');

      // send the token to the server
      stripeTokenHandler(result.token);


    }
  });
});


// Submit the form with the token ID.
function stripeTokenHandler(token) {
  // Insert the token ID into the form so it gets submitted to the server
  var form = document.getElementById('payment-form');
  var hiddenInput = document.createElement('input');
  hiddenInput.setAttribute('type', 'hidden');
  hiddenInput.setAttribute('name', 'stripeToken');
  hiddenInput.setAttribute('value', token.id);
  form.appendChild(hiddenInput);

  // Submit the form
  form.submit();


}
