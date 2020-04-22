from async_rx.observable import rx_range


def get_observable():
    return rx_range(start=0, stop=100)
