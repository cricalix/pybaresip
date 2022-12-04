import testslide.dsl as tdsl
from testslide import _ContextData as ContextData
from testslide.dsl import _DSLContext as DSLContext
import pybaresip.baresip as pbs
from .context import PyBareSIPContext


@tdsl.context
def baresip_uanext(context: DSLContext) -> None:
    context.shared_context(PyBareSIPContext)
    context.merge_context("PyBareSIPContext")

    @context.sub_context
    def when_the_baresip_major_version_is_2(context: DSLContext) -> None:
        @context.before
        async def before(self: ContextData) -> None:
            self.bs._baresip_version = pbs.BaresipVersion(major=2, minor=0, patch=0)

        @context.sub_context
        def when_uanext_is_called(context: DSLContext) -> None:
            @context.example
            async def it_raises_NotImplementedError(self: ContextData) -> None:
                with self.assertRaises(NotImplementedError):
                    await self.bs.uanext()

    @context.sub_context
    def when_the_baresip_major_version_is_1(context: DSLContext) -> None:
        @context.before
        async def before(self: ContextData) -> None:
            self.bs._baresip_version = pbs.BaresipVersion(major=1, minor=0, patch=0)

        @context.sub_context
        def when_uanext_is_called(context: DSLContext) -> None:
            @context.before
            async def before(self: ContextData) -> None:
                self.mock_async_callable(
                    target=self.bs, method="invoke"
                ).to_return_value("None").for_call("uanext").and_assert_called_once()

            @context.example
            async def it_calls_invoke_with_uanext(self: ContextData) -> None:
                await self.bs.uanext()

    @context.sub_context
    def when_the_baresip_major_version_is_0(context: DSLContext) -> None:
        @context.sub_context
        def when_uanext_is_called(context: DSLContext) -> None:
            @context.example
            async def it_raises_Exception(self: ContextData) -> None:
                with self.assertRaisesRegex(Exception, r"This function only works.*"):
                    await self.bs.uanext()
