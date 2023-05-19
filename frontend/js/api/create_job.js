import * as message from "../helper/message.js";
import * as schedule_job_api from "./schedule_job.js";

export function createJob(job) {
  fetch(`/jobs`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(job),
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
      schedule_job_api.scheduleJob(data.id);
    })
    .catch((error) => {
      message.showError(error);
    });
}
