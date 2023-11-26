# microblog

IMP notes:
Moment for common time conversion so that serve times remains in UTC and UI gives to local time to the user.
The Moment class can handle this. we instantiate this using Moment(app)

TO DO: 
**Examples:**
1. moment('2021-06-28T21:45:23Z').format('L')
- "06/28/2021"
1. moment('2021-06-28T21:45:23Z').format('LL')
- "June 28, 2021"
1. moment('2021-06-28T21:45:23Z').format('LLL')
- "June 28, 2021 2:45 PM"
1. moment('2021-06-28T21:45:23Z').format('LLLL')
- "Monday, June 28, 2021 2:45 PM"
1. moment('2021-06-28T21:45:23Z').format('dddd')
- "Monday"
1. moment('2021-06-28T21:45:23Z').fromNow()
- "7 hours ago"
1. moment('2021-06-28T21:45:23Z').calendar()
- "Today at 2:45 PM"

