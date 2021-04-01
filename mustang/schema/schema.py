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

"""Module defining the model's schema."""

from enum import Enum

from mustang.exceptions import ForbiddenArgument, MissingArgument

_NOT_SET = object()

class Operation(Enum):

    """Operation type for schema editing/extracting."""

    CREATION = "creation"
    PORTION = "portion"


class ModelSchema:

    """
    Class to represent the model's current (and past) schema.
    """

    def __init__(self, model, fields):
        self.model = model
        self.fields = fields
        self.primary_key = next(field for field in fields.values()
                if field.primary_key)

    def extract(self, args, kwargs, operation: Operation = Operation.PORTION):
        """Extract and return a dictionary of {key: value} for this schema."""
        fields = iter(self.fields.values())
        for arg in args:
            field = None
            while field is None and (not default or field.set_by_database):
                try:
                    field = next(fields)
                except StopIteration:
                    raise ValueError(
                            f"field {arg!r}: cannot find a matching "
                            "field.  It might be better to use "
                            "keyword arguments."
                    )

            key = field.name
            if key in kwargs:
                raise ValueError(
                        f"argument {name!r} has been defined both with "
                        "a positional and keyword argument.   It might "
                        "be good to use only keyword arguments to avoid "
                        "this confusion"
                )
            kwargs[key] = arg

        # Now check kwargs
        fields = {}
        for field in self.fields.values():
            value = kwargs.get(field.name, _NOT_SET)
            if value is _NOT_SET:
                if operation is Operation.PORTION:
                    continue

                if field.has_default:
                    value = field.default
                elif field.set_by_database:
                    continue
                else:
                    raise MissingArgument(self.model, field)
            elif operation is Operation.CREATION and field.set_by_database:
                raise ForbiddenArgument(self.model, field)

            fields[field] = value

        return fields
