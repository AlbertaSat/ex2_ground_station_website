export function formatDateToUTCString(dateObj) {
    let year = dateObj.getUTCFullYear().toString();
    let month = (dateObj.getUTCMonth() + 1).toString();
    let date = dateObj.getUTCDate().toString();
    let hours = dateObj.getUTCHours().toString();
    let minutes = dateObj.getUTCMinutes().toString();
    let seconds = dateObj.getUTCSeconds().toString();

    let dateArray = [year, month, date];
    let timeArray = [hours, minutes, seconds];

    let formattedDateString = dateArray.reduce((acc, cur) => acc + '-' + cur);
    let formattedTimeString = timeArray.reduce((acc, cur) => acc + ':' + ('0' + cur).slice(-2));
    return formattedDateString + ' ' + formattedTimeString + ' ' + '(UTC)';
}
