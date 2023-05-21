import * as message from "../helper/message.js";

// Fetch the execution type from id from the backend
export async function executionTypefromId (executionTypeId) {
    try {
        const response = await fetch(`/execution_types/${executionTypeId}`)
        const data = await response.json();
        return data;
      } catch (error) {
        message.showError(error);
        return null;
      }
  }