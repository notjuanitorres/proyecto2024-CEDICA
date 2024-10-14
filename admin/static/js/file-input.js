const fileInputs = document.querySelectorAll(".file-input");

// Attach event listener to each file input
fileInputs.forEach(fileInput => {
  fileInput.onchange = () => {
    const fileNameElement = fileInput.closest(".file").querySelector(".file-name");
    
    if (fileInput.files.length > 0) {
      // Check if input is for multiple files or a single file
      if (fileInput.hasAttribute("multiple")) {
        // Handle multiple files: display all file names, joined by commas
        const fileNames = Array.from(fileInput.files).map(file => file.name).join(", ");
        fileNameElement.textContent = fileNames;
      } else {
        // Handle single file: display just the name of the first file
        fileNameElement.textContent = fileInput.files[0].name;
      }
    } else {
      // No files selected: reset text
      fileNameElement.textContent = "No files selected";
    }
  };
});
