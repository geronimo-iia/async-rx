"""async-rx definition."""
from pkg_resources import DistributionNotFound, get_distribution

from .protocol import (
    Subscription,
    NextHandler,
    CompleteHandler,
    ErrorHandler,
    Observable,
    Observer,
    Subscribe,
    Subject,
    ConnectableObservable,
    ObservableFactory,
    SubjectEventHandler,
    SubjectHandler,
    ConnectableObservableHandler,
    default_subscription,
    PredicateOperator,
    AccumulatorOperator,
    SubjectFactory,
)

from .observer import observer
from .subject import subject, subject_handler, replay_subject, behavior_subject
from .multicast import multicast, publish_behavior, publish_replay
from .observable import (
    rx_create,
    rx_defer,
    rx_empty,
    rx_forward,
    rx_of,
    rx_range,
    rx_throw,
    rx_from,
    rx_distinct,
    rx_filter,
    rx_first,
    rx_last,
    rx_skip,
    rx_take,
    rx_reduce,
    rx_count,
    rx_max,
    rx_min,
    rx_sum,
    rx_avg,
    rx_merge,
    rx_zip,
)


__all__ = [
    # protocol
    'Subscription',
    'NextHandler',
    'CompleteHandler',
    'ErrorHandler',
    'Observable',
    'Observer',
    'Subscribe',
    'Subject',
    'ConnectableObservable',
    'ObservableFactory',
    'SubjectEventHandler',
    'SubjectHandler',
    'ConnectableObservableHandler',
    'default_subscription',
    'PredicateOperator',
    'AccumulatorOperator',
    'SubjectFactory',
    'observer',
    'subject',
    'subject_handler',
    'replay_subject',
    'behavior_subject',
    'multicast',
    'publish_behavior',
    'publish_replay',
    "rx_create",
    "rx_defer",
    "rx_empty",
    "rx_forward",
    "rx_of",
    "rx_range",
    "rx_throw",
    "rx_from",
    "rx_distinct",
    "rx_filter",
    "rx_first",
    "rx_last",
    "rx_skip",
    "rx_take",
    "rx_reduce",
    "rx_count",
    "rx_max",
    "rx_min",
    "rx_sum",
    "rx_avg",
    "rx_merge",
    "rx_zip",
]

try:
    __version__ = get_distribution('async_rx').version
except DistributionNotFound:
    __version__ = '(local)'
