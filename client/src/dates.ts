const minute = 60,
  hour = minute * 60,
  day = hour * 24,
  week = day * 7;

export function friendlyDate(date: Date): string {
  const delta = (new Date().getTime() - date.getTime()) / 1000;
  let res = null;
  if (delta < minute) {
    res = 'just now';
  } else if (delta < 2 * minute) {
    res = 'a minute ago';
  } else if (delta < hour) {
    res = Math.floor(delta / minute) + ' minutes ago';
  } else if (delta < 2 * hour) {
    res = 'an hour ago';
  } else if (delta < day) {
    res = Math.floor(delta / hour) + ' hours ago';
  } else if (delta < day * 2) {
    res = 'yesterday';
  } else if (delta < week) {
    res = Math.ceil(delta / day) + ' days ago';
  } else {
    res = date.toDateString();
  }
  return res;
}
