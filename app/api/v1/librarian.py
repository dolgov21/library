from fastapi import APIRouter

router = APIRouter(prefix="/api/v1/librarian", tags=["Librarian"])

BOOKS = {"books": [{"title": "Red Hat"}, {"title": "1984"}]}


@router.get("books")
async def get_books() -> dict[str, list[dict[str, str]]]:
    return BOOKS
