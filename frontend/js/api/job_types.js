import * as string_utils from "../helper/string_utils.js";
import * as constant from "../helper/constant.js";

export async function jobTypes() {
  // Fetch the event mapping from the backend
  try {
    const response = await fetch(`/job_types`);
    const data = await response.json();
    return data;
  } catch (error) {
    message.showError(error);
    return null;
  }
}

export async function createJobTypes() {
  const fetchAllJobTypes = await jobTypes();

  const jobTypeSelect = document.getElementById("jobType");
  const jobExecutionNameSelect = document.getElementById("jobExecutionName");

  // Iterate over the job types and create <option> elements
  constant.jobType.forEach((jobType) => {
    const option = document.createElement("option");
    option.textContent = string_utils.parseExecutionType(jobType); // Set the text to the job type name
    option.value = jobType;
    jobTypeSelect.appendChild(option);
  });

  // Iterate over the execution types and create <option> elements
  fetchAllJobTypes.forEach((jobExecutionName) => {
    if (jobExecutionName.job_type === "CODE") {
      const option = document.createElement("option");
      option.value = jobExecutionName.id;
      option.textContent = string_utils.parseExecutionType(
        jobExecutionName.name
      ); // Set the text to the execution type name
      jobExecutionNameSelect.appendChild(option);
    }
  });
}

// Fetch the job type from id from the backend
export async function jobTypefromId(jobTypeId) {
  try {
    const response = await fetch(`/job_types/${jobTypeId}`);
    const data = await response.json();
    return data;
  } catch (error) {
    message.showError(error);
    return null;
  }
}

export async function updateJobTypes(existingjobType) {
  const fetchAllJobTypes = await jobTypes();

  const updateJobExecutionNameSelect = document.getElementById(
    "updateJobExecutionName"
  );

  // Iterate over the job types and create <option> elements
  fetchAllJobTypes.forEach((jobType) => {
    if (jobType.job_type == "CODE") {
      const option = document.createElement("option");
      option.value = jobType.id; // Set the value to the job type ID
      option.textContent = string_utils.parseExecutionType(jobType.name); // Set the text to the job type name
      if (jobType.name == existingjobType) {
        option.selected = true;
      }
      updateJobExecutionNameSelect.appendChild(option);
    }
  });
}
