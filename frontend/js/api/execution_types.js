import * as string_utils from "../helper/string_utils.js";

export function executionTypes() {
  // Fetch the execution types from the backend
  fetch("/execution_types")
    .then((response) => response.json())
    .then((data) => {
      const executionTypeSelect = document.getElementById("executionType");

      // Iterate over the execution types and create <option> elements
      data.forEach((executionType) => {
        const option = document.createElement("option");
        option.value = executionType.id; // Set the value to the execution type ID
        option.textContent = string_utils.parseExecutionType(
          executionType.name
        ); // Set the text to the execution type name
        executionTypeSelect.appendChild(option);
      });
    });
}
