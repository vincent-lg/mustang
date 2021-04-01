# Copyright (c) 2021, LE GOFF Vincent
# All rights reserved.

# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:

# * Redistributions of source code must retain the above copyright notice, this
#   list of conditions and the following disclaimer.

# * Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.

# * Neither the name of ytranslate nor the names of its
#   contributors may be used to endorse or promote products derived from
#   this software without specific prior written permission.

# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.


"""Module containing the base class BaseCommand, described below."""

from argparse import ArgumentParser

class BaseCommand:

    """Base class of a command-line tool.

    This class is mainly a bridge between a set of commands and
    the 'argparse' module.  The latter manage sub-commands, but
    the automation of function calls isn't very straightforward.
    This wrapper is used to create a simple (and as clean as
    possible) distinction between sub-commands.

    To create a new command, you should inherit from this class.
    The '__init__' method can be redefined to add arguments to the
    parser (the 'parser' attribute).  The 'execute' method is
    also to be redefined.

    """

    def __init__(self, parser=None):
        parser = parser or ArgumentParser()
        self.parser = parser
        self.subparsers = None
        self.parser.set_defaults(func=self.execute)

    def add_subcommand(self, CommandClass):
        """Add a sub-command."""
        if self.subparsers is None:
            self.subparsers = self.parser.add_subparsers()
        parser = self.subparsers.add_parser(CommandClass.name)
        command = CommandClass(parser)

    def execute(self, args):
        """Execute the command."""
        raise NotImplementedError
