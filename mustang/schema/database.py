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

"""Class describing a database, working with a database engine."""

from typing import Optional, Sequence, Type, Union

from mustang.engine.base import BaseEngine
from mustang.engine.sqlite import Sqlite3Engine
from mustang.schema.model import Model, MODELS

class Database:

    """
    A Mustang database, linking the ORM with an engine.

    This is the main class for all databases.  It is linked to a database
    engine (sqlite by default) and will delegate to this engine most
    of the tasks it should perform.  However, this class also provides
    the true meat of the Object-Relational Mapping (ROM).

    It is possible to ovverride this class to change most aspects of the
    library, optimize some details, alter some behavior.

    """

    def __init__(self):
        self._engine = Sqlite3Engine(self)
        self._models = ()

    @property
    def engine(self):
        """Return the database engine currently being used."""
        return self._engine
    @engine.setter
    def engine(self, engine: Union[BaseEngine, Type[BaseEngine]]):
        """
        Change the engine in use.

        Args:
            engine (Engine or subclass of Engine): the new database engine.
                    It can be instantiated or not.  It is preferrable
                    to let this property handles instantiation.

        """
        if issubclass(engine, BaseEngine):
            engine = engine(self)
        else:
            engine.database = self

        self._engine = engine

    def bind(self, models: Optional[Sequence[Model]] = None):
        """
        Bind this database to the specified, or the detected, models.

        If this method is called with no argument, all imported classes
        inherited from models are bound with this database.  You can
        also spedcify a list (or a sequence of any type) of models to bind.

        Args:
            models (optional, sequence of Model): the models to bind.

        """
        models = MODELS if models is None else models

        # Check that all models equire no external bound models.
        for cls in models:
            # ... add checks here.
            cls.load_schema()
            cls._engine = self._engine

        self.models = tuple(models)

    def init(self, *args, **kwargs):
        """
        Initialize (create if necessary) the database.

        Positional or keyword arguments are sent to the database engine.

        """
        self._engine.init(*args, **kwargs)
        self._engine.create_migration_table()

        # Check the model schemas.
        for cls in self.models:
            saved_schema = self._engine.get_saved_schema_for(cls)
            if saved_schema is None:
                self._engine.create_table_for(cls)
            else:
                diff = self.create_diff_between(saved_schema, cls._schema)
                if diff is not None:
                    self._engine.apply_diff_for(cls, diff)

    def close(self):
        """Close the database."""
        return self._engine.close()

    def destroy(self):
        """Destroy the database."""
        self._engine.destroy()
