var req1;

// using jQuery
function getCookie(name) {
	var cookieValue = null;
	if (document.cookie && document.cookie != '') {
		var cookies = document.cookie.split(';');
		for (var i = 0; i < cookies.length; i++) {
			var cookie = jQuery.trim(cookies[i]);
			// Does this cookie string begin with the name we want?
			if (cookie.substring(0, name.length + 1) == (name + '=')) {
				cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
				break;
			}
		}
	}
	return cookieValue;
}
var csrftoken = getCookie('csrftoken');


function csrfSafeMethod(method) {
	// these HTTP methods do not require CSRF protection
	return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
	beforeSend: function(xhr, settings) {
		if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
			xhr.setRequestHeader("X-CSRFToken", csrftoken);
		}
	}
});

function sendRequest() {
	if (window.XMLHttpRequest) {
		req1 = new XMLHttpRequest();
	} else {
		req1 = new ActiveXObject("Microsoft.XMLHTTP");
	}
	lastupdate = document.getElementById("lastupdate");
	//alert(lastupdate);
	console.log("lastupdate " + lastupdate);
	req1.onreadystatechange = function() {
		if (req1.readyState != 4) return;   // hren 
		if (req1.status != 200) return;     // hren
		var data = JSON.parse(req1.responseText);
		handleResponse(data);
	};
	req1.open("GET", "/get_globalstream_newpostonly_json?lastupdate="+lastupdate.innerHTML, true);
	req1.send();
} // checked

function handleResponse(data){
	var globalstream_newpostonly = document.getElementById("globalstream_newpostonly");
	
//	var data = JSON.parse(req1.responseText);  // hren   data or responseText ???
	console.log(data);
	posts = JSON.parse(data['response_text']);     //  ???  value from get_globalstream_newpostonly_json in views.py
	console.log(posts);
	last_update = data['lastupdate'];   //  ??? value from get_globalstream_newpostonly_json in views.py
	//alert(last_update);
	
	
	var updatePosts = "";
	var i;
	for (i=0; i < posts.length; i++)
	{
		var id = posts[i]["pk"];
		var postText = posts[i]["fields"]["text"];
		var postUsername = posts[i]["fields"]["username"];
		var postTimeline = posts[i]["fields"]["timeline"];
	
	var newPost = "<div class=\"w3-row-padding w3-margin-top w3-col m12 w3-card-2 w3-round w3-white w3-container w3-padding w3-left-align\"><table><img src=\"/uploadavater?username=" + postUsername + "\" class=\"w3-circle\" height=\"75\" width=\"75\">" + postText + "<br><a href=\"profile?username=" + postUsername + "\">" + postUsername + "</a>" + postTimeline + "<br></table><button onclick=\"makeComment(this)\" name=\"Comment\" value=\"Comment\">Comment</button><input type=\"text\" name=\"Commentinput\"></input></div>"
	updatePosts += newPost;
	console.log("hii");
	console.log(updatePosts)
	}
	globalstream_newpostonly.innerHTML = updatePosts + globalstream_newpostonly.innerHTML;
	//alert(last_update);
	document.getElementById("lastupdate").innerHTML = last_update;
	//alert(document.getElementById("lastupdate").innerHTML);
}  // checked


window.setInterval(sendRequest, 7000);

var req2;

function makeComment(tag){                                                   // hren tag
	/*
	var usernamePost = document.getElementById("usernamePost").innerHTML; // hren
	var username = document.getElementById("username").innerHTML;         // hren
	var timelinePost = document.getElementById("timelinePost").innerHTML; // hren
	var commentText = document.getElementById("commentText").innerHTML;   // hren
	*/
	var usernamePost = tag.previousElementSibling.innerHTML;
	var usernameComment = tag.nextElementSibling.innerHTML;
	var timelinePost = tag.nextElementSibling.nextElementSibling.innerHTML;
	var textComment = tag.nextElementSibling.nextElementSibling.nextElementSibling.value;
	var d = new Date();
	var getMonth = d.getMonth() + 1;
	var timelineComment = d.getFullYear() + "-" + getMonth + "-" + d.getDate() + " " + d.getHours() + ":" + d.getMinutes() + ":" + d.getSeconds();
	/*
	alert(usernamePost);
	alert(usernameComment);
	alert(timelinePost);
	alert(textComment);
	alert(d);
	*/
<<<<<<< HEAD

=======
	
>>>>>>> 330bd060892d70cedb6a3aedfd6d24c19614b429
	var newComment = "<tr><td><img src=\"/uploadavater?username=" + usernameComment + "\" class=\"w3-circle\" height=\"50\" width=\"50\"></td><td><div class=\"comment-text\">" + textComment + "<br></div><div class=\"comment-info\"><pre><a href=\"profile?username=" + usernameComment + "\">" + usernameComment + "</a> " + timelineComment + "</pre></div></td></tr>";
	tag.previousElementSibling.previousElementSibling.innerHTML += newComment;
	if (window.XMLHttpRequest) {
		req2 = new XMLHttpRequest();
	} else {
		req2 = new ActiveXObject("Microsoft.XMLHTTP");
	}
	//req2.onreadystatechange = handle;
	req2.open("GET", "/save_comment?usernamePost=" + usernamePost + "&timelinePost=" + timelinePost + "&usernameComment=" + usernameComment + "&timelineComment=" + timelineComment + "&textComment=" + textComment, true);
	req2.send();	
} // checked





