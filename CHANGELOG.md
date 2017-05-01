Release 0.9
===========

- Added ability to replay events (use `Storage.replay_events()` function)
- Added ability to upcast events
- `Storage.get_events` now accepts both `aggregate_type` and `aggregate_id`
- Renamed `cq.handlers.publish` to `cq.handlers.handle_event`
- Repositories can now be declared using `repos` dictionary at the `BaseApp` subclasses
- Implemented `Storage.iter_all_events` method
