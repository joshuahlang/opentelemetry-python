# Copyright The OpenTelemetry Authors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# pylint: disable-all

from unittest import TestCase
from unittest.mock import patch

from opentelemetry.configuration import Configuration  # type: ignore


class TestConfiguration(TestCase):
    def setUp(self):
        # This is added here to force a reload of the whole Configuration
        # class, resetting its internal attributes so that each tests starts
        # with a clean class.
        from opentelemetry.configuration import Configuration  # type: ignore

    def tearDown(self):
        from opentelemetry.configuration import Configuration  # type: ignore

    def test_singleton(self):
        self.assertIsInstance(Configuration(), Configuration)
        self.assertIs(Configuration(), Configuration())

    @patch.dict(
        "os.environ",  # type: ignore
        {
            "OPENTELEMETRY_PYTHON_METER_PROVIDER": "meter_provider",
            "OPENTELEMETRY_PYTHON_TRACER_PROVIDER": "tracer_provider",
            "OPENTELEMETRY_PYTHON_OThER": "other",
            "OPENTELEMETRY_PYTHON_OTHER_7": "other_7",
            "OPENTELEMETRY_PTHON_TRACEX_PROVIDER": "tracex_provider",
        },
    )
    def test_environment_variables(self):  # type: ignore
        self.assertEqual(
            Configuration().METER_PROVIDER, "meter_provider"
        )  # pylint: disable=no-member
        self.assertEqual(
            Configuration().TRACER_PROVIDER, "tracer_provider"
        )  # pylint: disable=no-member
        self.assertEqual(
            Configuration().OThER, "other"
        )  # pylint: disable=no-member
        self.assertEqual(
            Configuration().OTHER_7, "other_7"
        )  # pylint: disable=no-member
        self.assertIsNone(Configuration().TRACEX_PROVIDER)

    @patch.dict(
        "os.environ",  # type: ignore
        {"OPENTELEMETRY_PYTHON_TRACER_PROVIDER": "tracer_provider"},
    )
    def test_property(self):
        with self.assertRaises(AttributeError):
            Configuration().TRACER_PROVIDER = "new_tracer_provider"

    def test_slots(self):
        with self.assertRaises(AttributeError):
            Configuration().XYZ = "xyz"  # pylint: disable=assigning-non-slot

    def test_getattr(self):
        self.assertIsNone(Configuration().XYZ)
