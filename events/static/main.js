
$(document).ready(function(){
	console.log("Hi there!")

	$(".button-collapse").sideNav();
    $('.fixed-action-btn').openFAB();
    $('.fixed-action-btn').closeFAB();


    $(document).ready(function(){
      $('.parallax').parallax();
    });

///// Register /////
    $('#nav').on('click', ".register", function(event){
    	event.preventDefault();
        var template = $('#register-template').html();
        var renderM = Mustache.render(template);
        $('#answer_div').html(renderM);
    });

    $('#answer_div').on('submit', '#register_form',function(event){
    event.preventDefault();

    var query_string = $(this).serialize() // returns all the data in your form

    $.ajax({
        method: "POST",
        url: "users/register",
        data: query_string,
    }).done(function(data, status){
            console.log(data);//for testing 

        $('#answer_div').html(data.Message);
        $('#answer_div').append("<br><br>");

		if (data.success){
			////// if they registered then display the Login ////////
                var template = $('#login-template').html();
		        var renderM = Mustache.render(template);
		        $('#answer_div').html(renderM);
		        $('#answer_div').append("<br><br>");
		        $('#answer_div').append(data.Message);
            }
        });
    });

///// Login /////
    $('#nav').on('click', ".login", function(event){
    	event.preventDefault();
        var template = $('#login-template').html();
        var renderM = Mustache.render(template);
        $('#answer_div').html(renderM);
    });

    $('#answer_div').on('submit', '#login_form',function(event){
    event.preventDefault();

    var query_string = $(this).serialize() // returns all the data in your form

    $.ajax({
        method: "POST",
        url: "users/login",
        data: query_string,
    }).done(function(data, status){
            console.log(data);//for testing 

    if (data.access_token){
        $.cookie("token", data.access_token)
        // if they logged in correctly, then render a new nav bar

        var template = $('#index-template').html();
        var renderM = Mustache.render(template);
        $('#answer_div').html(renderM);  

        var template = $('#nav-template').html();
        var renderM = Mustache.render(template);
        $('#nav').html(renderM);  
    } else {
        $('#answer_div').html(data.response);
        $('#answer_div').append("<br><br>");
    };

        });
    });

///// Create Event /////
    $('#nav').on('click', ".create", function(event){
    	event.preventDefault();
        var template = $('#create-template').html();
        var renderM = Mustache.render(template);
        $('#answer_div').html(renderM);
    });

    $('#answer_div').on('submit', '#create_form',function(event){
    event.preventDefault();

    var query_string = $(this).serialize() // returns all the data in your form
    // this works but tom is no going to like it 
    var token =("&token=" + $.cookie("token"));
    query_string = query_string.concat(token);

    $.ajax({
        method: "POST",
        url: "events/create",
        data: query_string,
    }).done(function(data, status){
            console.log(data);//for testing 

        var template = $('#all-results').html();
        var renderM = Mustache.render(template,data);
        $('#answer_div').html(renderM);  
        });
    });


////// Get All Your Events /////
    $('#nav').on('click', ".all", function(event){
    event.preventDefault();

    var query_string = $(this).serialize() // returns all the data in your form
    var query_string = ("token=" + $.cookie("token"));

    $.ajax({
        method: "POST",
        url: "events/all",
        data: query_string,
    }).done(function(data, status){
            console.log(data);//for testing 

        var template = $('#all-results').html();
        var renderM = Mustache.render(template,data);
        $('#answer_div').html(renderM);  
        });
    });

///// Logout /////
    $('#nav').on('click', ".logout", function(event){
    event.preventDefault();

    var query_string = $(this).serialize() // returns all the data in your form
    var token =("token=" + $.cookie("token"));
    query_string = query_string.concat(token);

    $.ajax({
        method: "POST",
        url: "users/logout",
        data: query_string,
    }).done(function(data, status){
            console.log(data);//for testing 

    $.removeCookie('token');

    $('#answer_div').html(" <h2> Goodbye, See you soon!</h2>");
    $('#answer_div').append(data.response);

    var template = $('#pre-nav-template').html();
    var renderM = Mustache.render(template);
    $('#nav').html(renderM);  

    });
});

///// Delete Event/////
    $('#answer_div').on('submit', '.delete_form',function(event){
    event.preventDefault();

    if(confirm("Are you sure you would like to delete this event?")){
        var query_string = $(this).serialize() // returns all the data in your form
        var token =("token=" + $.cookie("token"));
        query_string = query_string.concat(token);

        $.ajax({
            method: "POST",
            url: $(this).attr("action"),
            data: query_string,
        }).done(function(data, status){
                console.log(data);//for testing 

            $.ajax({
                method: "POST",
                url: "events/all",
                data: query_string,
            }).done(function(data, status){
                    console.log(data);//for testing 

                var template = $('#all-results').html();
                var renderM = Mustache.render(template,data);
                $('#answer_div').html(renderM);  
                });
        });
    };
});

///// Edit Event /////
    $('#answer_div').on('click', "#edit_button", function(event){
        event.preventDefault();
        console.log("clicked");

    $.ajax({
        method: "GET",
        url: $(this).attr("href"),
    }).done(function(data, status){
        console.log(data);//for testing 

        var template = $('#edit-template').html();
        var renderM = Mustache.render(template,data);
        $('#answer_div').html(renderM);  
    });

    $('#answer_div').on('submit', '#edit_form',function(event){
    event.preventDefault();

    var query_string = $(this).serialize() // returns all the data in your form
    var token =("&token=" + $.cookie("token"));
    query_string = query_string.concat(token);

    $.ajax({
        method: "POST",
        url: $(this).attr("action"),
        data: query_string,
    }).done(function(data, status){
            console.log(data);//for testing 

        var template = $('#all-results').html();
        var renderM = Mustache.render(template,data);
        $('#answer_div').html(renderM);  
        });
    });

});

////// Get All Events /////
    $('#nav').on('click', ".getall", function(event){
    event.preventDefault();

    $.ajax({
        method: "POST",
        url: "events/getall",
    }).done(function(data, status){
            console.log(data);//for testing 

        var template = $('#all-events').html();
        var renderM = Mustache.render(template,data);
        $('#answer_div').html(renderM);  
        });
    });


////// Attend Events /////
    $('#answer_div').on('click', '#attend_button',function(event){
    event.preventDefault();

    if(confirm("Please comfirm you want to attend this event")){
        var query_string = $(this).serialize() // returns all the data in your form
        var token =("token=" + $.cookie("token"));
        query_string = query_string.concat(token);

        $.ajax({
            method: "POST",
            url: $(this).attr("href"),
            data: query_string,
        }).done(function(data, status){
                console.log(data);//for testing 
                alert("Atteding!")

            $.ajax({
                method: "POST",
                url: "events/getall",
            }).done(function(data, status){
                    console.log(data);//for testing 

                var template = $('#all-results').html();
                var renderM = Mustache.render(template,data);
                $('#answer_div').html(renderM);  
                });
        });
    };
});


////// Events Your Attending/////
    $('#nav').on('click', '.attending',function(event){
    event.preventDefault();

    var query_string = $(this).serialize() // returns all the data in your form
    var query_string = ("token=" + $.cookie("token"));

    $.ajax({
        method: "POST",
        url: "events/attending",
        data: query_string,
    }).done(function(data, status){
            console.log(data);//for testing 

        var template = $('#all-results').html();
        var renderM = Mustache.render(template,data);
        $('#answer_div').html(renderM);  
        });

});

});




