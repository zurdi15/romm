from fastapi import APIRouter
import emoji
import json

from logger.logger import log, COLORS
from utils import rom_exists_db
from utils import fs, fastapi
from handler import dbh
from models.platform import Platform
from models.rom import Rom

router = APIRouter()


@router.get("/scan")
def scan(platforms: str, full_scan: bool=False) -> dict:
    """Scan platforms and roms and write them in database."""

    log.info(emoji.emojize(":magnifying_glass_tilted_right: Scanning "))
    fs.store_default_resources()

    # Scanning platform
    fs_platforms: list[str] = fs.get_platforms()
    platforms: list[str] = json.loads(platforms) if len(json.loads(platforms)) > 0 else fs_platforms
    log.info(f"Platforms to be scanned: {', '.join(platforms)}")
    for platform in platforms:
        log.info(emoji.emojize(f":video_game: {platform} {COLORS['reset']}"))
        scanned_platform: Platform = fastapi.scan_platform(platform)
        if platform != str(scanned_platform): log.info(f"Identified as {COLORS['blue']}{scanned_platform}{COLORS['reset']}")
        dbh.add_platform(scanned_platform)

        # Scanning roms
        log.info(f"Scanning roms")
        fs_roms: list[str] = fs.get_roms(platform)
        for rom in fs_roms:
            rom_id: int = rom_exists_db(rom['file_name'], platform)
            if rom_id and not full_scan: continue
            log.info(f"Getting {COLORS['orange']}{rom['file_name']}{COLORS['reset']} details")
            if rom['multi']: [log.info(f"\t - {COLORS['orange_i']}{file}{COLORS['reset']}") for file in rom['files']]
            scanned_rom: Rom = fastapi.scan_rom(scanned_platform, rom)
            if rom_id: scanned_rom.id = rom_id
            dbh.add_rom(scanned_rom)

    # Purge database
    log.info(emoji.emojize(":wastebasket:  Purging database"))
    [dbh.purge_roms(platform, [rom['file_name'] for rom in fs.get_roms(platform)]) for platform in platforms]
    dbh.purge_platforms(fs_platforms)
    return {'msg': 'success'}