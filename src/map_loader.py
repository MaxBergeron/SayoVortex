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

        print(f"Loaded map from map loader: {self.song_title} by {self.song_artist} [{self.song_version}]")
        
        # Raw object lists (keep original structure so callers can inspect)
        self.hit_objects: List[Any] = list(song_data_folder.get("HitObjects", []) or [])
        self.laser_objects: List[Any] = list(song_data_folder.get("LaserObjects", []) or [])

        self.total_hit_objects = len(self.hit_objects)
        self.total_laser_objects = len(self.laser_objects)
        print(f"Total hit objects: {self.total_hit_objects}, Total laser objects: {self.total_laser_objects}")
        # Print first hit object and laser object if they exist
        if self.hit_objects:
            print(f"First hit object position: {self.hit_objects[0].position}")
        if self.laser_objects:
            print(f"First laser object position: {self.laser_objects[0].poition}")


    def __repr__(self) -> str:
        return (
            f"AssignMapValues(title={self.song_title!r}, artist={self.song_artist!r}, "
            f"creator={self.song_creator!r}, version={self.song_version!r})"
        )
