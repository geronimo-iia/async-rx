"""async-rx definition."""
from pkg_resources import DistributionNotFound, get_distribution

try:
    __version__ = get_distribution('async_rx').version
except DistributionNotFound:
    __version__ = '(local)'

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
    # observer
    'observer',
    # subject
    'subject',
    'subject_handler',
    'replay_subject',
    'behavior_subject',
    # multicast
    'multicast',
    'publish_behavior',
    'publish_replay',
    # observable
    "rx_create",
    "rx_defer",
    "rx_empty",
    "rx_forward",
    "rx_of",
    "rx_range",
    "rx_throw",
    "rx_from",
    # observable filter
    "rx_distinct",
    "rx_filter",
    "rx_first",
    "rx_last",
    "rx_skip",
    "rx_take",
    ## observablemath
    "rx_reduce",
    "rx_count",
    "rx_max",
    "rx_min",
    "rx_sum",
    "rx_avg",
    # observable combinator
    "rx_merge",
    "rx_zip",
    # observable time
    # "rx_debounce",
    # "rx_timer",
]
