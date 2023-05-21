import * as string_utils from "../helper/string_utils.js";
import * as constant from "../helper/constant.js";

export function jobTypes() {
  // Fetch the event mapping from the backend
  fetch("/job_types")
    .then((response) => response.json())
    .then((data) => {
      const jobTypeSelect = document.getElementById("jobType");
      const jobExecutionNameSelect =
        document.getElementById("jobExecutionName");

      // Iterate over the execution types and create <option> elements
      constant.jobType.forEach((jobExecutionType) => {
        const option = document.createElement("option");
        option.textContent = string_utils.parseExecutionType(jobExecutionType); // Set the text to the execution type name
        option.value = jobExecutionType;
        jobTypeSelect.appendChild(option);
      });

      // Iterate over the execution types and create <option> elements
      data.forEach((jobExecutionName) => {
        if (jobExecutionName.job_type === "CODE") {
          const option = document.createElement("option");
          option.value = jobExecutionName.id;
          option.textContent = string_utils.parseExecutionType(
            jobExecutionName.name
          ); // Set the text to the execution type name
          jobExecutionNameSelect.appendChild(option);
        }
      });
    });
}

// Fetch the job type from id from the backend
export async function jobTypefromId (jobTypeId) {
  try {
      const response = await fetch(`/job_types/${jobTypeId}`)
      const data = await response.json();
      return data;
    } catch (error) {
      message.showError(error);
      return null;
    }
}
