import * as status_api from "../api/status.js";
import * as retry_job_api from "../api/retry_job.js";
import * as stop_job_api from "../api/stop_job.js";
import * as constant from "../helper/constant.js";
import * as date_time_utils from "../helper/date_time_utils.js";
import * as update_job_form from "./update_job_form.js";
import * as execution_type_api from "../api/execution_types.js";
import { showError } from "./message.js";

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
    // Create a shimmer effect for the loading state
    const shimmerTable = document.createElement("table");
    shimmerTable.className =
      "mt-4 w-full bg-white border border-gray-300 rounded animate-pulse";

    const shimmerTbody = document.createElement("tbody");
    shimmerTbody.className = "divide-y divide-gray-600";

    // Create a shimmer row
    const shimmerRow = document.createElement("tr");
    shimmerRow.className = "bg-gray-400 animate-pulse";

    const shimmerColumn = document.createElement("td");
    shimmerColumn.className = "py-32 px-32 border-b";
    shimmerRow.appendChild(shimmerColumn);

    // Add the shimmer row to the shimmer table body
    shimmerTbody.appendChild(shimmerRow);

    // Add the shimmer table body to the shimmer table
    shimmerTable.appendChild(shimmerTbody);

    // Add the shimmer table to the tables container
    tablesContainer.appendChild(shimmerTable);

    const executionTypes = await execution_type_api.executionTypes();

    // Fetch data for each status in parallel
    const fetchPromises = statuses.map((status) =>
      fetch(`/jobs?status=${status}`).then((response) => response.json())
    );

    Promise.all(fetchPromises)
      .then((dataList) => {
        // Remove the shimmer table once the actual data is fetched
        shimmerTable.remove();

        // Create a table for each status using the fetched job data
        dataList.forEach((data, index) => {
          const status = statuses[index];

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

          const jobExecutionTypeHeader = document.createElement("th");
          jobExecutionTypeHeader.className =
            "py-2 px-4 border-b bg-gray-100 text-left";
          jobExecutionTypeHeader.textContent = "Job Execution Type";

          const jobTimeHeader = document.createElement("th");
          jobTimeHeader.className = "py-2 px-4 border-b bg-gray-100 text-left";

          if (status === "Failed") {
            jobTimeHeader.textContent = "Failure Time";
          } else if (status === "Completed") {
            jobTimeHeader.textContent = "Completion Time";
          } else if (status === "Scheduled") {
            jobTimeHeader.textContent = "Schedule Time";
          }

          const priorityHeader = document.createElement("th");
          priorityHeader.className = "py-2 px-4 border-b bg-gray-100 text-left";
          priorityHeader.textContent = "Priority";

          const recurringHeader = document.createElement("th");
          recurringHeader.className =
            "py-2 px-4 border-b bg-gray-100 text-left";
          recurringHeader.textContent = "Recurring";

          const statusHeader = document.createElement("th");
          statusHeader.className = "py-2 px-4 border-b bg-gray-100 text-center";
          statusHeader.textContent = "Status";

          const actionsHeader = document.createElement("th");
          actionsHeader.className = "py-2 px-4 border-b bg-gray-100 text-right";
          actionsHeader.textContent = "Actions";

          headerRow.appendChild(jobNameHeader);
          headerRow.appendChild(jobExecutionTypeHeader);

          if (
            status === "Failed" ||
            status === "Completed" ||
            status === "Scheduled"
          ) {
            headerRow.appendChild(jobTimeHeader);
          }
          headerRow.appendChild(recurringHeader);
          if (status == "Scheduled") {
            headerRow.appendChild(priorityHeader);
          }
          headerRow.appendChild(statusHeader);
          if (status != "Completed") headerRow.appendChild(actionsHeader);

          thead.appendChild(headerRow);
          table.appendChild(thead);

          const tbody = document.createElement("tbody");

          // Filter jobs based on status
          const jobs = data.filter((job) => job.status === status);

          // Iterate over the filtered jobs and create HTML elements for each job
          jobs.forEach(async (job) => {
            const listItem = document.createElement("tr");

            const jobName = document.createElement("td");
            jobName.className = "py-2 px-4 border-b text-left";
            jobName.textContent = job.name;

            const jobExecutionType = document.createElement("td");
            jobExecutionType.className = "py-2 px-4 border-b text-left";

            const executionType = executionTypes.filter(
              (executionType) => executionType.id === job.execution_type_id
            )[0];

            if (executionType.name == "TIME_SPECIFIC") {
              const timeSpecificJobExecutionType =
                document.createElement("span");
              timeSpecificJobExecutionType.className =
                "px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-green-100 text-green-800";
              timeSpecificJobExecutionType.textContent = "Time Specific";

              jobExecutionType.append(timeSpecificJobExecutionType);
            } else if (executionType.name == "EVENT_BASED") {
              const eventBasedJoBExecutionType = document.createElement("span");
              eventBasedJoBExecutionType.className =
                "px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-blue-100 text-blue-800";
              eventBasedJoBExecutionType.textContent = "Event Based";

              jobExecutionType.append(eventBasedJoBExecutionType);
            }

            const jobTime = document.createElement("td");
            jobTime.className = "py-2 px-4 border-b text-left";

            const jobPriority = document.createElement("td");
            jobPriority.className = "py-2 px-4 border-b text-left";

            const priorityTag = document.createElement("span");
            priorityTag.className =
              "inline-block bg-blue-500 text-white text-xs font-semibold px-2 rounded";

            const jobRecurring = document.createElement("td");
            jobRecurring.className = "py-2 px-4 border-b text-left";

            const recurringIndicator = document.createElement("span");
            recurringIndicator.className =
              "inline-block w-4 h-4 rounded-full mr-2";
            if (job.event_mapping_id != null) {
              recurringIndicator.textContent = "---";
            } else {
              recurringIndicator.classList.add(
                job.recurring ? "bg-green-500" : "bg-red-500"
              );
            }

            if (status === "Failed" || status === "Completed") {
              jobTime.textContent = date_time_utils.parseDateTime(
                job.updated_at
              );
            } else if (status === "Scheduled") {
              priorityTag.textContent = job.priority;

              if (job.event_mapping_id == null) {
                jobTime.textContent = date_time_utils.parseDateTime(
                  job.execution_time
                );
              } else {
                jobTime.textContent = "---";
              }
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
            editButton.onclick = function () {
              update_job_form.showEditForm(job);
            };

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
            listItem.appendChild(jobExecutionType);

            if (
              status === "Failed" ||
              status === "Completed" ||
              status === "Scheduled"
            ) {
              listItem.appendChild(jobTime);
            }

            jobRecurring.appendChild(recurringIndicator);
            listItem.appendChild(jobRecurring);

            if (status == "Scheduled") {
              jobPriority.appendChild(priorityTag);
              listItem.appendChild(jobPriority);
            }
            listItem.appendChild(jobStatus);
            if (status != "Completed") listItem.appendChild(actionsColumn);

            tbody.appendChild(listItem);
          });

          table.appendChild(tbody);
          tablesContainer.appendChild(subTableHeading);
          tablesContainer.appendChild(table);
        });
      })
      .catch((error) => {
        showError(error);
        shimmerTable.remove();
      });
  }
}
