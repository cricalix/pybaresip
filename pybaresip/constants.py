import enum


class CallStatus(enum.Enum):
    # baresip has disconnected from the callee/caller
    DISCONNECTED = enum.auto()
    # baresip has a session established with the callee/caller
    ESTABLISHED = enum.auto()
    # baresip has signaled that there's a new call coming in
    INCOMING = enum.auto()
    # special flag value, not produced by baresip
    NONE = enum.auto()
    # baresip has signaled the call is on hold
    ON_HOLD = enum.auto()
    # baresip has signaled that there's a call outbound
    OUTGOING = enum.auto()
    # baresip has signaled that the outbound call is ringing
    RINGING = enum.auto()
    # special flag value, not produced by baresip
    UKNOWN = enum.auto()
