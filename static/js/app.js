/* Template Name: Cristino - Responsive Personal Template
   Author: Shreethemes
   Email: shreethemes@gmail.com
   Website: http://www.shreethemes.in
   Version: 1.9.0
   Created: May 2020
   File Description: Main JS file of the template
*/

/************************/
/*       INDEX          */
/*=======================
 *  01.  Loader         *
 *  02.  Menu           *
 *  03.  Scrollspy      *
 *  04.  Magnific Popup *
 *  05.  Owl Carousel   *
 *  06.  Back to top    *
 *  07.  Feather Icon   *
 =======================*/

// Preloader
window.onload = function loader() {
    setTimeout(() => {
        document.getElementById('preloader').style.visibility = 'hidden';
        document.getElementById('preloader').style.opacity = '0';
    }, 350);
}


// Menu sticky
function windowScroll() {
    const navbar = document.getElementById("navbar");
    if (
        document.body.scrollTop >= 50 ||
        document.documentElement.scrollTop >= 50
    ) {
        navbar.classList.add("nav-sticky");
    } else {
        navbar.classList.remove("nav-sticky");
    }
}

window.addEventListener('scroll', (ev) => {
    ev.preventDefault();
    windowScroll();
})

// back-to-top
var mybutton = document.getElementById("back-to-top");
window.onscroll = function () {
    scrollFunction();
};

function scrollFunction() {
    if (document.body.scrollTop > 100 || document.documentElement.scrollTop > 100) {
        mybutton.style.display = "block";
    } else {
        mybutton.style.display = "none";
    }
}

function topFunction() {
    document.body.scrollTop = 0;
    document.documentElement.scrollTop = 0;
}

//Feather icon
feather.replace()

// Navbar Active Class
var spy = new Gumshoe('#navbar-navlist a', {
    // Active classes
    // navClass: 'active', // applied to the nav list item
    // contentClass: 'active', // applied to the content
    offset: 80
});


function stickMessage() {
    var navbarHeight = document.getElementById('navbar').offsetHeight;
    var messagesContainer = document.getElementById('messages-container');
    messagesContainer.style.top = navbarHeight + 15 + 'px';
}

stickMessage()

window.addEventListener('scroll', function () {
    stickMessage()
});

document.addEventListener("DOMContentLoaded", function () {
    const themeSwitcher = document.getElementById('theme-switcher');
    const savedTheme = localStorage.getItem('theme');

    // Function to apply the theme after a short delay
    function applyTheme(theme) {
            if (theme === 'dark') {
                document.getElementById('theme-opt').href = darkPath;
                themeSwitcher.checked = true;
            } else {
                document.getElementById('theme-opt').href = lightPath;
                themeSwitcher.checked = false;
            }
    }

    // Check the saved theme from localStorage and set the checkbox state
    themeSwitcher.checked = savedTheme === 'dark';

    // Handle toggle switch
    themeSwitcher.addEventListener('change', function () {
        if (this.checked) {
            applyTheme('dark');
            localStorage.setItem('theme', 'dark');
        } else {
            applyTheme('light');
            localStorage.setItem('theme', 'light');
        }
    });
});
