// script.js

// Get the modal
const modal = document.getElementById('modal');

// Get the button that opens the modal
const startBtn = document.getElementById('start');

// Get the <span> element that closes the modal
const closeModalButton = document.getElementById('closeModalButton');

// When the user clicks the button, open the modal with animation
startBtn.onclick = function() {
    modal.style.display = 'block'; // Make the modal visible
    setTimeout(() => { // Wait for the next frame to start animation
        modal.style.opacity = '1'; // Fade in the overlay
        document.querySelector('.modal-content').style.transform = 'scale(1)'; // Scale up the content
    }, 10);
}

// When the user clicks on <span> (x), close the modal with animation
closeModalButton.onclick = function() {
    modal.style.opacity = '0'; // Fade out the overlay
    document.querySelector('.modal-content').style.transform = 'scale(0.5)'; // Scale down the content
    setTimeout(() => { // Wait for animation to finish before hiding the modal
        modal.style.display = 'none';
    }, 300);
}

// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
    if (event.target === modal) {
        closeModalButton.onclick();
    }
}

function showPassPanel(){
    const passField = document.getElementById('password');
    if (passField.type === 'password'){
        passField.type = 'text';
    }
    else{
        passField.type = 'password';
    }
}
