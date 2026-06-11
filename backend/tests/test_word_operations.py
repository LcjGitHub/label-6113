import pytest


class TestCreateWord:
    def test_create_word_success(self, client):
        word_data = {
            "dialect_word": "测试词",
            "mandarin": "测试普通话",
            "pinyin": "cè shì cí",
            "region": "北京",
            "example": "这是一个测试例句。",
            "source": "测试来源",
            "remark": "测试备注",
        }
        response = client.post("/api/words", json=word_data)
        assert response.status_code == 201
        data = response.get_json()
        assert data["dialect_word"] == "测试词"
        assert data["mandarin"] == "测试普通话"
        assert data["pinyin"] == "cè shì cí"
        assert data["region"] == "北京"
        assert data["example"] == "这是一个测试例句。"
        assert data["source"] == "测试来源"
        assert data["remark"] == "测试备注"
        assert "id" in data
        assert isinstance(data["id"], int)

    def test_create_word_missing_dialect_word(self, client):
        word_data = {
            "mandarin": "测试普通话",
            "region": "北京",
        }
        response = client.post("/api/words", json=word_data)
        assert response.status_code == 400
        data = response.get_json()
        assert "error" in data
        assert "方言词" in data["error"]

    def test_create_word_missing_mandarin(self, client):
        word_data = {
            "dialect_word": "测试词",
            "region": "北京",
        }
        response = client.post("/api/words", json=word_data)
        assert response.status_code == 400
        data = response.get_json()
        assert "error" in data
        assert "普通话" in data["error"]

    def test_create_word_missing_region(self, client):
        word_data = {
            "dialect_word": "测试词",
            "mandarin": "测试普通话",
        }
        response = client.post("/api/words", json=word_data)
        assert response.status_code == 400
        data = response.get_json()
        assert "error" in data
        assert "地区" in data["error"]

    def test_create_word_empty_dialect_word(self, client):
        word_data = {
            "dialect_word": "   ",
            "mandarin": "测试普通话",
            "region": "北京",
        }
        response = client.post("/api/words", json=word_data)
        assert response.status_code == 400
        data = response.get_json()
        assert "error" in data
        assert "方言词" in data["error"]

    def test_create_word_only_required_fields(self, client):
        word_data = {
            "dialect_word": "测试词",
            "mandarin": "测试普通话",
            "region": "北京",
        }
        response = client.post("/api/words", json=word_data)
        assert response.status_code == 201
        data = response.get_json()
        assert data["dialect_word"] == "测试词"
        assert data["mandarin"] == "测试普通话"
        assert data["region"] == "北京"
        assert data["pinyin"] == ""
        assert data["example"] == ""
        assert data["source"] == ""
        assert data["remark"] == ""

    def test_create_word_no_body(self, client):
        response = client.post("/api/words")
        assert response.status_code == 400
        data = response.get_json()
        assert "error" in data


class TestBatchDelete:
    def test_batch_delete_success(self, client):
        response = client.get("/api/words")
        words = response.get_json()
        word_ids = [word["id"] for word in words[:3]]

        delete_response = client.post("/api/words/batch-delete", json={"ids": word_ids})
        assert delete_response.status_code == 200
        delete_data = delete_response.get_json()
        assert delete_data["deleted_count"] == 3

        verify_response = client.get("/api/words")
        verify_data = verify_response.get_json()
        assert len(verify_data) == 2
        remaining_ids = [word["id"] for word in verify_data]
        for wid in word_ids:
            assert wid not in remaining_ids

    def test_batch_delete_empty_array(self, client):
        response = client.post("/api/words/batch-delete", json={"ids": []})
        assert response.status_code == 400
        data = response.get_json()
        assert "error" in data

    def test_batch_delete_no_ids_field(self, client):
        response = client.post("/api/words/batch-delete", json={})
        assert response.status_code == 400
        data = response.get_json()
        assert "error" in data

    def test_batch_delete_invalid_ids(self, client):
        response = client.post("/api/words/batch-delete", json={"ids": ["abc", "def"]})
        assert response.status_code == 400
        data = response.get_json()
        assert "error" in data

    def test_batch_delete_mixed_valid_and_invalid_ids(self, client):
        response = client.get("/api/words")
        words = response.get_json()
        valid_id = words[0]["id"]

        delete_response = client.post(
            "/api/words/batch-delete", json={"ids": [valid_id, 9999, "abc"]}
        )
        assert delete_response.status_code == 200
        delete_data = delete_response.get_json()
        assert delete_data["deleted_count"] == 1

    def test_batch_delete_nonexistent_ids(self, client):
        response = client.post("/api/words/batch-delete", json={"ids": [9999, 8888]})
        assert response.status_code == 200
        data = response.get_json()
        assert data["deleted_count"] == 0

    def test_batch_delete_single_id(self, client):
        response = client.get("/api/words")
        words = response.get_json()
        word_id = words[0]["id"]

        delete_response = client.post("/api/words/batch-delete", json={"ids": [word_id]})
        assert delete_response.status_code == 200
        delete_data = delete_response.get_json()
        assert delete_data["deleted_count"] == 1

        verify_response = client.get(f"/api/words/{word_id}")
        assert verify_response.status_code == 404

    def test_batch_delete_string_ids(self, client):
        response = client.get("/api/words")
        words = response.get_json()
        word_ids = [str(word["id"]) for word in words[:2]]

        delete_response = client.post("/api/words/batch-delete", json={"ids": word_ids})
        assert delete_response.status_code == 200
        delete_data = delete_response.get_json()
        assert delete_data["deleted_count"] == 2
