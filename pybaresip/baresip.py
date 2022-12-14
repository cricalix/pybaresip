#!/usr/bin/env python3
from __future__ import annotations

import dataclasses as dc
import functools
import json
import logging
import re
from typing import Callable, Dict

import dbus_next.aio as aio_dn
import dbus_next.errors as dn_err

import pybaresip.exceptions as pbs_ex

logger: logging.Logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
EventParams = Dict[str, str]


@dc.dataclass
class BaresipVersion:
    major: int
    minor: int
    patch: int

    def __str__(self) -> str:
        return f"{self.major}.{self.minor}.{self.patch}"


@dc.dataclass
class BaresipModule:
    name: str
    modtype: str
    references: int


def requires_version(fn: Callable) -> Callable:
    @functools.wraps(fn)
    def _inner(self, *args, **kwargs) -> None:
        if self._baresip_version.major == 0:
            raise Exception(
                "This function only works if it can determine the baresip version. "
                "The version is detected when `connect()` is executed."
            )
        return fn(self, *args, **kwargs)

    return _inner


class PyBareSIP:
    def __init__(
        self, bus_name: str = "com.github.Baresip", path: str = "/baresip"
    ) -> None:
        self._baresip_version = BaresipVersion(0, 0, 0)

    @property
    def ver(self) -> BaresipVersion:
        return self._baresip_version

    def handle_event_application_create(self, event: EventParams) -> None:
        logger.debug(event)

    def handle_event_application_exit(self, event: EventParams) -> None:
        """
        Called when baresip emits an application exit event on DBus
        """
        logger.debug("baresip exited")

    def handle_event_application_shutdown(self, event: EventParams) -> None:
        """
        Called when baresip emits an application shutdown event on DBus.

        This shows up when a User-Agent is shut down.
        """
        logger.debug(f"handle_event_application_shutdown for {event['accountaor']}")

    def handle_event_call_call_outgoing(self, event: EventParams) -> None:
        logger.debug(f"Outbound call to {event['peeruri']}")

    def handle_event_create(self, event: EventParams) -> None:
        logger.debug(f"handle_event_create {event}")

    def handle_event_other_call_local_sdp(self, event: EventParams) -> None:
        logger.debug(f"handle_event_other_call_local_sdp {event['type']}")

    def handle_event_other_module(self, event: EventParams) -> None:
        """
        Called on things like baresip starting up when this library is already listening
        on the bus.
        """
        logger.debug(f"handle_event_other_module {event['param']}")

    def handle_event_register_registering(self, event: EventParams) -> None:
        """
        Called when baresip emits a REGISTERING event on DBus.

        This shows up when a User-Agent is shut down.
        """
        logger.debug(f"handle_event_register_registering {event['accountaor']}")

    def handle_event_register_unregistering(self, event: EventParams) -> None:
        """
        Called when baresip emits an UNREGISTERING event on DBus.

        This shows up when a User-Agent is unregistered.
        """
        logger.debug(f"handle_event_register_unregistering for {event['accountaor']}")

    def handle_event_register_register_fail(self, event: EventParams) -> None:
        """
        Called when baresip emits an REGISTER_FAIL event on DBus.

        This shows up when a User-Agent registration attempt fails.
        """
        logger.debug(
            f"handle_event_register_register_fail {event['accountaor']}: "
            f"{event['param']}"
        )

    def handle_event(self, klass: str, event_type: str, event: EventParams) -> None:
        """
        Callback router for 'event' signals.
        """
        klass = event["class"].lower()
        evtype = event["type"].lower()
        func = f"handle_event_{klass}_{evtype}"
        print(f"Calling self.{func}(event={event})")
        try:
            getattr(self, func)(event=event)
        except KeyError:
            logger.error(f"Could not find function '{func}' to handle request.")

    def _changed_event(self, klass: str, evtype: str, param: str) -> None:
        """
        Callback for the dbus_next on_<signal> handlers, where signal is 'event'
        """
        self.handle_event(klass=klass, event_type=evtype, event=json.loads(param))

    def _changed_message(self, ua: str, peer: str, ctype: str, body: str) -> None:
        """
        Callback for the dbus_next on_<signal> handlers, where signal is 'message'
        """
        logger.error(
            f"Cannot handle messages. ua={ua} peer={peer} ctype={ctype} body={body}"
        )

    async def invoke(self, action: str) -> str:
        """
        Directly invoke a method over DBus.

        Class methods like `dial()` wrap this method.
        """
        logger.debug(f"Invoking {action}")
        return await self._interface.call_invoke(action)  # type: ignore[attr-defined]

    async def wait_for_disconnect(self) -> None:
        """
        Blocking call, allows the class to monitor the bus for events/messages.
        """
        await self._bus.wait_for_disconnect()

    async def connect(self) -> None:
        bus = await aio_dn.MessageBus().connect()
        try:
            api = await bus.introspect(self.bus_name, self.path)
        except dn_err.DBusError as e:
            if f"{self.bus_name} was not provided" in str(e):
                msg = (
                    f"{self.bus_name} was not found on DBus. Is baresip running with "
                    "the dbus module?"
                )
            else:
                msg = f"Failed when trying to introspect the baresip endpoint: {str(e)}"
            raise Exception(
                f"Could not introspect {self.bus_name}{self.path}: {msg}"
            ) from e
        proxy_object = bus.get_proxy_object(self.bus_name, self.path, api)
        interface = proxy_object.get_interface(self.bus_name)
        # These are dynamically defined methods that come from the introspection. mypy has to
        # be told to ignore them.
        interface.on_event(self._changed_event)  # type: ignore[attr-defined]
        interface.on_message(self._changed_message)  # type: ignore[attr-defined]
        self._interface = interface
        self._bus = bus
        await self.version()

    async def about(self) -> str:
        """
        Fetches the 'about' details from the baresip program.

        Does not trigger any DBus messages.
        """
        return await self.invoke("about")

    async def accept(self) -> str:
        """
        Instructs baresip to accept an inbound call.

        Does not emit anything on DBus.
        """
        return await self.invoke("accept")

    async def apistate(self) -> str:
        """
        Fetches the status of User-Agents.
        """
        return await self.invoke("apistate")

    async def auloop(self) -> str:
        return await self.invoke("auloop")

    async def auloop_stop(self) -> str:
        return await self.invoke("auloop_stop")

    async def auplay(self) -> str:
        """
        Instructs baresip to change the audio player.
        """
        return await self.invoke("auplay")

    async def ausrc(self) -> str:
        """
        Instructs baresip to change the audio source.
        """
        return await self.invoke("ausrc")

    async def callstat(self) -> str:
        return await self.invoke("callstat")

    async def conf_reload(self) -> str:
        """
        Instructs baresip to reload its configuration.
        """
        return await self.invoke("conf_reload")

    async def config(self) -> str:
        """
        Fetches the current configuration file from baresip.

        Does not emit anything on DBus
        """
        return await self.invoke("config")

    async def contact_next(self) -> str:
        return await self.invoke("contact_next")

    async def contact_prev(self) -> str:
        return await self.invoke("contact_prev")

    async def contacts(self) -> str:
        """
        Fetches a list of contacts from baresip. These contacts come from a configuration
        file.

        Does not emit anything on DBus.
        """
        return await self.invoke("contacts")

    async def dial(self, destination: str) -> str:
        """
        Instructs baresip to dial a destination. Baresip picks the User-Agent to use.

        Emits events on DBus.
        """
        return await self.invoke(f"dial {destination}")

    async def dial_contact(self) -> str:
        return await self.invoke("dial_contact")

    async def hangup(self) -> str:
        """
        Instructs baresip to hang up an existing active call.

        Does not emit anything on DBus.
        """
        return await self.invoke("hangup")

    async def help(self) -> str:
        """
        Fetches the baresip /help command output. Generally not useful for this library.

        Does not emit anything on DBus.
        """
        return await self.invoke("help")

    async def insmod(self, module: str) -> str:
        """
        Instructs baresip to insert a module, such as 'g711'.

        Does not emit anything on DBus when the module is loaded.
        """
        module = module.strip()
        if " " in module:
            raise Exception(f"Module names may not contain spaces ({module}")
        return await self.invoke(f"insmod {module}")

    async def listcalls(self) -> str:
        """
        Fetches active calls, broken down by User-Agent.

        Does not emit anything on DBus.
        """
        return await self.invoke("listcalls")

    async def loglevel(self) -> str:
        """
        Instructs baresip to change the console log level. This is a cycling toggle.

        Does not emit anything on DBus.
        """
        return await self.invoke("loglevel")

    async def main(self) -> str:
        """
        Fetches main loop debugging information from baresip.

        Does not emit anything on DBus.
        """
        return await self.invoke("main")

    async def memstat(self) -> str:
        """
        Fetches memory status data from baresip. Does not work in v2.9.0 of baresip.

        Does not emit anything on DBus.
        """
        return await self.invoke("memstat")

    async def message(self) -> str:
        return await self.invoke("message")

    async def modules(self) -> str:
        """
        Fetches the list of loaded modules from baresip.

        Does not emit anything on DBus.
        """
        return await self.invoke("modules")

    async def netstat(self) -> str:
        """
        Fetches the list of interfaces that baresip is listening on, and the DNS servers
        in use.

        Does not emit anything on DBus.
        """
        return await self.invoke("netstat")

    async def options(self, account: str) -> str:
        """
        TODO: Decipher this command.

        Does not emit anything on DBus, even when it fails.
        """
        return await self.invoke(f"options {account}")

    async def play(self, filename: str) -> str:
        """
        Instructs baresip to play a sound file. If baresip has not been configured, and has
        loaded the ALSA modules, the sound will play through the local soundcard.

        Does not emit anything on DBus.
        """
        return await self.invoke(f"play {filename}")

    async def quit(self) -> str:
        """
        Instructs baresip to shut down.

        Emits events on DBus as registrations etc are shut down and deregistered.
        """
        return await self.invoke("quit")

    async def reginfo(self) -> str:
        """
        Fetches a list of registered user agents.

        Does not emit anything on DBus.
        """
        return await self.invoke("reginfo")

    async def rmmod(self, module: str) -> str:
        """
        Instructs baresip to unload a loaded module, such as 'g711'.

        Does not emit anything on DBus when the module is unloaded.
        """
        module = module.strip()
        if " " in module:
            raise Exception(f"Module names may not contain spaces ({module}")
        return await self.invoke(f"rmmod {module}")

    async def sipstat(self) -> str:
        """
        Fetches tranports, connections, transactions from baresip.

        Does not emit anything on DBus.
        """
        return await self.invoke("sipstat")

    async def sysinfo(self) -> str:
        """
        Fetches system information from baresip - kernel, version of baresip, compiler etc.

        Does not emit anything on DBus.
        """
        return await self.invoke("sysinfo")

    async def timers(self) -> str:
        """
        Fetches active timers from baresip.

        Does not emit anything on DBus.
        """
        return await self.invoke("timers")

    async def uaaddheader(self, key: str, value: str) -> str:
        """
        Instructs baresip to add a header to a User-Agent.
        """
        return await self.invoke(f"uaaddheader {key}={value}")

    async def uadel(self, account: str) -> str:
        """
        Instructs baresip to delete a User-Agent from the internal registry.
        """
        return await self.invoke(f"uadel {account}")

    async def uafind(self, account: str) -> str:
        """
        Instructs baresip to find a User-Agent matching the account.

        If an agent is not found, a string error message is returned.

        Does not emit anything on DBus.
        """
        return await self.invoke(f"uafind {account}")

    async def uanew(self, account: str, flags: dict[str, str] | None = None) -> str:
        """
        Creates a new User-Agent in baresip. baresip will use this agent as a
        Caller-ID for outbound calls.

        A User-Agent is specified as <protocol>:<username>@<address>:<port>;<flags>

        This function enforces that the protocol is set to "sip".

        P

        Triggers:
        * application.CREATE
        """
        ua_full = r"^sip:\w+@.*(:\d+)?"
        ua_missing_proto = r"^\w+@.*(:\d+)?"
        if not re.match(ua_full, account):
            if not re.match(ua_missing_proto, account):
                raise Exception(
                    f"'{account}' does not appear to be a valid User-Agent string."
                )
            else:
                account = f"sip:{account}"
                logger.warning(f"{account} did not start with 'sip'. Prefix added.")
        if flags:
            account_flags = ";".join([f"{k}={v}" for k, v in flags.items()])
            account = f"{account};{account_flags}"
        return await self.invoke(f"uanew {account}")

    @requires_version
    async def uanext(self) -> str:
        """
        FIXME: Does not exist in 2.9
        """
        if self._baresip_version.major == 2:
            raise NotImplementedError(
                f"baresip {self.ver} does not support this command"
            )
        return await self.invoke("uanext")

    async def uastat(self) -> str:
        """
        Fetches the current User-Agents from baresip.

        Does not emit anything on DBus.
        """
        return await self.invoke("uastat")

    async def uuid(self) -> str:
        """
        Fetches the current UUID from baresip.

        Purpose unknown.

        Does not emit anything on DBus.
        """
        return await self.invoke("uuid")

    async def vidloop(self) -> str:
        raise NotImplementedError()

    async def vidloop_stop(self) -> str:
        raise NotImplementedError()

    async def vidsrc(self) -> str:
        raise NotImplementedError()

    async def loaded_modules(self) -> list[BaresipModule]:
        """
        Wraps `modules()` to provide a formatted output of loaded modules on the baresip
        server.
        """
        mods = await self.modules()
        modline_pattern = re.compile(
            r"\s+(?P<name>\w+) type=(?P<modtype>(\w+|\w+ \w+|\s))\s+ref=(?P<ref>\d+)"
        )
        modules = []
        for line in mods.splitlines():
            x = modline_pattern.search(line)
            if x:
                modules.append(
                    BaresipModule(
                        name=x.group("name"),
                        modtype=x.group("modtype"),
                        references=int(x.group("ref")),
                    )
                )
        return modules

    async def user_agent_exists(self, account: str) -> bool:
        """
        Wraps `uafind()` to find out if a User-Agent exists.
        """
        x = await self.uafind(account=account)
        return "could not find" not in x

    async def new_user_agent(
        self,
        account: str,
        password: str | None = None,
        flags: dict[str, str] | None = None,
    ) -> str:
        """
        Wraps`uanew()` to provide a potentially friendlier method name.
        """
        if password and flags:
            # Clobber.
            flags["auth_pass"] = password
        elif password and not flags:
            flags = {"auth_pass": password}

        return await self.uanew(account=account, flags=flags)

    async def version(self) -> BaresipVersion:
        """
        Attempts to fetch a version number using the 'about' baresip command.
        """
        pattern = re.compile(r"\s+((?P<major>\d+)\.(?P<minor>\d+)\.(?P<patch>\d+))\s+")
        about = await self.about()
        m = pattern.search(about)
        if m:
            self._baresip_version = BaresipVersion(
                int(m.group("major")), int(m.group("minor")), int(m.group("patch"))
            )
            logger.info(f"baresip version is {str(self._baresip_version)}")
        else:
            raise pbs_ex.BaresipVersionError(
                "Could not determine version from 'about' command. You need to "
                "override the 'version' method."
            )
        return self._baresip_version
