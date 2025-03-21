// Language switcher functionality
document.addEventListener('DOMContentLoaded', function () {
    // Get all language switcher links
    const languageLinks = document.querySelectorAll('.language-switcher .dropdown-item');

    // Add click event listener to each link
    languageLinks.forEach(link => {
        link.addEventListener('click', function (e) {
            e.preventDefault();

            // Get the language from the href attribute
            const lang = this.getAttribute('href').split('/')[1] || 'en';

            // Get the current URL
            let currentUrl = window.location.pathname;

            // If we're on a language-specific page (e.g., /es/blog/...)
            // we need to remove the language prefix
            const urlParts = currentUrl.split('/');
            if (urlParts.length > 1 && ['en', 'es'].includes(urlParts[1])) {
                // Remove the language part
                urlParts.splice(1, 1);
                currentUrl = urlParts.join('/');
                if (currentUrl === '') currentUrl = '/';
            }

            // Construct the new URL with the selected language
            // For the default language (en), we don't add a prefix
            let newUrl;
            if (lang === 'en') {
                newUrl = currentUrl;
            } else {
                // Make sure we don't add double slashes
                if (currentUrl.startsWith('/')) {
                    newUrl = '/' + lang + currentUrl;
                } else {
                    newUrl = '/' + lang + '/' + currentUrl;
                }
            }

            // No need to add query parameter - Polyglot handles language via URL path

            // Navigate to the new URL
            window.location.href = newUrl;
        });
    });
});