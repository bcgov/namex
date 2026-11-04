from namex.models import State

# Only allow editing if the request is in certain valid states
request_editable_states = [State.INPROGRESS, State.DRAFT, State.RESERVED, State.COND_RESERVE, State.PENDING_PAYMENT]

contact_editable_states = [
    State.INPROGRESS,
    State.DRAFT,
    State.APPROVED,
    State.REJECTED,
    State.CONDITIONAL,
    State.CONSUMED,
]
