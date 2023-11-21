

$(document).ready(function() {
    // Attach a click event listener to all buttons
    $('button').on('click', function() {
        console.log('Button Pressed:', $(this).text());
    });
});