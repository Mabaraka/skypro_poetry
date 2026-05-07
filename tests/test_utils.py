import json
from pathlib import Path

from src.utils import convert_json


def test_convert_json_success(tmp_path, json_transactions):
    tmp_file = tmp_path / "file.json"
    with open(tmp_file, "w", encoding="utf-8") as f:
        json.dump(json_transactions, f, ensure_ascii=False)

    result = convert_json(str(tmp_file))

    assert result == json_transactions


def test_convert_json_wrong_path():
    path = Path("wrong_path")

    result = convert_json(str(path))

    assert not path.exists()
    assert result == []


def test_convert_json_empty_file(tmp_path):
    tmp_file = tmp_path / "file.json"
    tmp_file.touch()

    result = convert_json(str(tmp_file))

    assert tmp_file.exists()
    assert result == []


def test_convert_json_wrong_structure_format(tmp_path):
    tmp_file = tmp_path / "file.json"
    tmp_file.write_text(json.dumps({"a": 1, "b": 2}))

    result = convert_json(str(tmp_file))

    assert tmp_file.exists()
    assert result == []
