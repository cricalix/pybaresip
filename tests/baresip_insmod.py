import testslide.dsl as tdsl
from testslide import _ContextData as ContextData
from testslide.dsl import _DSLContext as DSLContext

from .context import PyBareSIPContext


@tdsl.context
def baresip_insmod(context: DSLContext) -> None:
    context.shared_context(PyBareSIPContext)
    context.merge_context("PyBareSIPContext")

    @context.sub_context
    def when_insmod_is_called(context: DSLContext) -> None:
        @context.sub_context
        def with_a_single_module_name(context: DSLContext) -> None:
            @context.before
            async def before(self: ContextData) -> None:
                self.mock_async_callable(
                    target=self.bs, method="invoke"
                ).to_return_value("None").for_call(
                    "insmod auconv"
                ).and_assert_called_once()

            @context.example
            async def it_calls_invoke_with_insmod(self: ContextData) -> None:
                await self.bs.insmod(module="auconv")

        @context.sub_context
        def with_a_single_module_name_that_has_whitespace(context: DSLContext) -> None:
            @context.before
            async def before(self: ContextData) -> None:
                self.mock_async_callable(
                    target=self.bs, method="invoke"
                ).to_return_value("None").for_call(
                    "insmod auconv"
                ).and_assert_called_once()

            @context.example
            async def it_calls_invoke_with_insmod(self: ContextData) -> None:
                await self.bs.insmod(module=" auconv ")

        @context.sub_context
        def with_a_space_in_the_module_name(context: DSLContext) -> None:
            @context.example
            async def it_raises(self: ContextData) -> None:
                with self.assertRaisesRegex(Exception, "Module names may not contain"):
                    await self.bs.insmod(module="auconv fred")
