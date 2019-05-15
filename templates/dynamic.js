$(document).ready(function() {
	$('#support_modal_links').on('click', 'a:not(".not-support")', function(e) {
		e.preventDefault();
		$link = $(this);

//		$(document).on('opened.fndtn.reveal', '#supportModal', function(){
//			$('#supportModal').css({'height': 'auto', 'overflow': 'visible'});
//			$('#supportModal input[type="text"]').focus();
//			$(document).foundation();
//		});

		$('#supportModal').foundation('reveal', 'open', {
			url: '{{ domain }}',
			method: 'POST',
			data: {support_menu: true, form: $link.attr('data-form')}
		});

		$('#supportDrop').foundation('dropdown', 'close', $('#supportDrop'))
	});

	$(".adminBlock").on('click', '#supportTicket', function(e) {
		e.preventDefault();
		$link = $(this);

		$('#supportModal').foundation('reveal', 'open', {
			url: '{{ domain }}',
			method: 'POST',
			data: {support_menu: true, form: $link.attr('data-form')}
		});

		$('#supportDrop').foundation('dropdown', 'close', $('#supportDrop'))
	});

	$('.company-drop').on('click', 'a.support-trigger', function(e) {
		e.preventDefault();
		$link = $(this);

		$('#supportModal').foundation('reveal', 'open', {
			url: '{{ domain }}',
			method: 'POST',
			data: {support_menu: true, form: $link.attr('data-form')}
		});
	});
});
