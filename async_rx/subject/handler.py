from ..protocol import SubjectEventHandler, SubjectHandler, SubjectHandlerDefinition

__all__ = ["subject_handler"]


def subject_handler(on_subscribe: SubjectEventHandler, on_unsubscribe: SubjectEventHandler) -> SubjectHandler:
    """Create a SubjectHandler.

    Args:
        on_subscribe (SubjectEventHandler): on subscribe event handler
        on_unsubscribe (SubjectEventHandler): on unsubscribe event handler
    Returns:
        (SubjectHandler): a SubjectHandler instance.

    """
    return SubjectHandlerDefinition(on_subscribe=on_subscribe, on_unsubscribe=on_unsubscribe)
