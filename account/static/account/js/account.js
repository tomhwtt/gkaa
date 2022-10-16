function submitForm(f){
  event.target.disabled = true;

  let spin = document.getElementById('cover-spin');
  spin.classList.remove('invisible');

  let form = document.getElementById(f);
  form.submit();
}


function enableButton(b){
  let button = document.getElementById(b);
  button.classList.remove('disabled');
  button.innerText = 'Add New Image';
}
