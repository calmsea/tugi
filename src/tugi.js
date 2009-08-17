function json_update(json_url) {
//    alert('json_update');
    opts = { onComplete: json_complete };
    new Ajax.Request(json_url, opts);
		return true;
}
function json_complete(req, json) {
//    alert('json_complete');
		var my_div = document.createElement('div');

		Element.extend(my_div);
		my_div.addClassName('pending');
		my_div.innerHTML = req.responseText;

    $('tugi_view').appendChild(my_div)
}
