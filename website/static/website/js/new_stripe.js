// Create a Stripe client.
var stripe_pk = document.getElementById('stripe_pk').value;
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

function getStripeToken(){

  let target = event.target;
  target.classList.add('disabled');

  let spinner = document.getElementById('cover-spin');
  spinner.classList.remove('invisible');

  // create the stripe token
  stripe.createToken(card).then(function(result) {

    // if there is an error
    if (result.error) {

      // hide the spinner
      spinner.classList.add('disabled');

      // display the error
      var errorElement = document.getElementById('card-errors');

      errorElement.textContent = result.error.message;

      // if there is an error, they will need the button back again
      target.classList.remove('disabled');

    } else {

      let tokenID = document.getElementById('stripeToken');

      // if the result object exists and is valid
      // and tokenID is blank (no duplicate charges)
      if (typeof result == 'object' && result.token.id != undefined && !tokenID.value) {

        tokenID.value = result.token.id;
        document.getElementById('stripeForm').submit();

      // if error, show an error
      }else{


      }

    }

  });

};
