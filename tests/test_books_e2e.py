import pytest


@pytest.mark.asyncio
async def test_books_end_to_end(client):
    create_payload = {
        "serial_number": "123456",
        "title": "Z Mgły Zrodzony",
        "author": "Brandon Sanderson",
    }
    create_payload_2 = {
        "serial_number": "000001",
        "title": "Designing Games",
        "author": "Tynan Sylvester",
    }
    resp = await client.post("/api/v1/books", json=create_payload)
    resp2 = await client.post("/api/v1/books", json=create_payload_2)
    assert resp.status_code == 200
    assert resp2.status_code == 200
    book = resp.json()
    assert book["title"] == "Z Mgły Zrodzony"
    assert book["serial_number"] == "123456"

    resp = await client.get("/api/v1/books")
    assert resp.status_code == 200
    books = resp.json()
    assert any(b["serial_number"] == "123456" for b in books)
    assert any(b["serial_number"] == "000001" for b in books)
    assert len(books) == 2

    resp = await client.get("/api/v1/books/123456")
    assert resp.status_code == 200
    book = resp.json()
    assert book["title"] == "Z Mgły Zrodzony"
    assert book["is_borrowed"] is False
    assert book["borrowed_at"] is None
    assert book["borrowed_by"] is None

    borrow_payload = {
        "is_borrowed": True,
        "borrowed_at": "2025-10-06T19:14:42.381109Z",
        "borrowed_by": "654321",
    }
    resp = await client.put("/api/v1/books/123456", json=borrow_payload)
    assert resp.status_code == 200
    updated = resp.json()
    assert updated["is_borrowed"] is True
    assert updated["borrowed_by"] == borrow_payload["borrowed_by"]
    assert updated["borrowed_at"] == borrow_payload["borrowed_at"]

    resp = await client.get("/api/v1/books/123456")
    assert resp.status_code == 200
    book = resp.json()
    assert book["is_borrowed"] is True
    assert book["borrowed_by"] == borrow_payload["borrowed_by"]
    assert book["borrowed_at"] == borrow_payload["borrowed_at"]

    return_payload = {"is_borrowed": False}
    resp = await client.put("/api/v1/books/123456", json=return_payload)
    assert resp.status_code == 200
    book = resp.json()
    assert book["is_borrowed"] is False
    assert book["borrowed_by"] is None
    assert book["borrowed_at"] is None

    resp = await client.get("/api/v1/books/123456")
    assert resp.status_code == 200
    book = resp.json()
    assert book["is_borrowed"] is False
    assert book["borrowed_at"] is None
    assert book["borrowed_by"] is None

    resp = await client.delete("/api/v1/books/123456")
    assert resp.status_code == 204
    resp = await client.get("/api/v1/books")
    assert all(b["serial_number"] != "123456" for b in resp.json())
    assert len(resp.json()) == 1
    resp = await client.get("/api/v1/books/123456")
    assert resp.status_code == 404

    resp = await client.delete("/api/v1/books/000001")
    assert resp.status_code == 204
    resp = await client.get("/api/v1/books")
    assert len(resp.json()) == 0
