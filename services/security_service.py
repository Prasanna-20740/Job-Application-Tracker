
import nh3


def sanitize_notes(notes):
    """
    Remove HTML tags and attributes from application notes.
    Preserve normal text content.
    """

    if notes is None:
        return None

    if not isinstance(notes, str):
        raise ValueError("Notes must be a string")

    cleaned_notes = nh3.clean(
        notes,
        tags=set(),
        attributes={}
    )

    return cleaned_notes.strip()
