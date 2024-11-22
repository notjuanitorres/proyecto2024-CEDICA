function previewImage(event) {
  const reader = new FileReader();
  reader.onload = function() {
      const output = document.getElementById('profile-image');
      output.src = reader.result;
      output.style.display = 'block';
  };
  reader.readAsDataURL(event.target.files[0]);
}

function removeImage() {
  const input = document.querySelector('input[type="file"]');
  const profileImage = document.getElementById('profile-image');
  input.value = '';
  profileImage.src = '#';
  profileImage.style.display = 'none';
}