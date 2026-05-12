from datetime import date, datetime

from sqlalchemy import Date, DateTime, Float, ForeignKey, Integer, String, Text, UniqueConstraint, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class Paper(Base):
    __tablename__ = "papers"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(512), index=True)
    abstract: Mapped[str | None] = mapped_column(Text)
    publication_date: Mapped[date | None] = mapped_column(Date, index=True)
    venue: Mapped[str | None] = mapped_column(String(256), index=True)
    source: Mapped[str] = mapped_column(String(64), index=True)
    doi: Mapped[str | None] = mapped_column(String(128), index=True)
    arxiv_id: Mapped[str | None] = mapped_column(String(64), index=True)
    openalex_id: Mapped[str | None] = mapped_column(String(128), index=True)
    citation_count: Mapped[int] = mapped_column(Integer, default=0, index=True)
    topic_id: Mapped[int | None] = mapped_column(Integer, index=True)
    embedding: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())

    authors: Mapped[list["Author"]] = relationship(
        secondary="paper_authors", back_populates="papers", cascade="save-update"
    )
    institutions: Mapped[list["Institution"]] = relationship(
        secondary="paper_institutions", back_populates="papers", cascade="save-update"
    )
    keywords: Mapped[list["Keyword"]] = relationship(
        secondary="paper_keywords", back_populates="papers", cascade="save-update"
    )

    __table_args__ = (
        UniqueConstraint("source", "arxiv_id", name="uq_paper_source_arxiv"),
        UniqueConstraint("source", "doi", name="uq_paper_source_doi"),
        UniqueConstraint("source", "openalex_id", name="uq_paper_source_openalex"),
    )


class Author(Base):
    __tablename__ = "authors"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(256), unique=True, index=True)
    papers: Mapped[list[Paper]] = relationship(secondary="paper_authors", back_populates="authors")


class Institution(Base):
    __tablename__ = "institutions"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(256), unique=True, index=True)
    country_code: Mapped[str | None] = mapped_column(String(8), index=True)
    papers: Mapped[list[Paper]] = relationship(secondary="paper_institutions", back_populates="institutions")


class Keyword(Base):
    __tablename__ = "keywords"

    id: Mapped[int] = mapped_column(primary_key=True)
    term: Mapped[str] = mapped_column(String(128), unique=True, index=True)
    papers: Mapped[list[Paper]] = relationship(secondary="paper_keywords", back_populates="keywords")


class PaperAuthor(Base):
    __tablename__ = "paper_authors"

    paper_id: Mapped[int] = mapped_column(ForeignKey("papers.id"), primary_key=True)
    author_id: Mapped[int] = mapped_column(ForeignKey("authors.id"), primary_key=True)
    position: Mapped[int | None] = mapped_column(Integer)


class PaperInstitution(Base):
    __tablename__ = "paper_institutions"

    paper_id: Mapped[int] = mapped_column(ForeignKey("papers.id"), primary_key=True)
    institution_id: Mapped[int] = mapped_column(ForeignKey("institutions.id"), primary_key=True)


class PaperKeyword(Base):
    __tablename__ = "paper_keywords"

    paper_id: Mapped[int] = mapped_column(ForeignKey("papers.id"), primary_key=True)
    keyword_id: Mapped[int] = mapped_column(ForeignKey("keywords.id"), primary_key=True)
    weight: Mapped[float | None] = mapped_column(Float)
