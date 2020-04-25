# async-rx


[![Unix Build Status](https://img.shields.io/travis/geronimo-iia/async-rx/master.svg?label=unix)](https://travis-ci.com/geronimo-iia/async-rx)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/fe669a02b4aa46b5b1faf619ba2bf382)](https://www.codacy.com/app/geronimo-iia/async-rx?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=geronimo-iia/async-rx&amp;utm_campaign=Badge_Grade)
[![PyPI Version](https://img.shields.io/pypi/v/async-rx.svg)](https://pypi.org/project/async-rx)
[![PyPI License](https://img.shields.io/pypi/l/async-rx.svg)](https://pypi.org/project/async-rx)

Versions following [Semantic Versioning](https://semver.org/)

## Overview

A free implemntation of "rx" alias "react" alias "the power of observable pattern and his children" for application server side.

Implementation relie on:

- async function with curio framework
- closed variable, clojure
- python 3.8 Protocol declaration
- a taste of namedtuple
- a taste for curiosity
- shake it and tadaa !

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
I can't purpose your the best state of the explanation, but... AMHPOV, if you like to known how slug are done behind the scence, you should remember:

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






