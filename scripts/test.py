#!/usr/bin/env python3
from __future__ import annotations

import asyncio
import functools
import logging
from typing import Callable

import click

import pybaresip.baresip as pbs


logger: logging.Logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
logging.basicConfig()


def asyncio_run(fn: Callable) -> Callable:
    """
    A decorator that wraps an async def in asyncio.run
    """

    @functools.wraps(fn)
    def wrapper(*args, **kwargs) -> None:
        asyncio.run(fn(*args, **kwargs))

    return wrapper


@click.command
@asyncio_run
async def cli() -> None:
    acct = "sip:tst@localhost:5060"
    bs = pbs.PyBareSIP()
    await bs.connect()
    # await bs.new_user_agent(f"{acct}};regint=0")
    # x = await bs.invoke("uanew sip:test@localhost:5060;regint=0;auth_pass=test")
    # time.sleep(1)
    # x = await bs.invoke("dial test@192.168.0.1")
    #
    # print(x)
    # print()
    # x = await bs.dial("test@sipura")
    #
    # print(x)
    # print()
    print(await bs.uastat())
    # print(await bs.user_agent_exists(acct))

    await bs.wait_for_disconnect()


if __name__ == "__main__":
    cli()
