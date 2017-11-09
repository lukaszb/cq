Release 0.11
============

- Fixed `Storage.gen_replay_events` (it was not yielding events)

Release 0.10
============

- Added ability to validate events
- Added `Storage.gen_replay_events` so user can i.e. follow progress of
  events being replayed


Release 0.9
===========

- Added ability to replay events (use `Storage.replay_events()` function)
- Added ability to upcast events
- `Storage.get_events` now accepts both `aggregate_type` and `aggregate_id`
- Renamed `cq.handlers.publish` to `cq.handlers.handle_event`
- Repositories can now be declared using `repos` dictionary at the `BaseApp` subclasses
- Implemented `Storage.iter_all_events` method
