function showEditModal(id, name, detail, price, imageUrl) {
    // เปิด modal
    const editModal = document.getElementById('edit_class_modal');
    editModal.showModal();
    
    // ตั้งค่าฟิลด์ฟอร์มให้มีค่าเท่ากับข้อมูลของคลาสนั้น ๆ
    document.getElementById('edit_class_id').value = id;
    document.getElementById('edit_class_name').value = name;
    document.getElementById('edit_class_detail').value = detail;
    document.getElementById('edit_class_price').value = price;
    document.getElementById('edit_class_image').value = imageUrl;
}

document.getElementById('edit_class_form').addEventListener('submit', function(event) {
    event.preventDefault(); // Prevent form from submitting the traditional way

    // Create FormData object from the form
    const form = event.target;
    const formData = new FormData(form);

    // Log the FormData contents for debugging
    for (const [key, value] of formData.entries()) {
        console.log(`${key}: ${value}`);
    }
    
    // Get the CSRF token from the hidden input field
    const csrfToken = form.querySelector('[name=csrfmiddlewaretoken]').value;

    // Make the AJAX request using fetch
    fetch("/ManageClasses/", {
        method: "PUT",
        body: formData,
        headers: {
            'X-CSRFToken': csrfToken, // CSRF Token for Django
            'Accept': 'application/json', // Specify that we expect JSON response
        }
    })
    .then(response => {
        if (!response.ok) { // Check for HTTP errors
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        if (data.success) {
            alert('Class updated successfully!');
            location.reload(); // Optionally reload the page or close the modal
        } else {
            alert('Error updating class: ' + JSON.stringify(data.errors)); // Use JSON.stringify for better error visibility
        }
    })
    .catch(error => console.error('Error:', error));
});
