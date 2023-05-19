// Fetch the distinct statuses from the backend
import * as message from "../helper/message.js";

export async function getDistinctStatus() {
  try {
    const response = await fetch("/jobs/status");
    const data = await response.json();
    return data;
  } catch (error) {
    message.showError(error);
    return [];
  }
}
