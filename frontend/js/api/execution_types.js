import * as string_utils from "../helper/string_utils.js";

export async function executionTypes() {
  // Fetch the execution types from the backend
  try {
    const response = await fetch(`/execution_types`);
    const data = await response.json();
    return data;
  } catch (error) {
    message.showError(error);
    return null;
  }
}

// Fetch the execution type from id from the backend
export async function executionTypefromId(executionTypeId) {
  try {
    const response = await fetch(`/execution_types/${executionTypeId}`);
    const data = await response.json();
    return data;
  } catch (error) {
    message.showError(error);
    return null;
  }
}
export async function createExecutionTypes() {
  const fetchAllExecutionTypes = await executionTypes();

  const executionTypeSelect = document.getElementById("executionType");

  // Iterate over the execution types and create <option> elements
  fetchAllExecutionTypes.forEach((executionType) => {
    const option = document.createElement("option");
    option.value = executionType.id; // Set the value to the execution type ID
    option.textContent = string_utils.parseExecutionType(executionType.name); // Set the text to the execution type name
    executionTypeSelect.appendChild(option);
  });
}
