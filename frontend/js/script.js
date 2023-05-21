import * as date_time_utils from "./helper/date_time_utils.js";
import * as job_type_api from "./api/job_types.js";
import * as execution_type_api from "./api/execution_types.js";
import * as event_mapping_api from "./api/event_mapping.js";
import * as create_job_type_api from "./api/create_job_type.js";
import * as create_job_api from "./api/create_job.js";

import * as create_job_status_table from "./helper/create_job_status_table.js";

const jobTypeSelect = document.getElementById("jobType");
const executionTypeSelect = document.getElementById("executionType");

const eventMapping = document.getElementById("event-mapping");
const jobTypeElement = document.getElementById("job-type");
const executionTimeElement = document.getElementById("job-execution-time");

const jobExecutionNameElement = document.getElementById("job-execution-name");
const jobScript = document.getElementById("job-script");
const executionTimeInput = document.getElementById("executionTime");

const jobRecurringElement = document.getElementById("job-recurring");

jobTypeSelect.addEventListener("change", function () {
  const value = this.value;
  if (value != "Code") {
    jobExecutionNameElement.style.display = "none";
    jobScript.style.display = "block";
  } else {
    jobExecutionNameElement.style.display = "block";
    jobScript.style.display = "none";
  }
});

executionTypeSelect.addEventListener("change", function () {
  const value = this.value;

  if (value == 2) {
    eventMapping.style.display = "block";
    jobTypeElement.style.display = "none";
    jobExecutionNameElement.style.display = "none";
    executionTimeElement.style.display = "none";
    jobScript.style.display = "none";
    jobRecurringElement.style.display = "none";
  } else {
    eventMapping.style.display = "none";
    jobTypeElement.style.display = "block";
    jobExecutionNameElement.style.display = "block";
    executionTimeElement.style.display = "block";
    jobRecurringElement.style.display = "block";
  }
});

document.addEventListener("DOMContentLoaded", function () {
  job_type_api.createJobTypes();
  execution_type_api.createExecutionTypes();
  event_mapping_api.eventMapping();

  create_job_status_table.createTablesForStatuses();

  const currentDateTime = date_time_utils.getCurrentDateTime();
  executionTimeInput.min = currentDateTime;
  executionTimeInput.value = currentDateTime;

  const jobCreationForm = document.getElementById("jobCreationForm");

  // Function to handle job creation
  jobCreationForm.addEventListener("submit", async function (event) {
    event.preventDefault();

    const name = document.getElementById("jobName").value;
    const job_type_id = document.getElementById("jobExecutionName").value;
    const execution_type_id = document.getElementById("executionType").value;
    const event_mapping_id = document.getElementById("eventMapping").value;
    const execution_time = date_time_utils.convertCurrentTimeToUTC(
      document.getElementById("executionTime").value
    );
    const recurring = document.getElementById("recurring").checked;
    const priority = document.getElementById("priority").value;
    const job_type_value = document.getElementById("jobType").value;
    const script = document.getElementById("jobScript").value;

    const event_based_job = {
      name,
      execution_type_id,
      event_mapping_id,
      priority,
    };

    const time_based_job = {
      name,
      job_type_id,
      execution_type_id,
      execution_time,
      recurring,
      priority,
    };

    const job_type = {
      name,
      job_type: job_type_value,
      script,
    };

    if (job_type_value == "SCRIPT") {
      create_job_type_api.createJobType(job_type, time_based_job);
    } else {
      if (execution_type_id == 2) {
        create_job_api.createJob(event_based_job);
      } else {
        create_job_api.createJob(time_based_job);
      }
    }
  });
});
