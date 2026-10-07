document.addEventListener('DOMContentLoaded', function() {
    var button = document.getElementById('menu_button');
    var nav = document.getElementById('nav');
    button.addEventListener('click', function() {
        var show = nav.classList.toggle('show');
        button.setAttribute('aria-expanded', String(show));
    });
});