export function parseExecutionType(str) {
  return toCapitalizedCase(str.replace(/_/g, " "));
}

export function toCapitalizedCase(str) {
  return str.toLowerCase().replace(/(?:^|\s)\w/g, function (match) {
    return match.toUpperCase();
  });
}
