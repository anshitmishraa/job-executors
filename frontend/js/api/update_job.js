import * as message from "../helper/message.js";
import * as update_schedule_job_api from "./update_schedule_job.js";

export function updateJob(job) {
  fetch(`/jobs/${job.id}`, {
    method: "PUT",
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
      console.log(data);
      update_schedule_job_api.updateScheduleJob(data.id);
    })
    .catch((error) => {
      message.showError(error);
    });
}
