export const convertCurrentTimeToUTC = (time) => {
  const newTime = new Date(time).getTime() - 5 * 60 * 60;
  return new Date(newTime).toISOString();
};

export const getCurrentDateTime = function () {
  const now = new Date();
  const year = now.getFullYear();
  const month = String(now.getMonth() + 1).padStart(2, "0");
  const day = String(now.getDate()).padStart(2, "0");
  const hours = String(now.getHours()).padStart(2, "0");
  const minutes = String(now.getMinutes()).padStart(2, "0");
  return `${year}-${month}-${day}T${hours}:${minutes}`;
};

export function parseDateTime(timeString) {
  const dateTime = new Date(timeString);

  const options = {
    year: "numeric",
    month: "long",
    day: "numeric",
    hour: "numeric",
    minute: "numeric",
    second: "numeric",
    timeZone: "Asia/Kolkata", // Set the time zone to IST
  };
  const formattedTime = dateTime.toLocaleString(undefined, options); // Example output: "May 16, 2023, 5:41:12 PM"

  return formattedTime;
}
