from testslide import _ContextData as ContextData
from testslide.dsl import _DSLContext as DSLContext

import pybaresip.baresip as bs


def PyBareSIPContext(context: DSLContext) -> None:
    """
    Sets up self.bs as an instance of the class being tested.

    Sets up a default mock of the invoke method to catch failures at mocking.
    """

    @context.before
    async def before(self: ContextData) -> None:
        self.bs = bs.PyBareSIP()

    @context.before
    async def mock_invoke(self: ContextData) -> None:
        self.mock_async_callable(target=self.bs, method="invoke").to_return_value(
            "None"
        ).and_assert_not_called()
