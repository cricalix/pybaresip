import testslide.dsl as tdsl
from testslide import _ContextData as ContextData
from testslide.dsl import _DSLContext as DSLContext

import pybaresip.baresip as bs
import pybaresip.exceptions as pbs_ex

from .context import PyBareSIPContext

BANNER = """.------------------------------------------------------------.
|                      baresip 2.9.0                         |
|                                                            |
| Baresip is a portable and modular SIP User-Agent           |
| with audio and video support                               |
|                                                            |
| License:   BSD                                             |
| Homepage:  https://github.com/baresip/baresip              |
|                                                            |
'------------------------------------------------------------'"""


@tdsl.context
def baresip_version(context: DSLContext) -> None:
    context.shared_context(PyBareSIPContext)
    context.merge_context("PyBareSIPContext")

    @context.sub_context
    def when_the_baresip_banner_matches_the_expected_pattern(
        context: DSLContext,
    ) -> None:
        @context.before
        async def before(self: ContextData) -> None:
            self.mock_async_callable(target=self.bs, method="invoke").to_return_value(
                BANNER
            ).for_call("about").and_assert_called()

        @context.example
        async def it_returns_a_BaresipVersion_object(self: ContextData) -> None:
            x = await self.bs.version()
            self.assertIsInstance(x, bs.BaresipVersion)

        @context.example
        async def it_extracts_the_version_correctly(self: ContextData) -> None:
            x = await self.bs.version()
            self.assertEqual(2, x.major, "Major version")
            self.assertEqual(9, x.minor, "Minor version")
            self.assertEqual(0, x.patch, "Patch version")

    @context.sub_context
    def when_the_banner_does_not_match_the_expected_pattern(
        context: DSLContext,
    ) -> None:
        @context.before
        async def before(self: ContextData) -> None:
            self.mock_async_callable(target=self.bs, method="about").to_return_value(
                "totally radical"
            ).and_assert_called()

        @context.example
        async def it_raises_an_exception(self: ContextData) -> None:
            with self.assertRaises(pbs_ex.BaresipVersionError) as e:
                await self.bs.version()
            self.assertIn("Could not determine version", str(e.exception))
