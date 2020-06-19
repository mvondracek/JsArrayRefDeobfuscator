#!/usr/bin/env python3
import logging
import sys
import warnings
from contextlib import closing
from enum import unique, Enum
from typing import Optional, Sequence

from jsard import __author__ as package_author, __date__ as package_date, __version__ as package_version
from jsard.config import Config
from jsard.core import deobfuscate_files

__version__ = package_version
__date__ = package_date
__author__ = package_author

LOGGER = logging.getLogger(__name__)


@unique
class ExitCode(Enum):
    """
    Return codes.
    Some are inspired by sysexits.h.
    """
    EX_OK = 0
    """Program terminated successfully."""

    UNKNOWN_FAILURE = 1
    """Program terminated due to unknown error."""

    ARGUMENTS = 2
    """Incorrect or missing arguments provided."""

    KEYBOARD_INTERRUPT = 130
    """Program received SIGINT."""


def main(argv: Optional[Sequence[str]]) -> ExitCode:
    logging.captureWarnings(True)
    warnings.simplefilter('always', ResourceWarning)

    with closing(Config.from_args(argv[1:])) as config:  # argv[0] is program name
        # On error with parsing argument, program was terminated by `Config.from_args` with exit code 2 corresponding to
        # `ExitCode.ARGUMENTS`. If arguments contained -h/--help or --version, program was terminated with exit code 0,
        # which corresponds to `ExitCode.E_OK`
        if config.logging_level:
            logging.basicConfig(format='%(asctime)s %(name)s[%(process)d] %(levelname)s %(message)s',
                                level=config.logging_level)
        else:
            logging.disable(logging.CRITICAL)
        LOGGER.debug('Config parsed from args.')

        deobfuscate_files(config.input, config.output)
    return ExitCode.EX_OK


if __name__ == '__main__':
    exitcode: ExitCode = ExitCode.EX_OK
    try:
        exitcode = main(sys.argv)
    except KeyboardInterrupt:
        print('Stopping.')
        LOGGER.info('received KeyboardInterrupt, stopping')
        exitcode = ExitCode.KEYBOARD_INTERRUPT
    except Exception as e:
        print(str(e), file=sys.stderr)
        exitcode = ExitCode.UNKNOWN_FAILURE
    sys.exit(exitcode.value)
