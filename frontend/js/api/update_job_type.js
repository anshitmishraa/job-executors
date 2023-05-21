import * as message from "../helper/message.js";
import * as update_job_api from "./update_job.js";

export function updateJobType(job_type, job) {
  const job_type_id = job.job_type_id;

  fetch(`/job_types/${job_type_id}`, {
    method: "PUT",
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
      update_job_api.updateJob(job);
    })
    .catch((error) => {
      message.showError(error);
    });
}
