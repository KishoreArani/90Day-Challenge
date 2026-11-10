"""Day 2 · The job board bouncer

Job postings arrive from scrapers and forms, and they're messy. Your job: let the good ones in
as clean Pydantic models, and turn the bad ones away with a clear reason.

Run `python quest.py 2` after each TODO.
"""
from pydantic import BaseModel, HttpUrl, Field, ValidationError, field_validator, model_validator  # noqa: F401


class JobPosting(BaseModel):
    # TODO 2.1 · Add these fields:
    #   title: str
    #   company: str
    #   url: HttpUrl
    #   salary_lpa: a float or None, default None, and it can't be negative (hint: Field(default=None, ge=0))
    #   remote: bool, default False
    #   location: str or None, default None
    title : str
    company: str
    url: HttpUrl
    salary_lpa: float | None = Field(default=None, ge=0)
    remote: bool = False
    location: str| None = None

    # TODO 2.2 · Clean up the title with a @field_validator("title"):
    #   strip spaces at both ends and squash repeated spaces inside ("  ML   Engineer " -> "ML Engineer").
    #   If nothing is left, raise ValueError("title can't be empty").
    @field_validator("title")
    @classmethod
    def clean_title(cls, value: str) -> str:
        cleaned = " ".join(value.split())

        if not cleaned:
            raise ValueError("title can't be empty")

        return cleaned


    # TODO 2.3 · Add a @model_validator(mode="after"):
    #   an on-site job (remote is False) must have a location.
    #   If it's missing, raise ValueError("location is required for on-site jobs"). Return self otherwise.
    @model_validator(mode="after")
    def check_location(self):
        if not self.remote and not self.location:
            raise ValueError("location is required for on-site jobs")

        return self



def parse_postings(raw: list[dict]) -> tuple[list[JobPosting], list[str]]:
    """TODO 2.4 · Validate every record.

    Return (valid_postings, errors). For each bad record add ONE error string, using the first error
    Pydantic reports, in this exact format:  "record {index}: {field}: {message}"
    e.g. "record 3: url: Input should be a valid URL, relative URL without a base"
    (index starts at 0; field is the first item of the error's "loc", or "posting" if loc is empty)
    """
    valid_postings: list[JobPosting] = []
    errors: list[str] = []

    for index, record in enumerate(raw):
        try:
            posting = JobPosting.model_validate(record)
            valid_postings.append(posting)
        except ValidationError as exc:
            first_error = exc.errors()[0]
            location = first_error["loc"]
            field = location[0] if location else "posting"
            message = first_error["msg"]

            errors.append(f"record {index}: {field}: {message}")

    return valid_postings, errors
