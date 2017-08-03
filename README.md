# CQ

[![build-status-image]][travis]

CQ is a Python microframework built on top of [Command and Query Responsibility Segregation][cqrs] and [Event Sourcing][es] principles.

It is designed to:
* Help building new (micro)services.
* Easily integrate with existing [SQLAlchemy][sqlalchemy] or [Django][django] based applications.

## Usage

If you have never read about CQRS please get familiar with the "CQRS 101 Resources" section before proceeding.

#### Repository

#### Application

#### Aggregates

#### Events

#### Event Handlers

#### Examples

Please see [examples](examples) folder.

## Roadmap

Go to the [Project Board][project-board] for detailed release plans.

## How to Contribute

1. Check for open issues or open a fresh issue to start a discussion around a feature idea or a bug.
2. Fork this repository on GitHub to start making your changes to the **devel** branch (or branch off of it).
3. Write a test which shows that the bug was fixed or that the feature works as expected.
4. Send a pull request and bug the maintainer until it gets merged and published.


## CQRS 101 Resources

- [Greg Young - CQRS and Event Sourcing](https://www.youtube.com/watch?v=JHGkaShoyNs)
- [CQRS Intro by Martin Fowler][cqrs]
- [Event Sourcing Intro by Martin Fowler][es]

## Related Projects

- [Event Sourcing in Python](https://github.com/johnbywater/eventsourcing)
- [Axon](http://www.axonframework.org)
- [Eventhorizon](https://github.com/looplab/eventhorizon)


[build-status-image]: https://secure.travis-ci.org/lukaszb/cq.svg?branch=master
[travis]: http://travis-ci.org/lukaszb/cq
[cqrs]: https://martinfowler.com/bliki/CQRS.html
[es]: https://martinfowler.com/eaaDev/EventSourcing.html
[django]: https://www.djangoproject.com/
[sqlalchemy]: https://www.sqlalchemy.org/
[project-board]: https://github.com/lukaszb/cq/projects
