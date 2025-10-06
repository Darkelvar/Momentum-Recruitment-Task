from datetime import datetime, timezone

import pytest


@pytest.mark.asyncio
class TestBookErrorCases:

    # Creating tests
    @pytest.mark.parametrize("serial_number", ["12345", "1234567", "abcdef", True])
    async def test_create_invalid_serial_number(self, client, serial_number):
        payload = {
            "serial_number": serial_number,
            "title": "Z Mgły Zrodzony",
            "author": "Brandon Sanderson",
        }
        resp = await client.post("/api/v1/books", json=payload)
        print(resp.content)
        assert resp.status_code == 422

    @pytest.mark.parametrize(
        "title,author",
        [(True, "Brandon Sanderson"), ("Z Mgły Zrodzony", True), (123, 123)],
    )
    async def test_create_invalid_title_author_type(self, client, title, author):
        payload = {
            "serial_number": "123456",
            "title": title,
            "author": author,
        }
        resp = await client.post("/api/v1/books", json=payload)
        assert resp.status_code == 422

    @pytest.mark.parametrize(
        "title,author", [("", "Brandon Sanderson"), ("Z Mgły Zrodzony", "")]
    )
    async def test_create_empty_title_or_author(self, client, title, author):
        payload = {
            "serial_number": "123456",
            "title": title,
            "author": author,
        }
        resp = await client.post("/api/v1/books", json=payload)
        assert resp.status_code == 422

    async def test_create_duplicate_serial_number(self, client):
        payload = {
            "serial_number": "999999",
            "title": "Dune",
            "author": "Frank Herbert",
        }
        first = await client.post("/api/v1/books", json=payload)
        assert first.status_code == 200
        second = await client.post("/api/v1/books", json=payload)
        assert second.status_code == 409

    # Getting book tests
    async def test_get_nonexistent_book(self, client):
        resp = await client.get("/api/v1/books/111111")
        assert resp.status_code == 404

    async def test_get_invalid_book_id_type(self, client):
        resp = await client.get("/api/v1/books/notanumber")
        assert resp.status_code == 422

    # Updating book tests
    async def test_update_invalid_is_borrowed_type(self, client):
        payload = {
            "serial_number": "222222",
            "title": "Designing Games",
            "author": "Tynan Sylvester",
        }
        await client.post("/api/v1/books/", json=payload)

        resp = await client.put("/api/v1/books/222222", json={"is_borrowed": "yes"})
        assert resp.status_code == 422

    async def test_update_borrowed_missing_fields(self, client):
        payload = {
            "serial_number": "333333",
            "title": "Designing Games",
            "author": "Tynan Sylvester",
        }
        await client.post("/api/v1/books/", json=payload)

        resp = await client.put("/api/v1/books/333333", json={"is_borrowed": True})
        assert resp.status_code == 422

    async def test_update_return_should_clear_fields(self, client):
        payload = {
            "serial_number": "444444",
            "title": "Designing Games",
            "author": "Tynan Sylvester",
        }
        resp = await client.post("/api/v1/books", json=payload)
        assert resp.status_code == 200

        borrow_payload = {
            "is_borrowed": True,
            "borrowed_at": datetime.now(timezone.utc).isoformat(),
            "borrowed_by": "123456",
        }
        resp = await client.put("/api/v1/books/444444", json=borrow_payload)
        assert resp.status_code == 200
        data = resp.json()
        assert data["is_borrowed"] is True
        assert data["borrowed_by"] is not None
        assert data["borrowed_at"] is not None

        return_payload = {
            "is_borrowed": False,
            "borrowed_at": datetime.now(timezone.utc).isoformat(),
            "borrowed_by": "123456",
        }
        resp = await client.put("/api/v1/books/444444", json=return_payload)
        assert resp.status_code == 200
        data = resp.json()
        assert data["is_borrowed"] is False
        assert data["borrowed_by"] is None
        assert data["borrowed_at"] is None

        await client.put("/api/v1/books/444444", json=borrow_payload)
        return_payload = {
            "is_borrowed": False,
        }
        resp = await client.put("/api/v1/books/444444", json=return_payload)
        assert resp.status_code == 200
        data = resp.json()
        assert data["is_borrowed"] is False
        assert data["borrowed_by"] is None
        assert data["borrowed_at"] is None

    async def test_update_nonexistent_book(self, client):
        resp = await client.put("/api/v1/books/999998", json={"is_borrowed": False})
        assert resp.status_code == 404

    async def test_update_invalid_id_type(self, client):
        resp = await client.put("/api/v1/books/notanumber", json={"is_borrowed": True})
        assert resp.status_code == 422

    # Tests Delete
    async def test_delete_nonexistent_book(self, client):
        resp = await client.delete("/api/v1/books/777777")
        assert resp.status_code == 404

    async def test_delete_invalid_id_type(self, client):
        resp = await client.delete("/api/v1/books/abc123")
        assert resp.status_code == 422
