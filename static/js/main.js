document.addEventListener('DOMContentLoaded', function() {
    console.log('Property Management App initialized');

    // Handle the add tenant form submission
    const addTenantForm = document.querySelector('#addTenantForm');
    if (addTenantForm) {
        addTenantForm.addEventListener('submit', function(e) {
            e.preventDefault();
            const formData = new FormData(this);

            fetch(this.action, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    // Show success message
                    alert(data.message);
                    // Close the modal
                    const modal = bootstrap.Modal.getInstance(document.querySelector('#addTenantModal'));
                    modal.hide();
                    // Reload the page to show the new tenant
                    window.location.reload();
                } else {
                    // Show error messages
                    Object.keys(data.errors).forEach(field => {
                        const errorElement = document.createElement('div');
                        errorElement.className = 'invalid-feedback';
                        errorElement.textContent = data.errors[field].join(', ');
                        const inputElement = addTenantForm.querySelector(`#${field}`);
                        inputElement.classList.add('is-invalid');
                        inputElement.parentNode.appendChild(errorElement);
                    });
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('An error occurred while adding the tenant. Please try again.');
            });
        });
    }
});
