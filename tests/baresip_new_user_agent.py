import testslide.dsl as tdsl
from testslide import _ContextData as ContextData
from testslide.dsl import _DSLContext as DSLContext

from .context import PyBareSIPContext


@tdsl.context
def baresip_new_user_agent(context: DSLContext) -> None:
    context.shared_context(PyBareSIPContext)
    context.merge_context("PyBareSIPContext")

    @context.sub_context
    def when_no_flags_are_provided(context: DSLContext) -> None:
        @context.sub_context
        def and_no_password_are_provided(context: DSLContext) -> None:
            @context.before
            async def before(self: ContextData) -> None:
                self.mock_async_callable(target=self.bs, method="uanew").for_call(
                    account="does not matter", flags=None
                ).to_return_value("").and_assert_called_once()

            @context.example
            async def it_calls_uanew_without_flags(self: ContextData) -> None:
                await self.bs.new_user_agent("does not matter")

    @context.sub_context
    def when_flags_are_provided(context: DSLContext) -> None:
        @context.sub_context
        def but_password_is_not_provided(context: DSLContext) -> None:
            @context.before
            async def before(self: ContextData) -> None:
                self.mock_async_callable(target=self.bs, method="uanew").for_call(
                    account="does not matter", flags={"regint": "0"}
                ).to_return_value("").and_assert_called_once()

            @context.example
            async def it_calls_uanew_and_passes_the_flags(self: ContextData) -> None:
                await self.bs.new_user_agent("does not matter", flags={"regint": "0"})

        @context.sub_context
        def and_password_is_provided(context: DSLContext) -> None:
            @context.before
            async def before(self: ContextData) -> None:
                self.mock_async_callable(target=self.bs, method="uanew").for_call(
                    account="does not matter",
                    flags={"regint": "0", "auth_pass": "fred"},
                ).to_return_value("").and_assert_called_once()

            @context.example
            async def it_calls_uanew_and_passes_the_password_in_flags(
                self: ContextData,
            ) -> None:
                await self.bs.new_user_agent(
                    "does not matter", password="fred", flags={"regint": "0"}
                )

    @context.sub_context
    def when_password_is_provided(context: DSLContext) -> None:
        @context.sub_context
        def but_flags_are_not_provided(context: DSLContext) -> None:
            @context.before
            async def before(self: ContextData) -> None:
                self.mock_async_callable(target=self.bs, method="uanew").for_call(
                    account="does not matter", flags={"auth_pass": "hello"}
                ).to_return_value("").and_assert_called_once()

            @context.example
            async def it_calls_uanew_and_passes_the_password_in_flasgs(
                self: ContextData,
            ) -> None:
                await self.bs.new_user_agent("does not matter", password="hello")
