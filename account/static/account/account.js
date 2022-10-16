
// init
$( document ).ready(function() {

  getUrlVars();

});

// get the profile type from the url and add an active class
function getUrlVars() {

  var href = window.location.href;
  var words = href.split('/')
  var type = words[5]

  $('#profileNav .' + type).addClass('active');

}

// open file select box for dropzone
$(document).on('click', '#dropzoneBtn', function(event){

  $('#dropzoneContainer').get(0).dropzone.hiddenFileInput.click();

});

$(document).on('click', '.profile-modal-icon', function(event){

  $('#profileImageModal').modal();

});


// open the team years modal
$(document).on('click', '#openTeamYearsModal', function(event){

  $('#teamYearsModal').modal('show');
  $('#sectionYear').focus();

});

$(document).on('click', '.add-team-date-btn', function(event){

  var next_action = $(this).attr('data-next');
  var profile_id = $('#profileID').val();
  var start_year = $('#startYear').val();
  var end_year = $('#endYear').val();
  var section_id = $('#dateSection').val();

  $.ajax({
      type:"post",
      url: '/account/ajax/profile/teamdate/new/',
      data:{'profile_id': profile_id,
            'start_year': start_year,
            'end_year': end_year,
            'section_id': section_id
    },
      dataType: "json",
      cache: false,
      success: function(result){

        if (next_action == 'new') {

          $('#endYear').val('');
          $('#dateSection').val('1');
          $('#startYear').val('').focus();

        }else {

          // hide the modal
          $('#teamYearsModal').modal('hide');

          // reload the page
          location.reload(true);
        }

      },
      error: function(error){

      }

    });

});

$(document).on('click', '.remove-date-icon', function(event){

  var date_id = $(this).attr('data-id');
  $('#date_' + date_id).remove();

  $.ajax({
      type:"post",
      url: '/account/ajax/profile/teamdate/delete/',
      data:{'date_id': date_id
    },
      dataType: "json",
      cache: false,
      success: function(result){

        console.log(result);

      },
      error: function(error){

      }

    });

});

// show warning for delete highlight
$(document).on('click', '.delete-highlight-icon', function(event){

  var highlight_id = $(this).attr('data-id');

  swal({
    title: "Are you sure?",
    text: "Do you want to delete this Highlight?",
    icon: "warning",
    buttons: true,
    dangerMode: true,
  })
  .then((willDelete) => {
    if (willDelete) {

      // delete and reload the page
      deleteHighlight(highlight_id)

    }
  });

});

// delete a highlight
function deleteHighlight(highlight_id){


  $.ajax({
      type:"post",
      url: '/account/ajax/highlight/delete/',
      data:{'highlight_id': highlight_id
    },
      dataType: "json",
      cache: false,
      success: function(result){

        // reload the page
        location.reload(true)

      },
      error: function(error){

      }

    });

}

// gets the highlights
function getHighlights(profile_id){

  $.ajax({
      type:"post",
      url: "/account/ajax/highlights/get/",
      data:{'profile_id': profile_id
    },
      dataType: "json",
      cache: false,
      success: function(result){

        // parse the returned json string
        var highlight_array = JSON.parse(result.highlight_list);

        // set the house legend
        if (highlight_array.length == 0) {
          $('#houseLegend').addClass('d-none');
        }else {
          $('#houseLegend').removeClass('d-none');
        }

        loadHighlightTable(highlight_array);

      },
      error: function(error){

      }

    });

}

// show warning for delete highlight
$(document).on('click', '.delete-oldhighlight-icon', function(event){

  var highlight_id = $(this).attr('data-id');

  swal({
    title: "Are you sure?",
    text: "Do you want to delete this Highlight?",
    icon: "warning",
    buttons: true,
    dangerMode: true,
  })
  .then((willDelete) => {
    if (willDelete) {

      // delete and reload the page
      deleteOldHighlight(highlight_id)

    }
  });

});


// delete a highlight
function deleteOldHighlight(highlight_id){

  $.ajax({
      type:"post",
      url: '/account/ajax/oldhighlight/delete/',
      data:{'highlight_id': highlight_id
    },
      dataType: "json",
      cache: false,
      success: function(result){

        location.reload(true)

      },
      error: function(error){

      }

    });

}


// show a warning for delete profile image
$(document).on('click', '.delete-profileimage-icon', function(event){

  var profileimage_id = $(this).attr('data-id');

  swal({
    title: "Are you sure?",
    text: "Do you want to delete this image?",
    icon: "warning",
    buttons: true,
    dangerMode: true,
  })
  .then((willDelete) => {
    if (willDelete) {

      // delete and reload the page
      deleteProfileImage(profileimage_id)

    }
  });

});


function deleteProfileImage(image_id){

  // remove the image right away then let ajax work in the background

  $.ajax({
      type:"post",
      url: '/account/profile/image/delete/',
      data:{'image_id': image_id
    },
      dataType: "json",
      cache: false,
      success: function(result){

        location.reload(true)

      },
      error: function(error){

      }

    });

}


$(document).on('click', '#openProfileMenuModal', function(event){

  $('#profileMenuModal').modal('show');

});


$(document).on('click', '#newProfileImageBtn', function(event){

  if ($('#upload-file-info').text()) {

    $(this).prop('disabled','disabled').text('Uploading File...')
    $('#profileImageForm').submit()

  }else{

    alert('Choose an Image');

  }

});
