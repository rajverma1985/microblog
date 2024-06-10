# microblog

IMP notes:
Moment for common time conversion so that serve times remains in UTC and UI gives to local time to the user.
The Moment class can handle this. we instantiate this using Moment(app)

**TO DO:**
- [ ] Babel not working \< I18n and L10n \>
- [ ] Ajax support for language translation
- [ ]

**Examples:**
- [x] `moment('2021-06-28T21:45:23Z').format('L')`
   - "06/28/2021"
- [x] `moment('2021-06-28T21:45:23Z').format('LL')`
   - "June 28, 2021"
- [x] `moment('2021-06-28T21:45:23Z').format('LLL')`
   - "June 28, 2021 2:45 PM"
- [x] `moment('2021-06-28T21:45:23Z').format('LLLL')`
   - "Monday, June 28, 2021 2:45 PM"
- [x] `moment('2021-06-28T21:45:23Z').format('dddd')`
   - "Monday"
- [x] `moment('2021-06-28T21:45:23Z').fromNow()`
   - "7 hours ago"
- [x] `moment('2021-06-28T21:45:23Z').calendar()`
   - "Today at 2:45 PM"


