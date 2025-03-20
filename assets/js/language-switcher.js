document.addEventListener('DOMContentLoaded', function () {
    // Function to get URL parameters
    function getUrlParameter(name) {
        name = name.replace(/[\[]/, '\\[').replace(/[\]]/, '\\]');
        var regex = new RegExp('[\\?&]' + name + '=([^&#]*)');
        var results = regex.exec(location.search);
        return results === null ? '' : decodeURIComponent(results[1].replace(/\+/g, ' '));
    }

    // Function to set a cookie
    function setCookie(name, value, days) {
        var expires = "";
        if (days) {
            var date = new Date();
            date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000));
            expires = "; expires=" + date.toUTCString();
        }
        document.cookie = name + "=" + (value || "") + expires + "; path=/";
    }

    // Function to get a cookie
    function getCookie(name) {
        var nameEQ = name + "=";
        var ca = document.cookie.split(';');
        for (var i = 0; i < ca.length; i++) {
            var c = ca[i];
            while (c.charAt(0) == ' ') c = c.substring(1, c.length);
            if (c.indexOf(nameEQ) == 0) return c.substring(nameEQ.length, c.length);
        }
        return null;
    }

    // Get the lang parameter from the URL
    var langParam = getUrlParameter('lang');

    // If the lang parameter is present, set it as a cookie and reload the page
    if (langParam && (langParam === 'en' || langParam === 'es')) {
        setCookie('preferred_lang', langParam, 30); // Set the cookie to expire in 30 days

        // If we're on a page with a query parameter, reload without it to avoid duplicate parameters
        if (window.location.search) {
            window.location.href = window.location.pathname;
            return; // Stop execution to prevent the rest of the code from running
        }
    }

    // Get the preferred language from the cookie
    var preferredLang = getCookie('preferred_lang');

    // Update the language switcher UI based on the preferred language
    if (preferredLang) {
        // Update the language icon text
        var languageIcon = document.querySelector('#languageDropdown i');
        if (languageIcon) {
            languageIcon.textContent = preferredLang.toUpperCase();
        }

        // Update the active class in the dropdown menu
        var dropdownItems = document.querySelectorAll('.language-switcher .dropdown-item');
        dropdownItems.forEach(function (item) {
            if (item.getAttribute('href').includes('lang=' + preferredLang)) {
                item.classList.add('active');
            } else {
                item.classList.remove('active');
            }
        });
    }
});