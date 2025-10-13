from importlib.resources import path

from src.game_objects import HitObject, LaserObject


class SongProcessor:
    
    def parse_sayovortex_file(self, path):
        data = {}
        current_section = None
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()

                # Skip blank lines or comments
                if not line or line.startswith("//"):
                    continue

                # Detect section headers like [General]
                if line.startswith("[") and line.endswith("]"):
                    current_section = line[1:-1]
                    data[current_section] = {}
                    continue

                # Ignore the version line
                if "SayoVortex file format" in line:
                    data["FileFormat"] = line
                    continue
                if current_section is None:
                    continue
                
                # Decide between key:value and CSV object while in a section
                if ":" in line:
                    key, value = map(str.strip, line.split(":", 1))
                    if isinstance(data[current_section], dict):
                        data[current_section][key] = value
                elif "," in line:
                    if isinstance(data[current_section], dict):
                        data[current_section] = []
                    parts = [p.strip() for p in line.split(",")]
                    if current_section == "HitObjects":
                        obj = HitObject(*parts)
                    elif current_section == "LaserObjects":
                        obj = LaserObject(*parts)
                    else:
                        obj = tuple(parts)
                    data[current_section].append(obj)
        return data