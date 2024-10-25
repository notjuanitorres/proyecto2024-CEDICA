const hasCuratorshipCheckbox = document.querySelector('input[name="has_curatorship"]');
const curatorshipDetails = document.getElementById('curatorship-details');
const hasDisabilityCheckbox = document.querySelector('input[name="has_disability"]');
const disabilityDetails = document.getElementById('disability-details');

function toggleDisabilityDetails() {
    if (hasDisabilityCheckbox.checked) {
        disabilityDetails.style.display = 'block';
    } else {
        disabilityDetails.style.display = 'none';
    }
}

function toggleCuratorshipDetails() {
    if (hasCuratorshipCheckbox.checked) {
        curatorshipDetails.style.display = 'block';
    } else {
        curatorshipDetails.style.display = 'none';
    }
}

hasCuratorshipCheckbox.addEventListener('change', toggleCuratorshipDetails);
toggleCuratorshipDetails();  // Initial check

hasDisabilityCheckbox.addEventListener('change', toggleDisabilityDetails);
toggleDisabilityDetails();  // Initial check
