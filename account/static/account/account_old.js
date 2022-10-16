
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

// open a modal to edit a highlight
$(document).on('click', '.edit-highlight-icon', function(event){

  var highlight_id = $(this).attr('data-id');
  var highlight_type = $(this).attr('data-type');
  var highlight_text = $(this).attr('data-text');

  setupHighlightModal(highlight_type,highlight_id,highlight_text);

});

// open a modal to add a highlight
$(document).on('click', '.highlight-btn', function(event){

  var type = $(this).attr('data-type');

  setupHighlightModal(type,'','')

});

function setupHighlightModal(type,highlight_id,highlight_text){

  if (highlight_id != '') {

    // set the action text for the modal title
    var action_text = 'Edit ';

    // fill in the modal fields
    $('#highlightText').val(highlight_text);
    $('#highlightID').val(highlight_id);

  }else {

    var action_text = 'Add ';

  };

  if (type=='team') {
    $('#highlightModal .modal-title').text(action_text + 'Team Highlight');
    $('#highlightType').val(0);
  }else if (type=='army') {
    $('#highlightModal .modal-title').text(action_text + 'Army Highlight');
    $('#highlightType').val(1);
  }else if (type=='civ') {
    $('#highlightModal .modal-title').text(action_text + 'Civilian Highlight');
    $('#highlightType').val(2);
  }else if (type=='license') {
    $('#highlightModal .modal-title').text(action_text + 'License or Rating');
    $('#highlightType').val(3);
  }else if (type=='award') {
    $('#highlightModal .modal-title').text(action_text + 'Award or Badge');
    $('#highlightType').val(4);
  }else {
    $('#highlightModal .modal-title').text(action_text + 'Team Highlight');
    $('#highlightType').val(0);
  }

  $('#highlightModal').modal();
  $('#highlightText').focus()


}

// adds a new highlight
$(document).on('click', '.add-highlight-btn', function(event){

  var csrf_token = $("input[name=csrfmiddlewaretoken]").val();
  var profile_id = $('#profileID').val();
  var highlight_text = $('#highlightText').val();
  var highlight_id = $('#highlightID').val();
  var highlight_type = $('#highlightType').val();
  var next_action = $(this).attr('data-next');

  if (highlight_type == 0) {
    var highlight_table = '#teamHighlightTable'
  }else if (highlight_type == 1) {
    var highlight_table = '#armyHighlightTable'
  }else if (highlight_type == 2) {
    var highlight_table = '#civHighlightTable'
  }else if (highlight_type == 3) {
    var highlight_table = '#licenseTable'
  }else if (highlight_type == 4) {
    var highlight_table = '#awardTable'
  }

  if (highlight_id == '') {
    var ajax_url = '/account/ajax/highlight/add/'
  }else{
    var ajax_url = '/account/ajax/highlight/edit/'
  }

  $.ajax({
      type:"post",
      url: ajax_url,
      data:{'profile_id': profile_id,
            'highlight_id': highlight_id,
            'highlight_text': highlight_text,
            'highlight_type': highlight_type
    },
      dataType: "json",
      headers: {'X-CSRFToken': csrf_token},
      cache: false,
      success: function(result){

        $('#highlightText').val('');

        // if save and close was clicked
        if (next_action == 'close') {

          $('#highlightModal').modal('hide');
          $('#highlightModal .modal-title').text('');

        // if save and new was clicked
        }else {

          $('#highlightText').focus();
          $('#highlightID').val('');

        }

        // parse the returned json string
        var highlight_array = JSON.parse(result.highlight_list);

        loadHighlightTable(highlight_table,highlight_array);


      },
      error: function(error){

      }

    });

});


function loadHighlightTable(highlight_table,highlight_array){

  // clear the table of any existing rows
  $(highlight_table).empty();

  // reload the table
  for (var h = 0; h < highlight_array.length; h++) {

    var table_highlight_text = highlight_array[h].highlight_text;

    if (h % 2 == 0) {
      var row_color = 'background-color:#f2f2f2;'
    }else{
      var row_color = 'background-color:#fff;'
    }

    var new_row = '<tr style="'+ row_color +'"><td>'+ table_highlight_text +'</td><td align="center" width="25px"> <i class="fas fa-edit font-weight-bold text-primary pointer edit-highlight-icon" style="font-size:1.5em;" data-id="{{ highlight.id }}" data-type="{{ highlight.type }}" data-text="{{ highlight.text }}"> </i></td><td align="center" width="25px"> <a href="" class="text-danger"> <i class="fas fa-times font-weight-bold" style="font-size:1.5em;"></i> </a></td></tr>'

    $(highlight_table).append(new_row);

    $(highlight_table + 'tr').addClass('bg-light');

  }

}

// open file select box for dropzone
$(document).on('click', '#dropzoneBtn', function(event){

  $('#dropzoneContainer').get(0).dropzone.hiddenFileInput.click();

});

$(document).on('click', '.profile-modal-icon', function(event){

  $('#profileImageModal').modal();

});

// remove a profile image
$(document).on('click', '.remove-profile-image', function(event){

  var image_id = $(this).attr('data-id');

  // remove the image right away then let ajax work in the background
  $('#image_' + image_id).remove();

  $.ajax({
      type:"post",
      url: '/account/profile/image/delete/',
      data:{'image_id': image_id
    },
      dataType: "json",
      cache: false,
      success: function(result){

      },
      error: function(error){

      }

    });

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
