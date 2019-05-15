$(document).ready(() => {
  $('.dash-center').each(function () {
    $(this).css('marginTop', `${-($(this).height() / 2) }px`);
  });
});

$('.adminBlock').on('click', '.add-new-user-app-button', (e) => {
  e.preventDefault();
  $('#add-new-user-app-modal').find('h2.setting-header.app-modal-header').text('Add New App');
  $('#add-new-user-app-modal').find('form').attr('data-id', '').trigger('reset');
  $('#add-new-user-app-modal').find('.save-new-user-app').val('Add App');
  $('#add-new-user-app-modal').foundation('reveal', 'open');
});

$('#add-new-user-app-modal').on('click', '.save-new-user-app', function (e) {
  e.preventDefault();
  form_data = { request_type: 'add-new-user-app' };
  if ($(this).parents('form').attr('data-id')) {
    form_data.id = $(this).parents('form').attr('data-id');
  }
  data = $('#add-new-user-app-modal form').serializeArray();
  $.each(data, function () {
    form_data[this.name] = this.value || '';
  });

  $.ajax({
    url: '/',
    type: 'POST',
    dataType: 'json',
    data: form_data,
  })
    .done((resp) => {
      if (resp.success) {
        $('#add-new-user-app-modal').foundation('reveal', 'close');
        window.location.reload();
      } else {
        html = `<strong>Save Failed: </strong> ${ resp.error}`;
        html += '<ul>';
        $(resp.errors).each((index, error) => {
          html += `<li>${  error  }</li>`;
        });
        html += '</ul>';
        $('#add-new-user-app-modal .msg-content').html(html);
      }
    });
});

$('.adminBlock').on('click', '.editaction', function (e) {
  e.preventDefault();
  $('#add-new-user-app-modal').find('h2.setting-header.app-modal-header').text(`Update App: ${$(this).siblings('.app-link').attr('data-app')}`);
  $('#add-new-user-app-modal').find('form').attr('data-id', $(this).attr('data-id')).trigger('reset');
  $('#add-new-user-app-modal').find('.save-new-user-app').val('Update App');

  $fields = $('#add-new-user-app-modal').find('form').find(':input');
  $($(this).get(0).attributes).each((index, attribute) => {
    if (attribute.name.indexOf('data-') == 0) {
      field = $('#add-new-user-app-modal').find('form').find(`[name="${attribute.name.split('-')[1]}"]`);
      if ($(field).length > 0) {
        field_type = $(field).prop('tagName').toLowerCase();
        if (field_type == 'select') {
          sf = $(field).find('option').filter(function () { return $(this).text() == $(attribute).val(); });
          $(sf).prop('selected', true);
        } else if (field_type == 'input' && $(field).attr('type') == 'checkbox') {
          check = ($(attribute).val() == 'True');
          $(field).prop('checked', check);
        } else {
          $(field).val($(attribute).val());
        }
      }
    }
  });
  $('#add-new-user-app-modal').foundation('reveal', 'open');
});

$('.adminBlock').on('click', '.app-modal', function (e) {
  e.preventDefault();
  $app = $(this).attr('data-app');
  $(`#${$app}-modal`).foundation('reveal', 'open');
});

$('.adminBlock').on('click', '.app_check', function (e) {
  if ($(this).attr('data-has_login') == 'true') {
    e.preventDefault();

    $('#navaway-modal #login-credential-details').hide();
    $('#navaway-modal #login-to-credentials').show();
    $('#navaway-modal #login-acct-key').val('');
    $('#navaway-modal #login-credential-viewuser').text('');
    $('#navaway-modal #login-credential-viewpw').text('');

    $title = $(this).parents('.dashboard-tile').find('h2').text();
    $('#navaway-modal').find('.navaway-site').text($title);
    $('#navaway-modal').attr('data-href', $(this).attr('href')).foundation('reveal', 'open');
  }
});

$('#navaway-modal').on('keyup', '#login-acct-key', (e) => {
  if (e.which == 13) {
    $('#navaway-modal .openlogin').trigger('click');
  }
});

$('#navaway-modal').on('click', '.openlogin', (e) => {
  e.preventDefault();
  $.ajax({
    url: '/login/login_search/',
    type: 'POST',
    global: false,
    dataType: 'json',
    data: { url: $('#navaway-modal').attr('data-href'), password: $('#login-acct-key').val() },
  })
    .done((resp) => {
      $('#navaway-modal .login-errors').text('');
      $('#navaway-modal #login-credential-viewuser').text(resp.username);
      $('#navaway-modal #login-credential-viewpw').text(resp.password);
      $('#navaway-modal #login-credential-copyuser').attr('data-copy', resp.username);
      $('#navaway-modal #login-credential-copypw').attr('data-copy', resp.password);
      $('#navaway-modal #login-credential-details').show();
      $('#navaway-modal #login-to-credentials').hide();
    }).fail((resp) => {
      $('#navaway-modal .login-errors').text(resp.responseJSON);
    });
});

$('#navaway-modal').on('click', '.opensite', (e) => {
  e.preventDefault();
  $('#navaway-link').attr('href', $('#navaway-modal').attr('data-href'));
  $('#navaway-link').get(0).click();
});

$('#navaway-modal').on('click', '.copy-text', function (e) {
  e.preventDefault();
  $('#login-credential-pw').show().val($(this).attr('data-copy')).select();
  document.execCommand('copy');
  $('#login-credential-pw').val('').hide();
});

$('#subscribe-modal').on('click', '.closeBtn', (e) => {
  e.preventDefault();
  $('a.close-reveal-modal').trigger('click');
});

$('.subscribe-modal').on('click', function (e) {
  e.preventDefault();

  if (undefined != $(this).attr('data-legal')) {
    $('#subscribe-modal #standard-subscription').hide();
    $('#subscribe-modal #legal-subscription').show();
    $('#subscribe-modal #legal-setup').attr('href', $(this).attr('data-legal'));
  } else {
    $('#subscribe-modal #standard-subscription').show();
    $('#subscribe-modal #legal-subscription').hide();
  }

  $('#subscribe-modal').foundation('reveal', 'open');
});
