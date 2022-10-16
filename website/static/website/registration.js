// Create a Stripe client.
$(document).on('click', '.attendee-type', function(event){


  // set the hidden field type
  let type = $(this).attr('data-type');
  $('#attendeeType').val(type);

  let name = $('#registerName').val();
  let email = $('#registerEmail').val();



  if (name && email) {

    // submit the form
    $('#startRegisterForm').submit()

  }



});

// add an attendee to either event
$(document).on('click', '.add-attendee', function(event){

  event.preventDefault()
  var event_id = $(this).attr('data-event');

  //first update any attendees that need it
  gatherAttendees(event_id)

});

// update veggieForm
$(document).on('click', '#updateAttendeesBtn', function(event){

    gatherAttendees(0)

});

// update the Attendee List
function gatherAttendees(event_id){

  var attendee_array = []

  $('.attendee').each(function(index, element) {

    let attendee_id = $(this).attr('data-id');
    let attendee_name = $(this).val()

      attendee_array.push({
        'attendee_id': attendee_id,
        'attendee_name': attendee_name
      })

  })

  var attendee_json_string = JSON.stringify(attendee_array);

  updateAttendees(attendee_json_string, event_id)

}

// update the attendee list
function updateAttendees(attendee_json_string, event_id){

  var csrf_token = $("input[name=csrfmiddlewaretoken]").val();

  $.ajax({
      type:"post",
      url:"/ajax/attendees/update/",
      data:{'attendees_string': attendee_json_string
    },
      dataType: "json",
      headers: {'X-CSRFToken': csrf_token},
      cache: false,
      success: function(result){

        if (event_id == 1 || event_id == 2) {

           var registration_id = $('#registration').val();
           window.location.href = '/reunion/register/' + registration_id + '/attendee/add/' + event_id +'/'

        }else if (event_id == 0) {

          $('#veggieForm').submit();

        }

      },
      error: function(error){


      }

    });

}
