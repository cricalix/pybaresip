import pexpect
import pybaresip.identity as identity
import shutil
import pybaresip.exceptions as exceptions
import os


class BareSIP:
    def __init__(
        self, identity: identity.Identity, baresip_exe: str | None = None
    ) -> None:
        """Starts a baresip sub-process, and communicates with it over stdio.

        identity: an Identity object with credentials
        baresip_exe: Override auto-detection of the baresip cli tool
        """
        self._baresip_exe = self._resolve_baresip_exe(baresip_exe)
        self.baresip = pexpect.spawn(self._baresip_exe)

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

    def run(self) -> None:
        while True:
            ...
