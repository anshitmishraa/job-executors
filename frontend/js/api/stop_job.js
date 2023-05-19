import * as message from "../helper/message.js";

export default function stopJob(job_id) {
  // Send a request to cancel the job
  fetch(`/jobs/stop-job/${job_id}`, { method: "POST" })
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
    })
    .catch((error) => {
      message.showError(error);
    });
}
