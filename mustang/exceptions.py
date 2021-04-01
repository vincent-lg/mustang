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

"""Module containing Mustang's exceptions."""

class MustangException(RuntimeError):

    """Exceptions specific to Mustang."""

    pass

class InvalidArgument(MustangException):

    """
    Model creation failed because of arguments.

    This exception is raised when the user wants to create a model
    but a specified (or missing) argument is present.

    """

    def __init__(self, model, field):
        self.model = model.__name__
        self.argument = field.name

class ForbiddenArgument(InvalidArgument):

    """Exception raised when this argument shouldn't be set."""

    def __str__(self):
        return (
                f"model {self.model}: can't set {self.field!r}, "
                "let the database do it"
        )

class MissingArgument(InvalidArgument):

    """Exception raised when the specified field is missing."""

    def __str__(self):
        return f"model {self.model}: missing the argument {self.argument!r}"

class SetByDatabase(InvalidArgument):

    """Exception raised when updating a field only the database should set."""

    def __str__(self):
        return (
                f"model {self.model}: only the database should set "
                f"{self.argument!r}"
        )
