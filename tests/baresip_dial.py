import testslide.dsl as tdsl
from testslide import _ContextData as ContextData
from testslide.dsl import _DSLContext as DSLContext

from .context import PyBareSIPContext


@tdsl.context
def baresip_dial(context: DSLContext) -> None:
    context.shared_context(PyBareSIPContext)
    context.merge_context("PyBareSIPContext")

    @context.sub_context
    def when_dial_is_called(context: DSLContext) -> None:
        @context.before
        async def before(self: ContextData) -> None:
            self.mock_async_callable(target=self.bs, method="invoke").to_return_value(
                "None"
            ).for_call("dial sip:test@localhost").and_assert_called_once()

        @context.example
        async def it_calls_invoke_with_dial(self: ContextData) -> None:
            await self.bs.dial("sip:test@localhost")
