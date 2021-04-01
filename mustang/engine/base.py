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

"""Module containing the base class for a database engine."""

from abc import ABCMeta, abstractmethod
from typing import Any, Dict, Optional, Type

from mustang.schema.field import Field

Model = 'mustang.schema.model.Model'

class BaseEngine(metaclass=ABCMeta):

    """
    Base class for a database engine.

    Adding a database engine can be done by inheriting from `BaseEngine`
    and setting the new engine in the database.

    """

    def __init__(self, database):
        self.database = database

    @abstractmethod
    def init(self, *args, **kwargs):
        """
        Initialize the database engine.

        Override this method in sub-classes.

        Optional and keyword arguments are supported.

        """

    @abstractmethod
    def close(self):
        """Close the database."""

    @abstractmethod
    def destroy(self):
        """Destroy the database."""

    @abstractmethod
    def create_migration_table(self):
        """
        Create the migration table, if it doesn't exist.

        Notice that this method will be called each time the engine
        is created, so this method should do nothing if the migration
        table already exists.

        """

    @abstractmethod
    def create_table_for(self, model):
        """
        Create a table for this model.

        Notice that this method is called each time the model is
        loaded, therefore this method should do nothing if the table
        already exists.

        Args:
            model (subclass of Model): the model.

        """

    @abstractmethod
    def get_saved_schema_for(self, model):
        """
        Return the saved schema for this model, if any.

        Returning `None` will lead to the database calling `create_table_for`.
        If migrations are supported for this engine, the schema should
        be returned (the list of fields stored in the last migration).

        Args:
            model (subclass of Model): the model.

        """

    @abstractmethod
    def get_instance(self, model: Type[Model],
            fields: Dict[Field, Any]) -> Optional[Model]:
        """
        Get, if possible, an instance with the specified fields.

        If more than one instance would match the specified fields, `None` is returned.  If no match is found, `None` is also returned.  For greater precision, use `select`.

        Args:
            model (subclass of Model): the model class.
            fields (dict): the field dictionary, containing, as keys,
                    field objects, ans as values, whatever value
                    (of whatever type) has been sent by the user.

        Returns:
            instance (Model or None): the instance matching these fields.

        """


    @abstractmethod
    def create_instance(self, instance: Model, fields: Dict[Field, Any]):
        """
        Create and update a model's instance fields.

        Args:
            instance (Model): the model to be populated.
            fields (dict): the dictionary or fields.  This should contain
                    field objects as keys and their values (can be
                    a default value).

        """

    @abstractmethod
    def update_instance(self, instance: Model, field: Field, value: Any):
        """
        If possible, update the specific instance's field.

        Args:
            instance (Model): the model to modify.
            field (Field): the field to be applied.
            value (Any): the field's new value.

        This value is supposed to have been filtered and allowed by the
        instance.

        """

    @abstractmethod
    def delete_instance(self, instance: Model):
        """
        Delete the specified instance from the database.

        Args:
            instance (Model): the model instance to be deleted.

        """
