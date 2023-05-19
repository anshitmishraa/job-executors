import * as message from "../helper/message.js";
import * as create_job_api from "./create_job.js";

export function createJobType(job_type, job) {
  fetch(`/job_types`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(job_type),
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
      job.job_type_id = data.id;
      create_job_api.createJob(job);
    })
    .catch((error) => {
      message.showError(error);
    });
}
