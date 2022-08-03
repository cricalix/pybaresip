from __future__ import annotations

import logging
import os
import shutil

import pexpect

import pybaresip.exceptions as exceptions
import pybaresip.identity as identity

logger: logging.Logger = logging.getLogger(__name__)


class BareSIP:
    def __init__(
        self,
        identity: identity.Identity,
        baresip_exe: str | None = None,
        baresip_config: str | None = None,
    ) -> None:
        """Starts a baresip sub-process, and communicates with it over stdio.

        identity: an Identity object with credentials
        baresip_exe: Override auto-detection of the baresip cli tool
        """
        self._baresip_exe = self._resolve_baresip_exe(baresip_exe)
        self._baresip_config = self._resolve_baresip_config(baresip_config)
        self.baresip = pexpect.spawn(
            self._baresip_exe, args=["-f", self._baresip_config]
        )

    def _resolve_baresip_exe(self, baresip_exe: str | None) -> str:
        if not baresip_exe:
            # Attempt to find it in the path
            baresip_exe = shutil.which(cmd="baresip")
            if not baresip_exe:
                # Failed to find it
                raise exceptions.BaresipNotFound("via PATH environment")
        else:
            if not os.path.isfile(path=baresip_exe):
                raise exceptions.BaresipNotFound(baresip_exe)
        return baresip_exe

    def _resolve_baresip_config(self, baresip_config: str | None) -> str:
        if not baresip_config:
            # TODO: Should the class auto-create a basic configuration file?
            baresip_config = "config"
        else:
            if not os.path.isfile(path=baresip_config):
                raise exceptions.BaresipConfigNotFound(baresip_config)
        return baresip_config

    def run(self) -> None:
        logger.info(f"Starting baresip via {self._baresip_exe}")
