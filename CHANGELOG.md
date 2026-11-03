# Changelog

## v0.6.1 (2026-11-03)

### Bug fixes

- Require icalendar 7.1.3 or newer ([`cca97cd`](https://github.com/mergecal/python-mergecal/commit/cca97cdf25dfa746275c5f528e5013dccc4c581c))

## v0.6.0 (2026-11-03)

### Bug fixes

- Make calendarmerger options keyword-only ([`9ba9e35`](https://github.com/mergecal/python-mergecal/commit/9ba9e3574f257a6182bc1fe4cac128bab1182394))
- Raise runtimeerror when merge() is called more than once ([`f9da634`](https://github.com/mergecal/python-mergecal/commit/f9da63434245905011d5428ced297b3e50de5777))
- Add type annotation to component_type fixture ([`a6f3189`](https://github.com/mergecal/python-mergecal/commit/a6f3189bf9b8f472b40d412e59220877d1cf85bc))
- Correct cal_color type and add cross-calendar color preservation test ([`75d9895`](https://github.com/mergecal/python-mergecal/commit/75d989578b0dfcd87c396fab9b875ed3f246736b))

### Documentation

- Document intention not implementation in component_type fixture ([`e559e1f`](https://github.com/mergecal/python-mergecal/commit/e559e1fa9bedc9e29fdf5dc13458c0c3ed20e598))
- Add list of features ([`d7647e9`](https://github.com/mergecal/python-mergecal/commit/d7647e9dff18a44ff0775f1a88e684047ccb912f))

### Features

- Use cal.journals and bump icalendar to >=7.0.2 ([`0f976bf`](https://github.com/mergecal/python-mergecal/commit/0f976bfa5715ab662941ad6e2eebe4525f13ac50))
- Merge rfc 7986 color property for calendar components ([`58fded2`](https://github.com/mergecal/python-mergecal/commit/58fded2a5a6e4dedde42d31d1c4c30976e808adb))
- Add calscale property to merged calendars for rfc 5545 compliance ([`d25e659`](https://github.com/mergecal/python-mergecal/commit/d25e659bb38139ba83b11103dc95174cc1375d2b))
- Handle multiple vcalendar components in a single ics file ([`b87b8c0`](https://github.com/mergecal/python-mergecal/commit/b87b8c0d6266b59cb3bfbc6b85e9772883fce2cc))

## v0.5.0 (2025-02-06)

### Features

- Add timezone support to output ([`bad44d6`](https://github.com/mergecal/python-mergecal/commit/bad44d698cc58d6c2dc247ae9de8dd53fa10a6e4))

## v0.4.2 (2025-02-04)

### Bug fixes

- Remove unneccerasy conversion of recurrence ids to utc ([`78b0e2e`](https://github.com/mergecal/python-mergecal/commit/78b0e2ed9f5ae15108aa61d3651945f253abc066))
- Remove unneccerasy conversion of recurrence_id ([`78b0e2e`](https://github.com/mergecal/python-mergecal/commit/78b0e2ed9f5ae15108aa61d3651945f253abc066))

## v0.4.1 (2025-01-31)

### Bug fixes

- Prevent skipping events without uids during merge ([`ca27fcb`](https://github.com/mergecal/python-mergecal/commit/ca27fcb6d23ba79a643e262adf292fe65d7be848))
- Prevent skipping events without uids during merge ([`c229666`](https://github.com/mergecal/python-mergecal/commit/c2296665a7ef85484e2ef2028411eaa2fbcc002a))

## v0.4.0 (2025-01-29)

## v0.3.14 (2025-01-19)

### Bug fixes

- Update dependency icalendar to v6.1.1 ([`9b1b2a6`](https://github.com/mergecal/python-mergecal/commit/9b1b2a6981aa3a14a17a9bb34a3a96434ead431b))

## v0.3.13 (2024-12-04)

### Bug fixes

- Update dependency typer to v0.15.1 ([`a035bc3`](https://github.com/mergecal/python-mergecal/commit/a035bc30b79a46c263a9455243cadaf0663a4096))

## v0.3.12 (2024-12-03)

### Bug fixes

- Update dependency typer to ^0.15.0 ([`aca9fed`](https://github.com/mergecal/python-mergecal/commit/aca9fed1500616dde5ee67310dbc721bf26bbb2f))

## v0.3.11 (2024-11-29)

### Bug fixes

- Update dependency typer to ^0.14.0 ([`b8173f8`](https://github.com/mergecal/python-mergecal/commit/b8173f8936274cd1091464ee3e3b004c3eada9ea))

## v0.3.10 (2024-11-23)

### Bug fixes

- Update dependency icalendar to v6.1.0 ([`e32be59`](https://github.com/mergecal/python-mergecal/commit/e32be59a430366f9c77705ad0df2f13a6ec1d81e))

## v0.3.9 (2024-11-19)

### Bug fixes

- Update dependency typer to v0.13.1 ([`209a3b2`](https://github.com/mergecal/python-mergecal/commit/209a3b26bd9c326dc72fe2162aed72e197329b71))

## v0.3.8 (2024-11-08)

### Bug fixes

- Update dependency typer to ^0.13.0 ([`58eb230`](https://github.com/mergecal/python-mergecal/commit/58eb230ccc179a36618354280efc89591fce0f14))

## v0.3.7 (2024-11-01)

### Bug fixes

- Update dependency rich to v13.9.4 ([`0b89e60`](https://github.com/mergecal/python-mergecal/commit/0b89e604fbc46159d5e23c7c7c2b0053a978b14d))

## v0.3.6 (2024-10-22)

### Bug fixes

- Update dependency rich to v13.9.3 ([`38bd903`](https://github.com/mergecal/python-mergecal/commit/38bd9035b792d6d154e949b375ad0d852921ab24))

## v0.3.5 (2024-10-13)

### Bug fixes

- Update dependency icalendar to v6.0.1 ([`619e542`](https://github.com/mergecal/python-mergecal/commit/619e542f91dfc260b85f19b07deb589df856e546))

## v0.3.4 (2024-10-06)

### Bug fixes

- Update dependency icalendar to v6 ([`3524faf`](https://github.com/mergecal/python-mergecal/commit/3524faf4eaf94cb019e5b5bb9b804e19d4349df3))

## v0.3.3 (2024-10-04)

### Bug fixes

- Update dependency rich to v13.9.2 ([`80bd3f5`](https://github.com/mergecal/python-mergecal/commit/80bd3f5fdefc7b696c90b946861c7b8a20d41c9f))

## v0.3.2 (2024-10-01)

### Bug fixes

- Update dependency rich to v13.9.1 ([`a1515db`](https://github.com/mergecal/python-mergecal/commit/a1515dbc1139b0b85cae2bd51710674db5329165))

### Features

- Skip vevent where uid, sequence and recurrence_id are the same ([`61f5d73`](https://github.com/mergecal/python-mergecal/commit/61f5d73d5be4fcee48777ec5de89db57d711e371))

## v0.3.1 (2024-09-10)

### Bug fixes

- Update dependency rich to v13.8.1 ([`44f9750`](https://github.com/mergecal/python-mergecal/commit/44f97502921dee5d62c3babcaf62c80788670479))

## v0.3.0 (2024-09-09)

### Features

- Add nicco as github sponsor ([`8b31bec`](https://github.com/mergecal/python-mergecal/commit/8b31becaaaf068d3268fafb5ce7cd1988f00e38e))

## v0.2.0 (2024-09-06)

### Bug fixes

- Changelog creation ([`05b32df`](https://github.com/mergecal/python-mergecal/commit/05b32df73344fea188feb36eb4abe6981895ccd4))
- Update dependency typer to ^0.12.0 ([`634b106`](https://github.com/mergecal/python-mergecal/commit/634b106fdbec9a3dd34cdd611825f5eb4cfe6053))

### Features

- Implement calendar merging functionality ([`1ce87e7`](https://github.com/mergecal/python-mergecal/commit/1ce87e7716f448686828d8962967d3d3b0eec0ae))

### Documentation

- Fix codedev link in readme ([`629fb86`](https://github.com/mergecal/python-mergecal/commit/629fb86b86e677294a95b7f021dd19c1018d2bb8))

## v0.1.0 (2024-09-05)

### Features

- Implement calendar merging functionality ([`989334a`](https://github.com/mergecal/python-mergecal/commit/989334afa2f5e91003a1319ada5e61c8051cddab))
- Initial project setup ([`fd12c9e`](https://github.com/mergecal/python-mergecal/commit/fd12c9ef927cdbea513f48828a1afbf30f8fe7e3))
