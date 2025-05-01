document.addEventListener("DOMContentLoaded", function () {
    const uploadInput = document.getElementById("imageUpload");
    const colorizeButton = document.getElementById("colorizeButton");
    const resultSection = document.getElementById("resultSection");
    const colorizedImage = document.getElementById("colorizedImage");
  
    // Handle file upload
    uploadInput.addEventListener("change", function (event) {
      const file = event.target.files[0];
      if (file) {
        const reader = new FileReader();
        reader.onload = function (e) {
          // Load the uploaded image into the img element for display
          const imageURL = e.target.result;
          colorizedImage.src = imageURL;
        };
        reader.readAsDataURL(file);
      }
    });
  
    // Colorize button click event
    colorizeButton.addEventListener("click", function () {
      if (!uploadInput.files[0]) {
        alert("Please upload an image first!");
        return;
      }
  
      // Simulating the colorization process (replace with actual AI API)
      setTimeout(function () {
        // In a real case, here you would call the AI model to process the image
        // For now, we'll just mock this by showing the same image
        resultSection.style.display = "block"; // Show the result section
        colorizedImage.style.opacity = 1; // Simulate a successful process
      }, 1000); // Simulate a 1-second processing delay
    });
  });