export const convertCurrentTimeToUTC = (time) => {
  const newTime = new Date(time).getTime() - 5 * 60 * 60;
  return new Date(newTime).toISOString();
};

export const convertCurrentTimeUTCToIST = (time) => {
  time = time + "Z";

  let utcDate = new Date(time);
  let istOffset = 5.5 * 60 * 60 * 1000; // IST offset is 5 hours 30 minutes ahead of UTC
  let istDate = new Date(utcDate.getTime() + istOffset);

  let formattedDateString = istDate.toISOString();
  
  return formattedDateString;
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
  timeString = timeString + "Z";
  const date = new Date(timeString);
  const istDate = date.toLocaleString("en-IN", {
    timeZone: "Asia/Kolkata",
    month: "long",
    day: "numeric",
    year: "numeric",
    hour: "numeric",
    minute: "numeric",
    second: "numeric",
  });
  return istDate;
}
