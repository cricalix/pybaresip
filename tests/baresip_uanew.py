import testslide.dsl as tdsl
from testslide import _ContextData as ContextData
from testslide.dsl import _DSLContext as DSLContext

import pybaresip.baresip as bs

from .context import PyBareSIPContext


@tdsl.context
def baresip_uanew(context: DSLContext) -> None:
    context.shared_context(PyBareSIPContext)
    context.merge_context("PyBareSIPContext")

    @context.sub_context
    def when_no_flags_are_provided(context: DSLContext) -> None:
        @context.sub_context
        def and_the_account_does_not_start_with_sip(context: DSLContext) -> None:
            @context.before
            async def before(self: ContextData) -> None:
                self.mock_async_callable(
                    target=self.bs, method="invoke"
                ).to_return_value("None").for_call(
                    "uanew sip:test@localhost"
                ).and_assert_called_once()
                self.mock_callable(target=bs.logger, method="warning").to_return_value(
                    None
                ).and_assert_called_once()

            @context.example
            async def it_adds_a_sip_prefix_and_calls_invoke(self: ContextData) -> None:
                await self.bs.uanew("test@localhost")

        @context.sub_context
        def and_the_account_is_properly_formatted(context: DSLContext) -> None:
            @context.before
            async def before(self: ContextData) -> None:
                self.mock_async_callable(
                    target=self.bs, method="invoke"
                ).to_return_value("None").for_call(
                    "uanew sip:test@localhost"
                ).and_assert_called_once()

            @context.example
            async def it_calls_invoke(self: ContextData) -> None:
                await self.bs.uanew("sip:test@localhost")

    @context.sub_context
    def when_flags_are_provided(context: DSLContext) -> None:
        @context.sub_context
        def and_the_account_is_properly_formatted(context: DSLContext) -> None:
            @context.sub_context
            def and_a_single_flag_is_provided(context: DSLContext) -> None:
                @context.before
                async def before(self: ContextData) -> None:
                    self.mock_async_callable(
                        target=self.bs, method="invoke"
                    ).to_return_value("None").for_call(
                        "uanew sip:test@localhost;regint=0"
                    ).and_assert_called_once()

                @context.example
                async def it_calls_invoke_with_the_flag_appended(
                    self: ContextData,
                ) -> None:
                    await self.bs.uanew("sip:test@localhost", flags={"regint": "0"})

            @context.sub_context
            def and_more_than_one_flag_is_provided(context: DSLContext) -> None:
                @context.before
                async def before(self: ContextData) -> None:
                    self.mock_async_callable(
                        target=self.bs, method="invoke"
                    ).to_return_value("None").for_call(
                        "uanew sip:test@localhost;regint=0;auth_pass=fred"
                    ).and_assert_called_once()

                @context.example
                async def it_calls_invoke_with_the_flags_appended(
                    self: ContextData,
                ) -> None:
                    await self.bs.uanew(
                        "sip:test@localhost", flags={"regint": "0", "auth_pass": "fred"}
                    )
