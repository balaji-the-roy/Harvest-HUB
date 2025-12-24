function openRegisterModal() {
    const modal = document.getElementById('registerModal');
    const modalBody = document.getElementById('modal-body');

    // Show modal
    modal.style.display = "block";

    // Load registration form
    fetch('/register/')
        .then(response => response.text())
        .then(html => {
            modalBody.innerHTML = html;
        });
}

function closeRegisterModal() {
    const modal = document.getElementById('registerModal');
    modal.style.display = "none";
}
