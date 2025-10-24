from src.game_objects import HitObject, LaserObject


class SongProcessor:
    
    def parse_sayovortex_file(self, path):
        data = {}

        class HitObjectWrapper:
            def __init__(self, *args):
                # parts come from CSV: key, duration, time
                self.config = int(args[0]) if len(args) > 0 and args[0] != '' else None
                self.duration = float(args[1]) if len(args) > 1 and args[1] != '' else None
                self.position = float(args[2]) if len(args) > 2 and args[2] != '' else None

            def __repr__(self):
                return f"HitObjectWrapper(config={self.config}, duration={self.duration}, position={self.position})"

        class LaserObjectWrapper:
            def __init__(self, *args):
                self.chain = bool(int(args[0])) if len(args) > 0 and args[0] != '' else None
                self.position = int(args[1]) if len(args) > 1 and args[1] != '' else None
                self.start = float(args[2]) if len(args) > 2 and args[2] != '' else None

            def __repr__(self):
                return f"LaserObjectWrapper(chain={self.chain}, start={self.start}, position={self.position})"

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
                        # create wrapper objects so callers can use dot-notation
                        obj = HitObjectWrapper(*parts)
                    elif current_section == "LaserObjects":
                        obj = LaserObjectWrapper(*parts)
                    else:
                        obj = tuple(parts)
                    data[current_section].append(obj)
        return data