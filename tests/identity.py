import pybaresip.identity as identity
import testslide.dsl as tdsl
from testslide import _ContextData as ContextData
from testslide.dsl import _DSLContext as DSLContext


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
