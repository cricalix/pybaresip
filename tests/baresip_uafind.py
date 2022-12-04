import testslide.dsl as tdsl
from testslide import _ContextData as ContextData
from testslide.dsl import _DSLContext as DSLContext

from .context import PyBareSIPContext


@tdsl.context
def baresip_uafind(context: DSLContext) -> None:
    context.shared_context(PyBareSIPContext)
    context.merge_context("PyBareSIPContext")

    @context.sub_context
    def when_uafind_is_called(context: DSLContext) -> None:
        @context.before
        async def before(self: ContextData) -> None:
            self.mock_async_callable(target=self.bs, method="invoke").to_return_value(
                "None"
            ).for_call("uafind sip:test@localhost:5060").and_assert_called_once()

        @context.example
        async def it_calls_invoke_with_uafind(self: ContextData) -> None:
            await self.bs.uafind(account="sip:test@localhost:5060")
