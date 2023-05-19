import * as message from "../helper/message.js";
import * as create_job_status_table from "../helper/create_job_status_table.js";

export function scheduleJob(job_id) {
  fetch(`/jobs/schedule-job/${job_id}`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
  })
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
      message.showSuccess(data.message);
      create_job_status_table.createTablesForStatuses();
    })
    .catch((error) => {
      message.showError(error);
    });
}
