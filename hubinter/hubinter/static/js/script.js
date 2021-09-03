// ------------------------- Home page ------------------------- //

// This func activate while pressing theme link
function show_theme_tags_and_videos(theme) {
    var tag_buttons = document.getElementsByClassName('tag-button')
    var tag_accordion_title = document.getElementById('tag-accordion-title')
    var videos = document.getElementsByClassName('item-thumbs')
    var scroll_down_hint = document.getElementById("scroll-down-hint")

    scroll_down_hint.style.display = "none"

    for (let video of videos) { // show all videos (accord to current theme)
        video.style.opacity = "1"
    }
    for (let tag_btn of tag_buttons) { // disable all tags
        tag_btn.classList.remove('selected-tag')
    }

    // Display tag buttons accord to current theme
    if (theme == 'all') {
        tag_accordion_title.innerHTML = 'ALL TAGS'
        for (let tag_btn of tag_buttons) {
            tag_btn.style.display = "inline-block"
        }
    }
    else {
        tag_accordion_title.innerHTML = 'TAGS FOR ' + theme.toUpperCase()
        for (let tag_btn of tag_buttons) {
            if( !tag_btn.classList.contains(theme) ) {
                tag_btn.style.display = "none"
            }
            else {
                tag_btn.style.display = "inline-block"
            }
        }
    }
};



// This func activate while pressing tag button
function show_videos_by_tag(tag_name) {
    var all_buttons = document.getElementsByClassName('tag-button')
    var tag_button = document.getElementById('tag-btn-' + tag_name)
    var videos = document.getElementsByClassName('item-thumbs')
    var scroll_down_hint = document.getElementById("scroll-down-hint")


    if (!tag_button.classList.contains('selected-tag')) { // enable tag

        let already_selected_tags_counter = 0
        for (let btn of all_buttons) { // get count of already enabled tags, BEFORE ENABLING CURRENT TAG!!!
            if ( btn.classList.contains('selected-tag') ) {
                already_selected_tags_counter += 1
            }
        }

        if (already_selected_tags_counter > 0) { // if there are some already enabled tags
            for (let video of videos) {          // (accordingly, the videos of the disabled tags are hidden)
                if( video.classList.contains(tag_name) ) { // just show videos of current tag
                    scroll_down_hint.style.display = "block"
                    video.style.opacity = "1"
                }
            }
        }
        else { // if NO tag is already enabled
            for (let video of videos) {
                if( !video.classList.contains(tag_name) ) {
                    scroll_down_hint.style.display = "block"
                    video.style.opacity = "0" // hiding all tag's videos except the current one
                }
            }
        }
        tag_button.classList.add('selected-tag') // add .class only now (to get correct value for already_selected_tags_counter)

    }


    else { // disable tag
        tag_button.classList.remove('selected-tag') // opposite, FIRSTLY remove class

        let already_selected_tags_counter = 0
        for (let btn of all_buttons) { // get count of already enabled tags, AFTER disabling current tag
            if ( btn.classList.contains('selected-tag') ) {
                already_selected_tags_counter += 1
            }
        }

        if (already_selected_tags_counter > 0) { // if there are some already enabled tags
            for (let video of videos) {          // (accordingly, the videos of the enabled tags are shown)
                if( video.classList.contains(tag_name) ) { // just hide videos of current tag
                    video.style.opacity = "0"
                }
            }
        }
        else { // if NO tag is already enabled (WE DISABLED LAST TAG ABOVE)
            for (let video of videos) { // just show all videos
                scroll_down_hint.style.display = "none"
                video.style.opacity = "1"
            }
        }

    }


};






// ------------------------- Add video form ------------------------- //

// Show tags by current selected theme in add-video form
const select_theme_block = document.getElementById('id_theme')
const select_tag_block = document.getElementById('id_tags')

// triggered when changing the selection
select_theme_block.addEventListener('change', function() {
    token = get_csrf_token();
    $.ajax({
        type: "POST",
        url: location.protocol + '//' + location.host + '/ajax/tags_by_theme/',
        data: {
            'theme' : select_theme_block.options[select_theme_block.selectedIndex].text, // send chosen theme name
            "csrfmiddlewaretoken" : token
        },
        success: function(response) {              
            tag_list = merge_into_single_array(response) // get one list of tags by chosen theme
            show_tags_by_theme(tag_list) // show only suitable ones
        },
        error: function(error) {
            show_tags_by_theme("all") // if something went wrong, leave all tags visible
        }
    })
});

// need to merge, because json returns array of arrays
function merge_into_single_array(ajax_response) {
    if (ajax_response['tags'] == "all") {
        tag_list = "all" // if current theme is not chosen, will show all tags
        return tag_list;
    }
    else {
        tag_list = []; // if chosen, merge tags into one array
        for (let tag_name of ajax_response['tags']) {
            tag_list.push(tag_name[0])
        }
        return tag_list;
    }
};

// show tags by theme only in add-video form
function show_tags_by_theme(tag_list) {
    if (tag_list == "all") {
        for (let tag_option_btn of select_tag_block.options) { // if not chosen, just show all tags 
            tag_option_btn.style.display = 'block';
            tag_option_btn.selected = false // remove all selections
        }
    }
    else {
        for (let tag_option_btn of select_tag_block.options) {
            if ( tag_list.includes(tag_option_btn.text) ) { // if tag in tag_list, leave it visible
                tag_option_btn.style.display = 'block';
                tag_option_btn.selected = false
            }
            else {
                tag_option_btn.style.display = 'none';
            }
        }
    }
};






// ------------------------- Video Detail ------------------------- //

// Process the like and dislike click event
function put_remove__like_dislike(btn_id, video_slug) {
    var button = document.getElementById(btn_id)

    // determine which button was pressed
    if (btn_id == 'like-btn') {
        like_control(button, video_slug);
    }
    else {
        dislike_control(button, video_slug);         
    }
};

// Control highlighting if pressed "LIKE" and call another func to send ajax-query
function like_control(button_obj, slug) { 
    if (button_obj.classList.contains('active')) { // if was already pressed, turn off it
        turn_off('like', slug);
        button_obj.classList.remove('active')
        button_obj.style.background = "#3C3F45"
    }
    else { // if it wasn't pressed, add it AND turn off opposite button
        turn_on('like', slug);
        var dislike_btn = document.getElementById('dislike-btn')
        dislike_btn.classList.remove('active')
        dislike_btn.style.background = "#3C3F45"
        button_obj.classList.add('active')
        button_obj.style.background = "#DE5E60"
    }
};
// Control highlighting if pressed "DISLIKE" and call another func to send ajax-query
function dislike_control(button_obj, slug) {
    if (button_obj.classList.contains('active')) { // the same as above...
        turn_off('dislike', slug);
        button_obj.classList.remove('active')
        button_obj.style.background = "#3C3F45"
    }
    else { // the same as above...
        turn_on('dislike', slug);
        var like_btn = document.getElementById('like-btn')
        like_btn.classList.remove('active')
        like_btn.style.background = "#3C3F45"
        button_obj.classList.add('active')
        button_obj.style.background = "#DE5E60"
    }
};

// Send ajax query to TURN ON like or dislike for video
function turn_on(marker_type, slug) {
    token = get_csrf_token();
    $.ajax({
        type: "POST",
        url: location.protocol + '//' + location.host + '/ajax/turn_on_marker/',
        data: {
            "marker_type" : marker_type,
            "slug" : slug, 
            "csrfmiddlewaretoken" : token
        },
        success: function(response) {
            if (response["need_to_login"]) {
                need_to_login__alert();
                like_btn = document.getElementById("like-btn")
                dislike_btn = document.getElementById("dislike-btn")
                document.getElementById("like-block").classList.remove("active")
                document.getElementById("dislike-block").classList.remove("active")
                like_btn.classList.remove("active")
                dislike_btn.classList.remove("active")
                like_btn.style.background = "#3C3F45"
                dislike_btn.style.background = "#3C3F45"
            }
            like_counter = document.getElementById('like-counter')
            dislike_counter = document.getElementById('dislike-counter')
            like_counter.textContent = response['current_likes']
            dislike_counter.textContent = response['current_dislikes']
        },
        error: function(error) {
            smth_wrong__alert();
            if (marker_type == "like") {
                btn = document.getElementById("like-btn")
                document.getElementById("like-block").classList.remove("active")
            }
            else {
                btn = document.getElementById("dislike-btn")
                document.getElementById("dislike-block").classList.remove("active")
            }
            btn.classList.remove("active")
            btn.classList.remove("active")
            btn.style.background = "#3C3F45"
            btn.style.background = "#3C3F45"
        }
    });
};

// Send ajax query to TURN OFF like or dislike for video
function turn_off(marker_type, slug) {
    token = get_csrf_token();
    $.ajax({
        type: "POST",
        url: location.protocol + '//' + location.host + '/ajax/turn_off_marker/',
        data: {
            "marker_type" : marker_type, 
            "slug" : slug,
            "is_ajax" : true,
            "csrfmiddlewaretoken" : token
        },
        success: function(response) {
            if (response["need_to_login"]) {
                need_to_login__alert();
                like_btn = document.getElementById("like-btn")
                dislike_btn = document.getElementById("dislike-btn")
                document.getElementById("like-block").classList.remove("active")
                document.getElementById("dislike-block").classList.remove("active")
                like_btn.classList.remove("active")
                dislike_btn.classList.remove("active")
                like_btn.style.background = "#3C3F45"
                dislike_btn.style.background = "#3C3F45"
            }
            like_counter = document.getElementById('like-counter')
            dislike_counter = document.getElementById('dislike-counter')
            like_counter.textContent = response['current_likes']
            dislike_counter.textContent = response['current_dislikes']
        },
        error: function(error) {
            smth_wrong__alert();
        }
    });
};




// Process subscribe click event
function subscribe_unsubscribe(author_username) {
    var subscribe_btn = document.getElementById("subscribe-btn")

    if ( !subscribe_btn.classList.contains("subscribed") ) { // if not subscribed (btn is red)
        subscribe_btn.classList.add("subscribed")
        subscribe_btn.text = "SUBSCRIBED"
        subscribe(author_username);
    }
    else {
        subscribe_btn.classList.remove("subscribed")
        subscribe_btn.text = "SUBSCRIBE"
        unsubscribe(author_username);
    }
}

// Send ajax-query to SUBSCRIBE current user on video's author
function subscribe(username) {
    token = get_csrf_token();
    $.ajax({
        type: "POST",
        url: location.protocol + '//' + location.host + '/ajax/subscribe_user/',
        data: {
            "author_username" : username,
            "csrfmiddlewaretoken" : token
        },
        success: function(response) {
            if (response["need_to_login"]) {
                var subscribe_btn = document.getElementById("subscribe-btn")
                subscribe_btn.classList.remove("subscribed")
                need_to_login__alert();
            }
            else if ("current_subs" in response) {
                var subs_counter = document.getElementById("subs-counter")
                subs_counter.innerHTML = String(response["current_subs"]) + " subs"
                if (!response["current_user_is_author"]) {
                    $(".wrapper_notifications-btn").css("display", "block")
                }
            }
        },
        error: function(error) {
            smth_wrong__alert();
        }
    });
}

// Send ajax-query to UNSUBSCRIBE current user from video's author
function unsubscribe(username) {
    token = get_csrf_token();
    $.ajax({
        type: "POST",
        url: location.protocol + '//' + location.host + '/ajax/unsubscribe_user/',
        data: {
            "author_username" : username,
            "csrfmiddlewaretoken" : token
        },
        success: function(response) {
            if (response["need_to_login"]) {
                var subscribe_btn = document.getElementById("subscribe-btn")
                subscribe_btn.classList.remove("subscribed")
                need_to_login__alert();
            }
            else if ("current_subs" in response) {
                var subs_counter = document.getElementById("subs-counter")
                subs_counter.innerHTML = String(response["current_subs"]) + " subs"
                $("#notification-btn").removeClass("notified")
                $(".wrapper_notifications-btn").css("display", "none")
            }
        },
        error: function(error) {
            smth_wrong__alert();
        }
    });
}



// Process notification click event
function notification(author_username) {
    var notification_btn = document.getElementById("notification-btn")

    if ( !notification_btn.classList.contains("notified") ) { // if not notified (btn is grey)
        notification_btn.classList.add("notified")
        notify(author_username);
    }
    else {
        notification_btn.classList.remove("notified")
        not_notify(author_username);
    }
}

// Send ajax-query to NOTIFY current user about new author videos
function notify(username) {
    token = get_csrf_token();
    $.ajax({
        type: "POST",
        url: location.protocol + '//' + location.host + '/ajax/notify_user/',
        data: {
            "author_username" : username,
            "csrfmiddlewaretoken" : token
        },
        success: function(response) {
            if (response["need_to_login"]) {
                var notification_btn = document.getElementById("notification-btn")
                notification_btn.classList.remove("notified")
                need_to_login__alert();
            }
            if (response["need_to_subscribe"]) {
                var notification_btn = document.getElementById("notification-btn")
                notification_btn.classList.remove("notified")
                $('#alert__area').html('<div class="alert alert-error fade in"><a class="close" data-dismiss="alert" href="#">&times;</a><strong>You should subscribe to the channel to enable notifications!</strong></div>')
                $('body,html').animate({ scrollTop: "0" }, 750, 'easeOutExpo' );
            }
        },
        error: function(error) {
            smth_wrong__alert();
        }
    });
}

// Send ajax-query to NOT NOTIFY current user about new author videos
function not_notify(username) {
    token = get_csrf_token();
    $.ajax({
        type: "POST",
        url: location.protocol + '//' + location.host + '/ajax/not_notify_user/',
        data: {
            "author_username" : username,
            "csrfmiddlewaretoken" : token
        },
        success: function(response) {
            if (response["need_to_login"]) {
                var notification_btn = document.getElementById("notification-btn")
                notification_btn.classList.remove("notified")
                need_to_login__alert();
            }
            if (response["need_to_subscribe"]) {
                var notification_btn = document.getElementById("notification-btn")
                notification_btn.classList.remove("notified")
                $('#alert__area').html('<div class="alert alert-error fade in"><a class="close" data-dismiss="alert" href="#">&times;</a><strong>You should subscribe to the channel to enable notifications!</strong></div>')
                $('body,html').animate({ scrollTop: "0" }, 750, 'easeOutExpo' );
            }
        },
        error: function(error) {
            smth_wrong__alert();
        }
    });
}



// Fill in hidden input with parent-comment id  AND  show comment-form in correct place if user answer for another comment
function show_comments_form(parent_comment_id, offset) {
    var answer_btn = document.getElementById('answer-text-' + parent_comment_id)

    if (answer_btn.classList.contains("white-text")) {
        $("#contact_message").val('')
        $("#id_parent_comment").val('')
        $(".comment-form").css({"margin-left" : "0", "margin-bottom" : "0"})
        $(".comment-form").insertAfter("#anchor-for-contact_message")
        answer_btn.classList.remove("white-text") 
    }
    else {
        $("#contact_message").val('')
        $("#id_parent_comment").val(parent_comment_id)
        $(".answer-btn-text").removeClass("white-text")
        $("#answer-text-" + parent_comment_id).addClass("white-text")
        $(".comment-form").css({"margin-bottom" : "50px"})

        if (offset == "1") { // show form with indent if we answer FOR ANOTHER ANSWER
            $(".comment-form").css({"margin-left" : "10%"})
        }
        else {
            $(".comment-form").css({"margin-left" : "0"})
        }

        $(".comment-form").insertAfter("#" + parent_comment_id)
        $("#contact_message").focus()
    };
};

// Send ajax query for adding comment with all comment-form's data 
function add_comment_query(video_slug) {
    if ( $(".comment-text").val().trim() ) {
        $.ajax({
            type: "POST",
            url: location.protocol + "//" + location.host + "/ajax/add_comment/",
            data: {
                "video_slug" : video_slug,
                "parent_comment" : $("#id_parent_comment").val(),
                "comment_text" : $(".comment-text").val(),
                "csrfmiddlewaretoken" : $('input[name="csrfmiddlewaretoken"]').val()
            },
            success: function(response) {
                comment_form_back_to_place();
                $("#comment-counter").text(response["current_comments_count"])
                var comment = get_comment_template(response)
                if (response['parent_comment_id'] == "no-parent") {
                    if ($(".no-comments-yet").length) {
                        $(".no-comments-yet").replaceWith('<hr><div class="comments"><div id="anchor-for-top_comment"></div></div>')
                    }
                    $(comment).insertAfter("#anchor-for-top_comment")
                    highlight_element_background(response['comment_id'], 800, "#26292E");
                }
                else {
                    $(comment).insertAfter("#" + response['parent_comment_id'])
                    highlight_element_background(response['comment_id'], 800, "#2B2D34");
                }
            },
            error: function(error) {
                comment_form_back_to_place();
                smth_wrong__alert();
            }
        });
    }
};
















// ------------------------- Other utils ------------------------- //

// Get current CSRF-token from cookies
function get_csrf_token() {
    var a = document.cookie.split(';');
    var token = ''
    for (i = 0; i < a.length; i++) {
        var b = a[i].split('=')
        b[0] = b[0].replace(/\s+/g, '')
        if (b[0] == 'csrftoken') {
            token = b[1]
        }
    }
    return token;
}


// Show alert, that user must log in
function need_to_login__alert() {
    $('#alert__area').html('<div class="alert alert-error fade in"><a class="close" data-dismiss="alert" href="#">&times;</a><strong>You should authenticate to interact with the videos!</strong></div>')
    $('body,html').animate({ scrollTop: "0" }, 750, 'easeOutExpo' );
}


// Show alert, that something went wrong on back-end
function smth_wrong__alert() {
    $('#alert__area').html('<div class="alert alert-error fade in"><a class="close" data-dismiss="alert" href="#">&times;</a><strong>Oops... Something went wrong! :(</strong></div>')
    $('body,html').animate({ scrollTop: "0" }, 750, 'easeOutExpo' );
}


// Put comment form back to initial position on page
function comment_form_back_to_place() {
    $(".comment-text").val('')
    $("#id_parent_comment").val('')
    $(".comment-form").css({"margin-left" : "0", "margin-bottom" : "0"})
    $(".comment-form").insertAfter("#anchor-for-contact_message")
    $("#submit-comment-btn").removeClass("active__comment-submit")
    $(".answer-btn-text").removeClass("white-text")
}


// Create HTML-template to the just-added comment
function get_comment_template(comment_data) {
    comment = `
    <div class="comment-block ${comment_data['answer'] ? "answer" : ""}" id="${comment_data['comment_id']}">
    <div class="comment__author-published">
        <b class="red-text"><a href="${comment_data['author_url']}">${comment_data['author_username'].substring(0, 30)}</a></b>
        <span class="side-margins">&#8226;</span>
        <span>${comment_data['created_at']}</span>
    </div>
    <div class="comment__text">
        <span style="max-width: 100%;">${comment_data['text']}</span>
    </div>
    <div class="comment__answer-btn">
        <a id="answer-text-${comment_data['comment_id']}" class="answer-btn-text" onclick="show_comments_form('${comment_data['comment_id']}', '${comment_data['answer'] ? "1" : "0"}')">
            <span>&#10150;</span>
            <span>&nbsp;Answer</span>
        </a>
    </div>
    `
    return comment;
}


// Highlight element's background with red color with subsequent color fading
function highlight_element_background(elem_id, time, back_to_color) {
    $("#" + elem_id).css({"background-color" : "#FF5D5F"})
    $("#" + elem_id).animate({"background-color" : back_to_color}, time)
}