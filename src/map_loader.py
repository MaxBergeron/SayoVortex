"""Utilities to parse and print map data (hit and laser objects).

This module provides `AssignMapValues` which extracts metadata and
keeps raw `HitObjects` and `LaserObjects` lists from a `song_data_folder`
dictionary. It exposes helpers to pretty-print those objects.
"""

from typing import Any, Dict, List


class AssignMapValues:
    """Parse and hold map metadata from a song_data_folder dict."""

    def __init__(self, song_data_folder: Dict[str, Any]):
        gen = song_data_folder.get("General", {}) or {}
        meta = song_data_folder.get("Metadata", {}) or {}

        self.song_path = gen.get("AudioFilename", "")
        # convert lead-in to int with safe fallback
        try:
            self.song_lead_in = int(gen.get("AudioLeadIn") or 0)
        except (ValueError, TypeError):
            self.song_lead_in = 0

        self.song_title = meta.get("Title", "")
        self.song_artist = meta.get("Artist", "")
        self.song_creator = meta.get("Creator", "")
        self.song_version = meta.get("Version", "")

        # Raw object lists (keep original structure so callers can inspect)
        self.hit_objects: List[Any] = list(song_data_folder.get("HitObjects", []) or [])
        self.laser_objects: List[Any] = list(song_data_folder.get("LaserObjects", []) or [])

        self.total_hit_objects = len(self.hit_objects)
        self.total_laser_objects = len(self.laser_objects)

    def _format_obj(self, obj: Any) -> str:
        """Return a readable string for common object types.

        Handles dicts, (list/tuple), and CSV-like strings often used in
        map file formats. Falls back to repr(obj).
        """
        if isinstance(obj, dict):
            return ", ".join(f"{k}={v!r}" for k, v in obj.items())
        if isinstance(obj, (list, tuple)):
            return ", ".join(repr(x) for x in obj)
        if isinstance(obj, str):
            # If it's a comma-separated string, split for readability
            if "," in obj:
                parts = [p.strip() for p in obj.split(",")]
                return ", ".join(parts)
            return obj
        return repr(obj)

    def print_hit_objects(self, *, show_index: bool = True) -> None:
        """Print all hit objects with readable formatting."""
        if not self.hit_objects:
            print("No hit objects.")
            return
        print(f"Total hit objects: {self.total_hit_objects}")
        for i, obj in enumerate(self.hit_objects, start=1):
            prefix = f"[{i}] " if show_index else ""
            print(prefix + self._format_obj(obj))

    def print_laser_objects(self, *, show_index: bool = True) -> None:
        """Print all laser objects with readable formatting."""
        if not self.laser_objects:
            print("No laser objects.")
            return
        print(f"Total laser objects: {self.total_laser_objects}")
        for i, obj in enumerate(self.laser_objects, start=1):
            prefix = f"[{i}] " if show_index else ""
            print(prefix + self._format_obj(obj))

    def __repr__(self) -> str:
        return (
            f"AssignMapValues(title={self.song_title!r}, artist={self.song_artist!r}, "
            f"creator={self.song_creator!r}, version={self.song_version!r})"
        )


if __name__ == "__main__":
    # Demo data and usage
    sample = {
        "General": {"AudioFilename": "song.mp3", "AudioLeadIn": "250"},
        "Metadata": {"Title": "Example", "Artist": "You", "Creator": "Mapper", "Version": "1.0"},
        "HitObjects": [
            {"time": 1000, "type": "tap", "x": 64, "y": 128},
            "2000,hold,128,64,500",
            [3000, "tap", 192, 96],
        ],
        "LaserObjects": [
            {"start": 1500, "end": 2500, "path": "sine"},
            "3500,4000,linear",
        ],
    }
    m = AssignMapValues(sample)
    print(m)
    print("\n-- Hit Objects --")
    m.print_hit_objects()
    print("\n-- Laser Objects --")
    m.print_laser_objects()
