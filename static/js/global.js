// Mobile Check
if (/Android|webOS|iPhone|iPad|iPod|BlackBerry/i.test(navigator.userAgent)) { window.isMobile = true; } else { window.isMobile = false; }

/*
	copyright year
*/
$('.curr-copyright-year').each(function () {
  $(this).append(new Date().getFullYear());
});

/*
	Mobile page title backup
*/
$(document).ready(() => {
  if ($('.simple-title').text().length == 0) {
    let title = $(document).find('title').text();
    $('.simple-title').text(title.split('|')[0].trim());
  }
});

$(document).on('click', 'li.has-children', function (e) {
  e.stopPropagation();

  let h = 0;
  const $parent = $(this);

  if ($parent.hasClass('top-level')) {
    $parent.siblings().each(function () {
      $(this).find('.opened').each(function () { $(this).removeClass('opened').css('max-height', '0px'); });
    });
  }

  $parent.find('ul').first().toggleClass('opened');
  $parent.find('ul').first().children().each(function () { h += $(this).outerHeight(); });

  if ($parent.find('ul').first().hasClass('opened')) {
    $parent.find('ul').first().css('max-height', `${h }px`);
  } else {
    $parent.find('ul').first().css('max-height', '0px');
  }

  if (!$parent.hasClass('top-level')) {
    const $top_level = $parent.find('ul').first().parents('.top-level');
    let th = 0;
    $top_level.children().each(function () { th += $(this).outerHeight(); });
    $parent.find('.opened').children().each(function () { th += $(this).outerHeight(); });
    $top_level.children('.opened').css('max-height', `${th}px`);
  }
});


/*
	Modal Alerts
*/
$(document).ready(() => {
  $('#modalAlert').hide();
  $('#modalAlert').css({ display: 'block', visible: 'visible' });
  $('#modalAlert').find('.alert-box').each(function () {
    $parent = $(this);
    $child = $(this).find('div.modalAlertContents');
    new_height = $child.height() + 60;
    $parent.css('min-height', `${new_height  }px`);
  });
  $('#modalAlert').css({ display: 'none', visible: 'hidden' });
  $('#modalAlert').foundation('reveal', 'open');
});

$(window).resize(() => {
  $('#modalAlert.open').find('.alert-box').each(function () {
    $parent = $(this);
    $child = $(this).find('div.modalAlertContents');
    new_height = $child.height() + 60;
    $parent.css('min-height', `${new_height  }px`);
  });
});


/*
	Flash Alerts
*/
$(window).ready(() => {
  $('#flash-alert').hide();
  $('#flash-alert').foundation('reveal', 'open');
  if ($('#flash-alert').length > 0) {
    window.setTimeout(() => {
			$('#flash-alert').foundation('reveal', 'close');
			// window.location.reload();
		}, 1000);
  }
});


/*
##################################
##		AJAX LOADING SCREEN		##
##################################
*/

const startAjaxLoader = function () {
  if ($('.bodyContent').hasClass('no-sidebar')) {
    left_offset = '0px';
  } else {
    left_offset = `${$('.sidebar').outerWidth() }px`;
  }
  height = `${$(window).height()}px`;


  if ($('.rrTopBar:visible').length > 0) {
    top_offset = `${$('.rrTopBar').height() + 61}px`;
  } else {
    top_offset = '61px';
  }
  if ($(window).width() < 1025) {
    $('#ajaxLoadingIcon').css({ top: '40px', left: '0px', height, position: 'fixed' });
  } else {
    $('#ajaxLoadingIcon').css({ top: top_offset, left: left_offset, height, position: 'fixed' });
  }
  $('#ajaxLoadingIcon').fadeIn(60);
};

const stopAjaxLoader = function () {
  $('#ajaxLoadingIcon').fadeOut(60);
};

$(document).ajaxStart(() => {
  startAjaxLoader();
});

$(document).ajaxStop(() => {
  stopAjaxLoader();
});


/*
######################################
##		Gets csrftoken for ajax		##
######################################
*/
function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie != '') {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      const cookie = jQuery.trim(cookies[i]);
      // Does this cookie string begin with the name we want?
      if (cookie.substring(0, name.length + 1) == (`${name}=`)) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}
const csrftoken = getCookie('csrftoken');

function capitalizeFirstLetter(string) {
  return string.charAt(0).toUpperCase() + string.slice(1);
}

function csrfSafeMethod(method) {
  // these HTTP methods do not require CSRF protection
  return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

$(document).ready(() => {
  $.ajaxSetup({
    beforeSend(xhr, settings) {
			if (!csrfSafeMethod(settings.type)) {
				// Send the token to same-origin, relative URLs only.
				// Send the token only if the method warrants CSRF protection
				// Using the CSRFToken value acquired earlier
				xhr.setRequestHeader("X-CSRFToken", csrftoken);
			}
		},
  });
});

/*
	Feed back, support and feature request
*/
$(document).on('click', '.leaveFeedbackBttn',
  (e) => {
    e.preventDefault();

    $('#leaveFeedback').foundation('reveal', 'open');
    Foundation.libs.dropdown.close($('#supportDrop'));


    return false;
  });

$(document).on('click', '.submitSupportTicketBttn',
  (e) => {
    e.preventDefault();

    $('#submitSupportTicket').foundation('reveal', 'open');
    Foundation.libs.dropdown.close($('#supportDrop'));
    $('#submitSupportTicket').bind('opened', () => {
			createFancySelect()
		});
    return false;
  });

$(document).on('click', '.featureRequestBttn',
  (e) => {
    e.preventDefault();

    $('#submitFeatureRequest').foundation('reveal', 'open');
    Foundation.libs.dropdown.close($('#supportDrop'));
    $('#submitFeatureRequest').bind('opened', () => {
		});

    return false;
  });

$(window).resize(() => {
  $('#leaveFeedback #cke_feedbackMessage').css('width', $('#leaveFeedback #cke_feedbackMessage').parents('.formRowValue').width());
});


/*
	Print Page
*/
$(document).on('click', '#print-page', (e) => {
  e.preventDefault();
  window.print();
});

/** **************************
*		Support Forms 		*
**************************** */

$(document).on('click', '#submit_support_request', function (e) {
  const form = $(this).parents('form');
  const request = $.ajax({
    url: '/',
    type: 'POST',
    data: `${form.serialize()}&support_menu=true`,
    dataType: 'json',
  });
  request.done((response) => {
    let valid = handle_errors(response, form);
    if (valid) {
      startAjaxLoader();
      window.location.reload();
    }
  });
});


/** **************************
*		Setup Wizard 		*
**************************** */

var handle_errors = function (response, $form) {
  $form.find('small.error').each(function () {
    $(this).remove();
  });
  if (response.hasOwnProperty('errors')) {
    for (const key in response.errors) {
      if (response.errors.hasOwnProperty(key)) {
        $form.find(`[name="${ key }"]`)
          .parents('.formRow')
          .find('.formRowLabel')
          .append(`<small class=error> ${ response.errors[key] }</small>`);
      }
    }
    return false;
  }
  if (response.hasOwnProperty('msg') && response.type == 'info') {
    if ($('#modalAlert').length == 0) {
      $('body').append('<div class="reveal-modal small" id="modalAlert">');
      $('#modalAlert').append('<a class="close-reveal-modal"><span class="icon-x-mark"></span></a>');
    }
    $('#modalAlert').show();
    $('.alert-box').each(function () {
      $parent = $(this);
      $child = $(this).find('div.modalAlertContents');
      new_height = $child.height() + 60;
      $parent.css('min-height', `${new_height }px`);
    });
    $('#modalAlert').hide();
    $('#modalAlert .alert-box').each(function () { $(this).remove(); });
    $('#modalAlert').append(`<div class="alert-box error"><span class="alert-icon icon-close"></span><div class="modalAlertContents">${ response.msg}</div></div>`);
    $('#modalAlert').foundation('reveal', 'open');
    return false;
  }
  return true;
};

$(document).on('click', '.save-continue, .skip', function (e) {
  e.preventDefault();
  const form = $(this).parents('form');
  const $curr_step = $(this).parents('.row');
  const next_step_count = parseInt($curr_step.attr('step')) + 1;
  const $next_step = $(`.row[step="${ next_step_count}"]`);

  if ($(this).is('.save-continue')) {
    const request = $.ajax({
      url: '/setup-wizard/',
      type: 'POST',
      data: form.serialize(),
      dataType: 'json',
    });
    request.done((response) => {
      let valid = handle_errors(response, form);
      if (valid) {
        $curr_step.addClass('hide');
        $next_step.removeClass('hide');
        $('.progress-step').removeClass('active');
        $(`.progress-step[step="${  next_step_count  }"]`).addClass('active');
      }
    });
  } else {
    startAjaxLoader();
    $curr_step.addClass('hide');
    $next_step.removeClass('hide');
    $('.progress-step').removeClass('active');
    $(`.progress-step[step="${next_step_count }"]`).addClass('active');
    stopAjaxLoader();
  }
});


$(document).on('click', '.save-prev, .skip-back', function (e) {
  e.preventDefault();
  const form = $(this).parents('form');
  const $curr_step = $(this).parents('.row');
  const prev_step_count = parseInt($curr_step.attr('step')) - 1;
  const $prev_step = $(`.row[step="${prev_step_count }"]`);

  if ($(this).is('.save-prev')) {
    const request = $.ajax({
      url: '/setup-wizard/',
      type: 'POST',
      data: form.serialize(),
      dataType: 'json',
    });

    request.done((response) => {
      let valid = handle_errors(response, form);
      if (valid) {
        $curr_step.addClass('hide');
        $prev_step.removeClass('hide');
        $('.progress-step').removeClass('active');
        $(`.progress-step[step="${  prev_step_count  }"]`).addClass('active');
      }
    });
  } else {
    startAjaxLoader();
    $curr_step.addClass('hide');
    $prev_step.removeClass('hide');
    $('.progress-step').removeClass('active');
    $(`.progress-step[step="${prev_step_count }"]`).addClass('active');
    stopAjaxLoader();
  }
});


$(document).on('click', '.save-finish, .skip-finish', function (e) {
  e.preventDefault();
  const form = $(this).parents('form');
  let rt = '/';

  if (undefined != $(this).attr('data-redirect')) {
    rt = $(this).attr('data-redirect');
  }

  if ($(this).is('.save-finish')) {
    const request = $.ajax({
      url: '/setup-wizard/',
      type: 'POST',
      data: form.serialize(),
      dataType: 'json',
    });

    request.done((response) => {
      let valid = handle_errors(response, form);
      if (valid) {
        startAjaxLoader();
        window.location.href = rt;
      }
    });
  } else {
    startAjaxLoader();
    window.location.href = rt;
  }
});

$(document).on('click', '#close-setup-link', (e) => {
  e.preventDefault();
  $('.go-to-setup-wiz').fadeOut();
  return false;
});


$(document).on('click', '.back-btn', (e) => {
  e.preventDefault();
  window.history.back();
});


$(window).resize(() => {
  $('.sidebar').removeClass('open');
  $('.bodyContent').removeClass('nav-push');
  $('.jPanelMenu-panel').css({ 'min-height': `${$(window).height() - 40  }px` });
});

$(document).ready(() => {
  $('#modalAlert').on('click', '#QBOProcessNow', (e) => {
		e.preventDefault();
		$("#modalAlert").foundation("reveal", "close");
		$.ajax({
		  method: "POST",
		  url: "/",
		  data: { action: "QBOProcessNow" }
		})
		launchPopup("/quickbooksimport/connectorapp/connectToQuickbooks/");
	});

  $('#modalAlert').on('click', '#QBOProcessLater', (e) => {
		e.preventDefault();
		$.ajax({
		  method: "POST",
		  url: "/",
		  data: { action: "QBOProcessLater" }
		})
		  .done(function() {
		    $("#modalAlert").foundation("reveal", "close");
			});
	});

  $(document).on('click', '.trigger-main-nav', (e) => {
		e.preventDefault();
		$('#main-navigation').toggle(500, 'swing');
	});
});
