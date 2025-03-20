// Language Switcher JavaScript

document.addEventListener('DOMContentLoaded', function () {
    // Get all language switcher links
    const languageSwitcherLinks = document.querySelectorAll('.language-switcher .dropdown-item');

    // Add click event listener to each link
    languageSwitcherLinks.forEach(function (link) {
        link.addEventListener('click', function (event) {
            // Get the href attribute
            const href = this.getAttribute('href');

            // If the href is just a query parameter (e.g., ?lang=en)
            if (href.startsWith('?')) {
                event.preventDefault();

                // Get the current URL
                const currentUrl = window.location.href;

                // Check if the URL already has query parameters
                const hasQueryParams = currentUrl.includes('?');

                // Construct the new URL
                let newUrl;
                if (hasQueryParams) {
                    // If the URL already has query parameters, replace the lang parameter if it exists
                    const urlParts = currentUrl.split('?');
                    const baseUrl = urlParts[0];
                    const queryParams = urlParts[1].split('&');

                    // Find and replace the lang parameter
                    let langParamExists = false;
                    const newQueryParams = queryParams.map(function (param) {
                        if (param.startsWith('lang=')) {
                            langParamExists = true;
                            return href.substring(1); // Remove the ? from the href
                        }
                        return param;
                    });

                    // If the lang parameter doesn't exist, add it
                    if (!langParamExists) {
                        newQueryParams.push(href.substring(1)); // Remove the ? from the href
                    }

                    // Construct the new URL
                    newUrl = baseUrl + '?' + newQueryParams.join('&');
                } else {
                    // If the URL doesn't have query parameters, add the lang parameter
                    newUrl = currentUrl + href;
                }

                // Navigate to the new URL
                window.location.href = newUrl;
            }
        });
    });
});