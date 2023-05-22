import * as message from "../helper/message.js";
import * as create_job_status_table from "../helper/create_job_status_table.js";

export function retryJob(job_id) {
  // Send a request to retry the job
  fetch(`/jobs/schedule-job/${job_id}`, { method: "POST" })
    .then((response) => {
      if (response.ok) {
        return response.json();
      } else {
        return response.json().then((data) => {
          throw new Error(data.detail);
        });
      }
    })
    .then((data) => {
      message.showSuccess(data.detail);
      create_job_status_table.createTablesForStatuses();
    })
    .catch((error) => {
      message.showError(error);
    });
}
