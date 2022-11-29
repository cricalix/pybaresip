import testslide.dsl as tdsl
from testslide import _ContextData as ContextData
from testslide.dsl import _DSLContext as DSLContext

import pybaresip.identity as identity


@tdsl.context
def identity_class(context: DSLContext) -> None:
    @context.sub_context
    def the_sip_property(context: DSLContext) -> None:
        @context.sub_context
        def when_user_and_password_are_provided(context: DSLContext) -> None:
            @context.example
            def it_makes_the_password_a_tag(self: ContextData) -> None:
                x = identity.Identity(
                    user="test", password="test", gateway="example.com", port=5061
                )
                self.assertEqual(x.sip, "sip:test@example.com:5061;auth_pass=test")

        @context.sub_context("when auth_pass is set in a flag")
        def when_auth_pass_is_set(context: DSLContext) -> None:
            @context.example
            def it_raises_an_error(self: ContextData) -> None:
                with self.assertRaises(identity.IdentityFlagError):
                    identity.Identity(
                        user="test",
                        password="test",
                        gateway="example.com",
                        port=5061,
                        flags=[{"auth_pass": "fred"}],
                    )

        @context.sub_context
        def when_no_port_is_provided(context: DSLContext) -> None:
            @context.example
            def it_defaults_the_port_to_5060(self: ContextData) -> None:
                x = identity.Identity(
                    user="test",
                    password="test",
                    gateway="example.com",
                )
                self.assertEqual(x.sip, "sip:test@example.com:5060;auth_pass=test")

        @context.sub_context
        def when_a_flag_is_provided(context: DSLContext) -> None:
            @context.example
            def it_appends_all_tags_correctly(self: ContextData) -> None:
                x = identity.Identity(
                    user="test",
                    password="test",
                    gateway="example.com",
                    flags=[{"regint": "0"}],
                )
                self.assertEqual(
                    x.sip, "sip:test@example.com:5060;regint=0;auth_pass=test"
                )
