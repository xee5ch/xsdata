from pathlib import Path
from typing import Type

from lxml import etree

from xsdata.formats.dataclass.parsers import JsonParser
from xsdata.formats.dataclass.parsers import XmlParser
from xsdata.formats.dataclass.serializers import JsonSerializer
from xsdata.formats.dataclass.serializers import XmlSerializer


def validate_bindings(schema: Path, clazz: Type):
    __tracebackhide__ = True

    obj = XmlParser().from_path(schema.with_suffix(".xml"), clazz)
    actual = JsonSerializer(indent=4).render(obj)

    expected = schema.with_suffix(".json")
    if expected.exists():
        assert expected.read_text() == actual
        assert obj == JsonParser().from_string(actual, clazz)
    else:
        expected.write_text(actual)

    xml = XmlSerializer(pretty_print=True).render(obj)

    validator = etree.XMLSchema(etree.parse(str(schema)))
    assert validator.validate(etree.fromstring(xml.encode())), validator.error_log

    expected.with_suffix(".xsdata.xml").write_text(xml)
