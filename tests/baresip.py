import testslide.dsl as tdsl
from testslide import _ContextData as ContextData
from testslide.dsl import _DSLContext as DSLContext

import pybaresip as pbs
import pybaresip.baresip as bs


@tdsl.context
def PyBareSIP(context: DSLContext) -> None:
    @context.before
    async def before(self: ContextData) -> None:
        self.bs = pbs.PyBareSIP()

    @context.before
    async def mock_invoke(self: ContextData) -> None:
        self.mock_async_callable(target=self.bs, method="invoke").to_return_value(
            "None"
        ).and_assert_not_called()

    @context.sub_context
    def uanew(context: DSLContext) -> None:
        @context.sub_context
        def when_the_account_does_not_start_with_sip(context: DSLContext) -> None:
            @context.before
            async def before(self: ContextData) -> None:
                self.mock_async_callable(
                    target=self.bs, method="invoke"
                ).to_return_value("None").for_call("uanew sip:test@localhost")
                self.mock_callable(target=bs.logger, method="warning").to_return_value(
                    None
                )

            @context.example
            async def it_adds_a_sip_prefix(self: ContextData) -> None:
                await self.bs.uanew("test@localhost")
