// Get the edit button and form elements
const editFormPopup = document.getElementById("editFormPopup");
const updateButton = document.getElementById("updateButton");
const cancelButton = document.getElementById("cancelButton");
import * as execution_type_api from "../api/execution_types.js";

// Add event listener to the cancel button
cancelButton.addEventListener("click", () => {
  // Hide the edit form popup
  editFormPopup.classList.add("hidden");
});

// Add event listener to the update button (submitting the form)
updateButton.addEventListener("click", () => {
  // Perform the update operation
  // ...

  // Hide the edit form popup
  editFormPopup.classList.add("hidden");
});

export function showEditForm(job) {
  console.log(job);
  // Get the form fields
  const jobNameField = document.getElementById("updateJobName");
  const executionTypeField = document.getElementById("updateExecutionType");
  // Populate the form fields with job data
  jobNameField.value = job.name;
  executionTypeField.value = execution_type_api.executionTypefromId(
    job.execution_type_id
  ).name;

  // Show the edit form popup
  editFormPopup.classList.remove("hidden");
}
