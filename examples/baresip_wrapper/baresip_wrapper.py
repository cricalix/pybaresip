#!/usr/bin/env python3

"""
This is a sample that shows how BareSIP could be run via a thread in a
Python script/program. It's not guaranteed to work; more to be a starting
point for your own explorations.

For pybaresip's design, I opted to move away from running baresip via a
thread; the OS is perfectly capable of starting baresip automatically, or
a script could be used to start it, and then start the Python code that
needs baresip.
"""

from __future__ import annotations

import logging
import multiprocessing
import os
import shutil
import subprocess
import threading

logger: logging.Logger = logging.getLogger(__name__)


class BareSIP(threading.Thread):
    def __init__(
        self,
        stop_event: threading.Event,
        baresip_exe: str | None = None,
    ) -> None:
        """
        Starts a baresip subprocess, and waits for stop_event to be set, thus
        indicating that the subprocess should be terminated.

        baresip_exe: Override auto-detection of the baresip cli tool
        """

        self._baresip_exe = self._resolve_baresip_exe(baresip_exe)
        self.stop_event = stop_event
        super().__init__()

    def _resolve_baresip_exe(self, baresip_exe: str | None) -> str:
        if not baresip_exe:
            # Attempt to find it in the path
            baresip_exe = shutil.which(cmd="baresip")
            if not baresip_exe:
                # Failed to find it
                raise Exception("'baresip' not found via PATH environment")
        else:
            if not os.path.isfile(path=baresip_exe):
                raise Exception(f"{baresip_exe} not found")
        return baresip_exe

    def _status_change(self, x) -> None:
        logger.error("Status change: %s", x)

    def run(self) -> None:
        logger.info(f"Starting baresip via {self._baresip_exe}")
        proc = subprocess.Popen(self._baresip_exe)
        self.stop_event.wait()
        proc.kill()


if __name__ == "__main__":

    def runner(event: threading.Event) -> None:
        bs = BareSIP(stop_event=event, baresip_exe="/usr/bin/baresip")

    stopper = threading.Event()
    p = multiprocessing.Process(target=runner, args=(stopper,))
    p.start()
    stopper.set()
    p.join()
