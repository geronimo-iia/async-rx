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
    ConnectHandler,
    RefCountHandler,
    ConnectableObservable,
    ObservableFactory,
    SubjectEventHandler,
    SubjectHandler,
    ConnectableObservableEventHandler,
    ConnectableObservableHandler,
    PredicateOperator,
    AccumulatorOperator,
    SubjectFactory,
    rx_observer,
)

from .subject import rx_subject, rx_subject_replay, rx_subject_behavior

from .multicast import rx_publish, rx_publish_replay, rx_publish_behavior
from .observable import (
    rx_create,
    rx_defer,
    rx_distinct,
    rx_empty,
    rx_filter,
    rx_first,
    rx_forward,
    rx_from,
    rx_last,
    rx_of,
    rx_range,
    rx_skip,
    rx_take,
    rx_throw,
    rx_count,
    rx_max,
    rx_min,
    rx_sum,
    rx_avg,
    rx_buffer,
    rx_window,
    rx_merge,
    rx_concat,
    rx_zip,
    rx_amb,
    rx_map,
)

from .protocol.definition import __all__ as _def_all
from .protocol.observer import __all__ as _obs_all

__all__ = [
    "Subscription",
    "NextHandler",
    "CompleteHandler",
    "ErrorHandler",
    "Observable",
    "Observer",
    "Subscribe",
    "Subject",
    "ConnectHandler",
    "RefCountHandler",
    "ConnectableObservable",
    "ObservableFactory",
    "SubjectEventHandler",
    "SubjectHandler",
    "ConnectableObservableEventHandler",
    "ConnectableObservableHandler",
    "PredicateOperator",
    "AccumulatorOperator",
    "SubjectFactory",
    "rx_observer",
    # from observable
    "rx_create",
    "rx_defer",
    "rx_distinct",
    "rx_empty",
    "rx_filter",
    "rx_first",
    "rx_forward",
    "rx_from",
    "rx_last" "rx_of",
    "rx_range",
    "rx_skip",
    "rx_take",
    "rx_throw",
    "rx_reduce",
    "rx_count",
    "rx_max",
    "rx_min",
    "rx_sum",
    "rx_avg",
    "rx_buffer",
    "rx_window",
    "rx_merge",
    "rx_concat",
    "rx_zip",
    "rx_amb",
    "rx_map",
    # subject
    "rx_subject",
    "rx_subject_replay",
    "rx_subject_behavior"
    # multicast
    "rx_publish",
    "rx_publish_replay",
    "rx_publish_behavior",
]

try:
    __version__ = get_distribution('async_rx').version
except DistributionNotFound:
    __version__ = '(local)'
