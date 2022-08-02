[![Build Status](https://github.com/facebook/TestSlide/workflows/CI/badge.svg)](https://github.com/cricalix/pybaresip/actions?query=workflow%3ACI)
[![GitHub license](https://img.shields.io/github/license/cricalix/pybaresip)](LICENSE)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

pybaresip is a wrapper around the **baresip** executable, and uses **baresip** to handle all of the work related to setting up a SIP session, and transmitting audio over the session.

## Goals

Initially:

* Subclass `threading.Thread` to stay out of the way of calling programs
* Support registered and non-registered calling
* Support text-to-speech via callbacks
* Use current Python3 syntax for type hints

# Credits

For the original version that inspired this one - [baresipy](https://github.com/OpenJarbas/baresipy)
