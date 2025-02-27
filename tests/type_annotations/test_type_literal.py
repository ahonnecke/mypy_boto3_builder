import pytest

from mypy_boto3_builder.type_annotations.type_literal import TypeLiteral


class TestTypeLiteral:
    def setup_method(self) -> None:
        self.result = TypeLiteral("test", ("a", "b"))

    def test_init(self) -> None:
        assert self.result.children == {"a", "b"}
        assert hash(self.result)
        assert TypeLiteral("Type", ["a"]).name == "TypeType"
        assert TypeLiteral("__stringType", ["a", "b"]).name == "ABType"
        assert TypeLiteral("Protocol", ["a"]).name == "ProtocolType"
        assert TypeLiteral("Other", ["a"]).name == "Other"
        with pytest.raises(ValueError):
            TypeLiteral("test", [])

    def test_get_sort_key(self) -> None:
        assert self.result.get_sort_key() == "test"

    def test_render(self) -> None:
        assert self.result.render() == "test"
        assert TypeLiteral("test", ("a", "b")).render() == "test"
        assert TypeLiteral("test", ["a"]).render() == "Literal['a']"

    def test_render_children(self) -> None:
        assert self.result.render_children() == "'a', 'b'"

    def test_get_import_record(self) -> None:
        assert self.result.get_import_record().render() == "from .literals import test"
        assert (
            TypeLiteral("test", ["a"]).get_import_record().render() == "from typing import Literal"
        )

    def test_add_child(self) -> None:
        with pytest.raises(ValueError):
            self.result.add_child(TypeLiteral("test", ("a", "b")))

    def test_is_type(self) -> None:
        assert self.result.is_literal()
        assert not self.result.is_dict()
        assert not self.result.is_list()

    def test_copy(self) -> None:
        assert self.result.copy().children == self.result.children

    def test_is_same(self) -> None:
        assert self.result.is_same(TypeLiteral("other", ["a", "b"]))
        assert not self.result.is_same(TypeLiteral("other", ["a", "b", "c"]))
