import * as execution_type_api from "../api/execution_types.js";
import * as date_time_utils from "../helper/date_time_utils.js";
import * as job_type_api from "../api/job_types.js";
import * as event_mapping_api from "../api/event_mapping.js";

// Get the edit button and form elements
const editFormPopup = document.getElementById("editFormPopup");
const updateButton = document.getElementById("updateButton");
const cancelButton = document.getElementById("cancelButton");

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

export async function showEditForm(job) {
  // Get the form fields

  // Populate the form fields with job data
  const updateJobNameField = document.getElementById("updateJobName");
  updateJobNameField.value = job.name;

  const updateExecutionTypeField = document.getElementById(
    "updateExecutionType"
  );
  const executionType = await execution_type_api.executionTypefromId(
    job.execution_type_id
  );
  updateExecutionTypeField.value = executionType.name;

  const updateJobTypeField = document.getElementById("updateJobType");
  const updateJobTypeElement = document.getElementById("update-job-type");

  const updateJobExecutionNameField = document.getElementById(
    "updateJobExecutionName"
  );
  const updateJobExecutionNameElement = document.getElementById(
    "update-job-execution-name"
  );
  const updateJobRecurringElement = document.getElementById(
    "update-job-recurring"
  );

  const updateJobScriptField = document.getElementById("updateJobScript");
  const updateJobScriptFieldElement =
    document.getElementById("update-job-script");

  const updateEventMappingField = document.getElementById("updateEventMapping");
  const updateEventMappingElement = document.getElementById(
    "update-event-mapping"
  );

  const updateJobExecutionTimeElement = document.getElementById(
    "update-job-execution-time"
  );

  if (executionType.name == "TIME_SPECIFIC") {
    const jobType = await job_type_api.jobTypefromId(job.job_type_id);
    updateJobTypeField.value = jobType.job_type;
    updateJobTypeElement.style.display = "block";

    if (jobType.job_type == "CODE") {
      job_type_api.updateJobTypes(jobType.name);
      updateJobExecutionNameElement.style.display = "block";
    } else if (jobType.job_type == "SCRIPT") {
      updateJobScriptField.value = jobType.script;
      updateJobScriptFieldElement.style.display = "block";
    }
  } else if (executionType.name == "EVENT_BASED") {
    const eventMapping = await event_mapping_api.eventMappingfromId(
      job.event_mapping_id
    );
    event_mapping_api.updateEventMapping(jobType.name);
    updateEventMappingField.value = eventMapping.name;
    updateEventMappingElement.style.display = "block";
    updateJobExecutionNameElement.style.display = "none";
    updateJobExecutionTimeElement.style.display = "none";
    updateJobRecurringElement.style.display = "none";
  }

  const currentDateTime = date_time_utils.getCurrentDateTime();
  const updateExecutionTimeField = document.getElementById(
    "updateExecutionTime"
  );
  updateExecutionTimeField.value = date_time_utils
    .convertCurrentTimeUTCToIST(job.execution_time)
    .slice(0, -5);
  updateExecutionTimeField.min = currentDateTime;

  const updateRecurringField = document.getElementById("updateRecurring");
  updateRecurringField.checked = job.recurring;

  const updatePriorityField = document.getElementById("updatePriority");
  updatePriorityField.value = job.priority;

  // Show the edit form popup
  editFormPopup.classList.remove("hidden");
}
