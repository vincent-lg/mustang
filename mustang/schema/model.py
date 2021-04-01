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

"""Base class for all models."""

from typing import Dict, Optional, Type

from mustang.exceptions import SetByDatabase
from mustang.schema.field import Field
from mustang.schema.schema import ModelSchema, Operation

MODELS = set()
_NOT_SET = object()

class MetaModel(type):

    """Metaclass for all models."""

    def __new__(cls, name, bases, attrs):
        cls = super().__new__(cls, name, bases, attrs)
        if cls.__name__ != "Model":
            MODELS.add(cls)
            cls._fields = MetaModel.get_fields(cls)
        return cls

    @staticmethod
    def get_fields(model: Type["Model"]) -> Dict[str, Field]:
        """Get the tuple of fields from a model."""
        fields = {}
        for key, value in tuple(model.__dict__.items()):
            if isinstance(value, Field):
                value.name = key
                fields[key] = value

        # If there is no PrimaryKey field, add one.
        if not any(field for field in fields.values() if field.primary_key):
            if any(field for field in fields.values() if field.name == "id"):
                raise ValueError(
                        f"model {model!r}: no primary key is defined, but "
                        "there already exists a field of name 'id', so no "
                        "key can be added.  You should specify ONE "
                        "primary key in your model class"
                )

            primary_key = Field(int, primary_key=True, name="id")
            fields = dict(id=primary_key, **fields)
        elif len(field for field in fields.values() if field.primary_key) < 1:
            raise ValueError(
                    f"model {model!r}: there are at least two primary key "
                    "fields, which is not allowed.  Please choose one "
                    "primary key field, although you can have secondary "
                    "key fields, and composite keys, if you want"
            )

        return fields

    def __str__(self):
        text = f"{self.__name__} ("
        if self._fields:
            indent = "\n" + " " * 4
            text += indent + indent.join(
                    str(field) for field in self._fields.values())
            text += "\n)"
        else:
            text += ")"

        return text

    def load_schema(self):
        """Load the model's schema."""
        self._schema = ModelSchema(self, self._fields)

    def create(self, *args, **kwargs):
        """Create and return a model instance."""
        fields = self._schema.extract(args, kwargs, Operation.CREATION)
        return self._engine.create_instance(self, fields)

    def get(self, *args, **kwargs):
        """
        Get a model instance from the database.

        Optional and keyword arguments are supported.

        Returns:
            instance (Model): the model instance or None.

        Note:
            If no model is found, or if several models with these fields
            are found, return None.

        """
        fields = self._schema.extract(args, kwargs, operation=Operation.PORTION)
        return self._engine.get_instance(self, fields)


class Model(metaclass=MetaModel):

    """
    Base class for all database models.

    Models match tables in a database.  A class in-code contains fields,
    each field being a database column when stored.  Models are not
    directly linked to a database, though once instantiated, models
    usually can connect to a database engine to perform operations.
    A database can decide to map all models (all imported classes inheriting
    from `Model`) or a specific set.

    """

    _alt_name: Optional[str] = None
    _engine: Optional['mustang.engine.base.BaseEngine'] = None
    _fields = {}

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        self._has_init = True

    def __repr__(self):
        pk = self._schema.primary_key
        value = getattr(self, pk.name)
        return f"<{type(self).__name__}({pk.name}={value!r})>"

    def __setattr__(self, key, value):
        """If a field is updated, notify the database engine."""
        field = self._fields.get(key, _NOT_SET)
        has_init = getattr(self, "_has_init", False)
        if has_init and field and not key.startswith("_"):
            if field.set_by_database:
                raise SetByDatabase(type(self), field)

            field.accept(value)
            self._engine.update_instance(self, field, value)
        else:
            super().__setattr__(key, value)

    def delete(self):
        """Remove this object from the database."""
        return self._engine.delete_instance(self)
