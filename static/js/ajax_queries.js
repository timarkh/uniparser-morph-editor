$( document ).ready(
	function() {
		assign_input_events();
		get_cur_word();
	}
);

function get_cur_word() {
	$.ajax({
		url: "cur_word",
		type: "GET",
		success: show_lemma,
		error: function(errorThrown) {
			alert( JSON.stringify(errorThrown) );
		}
	});
}

function get_prev_word() {
	$.ajax({
		url: "prev_word",
		data: $("#lemma_form").serialize(),
		type: "GET",
		success: show_lemma,
		error: function(errorThrown) {
			alert( JSON.stringify(errorThrown) );
		}
	});
}

function get_next_word() {
	$.ajax({
		url: "next_word",
		data: $("#lemma_form").serialize(),
		type: "GET",
		success: show_lemma,
		error: function(errorThrown) {
			alert( JSON.stringify(errorThrown) );
		}
	});
}

function save_dict() {
	$.ajax({
		url: "save_dict",
		data: $("#lemma_form").serialize(),
		type: "GET",
		success: function () {},
		error: function(errorThrown) {
			alert( JSON.stringify(errorThrown) );
		}
	});
}

function show_lemma(data) {
	$("#lemma_form").html(data.contents);
	create_tag_buttons(data.settings.tags);
	highlight_tag_buttons();
}

function create_tag_buttons(tagsDict) {
	$("#tag_buttons").html("");
	for (var key in tagsDict) {
		var tag = tagsDict[key];
		$("#tag_buttons").append("<button type=\"button\" class=\"btn btn-tag\" data-key=\"" + key + "\">" + tag + "</button>");
	}
}

function highlight_tag_buttons() {
	var val = ",";
	$(".form-control-gramm").each(function (index) {
		val += $(this).val();
	});
	val += ",";
	$(".btn-tag").each(function (index) {
		if (val.includes("," + $(this).text() + ",")) {
			$(this).toggleClass("btn-tag-on");
		}
	});
}

function escapeRegExp(string) {
  return string.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
}

function process_keypress(e) {
	if (e.key == "ArrowRight") {
		get_next_word();
	}
	else if (e.key == "ArrowLeft") {
		get_prev_word();
	}
	else if (e.key == "Enter") {
		save_dict();
	}
	else if (e.key == "1") {
		// Leave only the first segment in translations
		$(".form-control-trans").each(function (indexGr) {
			$(this).val($(this).val().replace(/^[0-9.,(): ]*([^,.;()]*?) *[,.;()].*/g, "$1"));
		});
	}
	else if (e.key == "2") {
		// Leave only the second segment in translations
		$(".form-control-trans").each(function (indexGr) {
			$(this).val($(this).val().replace(/^[0-9.,(): ]*([^,.;()]*?) *[0-9]*[,.;()][0-9.,(): ]*([^,.;()]*?) *(?:[,.;()].*$|$)/g, "$2"));
		});
	}
	else if (e.key == "-") {
		// Mark lemma for removal
		$(".form-control-lemma").each(function (indexGr) {
			$(this).val($(this).val() + "-");
		});
	}
	else {
		$(".btn-tag").each(function (indexTag) {
			if (e.key == $(this).attr("data-key")) {
				if ($(this).hasClass("btn-tag-on")) {
					var rxTagMiddle = new RegExp("," + escapeRegExp($(this).text()) + ",", "g");
					var rxTagStart = new RegExp("^" + escapeRegExp($(this).text()) + ",", "g");
					var rxTagEnd = new RegExp("," + escapeRegExp($(this).text()) + "$", "g");
					$(".form-control-gramm").each(function (indexGr) {
						$(this).val($(this).val().replace(rxTagMiddle, ","));
						$(this).val($(this).val().replace(rxTagStart, ""));
						$(this).val($(this).val().replace(rxTagEnd, ""));
					});
				}
				else {
					var tag = $(this).text();
					$(".form-control-gramm").each(function (indexGr) {
						$(this).val($(this).val() + "," + tag);
					});
				}
				$(this).toggleClass("btn-tag-on");
			}
		});
	}
}

function assign_input_events() {
	$("#prev_word").unbind('click');
	$("#next_word").unbind('click');
	$("#save_dict").unbind('click');
	$("#prev_word").click(get_prev_word);
	$("#next_word").click(get_next_word);
	$("#save_dict").click(save_dict);
	$(document).keydown(process_keypress);
}