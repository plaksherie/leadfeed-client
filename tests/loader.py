import tomllib
from pathlib import Path

from tests.schema import Config

config_name = 'config.toml'
# config_file = Path(current_module_path.parent / config_name)
config = Config.model_validate(tomllib.loads(Path(config_name).read_text(encoding="utf-8")))
