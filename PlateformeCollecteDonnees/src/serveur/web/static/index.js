// index.js

document.addEventListener('DOMContentLoaded', function() {
    const body = document.body;
    const themeToggle = document.getElementById('themeToggle');

    themeToggle.addEventListener('click', function () {
        body.classList.toggle('dark-theme');
        if (body.classList.contains('dark-theme')) {
            document.cookie = "theme=dark; expires=Fri, 31 Dec 9999 23:59:59 GMT";
        } else {
            document.cookie = "theme=light; expires=Fri, 31 Dec 9999 23:59:59 GMT";
        }
        applyThemeFromCookie();
    });

    // Apply theme from cookie on page load
    applyThemeFromCookie();

    function applyThemeFromCookie() {
        const themeCookie = getCookie('theme');
        if (themeCookie === 'dark') {
            body.classList.add('dark-theme');
        } else {
            body.classList.remove('dark-theme');
        }
    }

    function getCookie(name) {
        const cookieValue = document.cookie.match('(^|;)\\s*' + name + '\\s*=\\s*([^;]+)');
        return cookieValue ? cookieValue.pop() : '';
    }
});
