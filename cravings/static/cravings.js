// Opening and closing sidebar on mobile
document.addEventListener('DOMContentLoaded', () => {
    document.querySelector('.sidebar').style.width = "0";
    document.querySelector('.open-sidebar-button').style.display = "block";
    document.querySelector('.close-sidebar-button').style.display = "none";
});

function openSidebar() {
    document.querySelector('.sidebar').style.width = "60vw";
    document.querySelector('.banner').style.filter = "brightness(60%)";
    document.querySelector('.mobile-body').style.filter = "brightness(60%)";
    document.querySelector('.mobile-body').style.backgroundColor = "#dddddd";
    document.querySelector('.open-sidebar-button').style.display = "none";
    document.querySelector('.close-sidebar-button').style.display = "block";
}

function closeSidebar() {
    document.querySelector('.sidebar').style.width = "0";
    document.querySelector('.banner').style.filter = "brightness(100%)";
    document.querySelector('.mobile-body').style.filter = "brightness(100%)";
    document.querySelector('.mobile-body').style.backgroundColor = "white";
    document.querySelector('.open-sidebar-button').style.display = "block";
    document.querySelector('.close-sidebar-button').style.display = "none";
}

// Showing and hiding subcategories in sidebar
function showSubcategories(show_button) {
    let category = show_button.parentNode.parentNode;
    let hide_button = category.querySelector('.hide-button');
    category.querySelector('.category-scroll').style.height = "140px";
    show_button.style.display = "none";
    hide_button.style.display = "inline-block";
}

function hideSubcategories(hide_button) {
    let category = hide_button.parentNode.parentNode;
    let show_button = category.querySelector('.show-button');
    category.querySelector('.category-scroll').style.height = "0";
    hide_button.style.display = "none";
    show_button.style.display = "inline-block";
}

// Display small restaurant card image, highlight/unhighlight as mouse hovers, show/hide actions button
document.addEventListener('DOMContentLoaded', () => {
    display_small_card_images();
});

function display_small_card_images() {
    let cards = document.querySelectorAll('.small-card');
    for (var i=0; i<cards.length; i++) {
        const card = cards[i];
        const img_link = card.querySelector('.hidden-image').innerHTML;
        card.style.backgroundImage = `linear-gradient(rgba(255,255,255,0.7), rgba(255,255,255,0.7)), url(${img_link})`;
        card.style.backgroundSize = 'cover';
    }
}

function highlight_small_card(small_card) {
    const img_link = small_card.querySelector('.hidden-image').innerHTML;
    small_card.style.backgroundImage = `linear-gradient(rgba(255,255,255,0.3), rgba(255,255,255,0.3)), url(${img_link})`;
    small_card.querySelector('.card-actions').querySelector('button').style.visibility = 'visible';
}

function unhighlight_small_card(small_card) {
    const img_link = small_card.querySelector('.hidden-image').innerHTML;
    small_card.style.backgroundImage = `linear-gradient(rgba(255,255,255,0.7), rgba(255,255,255,0.7)), url(${img_link})`;
    small_card.querySelector('.card-actions').querySelector('button').style.visibility = 'hidden';
}

// Highlight/unhighlight large restaurant card image as mouse hovers
function highlight_large_card(large_card) {
    large_card.style.boxShadow = '0px 0px 3px 3px #cccccc';
}

function unhighlight_large_card(large_card) {
    large_card.style.boxShadow = 'none';
}

// Star rating on restaurant view, cards
document.addEventListener('DOMContentLoaded', () => {
    restaurant_rating();
    card_ratings();
    review_rating();
});

function card_ratings() {
    let cards = document.querySelectorAll('.card-star-rating');
    for (var i=0; i<cards.length; i++) {
        star_rating(cards[i]);
    }
}

function restaurant_rating() {
    let restaurant_headers = document.querySelectorAll('.restaurant-star-rating');
    for (var i=0; i<restaurant_headers.length; i++) {
        star_rating(restaurant_headers[i]);
    }
}

function review_rating() {
    let reviews = document.querySelectorAll('.review-star-rating');
    for (var i=0; i<reviews.length; i++) {
        star_rating(reviews[i]);
    }
}

function star_rating(div) {
    let stars = div.querySelectorAll('.fa');
    console.log(div);
    console.log(stars);
    let mean_rating = Math.round(div.parentNode.querySelector('.hidden-stars').innerHTML);
    for (var i=0; i<mean_rating; i++) {
        stars[i].classList.add('checked');
    }
}

// Crave/Uncrave
document.addEventListener('DOMContentLoaded', () => {
    crave_uncrave_buttons();
});

function crave_uncrave_buttons() {
    let restaurant_divs = document.querySelectorAll('.restaurant-instance');
    for (var i=0; i<restaurant_divs.length; i++) {
        let div = restaurant_divs[i];
        let clean_name = div.querySelector('.clean-name').textContent;
        let data = JSON.parse(document.querySelector(`#${clean_name}`).textContent);

        if (data['is_craved']) {
            div.querySelector('.crave').style.display = "none";
        }
        else {
            div.querySelector('.uncrave').style.display = "none";
        }
    }
}

function add_to_cravings(element, username, restaurant_name) {
    fetch(`/cravings/${username}`, {
        method: 'PUT',
        body: JSON.stringify({
            restaurant_name: restaurant_name,
            crave: true,
        })
    });

    element.style.display = "none";
    element.parentNode.querySelector('.uncrave').style.display = "inline-block";

    let header_restaurant_name = document.querySelector('.title').querySelector('a').textContent;
    if (header_restaurant_name === restaurant_name) {
        document.querySelector('.restaurant-buttons').querySelector('.crave').style.display = "none";
        document.querySelector('.restaurant-buttons').querySelector('.uncrave').style.display = "inline-block";
        document.querySelector('.restaurant-buttons').querySelector('.second-level').style.marginLeft = "353px";
    }
}

function remove_from_cravings(element, username, restaurant_name) {
    fetch(`/cravings/${username}`, {
        method: 'PUT',
        body: JSON.stringify({
            restaurant_name: restaurant_name,
            crave: false,
        })
    });

    element.style.display = "none";
    element.parentNode.querySelector('.crave').style.display = "inline-block";

    let header_restaurant_name = document.querySelector('.title').querySelector('a').textContent;
    if (header_restaurant_name === restaurant_name) {
        document.querySelector('.restaurant-buttons').querySelector('.uncrave').style.display = "none";
        document.querySelector('.restaurant-buttons').querySelector('.crave').style.display = "inline-block";
        document.querySelector('.restaurant-buttons').querySelector('.second-level').style.marginLeft = "308px";
    }
}

// Showing/hiding new dinelist menu on left sidebar
function show_new_dinelist_menu_desktop() {
    document.querySelector('.desktop-new-dinelist').querySelector('.new-dinelist-form').style.height = "115px";
}

function hide_new_dinelist_menu_desktop() {
    event.preventDefault();
    document.querySelector('.desktop-new-dinelist').querySelector('.new-dinelist-form').style.height = "0";
}

function show_new_dinelist_menu_mobile() {
    document.querySelector('.mobile-new-dinelist').querySelector('.new-dinelist-form').style.height = "10vh";
}

function hide_new_dinelist_menu_mobile() {
    event.preventDefault();
    document.querySelector('.mobile-new-dinelist').querySelector('.new-dinelist-form').style.height = "0";
}

// Add/remove restaurant to/from dinelist
function add_to_dinelist(restaurant_name, dinelist_name) {
    fetch('/dinelist', {
        method: 'PUT',
        body: JSON.stringify({
            restaurant_name: restaurant_name,
            dinelist_name: dinelist_name,
            action: 'add',
        })
    });
}

function remove_from_dinelist(restaurant_name, dinelist_name, restaurant_class) {
    fetch('/dinelist', {
        method: 'PUT',
        body: JSON.stringify({
            restaurant_name: restaurant_name,
            dinelist_name: dinelist_name,
            action: 'remove',
        })
    });

    document.querySelector(`.${restaurant_class}`).style.display = "none";
}
