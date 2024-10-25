function setupFamilyForm() {
    // General 
    const hasFamilyAssignmentCheckbox = document.querySelector('input[name="has_family_assignment"]');
    const familyAssignmentDetails = document.getElementById('family-assignment-details');
    const hasPensionCheckbox = document.querySelector('input[name="has_pension"]');
    const pensionDetails = document.getElementById('pension-details');
    // Family Members
    const addFamilyMemberButton = document.getElementById('add-family-member');
    const removeFamilyMemberButton = document.getElementById('remove-family-member');
    const familyMemberContainer = document.getElementById('family-member-container');
    const secondFamilyMember = document.querySelector('.family-member[data-id="2"]');
    const is_optional = document.querySelector('#family_members-1-is_optional')

    function toggleFamilyAssignmentDetails() {
        if (hasFamilyAssignmentCheckbox.checked) {
            familyAssignmentDetails.style.display = 'block';
        } else {
            familyAssignmentDetails.style.display = 'none';
        }
    }

    function togglePensionDetails() {
        if (hasPensionCheckbox.checked) {
            pensionDetails.style.display = 'block';
        } else {
            pensionDetails.style.display = 'none';
        }
    }

    function updateRequiredFields() {
        const fields = secondFamilyMember.querySelectorAll('.family-input');
        const isVisible = secondFamilyMember.dataset.visible === 'true';
        if (isVisible) {
            is_optional.value = "False"
            secondFamilyMember.style.display = 'block'
        }else {
            secondFamilyMember.style.display = "none"
            is_optional.value = "True"
        }
        fields.forEach(field => {
            if (isVisible) {
                field.setAttribute('required', 'required');
                field.style.display = 'block';
            } else {
                field.removeAttribute('required');
                field.style.display = 'none';
            }
        });
    }
    if (addFamilyMemberButton) {
        addFamilyMemberButton.addEventListener('click', function () {
            secondFamilyMember.dataset.visible = true
            addFamilyMemberButton.style.display = 'none';
            removeFamilyMemberButton.style.display = 'block'
            secondFamilyMember.style.display = "block"
            updateRequiredFields(secondFamilyMember)
        });
    }

    if (removeFamilyMemberButton) {
        removeFamilyMemberButton.addEventListener('click', function (event) {
            const familyMember = event.target.closest('.family-member');
            if (familyMember) {
                addFamilyMemberButton.style.display = 'block';
                secondFamilyMember.dataset.visible = false
                updateRequiredFields(familyMember)
            }
        });
    }

    familyMemberContainer.addEventListener('click', function (event) {
        if (event.target.classList.contains('remove-family-member')) {
            const familyMember = event.target.closest('.family-member');
            if (familyMember) {
                familyMember.style.display = 'none';
                familyMember.querySelectorAll('input, select').forEach(input => {
                    input.value = '';
                    input.required = false;
                });
            }
        }
    });
    hasPensionCheckbox.addEventListener('change', togglePensionDetails);
    hasFamilyAssignmentCheckbox.addEventListener('change', toggleFamilyAssignmentDetails);
    
    updateRequiredFields()
    toggleFamilyAssignmentDetails();
    togglePensionDetails();
}

document.addEventListener("DOMContentLoaded", () => {
    const $familyForm = document.getElementById("family-form")

    if (!$familyForm) {
        return
    }
    
    setupFamilyForm()
});