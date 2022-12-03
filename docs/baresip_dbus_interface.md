# bareSIP DBus Interface

From an introspection using a QT-based explorer:

    <interface name="com.github.Baresip">
        <method name="invoke">
            <arg type="s" name="command" direction="in"/>
            <arg type="s" name="response" direction="out"/>
        </method>
        <signal name="event">
            <arg type="s" name="class"/>
            <arg type="s" name="evtype"/>
            <arg type="s" name="param"/>
        </signal>
        <signal name="message">
            <arg type="s" name="ua"/>
            <arg type="s" name="peer"/>
            <arg type="s" name="ctype"/>
            <arg type="s" name="body"/>
        </signal>
    </interface>
