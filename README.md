# async-rx


[![Unix Build Status](https://img.shields.io/travis/geronimo-iia/async-rx/master.svg?label=unix)](https://travis-ci.com/geronimo-iia/async-rx)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/fe669a02b4aa46b5b1faf619ba2bf382)](https://www.codacy.com/app/geronimo-iia/async-rx?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=geronimo-iia/async-rx&amp;utm_campaign=Badge_Grade)
[![Coverage Status](https://coveralls.io/repos/github/geronimo-iia/async-rx/badge.svg?branch=master)](https://coveralls.io/github/geronimo-iia/async-rx?branch=master)[Scrutinizer Code Quality](https://img.shields.io/scrutinizer/g/geronimo-iia/async-rx.svg)](https://scrutinizer-ci.com/g/geronimo-iia/async-rx/?branch=master)[![PyPI Version](https://img.shields.io/pypi/v/async-rx.svg)](https://pypi.org/project/async-rx)
[![PyPI License](https://img.shields.io/pypi/l/async-rx.svg)](https://pypi.org/project/async-rx)

Versions following [Semantic Versioning](https://semver.org/)


## Overview

A free implemntation of "rx" alias "react" alias "the power of observable pattern and his children" for application server side.

Implementation is based on:

- async function with curio framework
- python 3.8 Protocol declaration
- our friends: poetry, flake8, pytest, mypy, sphinx, ...
- a taste of namedtuple
- closed variable, clojure function
- a taste of curiosity
- shake it, again a little bit and tadaa !

## Installation

Install this library directly into an activated virtual environment:

```text
$ pip install async-rx
```

or add it to your [Poetry](https://poetry.eustace.io/) project:

```text
$ poetry add async-rx
```

## API and Usage

After installation, the package can imported:

```text
$ python
>>> import async_rx
>>> async_rx.__version__
```

Take a look on [documentation](https://geronimo-iia.github.io/async-rx) and [API](https://geronimo-iia.github.io/async-rx/api.html).



| Function Name                                                                                                               | Description                                                                          |
| --------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------ |
| [rx_observer(on_next, on_error, on_completed)](https://geronimo-iia.github.io/async-rx/api.html#async_rx.rx_observer) | Return an observer.                                                                  |
| [rx_observer_from(observer, on_next, …)](https://geronimo-iia.github.io/async-rx/api.html#async_rx.rx_observer_from)       | Build an observer from another one.                                                  |
| [rx_collector(initial_value)](https://geronimo-iia.github.io/async-rx/api.html#async_rx.rx_collector)                  | Create an observer collector.                                                        |
| [rx_create(subscribe, ensure_contract, …)](https://geronimo-iia.github.io/async-rx/api.html#async_rx.rx_create)     | Create an observable with specific delayed execution ‘subscribe’.                    |
| [rx_defer(observable_factory)](https://geronimo-iia.github.io/async-rx/api.html#async_rx.rx_defer)                 | Create an observable when a subscription occurs.                                     |
| [rx_distinct(observable, frame_size)](https://geronimo-iia.github.io/async-rx/api.html#async_rx.rx_distinct)          | Create an observable which send distinct event inside a windows of size #frame_size. |
| [rx_empty()](https://geronimo-iia.github.io/async-rx/api.html#async_rx.rx_empty)                                   | Create an empty Observable.                                                          |
| [rx_filter(observable, predicate, …)](https://geronimo-iia.github.io/async-rx/api.html#async_rx.rx_filter)                                                                                        | Create an observable which event are filtered by a predicate function.               |
| [rx_first(observable)](https://geronimo-iia.github.io/async-rx/api.html#async_rx.rx_first)                                                                                                       | Create an observale which only take the first event and complete.                    |
| [rx_forward(observable, except_complet, …)](https://geronimo-iia.github.io/async-rx/api.html#async_rx.rx_forward)                                                                                  | Create an observable wich forward event.                                             |
| [rx_from(observable_input)](https://geronimo-iia.github.io/async-rx/api.html#async_rx.rx_from)                                                                                                  | Convert almost anything to an Observable.                                            |
| [rx_last(observable, count)](https://geronimo-iia.github.io/async-rx/api.html#async_rx.rx_last)                                                                                                 | Create an observale which only take #count (or less) last events and complete.       |
| [rx_of(*args)](https://geronimo-iia.github.io/async-rx/api.html#async_rx.rx_of)                                                                                                               | Convert arguments into an observable sequence.                                       |
| [rx_range(start, stop, step)](https://geronimo-iia.github.io/async-rx/api.html#async_rx.rx_range)                                                                                                | Create an observable sequence of range.                                              |
| [rx_skip(observable, count)](https://geronimo-iia.github.io/async-rx/api.html#async_rx.rx_skip)                                                                                                 | Create an obervable wich skip #count event on source.                                |
| [rx_take(observable, count)](https://geronimo-iia.github.io/async-rx/api.html#async_rx.rx_take)                                                                                                 | Create an observable which take only first #count event maximum (could be less).     |
| [rx_throw(error)](https://geronimo-iia.github.io/async-rx/api.html#async_rx.rx_throw)                                                                                                            | Create an observable wich always call error.                                         |
| [rx_reduce(observable, accumulator, …)](https://geronimo-iia.github.io/async-rx/api.html#async_rx.rx_reduce)                                                                                      | Create an observable which reduce source with accumulator and seed value.            |
| [rx_count(observable)](https://geronimo-iia.github.io/async-rx/api.html#async_rx.rx_count)                                                                                                       | Create an observable wich counts the emissions on the source and emits result.       |
| [rx_max(observable)](https://geronimo-iia.github.io/async-rx/api.html#async_rx.rx_max)                                                                                                         | Create an observable wich returns the maximal item in the source when completes.     |
| [rx_min(observable)](https://geronimo-iia.github.io/async-rx/api.html#async_rx.rx_min)                                                                                                         | Create an observable wich returns minimal item in the source when completes.         |
| [rx_sum(observable)](https://geronimo-iia.github.io/async-rx/api.html#async_rx.rx_sum)                                                                                                         | Create an observable wich return the sum items in the source when completes.         |
| [rx_avg(observable)](https://geronimo-iia.github.io/async-rx/api.html#async_rx.rx_avg)                                                                                                         | Create an observable wich return the average items in the source when completes.     |
| [rx_buffer(observable, buffer_size)](https://geronimo-iia.github.io/async-rx/api.html#async_rx.rx_buffer)                                                                                         | Buffer operator.                                                                     |
| [rx_window(observable, buffer_size)](https://geronimo-iia.github.io/async-rx/api.html#async_rx.rx_window)                                                                                         | Window operator.                                                                     |
| [rx_merge(*observables)](https://geronimo-iia.github.io/async-rx/api.html#async_rx.rx_merge)                                                                                                     | Flattens multiple Observables together by blending their values into one Observable. |
| [rx_concat(*observables)](https://geronimo-iia.github.io/async-rx/api.html#async_rx.rx_concat)                                                                                                    | Concat operator.                                                                     |
| [rx_zip(*observables)](https://geronimo-iia.github.io/async-rx/api.html#async_rx.rx_zip)                                                                                                       | Combine multiple Observables to create an Observable.                                |
| [rx_amb(*observables)](https://geronimo-iia.github.io/async-rx/api.html#async_rx.rx_amb)                                                                                                       | Amb operator.                                                                        |
| [rx_map(observable, transform, …)](https://geronimo-iia.github.io/async-rx/api.html#async_rx.rx_map)                                                                                           | Map operator.                                                                        |
| [rx_merge_map(*observables, transform)](https://geronimo-iia.github.io/async-rx/api.html#async_rx.rx_merge_map)                                                                                      | Merge map operator.                                                                  |
| [rx_group_by(observable, key_selector)](https://geronimo-iia.github.io/async-rx/api.html#async_rx.rx_group_by)                                                                                      | Group by operator.                                                                   |
| [rx_sample(observable, duration)](https://geronimo-iia.github.io/async-rx/api.html#async_rx.rx_sample)                                                                                            | Sample operator used to rate-limit the sequence.                                     |
| [rx_throttle(observable, duration)](https://geronimo-iia.github.io/async-rx/api.html#async_rx.rx_throttle)                                                                                          | Throttle operator.                                                                   |
| [rx_delay(observable, duration, buffer_size, …)](https://geronimo-iia.github.io/async-rx/api.html#async_rx.rx_delay)                                                                             | Delay operator.                                                                      |
| [rx_debounce(an_observable, duration)](https://geronimo-iia.github.io/async-rx/api.html#async_rx.rx_debounce)                                                                                       | Debounce operator.                                                                   |
| [rx_dict(initial_value)](https://geronimo-iia.github.io/async-rx/api.html#async_rx.rx_dict)                                                                                                     | Create an observable on dictionnary.                                                 |
| [rx_list(initial_value)](https://geronimo-iia.github.io/async-rx/api.html#async_rx.rx_list)                                                                                                     | Create an observable on list.                                                        |
| [rx_repeat(duration, producer)](https://geronimo-iia.github.io/async-rx/api.html#async_rx.rx_repeat)                                                                                              | Repeat data.                                                                         |
| [rx_repeat_series(source, ratio)](https://geronimo-iia.github.io/async-rx/api.html#async_rx.rx_repeat_series)                                                                                            | Repeat a series (delay, value) as an observable for each subscription.               |
| [rx_subject(subject_handler)](https://geronimo-iia.github.io/async-rx/api.html#async_rx.rx_subject)                                                                                                | Create a subject.                                                                    |
| [rx_subject_from(a_subject, subscribe, …)](https://geronimo-iia.github.io/async-rx/api.html#async_rx.rx_subject_from)                                                                                   | Build a subject from another one by override some function.                          |
| [rx_subject_replay(buffer_size, subject_handler)](https://geronimo-iia.github.io/async-rx/api.html#async_rx.rx_subject_replay)                                                                            | Create a replay subject.                                                             |
| [rx_subject_behavior(subject_handler)](https://geronimo-iia.github.io/async-rx/api.html#async_rx.rx_subject_behavior)                                                                                       | Create a behavior subject.                                                           |
| [rx_publish(an_observable, subject_handler, …)](https://geronimo-iia.github.io/async-rx/api.html#async_rx.rx_publish)                                                                              | Create a Connectable Observable.                                                     |
| [rx_publish_replay(an_observable, …)](https://geronimo-iia.github.io/async-rx/api.html#async_rx.rx_publish_replay)                                                                                        | Create a publish_replay.                                                             |
| [rx_publish_behavior(an_observable, …)](https://geronimo-iia.github.io/async-rx/api.html#async_rx.rx_publish_behavior)                                                                                      | Create a publish_behavior.                                                           |

## A short sample

With this amazing observer:

```python
class ObserverCounterCollector:
    def __init__(self):
        self.on_next_count = 0
        self.on_completed_count = 0
        self.on_error_count = 0
        self.items: Any = list([]) # a bad idea isn't it

    async def on_next(self, item: Any) -> None:
        """Process item."""
        self.items.append(item)
        self.on_next_count += 1

    async def on_completed(self) -> None:
        """Signal completion of this observable."""
        self.on_completed_count += 1

    async def on_error(self, err: Any) -> None:
        self.on_error_count += 1

```

We will going to select odd number:

```python
async def _predicate(item: int) -> bool:
    return item % 2 == 0

seeker = ObserverCounterCollector()

observable = rx_range(start=0, stop=100) # create an observable of [0, 1, ..., 99]
sub = await rx_filter(observable=observable, predicate=_predicate).subscribe(an_observer=seeker) # filter and subscribe
sub() # release resource

# we have :
assert seeker.on_next_count == 50
assert seeker.on_completed_count == 1
assert seeker.on_error_count == 0
assert seeker.items[0:6] == [0, 2, 4, 6, 8, 10]

```


## Your new on react/rx and wanna taste it ?

First question: Where to begin ?

If you read this page, you probably ever doing lot of search on google & co, and probably loose as me about
react component in html/js/whatever.
I can't purpose your the best state of the explanation, but... AMHPOV, if you like to known how slug are done behind the scene, you should remember:

- what is Observable pattern (or listener, alias callback)
- what is an event emiter (something which send event ?)

ok, with this in mind:

- an observer receive event from an observable when he subscribe on it
- events are "on_next(item)", "on_completed()", and ... "on_error(err)"

Take a look in "protocole.py" and come back :)

Did you see Observer/Observable/XXXHandler/Subscribe ? And Subcription (yes it will called for unsubscribe) ?

So ```rx_from([1, 2, ...])``` create an observable which will send items of list in sequence when an observer subscribe on it.
Take time to look at test unit :)
You can go into observable module and see all rx_from, rx_defer, rx_last, ...

But but but, what is a freaking "subject" ?

It's like an observer AND an observable which can multicast items from an observable to several observers.
As it is an observer, it can receive data from somewhere. 
As it is an observable, observer can subscribe on it.

Take a look under subject module and test unit, see what is a replay_subject, funny no ?
See the function [subject](https://geronimo-iia.github.io/async-rx/api.html#async_rx.Subject).

At the last for the goods: the big gun, the "ConnectableObservable" alias multicast. oh my god, they kill kenny!

Its like a subject which you can connect/disconnect as you want or automatically (with a call on ref_count).
"connect" mean that subject start to receive from observable, so items will be send on observers.

I hope this could help you a little bit :)


## Reference

 - [reactivex](http://reactivex.io/documentation/observable.html)
 - [reactjs](https://reactjs.org/)
 - [The Reactive Manifesto](https://www.reactivemanifesto.org/)
 - [working with unreliable observers using reactive extensions](https://www.ru.nl/publish/pages/769526/dorus_peelen.pdf)
 - ...






