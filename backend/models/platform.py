from sqlalchemy import Column, String, Integer

from config import DEFAULT_PATH_COVER_S
from .base import BaseModel


class Platform(BaseModel):
    __tablename__ = "platforms"
    fs_slug: str = Column(String(length=50), primary_key=True)

    igdb_id: str = Column(String(length=10), default="")
    sgdb_id: str = Column(String(length=10), default="")

    slug: str = Column(String(length=50), default="")
    name: str = Column(String(length=400), default="")
    generation: str = Column(Integer, default=-1)

    pf_name: str = Column(String(length=400), default="")
    pf_slug: str = Column(String(length=50), default="")

    logo_path: str = Column(String(length=1000), default=DEFAULT_PATH_COVER_S)
    logo_url: str = Column(String(length=1000), default="")
    
    n_roms: int = Column(Integer, default=0)

    def __repr__(self) -> str:
        return self.name
