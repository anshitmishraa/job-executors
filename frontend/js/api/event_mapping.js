import * as string_utils from "../helper/string_utils.js";

// Fetch the event mapping from the backend
export function eventMapping() {
  fetch("/event_mappings")
    .then((response) => response.json())
    .then((data) => {
      const eventMappingSelect = document.getElementById("eventMapping");

      // Iterate over the execution types and create <option> elements
      data.forEach((eventMapping) => {
        const option = document.createElement("option");
        option.value = eventMapping.id; // Set the value to the execution type ID
        option.textContent = string_utils.parseExecutionType(eventMapping.name); // Set the text to the execution type name
        eventMappingSelect.appendChild(option);
      });
    });
}

// Fetch the event mapping from id from the backend
export async function eventMappingfromId (eventMappingId) {
  try {
      const response = await fetch(`/event_mappings/${eventMappingId}`)
      const data = await response.json();
      return data;
    } catch (error) {
      message.showError(error);
      return null;
    }
}
