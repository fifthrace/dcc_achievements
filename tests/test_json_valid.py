import json
import os


def test_detailed_achievements_json():
    json_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "detailed_achievements.json")
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    assert isinstance(data, list), "JSON should contain a list of achievements"

    for entry in data:
        assert isinstance(entry, dict), "Each achievement should be a dictionary"
        assert "title" in entry, "Missing 'title' key"
        assert "description" in entry, "Missing 'description' key"
        assert "url" in entry, "Missing 'url' key"
        url = entry["url"]
        assert isinstance(url, str) and url.startswith("https://"), "URL must start with 'https://'"

