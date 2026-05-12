from __future__ import annotations

from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="SYDEL_", extra="ignore")

    project_name: str = "SYDEL Document Engine"
    environment: str = "dev"
    output_dir: Path = Path("outputs")
