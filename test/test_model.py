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

"""Test the model API."""

from test.base import BaseTest

from mustang import Field, Model
from mustang.exceptions import *

class Person(Model):

    """A simple person."""

    first = Field(str)
    last = Field(str)
    age = Field(int)
    height = Field(float)

class TestModels(BaseTest):

    """Test the model API."""

    def setUp(self):
        super().setUp()
        self.db.bind((Person, ))

    def test_create(self):
        """Create several instances."""
        # Create a person with all fields.
        person = Person.create(first="Vincent", last="Le Goff", age=31, height=1.72)
        self.assertEqual(person.first, "Vincent")
        self.assertEqual(person.last, "Le Goff")
        self.assertEqual(person.age, 31)
        self.assertEqual(person.height, 1.72)

        # Check that this person has a valid ID.
        self.assertIsNotNone(person.id)

        # Creating a person with missing fields should raise an error.
        with self.assertRaises(MissingArgument):
            Person.create(first="Vincent")

        # Creating a person with an ID shouldn't be allowed.
        with self.assertRaises(ForbiddenArgument):
            Person.create(id=4, first="Vincent", last="Le Goff",
                    age=31, height=1.72)

    def test_get(self):
        """Test to get a model."""
        person = Person.create(first="Vincent", last="Le Goff", age=31,
                height=1.72)
        self.assertIsNotNone(Person.get(id=person.id))
        self.assertIsNone(Person.get(id=person.id + 1))

    def test_update(self):
        """Test to update a model."""
        person = Person.create(first="Vincent", last="Le Goff", age=31,
                height=1.72)
        person.age = 8
        self.assertEqual(person.age, 8)

        # Check that the same result is obtained through getting the object.
        self.assertEqual(Person.get(id=person.id).age, 8)

        # But editing the ID raises an error.
        with self.assertRaises(SetByDatabase):
            person.id = 32

    def test_delete(self):
        """Create and delete a model."""
        person = Person.create(first="Vincent", last="Le Goff", age=31,
                height=1.72)
        self.assertIsNotNone(Person.get(id=person.id))
        person.delete()
        self.assertIsNone(Person.get(id=person.id))
