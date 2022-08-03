# Experiments and failures

## sarge

### PIPE mode

[sarge](https://sarge.readthedocs.io/en/latest/index.html) is a module for interacting with processes via stdio. It was tested with

```python
from sarge import Command, Capture
from subprocess import PIPE
import time

p = Command("baresip", stdout=Capture(buffer_size=1))
p.run(input=PIPE, async_=True)
print(p.stdout.readlines())
time.sleep(0.2)
p.stdin.write(b"/quit\n")
p.wait()
```

Unfortunately, the **/quit** never seems to make it to `baresip` - the **stdin.write** happens, because the program moves on to the **p.wait()** call and sits waiting for the program to do whatever it's doing.

### Feeder mode

Feeder mode appears to work.

```python
from sarge import Command, Capture, Feeder

f = Feeder()
p = Command("baresip", stdout=Capture(buffer_size=1))
p.run(input=f, async_=True)
output = p.stdout.readlines()

if b"baresip is ready.\n" in output:
    print("baresip up")
f.feed(b"/quit\n")
f.close()
p.wait()
```

For reasons as yet unknown, *some* of the interaction around **/quit** prints to the terminal where the script is running, but not all of it.

```
baresip up
/quit
Quit
```

*baresip up* is expected, but the command and the response are not. Looks like an issue with **baresip** not doing ioctls correctly, and thus picking up the pty of the terminal that's running the python code and using that for output/echo. This means that sarge, as nice as it is, is not viable for wrapping **baresip** until they fix that issue (and on Debian, the packaged version is 1.0.0, while upstream is at 2.5.0+.)