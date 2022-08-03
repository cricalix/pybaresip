import pybaresip as pbs

import testslide.dsl as tdsl
from testslide import _ContextData as ContextData
from testslide.dsl import _DSLContext as DSLContext
import testslide.strict_mock as tsm
import pexpect


@tdsl.context
def baresip_exe_resolution(context: DSLContext) -> None:
    @context.sub_context
    def when_no_exe_path_is_provided(context: DSLContext) -> None:
        @context.sub_context
        def and_baresip_is_in_the_path(context: DSLContext) -> None:
            @context.before
            def disable_pexpect_spawning(self: ContextData) -> None:
                mock_spawn = tsm.StrictMock(template=pexpect.spawn)
                self.mock_constructor(
                    target="pexpect", class_name="spawn"
                ).to_return_value(mock_spawn).and_assert_called_once()

            @context.before
            def mock_path_existence_to_true(self: ContextData) -> None:
                self.mock_callable(target="shutil", method="which").for_call(
                    cmd="baresip"
                ).to_return_value("/dummy/path/baresip").and_assert_called()

            @context.example
            def it_resolves_the_full_path(self: ContextData) -> None:
                ident = pbs.Identity(
                    user="unittest", password="unittest", gateway="unittest"
                )
                bs = pbs.BareSIP(ident)
                self.assertEqual(bs._baresip_exe, "/dummy/path/baresip")

        @context.sub_context
        def and_baresip_is_not_in_the_path(context: DSLContext) -> None:
            @context.before
            def mock_path_existence_to_None(self: ContextData) -> None:
                self.mock_callable(target="shutil", method="which").for_call(
                    cmd="baresip"
                ).to_return_value(None).and_assert_called()

            @context.example
            def it_raises_BaresipNotFound(self: ContextData) -> None:
                ident = pbs.Identity(
                    user="unittest", password="unittest", gateway="unittest"
                )
                with self.assertRaises(pbs.exceptions.BaresipNotFound) as ex:
                    pbs.BareSIP(ident)
                self.assertIn("via PATH environment", str(ex.exception))

    @context.sub_context
    def when_an_exe_path_is_provided(context: DSLContext) -> None:
        @context.sub_context
        def and_baresip_is_in_the_path(context: DSLContext) -> None:
            @context.before
            def disable_pexpect_spawning(self: ContextData) -> None:
                mock_spawn = tsm.StrictMock(template=pexpect.spawn)
                self.mock_constructor(
                    target="pexpect", class_name="spawn"
                ).to_return_value(mock_spawn).and_assert_called_once()

            @context.before
            def mock_path_existence_to_true(self: ContextData) -> None:
                self.mock_callable(target="os.path", method="isfile").for_call(
                    path="/dummy/path/baresip"
                ).to_return_value(True).and_assert_called()

            @context.example
            def it_resolves_the_full_path(self: ContextData) -> None:
                ident = pbs.Identity(
                    user="unittest", password="unittest", gateway="unittest"
                )
                bs = pbs.BareSIP(ident, baresip_exe="/dummy/path/baresip")
                self.assertEqual(bs._baresip_exe, "/dummy/path/baresip")

        @context.sub_context
        def and_baresip_is_not_in_the_path(context: DSLContext) -> None:
            @context.before
            def mock_path_existence_to_true(self: ContextData) -> None:
                self.mock_callable(target="os.path", method="isfile").for_call(
                    path="/dummy/path/baresip"
                ).to_return_value(False).and_assert_called()

            @context.example
            def it_raises_BaresipNotFound(self: ContextData) -> None:
                ident = pbs.Identity(
                    user="unittest", password="unittest", gateway="unittest"
                )
                with self.assertRaises(pbs.exceptions.BaresipNotFound) as ex:
                    pbs.BareSIP(ident, baresip_exe="/dummy/path/baresip")
                self.assertIn("/dummy/path/baresip", str(ex.exception))