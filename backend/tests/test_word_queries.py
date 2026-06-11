import pytest


class TestListWords:
    def test_list_words_no_filter(self, client):
        response = client.get("/api/words")
        assert response.status_code == 200
        data = response.get_json()
        assert isinstance(data, list)
        assert len(data) == 5
        regions = [word["region"] for word in data]
        assert "江西" in regions
        assert "广东" in regions
        assert "四川" in regions
        assert "上海" in regions
        assert "陕西" in regions

    def test_list_words_filter_by_region(self, client):
        response = client.get("/api/words?region=四川")
        assert response.status_code == 200
        data = response.get_json()
        assert isinstance(data, list)
        assert len(data) == 1
        assert data[0]["region"] == "四川"
        assert data[0]["dialect_word"] == "晓得"

    def test_list_words_filter_by_region_empty_result(self, client):
        response = client.get("/api/words?region=不存在的地区")
        assert response.status_code == 200
        data = response.get_json()
        assert isinstance(data, list)
        assert len(data) == 0

    def test_list_words_search_by_keyword(self, client):
        response = client.get("/api/words?keyword=晓得")
        assert response.status_code == 200
        data = response.get_json()
        assert isinstance(data, list)
        assert len(data) == 1
        assert data[0]["dialect_word"] == "晓得"

    def test_list_words_search_by_keyword_mandarin(self, client):
        response = client.get("/api/words?keyword=吃饭")
        assert response.status_code == 200
        data = response.get_json()
        assert isinstance(data, list)
        assert len(data) == 1
        assert data[0]["mandarin"] == "吃饭"

    def test_list_words_search_by_keyword_match_in_dialect_and_mandarin(self, client):
        response = client.get("/api/words?keyword=饭")
        assert response.status_code == 200
        data = response.get_json()
        assert isinstance(data, list)
        assert len(data) == 1
        word = data[0]
        assert "饭" in word["dialect_word"] or "饭" in word["mandarin"]

    def test_list_words_region_and_keyword_combined(self, client):
        response = client.get("/api/words?region=四川&keyword=晓得")
        assert response.status_code == 200
        data = response.get_json()
        assert isinstance(data, list)
        assert len(data) == 1
        assert data[0]["region"] == "四川"
        assert data[0]["dialect_word"] == "晓得"

    def test_list_words_region_and_keyword_no_match(self, client):
        response = client.get("/api/words?region=广东&keyword=晓得")
        assert response.status_code == 200
        data = response.get_json()
        assert isinstance(data, list)
        assert len(data) == 0

    def test_list_words_empty_keyword(self, client):
        response = client.get("/api/words?keyword=")
        assert response.status_code == 200
        data = response.get_json()
        assert isinstance(data, list)
        assert len(data) == 5

    def test_list_words_empty_region(self, client):
        response = client.get("/api/words?region=")
        assert response.status_code == 200
        data = response.get_json()
        assert isinstance(data, list)
        assert len(data) == 5
