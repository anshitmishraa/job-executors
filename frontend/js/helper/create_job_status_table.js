import * as status_api from "../api/status.js";
import * as retry_job_api from "../api/retry_job.js";
import * as stop_job_api from "../api/stop_job.js";
import * as constant from "../helper/constant.js";
import * as date_time_utils from "../helper/date_time_utils.js";

// Fetch the job list from the backend
export async function createTablesForStatuses() {
  const statuses = await status_api.getDistinctStatus();
  const tablesContainer = document.getElementById("tablesContainer");

  while (tablesContainer.firstChild) {
    tablesContainer.removeChild(tablesContainer.firstChild);
  }

  if (statuses.length === 0) {
    const emptyJobsContainer = document.createElement("div");
    emptyJobsContainer.className = "bg-white-100 p-4 text-center";

    const emptyJobsElement = document.createElement("p");
    emptyJobsElement.className = "text-gray-600 text-lg";
    emptyJobsElement.textContent = "No Jobs has been schehuled yet";

    emptyJobsContainer.append(emptyJobsElement);
    tablesContainer.append(emptyJobsContainer);
  } else {
    fetch("/jobs")
      .then((response) => response.json())
      .then((data) => {
        // Create a table for each status
        statuses.forEach((status) => {
          const subTableHeading = document.createElement("h4");
          subTableHeading.className = "text-2xl font-semibold py-4 text-center";
          subTableHeading.textContent = status + " - Job List";

          const table = document.createElement("table");
          table.className =
            "mt-4 w-full bg-white border border-gray-300 rounded";
          table.style = "border-collapse: collapse;";

          const thead = document.createElement("thead");
          const headerRow = document.createElement("tr");

          const jobNameHeader = document.createElement("th");
          jobNameHeader.className = "py-2 px-4 border-b bg-gray-100 text-left";
          jobNameHeader.textContent = "Job Name";

          const jobTimeHeader = document.createElement("th");
          jobTimeHeader.className = "py-2 px-4 border-b bg-gray-100 text-left";

          if (status === "Failed") {
            jobTimeHeader.textContent = "Failure Time";
          } else if (status === "Completed") {
            jobTimeHeader.textContent = "Completion Time";
          } else if (status === "Scheduled") {
            jobTimeHeader.textContent = "Schedule Time";
          }

          const statusHeader = document.createElement("th");
          statusHeader.className = "py-2 px-4 border-b bg-gray-100 text-center";
          statusHeader.textContent = "Status";

          const actionsHeader = document.createElement("th");
          actionsHeader.className = "py-2 px-4 border-b bg-gray-100 text-right";
          actionsHeader.textContent = "Actions";

          headerRow.appendChild(jobNameHeader);
          if (
            status === "Failed" ||
            status === "Completed" ||
            status === "Scheduled"
          ) {
            headerRow.appendChild(jobTimeHeader);
          }
          headerRow.appendChild(statusHeader);
          if (status != "Completed") headerRow.appendChild(actionsHeader);
          thead.appendChild(headerRow);
          table.appendChild(thead);

          const tbody = document.createElement("tbody");

          // Filter jobs based on status
          const jobs = data.filter((job) => job.status === status);

          // Iterate over the filtered jobs and create HTML elements for each job
          jobs.forEach((job) => {
            const listItem = document.createElement("tr");

            const jobName = document.createElement("td");
            jobName.className = "py-2 px-4 border-b text-left";
            jobName.textContent = job.name;

            const jobTime = document.createElement("td");
            jobTime.className = "py-2 px-4 border-b text-left";

            if (status === "Failed" || status === "Completed") {
              jobTime.textContent = date_time_utils.parseDateTime(
                job.updated_at
              );
            } else if (status === "Scheduled") {
              jobTime.textContent = date_time_utils.parseDateTime(
                job.execution_time
              );
            }

            const jobStatus = document.createElement("td");
            jobStatus.className = "py-2 px-4 border-b text-center";
            jobStatus.textContent = job.status;

            const retryButton = document.createElement("button");
            retryButton.className =
              "retryButton bg-red-500 text-white py-1 px-2 rounded mr-4";
            retryButton.textContent = "Retry";
            retryButton.onclick = function () {
              retry_job_api.retryJob(job.id);
            };
            const stopButton = document.createElement("button");
            stopButton.className =
              "stopButton bg-red-500 text-white py-1 px-2 rounded mr-4";
            stopButton.textContent = "Stop";
            stopButton.onclick = function () {
              stop_job_api.stopJob(job.id);
            };

            const editButton = document.createElement("button");
            editButton.className =
              "editButton bg-blue-500 text-white py-1 px-2 rounded mr-4";
            editButton.textContent = "Edit";

            const actionsColumn = document.createElement("td");
            actionsColumn.className = "py-2 px-4 border-b text-right";

            if (constant.isRetryButtonShown.includes(status)) {
              actionsColumn.appendChild(retryButton);
            }
            if (constant.isEditButtonShown.includes(status)) {
              actionsColumn.appendChild(editButton);
            }
            if (constant.isStopButtonShown.includes(status)) {
              actionsColumn.appendChild(stopButton);
            }

            listItem.appendChild(jobName);
            if (
              status === "Failed" ||
              status === "Completed" ||
              status === "Scheduled"
            ) {
              listItem.appendChild(jobTime);
            }
            listItem.appendChild(jobStatus);
            if (status != "Completed") listItem.appendChild(actionsColumn);

            tbody.appendChild(listItem);
          });

          table.appendChild(tbody);
          tablesContainer.appendChild(subTableHeading);
          tablesContainer.appendChild(table);
        });
      });
  }
}
