from __future__ import annotations

import dataclasses as dc


class IdentityFlagError(ValueError):
    ...


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
    def flag_names(self) -> list[str]:
        return [x for y in self.flags for x in y.keys()]

    @property
    def sip(self) -> str:
        """Returns the identity as a sip: address string with flags"""
        f = [f"{k}={v}" for x in self.flags for k, v in x.items()]
        return f"sip:{self.user}@{self.gateway}:{self.port};{';'.join(f)}"

    def __post_init__(self) -> None:
        if "auth_pass" in self.flag_names:
            raise IdentityFlagError("'auth_pass' must not be specified as a flag.")

        self.flags.append({"auth_pass": self.password})
