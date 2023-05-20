// Function to show the success message and automatically hide it after a delay
export const showSuccess = function (message) {
  const successContainer = document.getElementById("success-message");
  const successMessage = successContainer.querySelector(".success-message");

  successMessage.textContent = message;
  successContainer.style.display = "block";

  setTimeout(function () {
    successContainer.style.opacity = "0";
    setTimeout(function () {
      successContainer.style.display = "none";
      successContainer.style.opacity = "1";
    }, 300);
  }, 2000); // Adjust the delay (in milliseconds) as needed
};

// Function to show the error message and hide it when the close button is clicked
export function showError(message) {
  const errorContainer = document.getElementById("error-message");
  const closeButton = errorContainer.querySelector(".close-button");
  const errorMessage = errorContainer.querySelector(".error-message");

  errorMessage.textContent = message;
  errorContainer.style.display = "block";

  closeButton.addEventListener("click", function () {
    errorContainer.style.opacity = "0";
    setTimeout(function () {
      errorContainer.style.display = "none";
      errorContainer.style.opacity = "1";
    }, 300);
  });
}
