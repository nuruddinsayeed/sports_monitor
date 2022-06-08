'''
File: file_helper.py
Project: SportsSafety
File Created: Wednesday, 8th June 2022 11:13:55 pm
Author: Syeed (nur.syeed@stud.fra-uas.de, nuruddinsayeed14@gmail.com)
-----
Last Modified: Wednesday, 8th June 2022 11:13:56 pm
Modified By: Syeed (nur.syeed@stud.fra-uas.de>)
-----
Copyright 2022 - 2022 This Module Belongs to Open source project
'''

from pathlib import Path

def create_log_dir() -> None:
    """Creates Log Dir to avoid error if no Logs dir is created"""
    grand_par_dir = Path(__file__).resolve().parents[1]
    log_dir = grand_par_dir / "Logs"
    log_dir.mkdir(exist_ok=True)