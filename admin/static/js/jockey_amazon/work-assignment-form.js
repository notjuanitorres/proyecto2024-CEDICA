const hasScholarshipCheckbox = document.querySelector('input[name="has_scholarship"]');
const scholarshipDetails = document.getElementById('scholarship-details');

function toggleScholarshipDetails() {
    if (hasScholarshipCheckbox.checked) {
        scholarshipDetails.style.display = 'block';
    } else {
        scholarshipDetails.style.display = 'none';
    }
}
hasScholarshipCheckbox.addEventListener('change', toggleScholarshipDetails);
toggleScholarshipDetails();  // Initial check
