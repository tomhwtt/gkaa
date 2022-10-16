function createNewRegistration(){

  let subevents = document.querySelectorAll('.subevent');
  let subevent_string = []

  subevents.forEach((sub,index) => {

    subevent_string.push(
      {
        'id': sub.getAttribute('data-id'),
        'qty': sub.value
      }
    )

  })

  document.getElementById('subeventString').value = JSON.stringify(subevent_string);
  document.getElementById('newRegistrationForm').submit()

}
