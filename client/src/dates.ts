const minute = 60,
  hour = minute * 60,
  day = hour * 24,
  week = day * 7;

export function friendlyDate(date: Date): string {
  const delta = (new Date().getTime() - date.getTime()) / 1000;
  if (delta < minute) return 'just now';
  else if (delta < 2 * minute) return 'a minute ago';
  else if (delta < hour) return Math.floor(delta / minute) + ' minutes ago';
  else if (delta < 2 * hour) return 'an hour ago';
  else if (delta < day) return Math.floor(delta / hour) + ' hours ago';
  else if (delta < day * 2) return 'yesterday';
  else if (delta < week) return Math.ceil(delta / day) + ' days ago';
  else return date.toDateString();
}

export function friendlyDuration(seconds: number): string {
  if (seconds < 1) return '';
  else if (seconds < minute) return Math.floor(seconds) + ' seconds';
  else if (seconds < 2 * minute) return '1 minute ' + friendlyDuration(seconds % minute);
  else if (seconds < hour) return Math.floor(seconds / minute) + ' minutes ' + friendlyDuration(seconds % minute);
  else if (seconds < 2 * hour) return '1 hour ' + friendlyDuration(seconds % hour);
  else if (seconds < day) return Math.floor(seconds / hour) + ' hours ' + friendlyDuration(seconds % hour);
  else if (seconds < day * 2) return '1 day ' + friendlyDuration(seconds % day);
  else return Math.floor(seconds / day) + ' days ' + friendlyDuration(seconds % day);
}
