import testslide.dsl as tdsl
from testslide import _ContextData as ContextData
from testslide.dsl import _DSLContext as DSLContext

from .context import PyBareSIPContext


@tdsl.context
def baresip_conf_reload(context: DSLContext) -> None:
    context.shared_context(PyBareSIPContext)
    context.merge_context("PyBareSIPContext")

    @context.sub_context
    def when_conf_reload_is_called(context: DSLContext) -> None:
        @context.before
        async def before(self: ContextData) -> None:
            self.mock_async_callable(target=self.bs, method="invoke").to_return_value(
                "None"
            ).for_call("conf_reload").and_assert_called_once()

        @context.example
        async def it_calls_invoke_with_conf_reload(self: ContextData) -> None:
            await self.bs.conf_reload()
