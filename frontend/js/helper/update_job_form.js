import * as execution_type_api from "../api/execution_types.js";
import * as date_time_utils from "../helper/date_time_utils.js";
import * as job_type_api from "../api/job_types.js";
import * as event_mapping_api from "../api/event_mapping.js";
import * as update_job_api from "../api/update_job.js";
import * as update_job_type_api from "../api/update_job_type.js";

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
  event.preventDefault();

  const id = document.getElementById("updateJobId").value;
  const job_scheduler_id = document.getElementById(
    "updateJobSchedulerId"
  ).value;
  const status = document.getElementById("updateJobStatus").value;

  const name = document.getElementById("updateJobName").value;
  const job_type_id = document.getElementById("updateJobExecutionName").value;
  const execution_type_id = document.getElementById(
    "updateExecutionTypeId"
  ).value;
  const event_mapping_id = document.getElementById("updateEventMapping").value;
  const execution_time = date_time_utils.convertCurrentTimeToUTC(
    document.getElementById("updateExecutionTime").value
  );
  const recurring = document.getElementById("updateRecurring").checked;
  const priority = document.getElementById("updatePriority").value;
  const job_type_value = document.getElementById("updateJobType").value;
  const script = document.getElementById("updateJobScript").value;
  const updateExecutionTypeField = document.getElementById(
    "updateExecutionType"
  );

  const event_based_job = {
    id,
    name,
    execution_type_id,
    event_mapping_id,
    priority,
  };

  const time_based_job = {
    id,
    name,
    job_type_id,
    execution_type_id,
    execution_time,
    recurring,
    priority,
    job_scheduler_id,
    status,
  };

  const job_type = {
    name,
    job_type: job_type_value,
    script,
  };

  if (
    job_type_value == "SCRIPT" &&
    updateExecutionTypeField == "TIME_SPECIFIC"
  ) {
    update_job_type_api.updateJobType(job_type, time_based_job);
  } else {
    if (execution_type_id == 2) {
      update_job_api.updateJob(event_based_job);
    } else {
      update_job_api.updateJob(time_based_job);
    }
  }
});

export async function showEditForm(job) {
  // Get the form fields

  // Populate the form fields with job data
  const updateJobNameField = document.getElementById("updateJobName");
  updateJobNameField.value = job.name;

  const updateJobIdField = document.getElementById("updateJobId");
  updateJobIdField.value = job.id;

  const updateJobTypeIdField = document.getElementById("updateJobTypeId");
  updateJobTypeIdField.value = job.job_type_id;

  const updateJobSchedulerIdField = document.getElementById(
    "updateJobSchedulerId"
  );
  updateJobSchedulerIdField.value = job.job_scheduler_id;

  const updateJobStatusField = document.getElementById("updateJobStatus");
  updateJobStatusField.value = job.status;

  const updateExecutionTypeField = document.getElementById(
    "updateExecutionType"
  );
  const updateExecutionTypeIdField = document.getElementById(
    "updateExecutionTypeId"
  );
  const executionType = await execution_type_api.executionTypefromId(
    job.execution_type_id
  );
  updateExecutionTypeField.value = executionType.name;
  updateExecutionTypeIdField.value = executionType.id;

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
      updateJobExecutionNameElement.style.display = "none";
      updateEventMappingElement.style.display = "none";
    }
  } else if (executionType.name == "EVENT_BASED") {
    const eventMapping = await event_mapping_api.eventMappingfromId(
      job.event_mapping_id
    );
    event_mapping_api.updateEventMapping(eventMapping.name);
    updateEventMappingField.value = eventMapping.name;
    updateEventMappingElement.style.display = "block";
    updateJobExecutionNameElement.style.display = "none";
    updateJobExecutionTimeElement.style.display = "none";
    updateJobRecurringElement.style.display = "none";
    updateJobTypeElement.style.display = "none";
    updateJobScriptFieldElement.style.display = "none";
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
