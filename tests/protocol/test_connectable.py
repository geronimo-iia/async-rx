from async_rx.protocol import connectable_observable_handler


def test_connectable_observable_handler():
    async def dummy():
        pass

    handler = connectable_observable_handler(on_connect=dummy, on_disconnect=dummy)
    assert handler
    assert handler.on_connect
    assert handler.on_disconnect
