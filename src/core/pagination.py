from pydantic import BaseModel, Field


class Pagination(BaseModel):
    page: int = Field(default=1)
    page_size: int = Field(default=10)
    total_pages: int | None = None

    @property
    def offset(self) -> int:
        return (self.page - 1) * self.page_size
