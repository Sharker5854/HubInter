
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
                $('#alert__area').html('<div class="alert alert-error fade in"><a class="close" data-dismiss="alert" href="#">&times;</a><strong>You should authenticate to interact with the video!</strong></div>')
                $('body,html').animate({ scrollTop: "0" }, 750, 'easeOutExpo' );
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
            $('#alert__area').html('<div class="alert alert-error fade in"><a class="close" data-dismiss="alert" href="#">&times;</a><strong>Oops... Something went wrong! :(</strong></div>')
            $('body,html').animate({ scrollTop: "0" }, 750, 'easeOutExpo' );
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
                $('#alert__area').html('<div class="alert alert-error fade in"><a class="close" data-dismiss="alert" href="#">&times;</a><strong>You should authenticate to interact with the video!</strong></div>')
                $('body,html').animate({ scrollTop: "0" }, 750, 'easeOutExpo' );
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
            $('#alert__area').html('<div class="alert alert-error fade in"><a class="close" data-dismiss="alert" href="#">&times;</a><strong>Oops... Something went wrong! :(</strong></div>')
            $('body,html').animate({ scrollTop: "0" }, 750, 'easeOutExpo' );
        }
    });
};















// ------------------------- Other utils ------------------------- //
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