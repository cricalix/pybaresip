from __future__ import annotations

import copy
import dataclasses as dc


@dc.dataclass
class Identity:
    """An Account is the configuration for an identity used to make calls.

    If you want to suppress registration, add {"regint": 0} to flags.

    The password is automatically migrated to the flags as {"auth_pass": <password>}
    """

    user: str
    password: str
    gateway: str
    flags: list[dict[str, str]] = dc.field(default_factory=list)
    port: int = 5060

    @property
    def sip(self) -> str:
        """Returns the identity as a sip: address string with flags"""
        # Assign to self so this code doesn't end up putting auth_pass in the flags
        # repeatedly
        flags = copy.copy(self.flags)
        flags.append({"auth_pass": self.password})
        f = [f"{k}={v}" for x in flags for k, v in x.items()]
        return f"sip:{self.user}@{self.gateway}:{self.port};{';'.join(f)}"
