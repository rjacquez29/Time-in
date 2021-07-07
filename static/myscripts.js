// Timesheet ---------------------------

function sendmonth() {
  document.getElementById("month").submit();
}

function diff(start, end) {
  start = start.split(":");
  end = end.split(":");
  var startDate = new Date(0, 0, 0, start[0], start[1], 0);
  var endDate = new Date(0, 0, 0, end[0], end[1], 0);
  var diff = endDate.getTime() - startDate.getTime();
  var hours = Math.floor(diff / 1000 / 60 / 60);
  diff -= hours * 1000 * 60 * 60;
  var minutes = Math.floor(diff / 1000 / 60);

  // If using time pickers with 24 hours format, add the below line get exact hours
  if (hours < 0) hours = hours + 24;

  return (
    (hours <= 9 ? "0" : "") + hours + ":" + (minutes <= 9 ? "0" : "") + minutes
  );
}

function reformat(date) {
  x = date.split("/");
  return x[2] + "-" + x[1] + "-" + x[0];
}

function dataPass(id, from, to, reason, timestamp) {
  document.getElementById("edit_id").value = id;
  document.getElementById("edit_start").value = reformat(from);
  document.getElementById("edit_end").value = reformat(to);
  document.getElementById("edit_reason").value = reason;
}

function idPass(id) {
  document.getElementById("recId").value = id;
}
// end Timesheet ---------
