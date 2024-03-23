"""
This module extracts poker hands inside the compressed IRCdata.tgz file and re-formats them into human readable json files. Inside IRCdata.tgz are a bunch of comparessed <game_type>.<yyyymm>.tgz files that then include the following files/directories

- Hand file: ./<game_type>/<yyyymm>/hdb
- Roster file: ./<game_type>/<yyyymm>/hroster
- Player directory: ./<game_type>/<yyyymm>/pdb/ inside which we have player files
    - ./<game_type>/<yyyymm>/pdb/pdb.<player1>
    - ./<game_type>/<yyyymm>/pdb/pdb.<player2>
    - ...

The hdb files are in the following format

    812686674    8    1    2    0/0     0/0      0/0      1/150    
    812686676    8    2    2    2/200   2/1800   2/1800   2/1800    7c 4c 6h Kh 4s
    812686708    8    3    2    0/0     0/0      0/0      1/150    
    812686718    8    4    2    0/0     0/0      0/0      1/150    
    812686725    8    5    2    0/0     0/0      0/0      1/150    
    812686727    8    6    2    2/200   2/4200   2/10507  2/10507   5c 2h 4c Qd 5s
    812686767    8    7    2    0/0     0/0      0/0      1/500    
    812686787    8    8    2    2/200   0/0      0/0      1/400     Js Kc 5h
    812686802    8    9    2    0/0     0/0      0/0      1/500    
    812686807    8    10   2    0/0     0/0      0/0      1/150    

where the column names (not included in files) are

- timestamp
- dealer
- hand_num
- num_players
- num_players vs starting pot size (flop)
- num_players vs starting pot size (turn)
- num_players vs starting pot size (river)
- num_players vs starting pot size (showdown)
- board_cards (if shown)

The hroster files are in the following format

    812686674    2    flopsy    gfw
    812686676    2    flopsy    gfw
    812686708    2    flopsy    gfw
    812686718    2    flopsy    gfw
    812686725    2    flopsy    gfw
    812686727    2    flopsy    gfw
    812686767    2    flopsy    gfw
    812686787    2    flopsy    gfw
    812686802    2    flopsy    gfw
    812686807    2    flopsy    gfw

where the column names (not included in files) are

- timestamp 
- num_players 
- player1 
- player2
- ...

The pdb.<player> files are in the following format 

    Jefferson    814691656    2    1    Bc    bc    k    k    5130    900    1800    Qh    8d
    Jefferson    814691693    2    2    Bc    f     -    -    6030    400       0       
    Jefferson    814691746    2    1    Bf    -     -    -    5630     50       0       
    Jefferson    814691751    2    2    B     -     -    -    5580    100     150       
    Jefferson    814691753    2    1    Bf    -     -    -    5630     50       0       
    Jefferson    814691755    2    2    B     -     -    -    5580    100     150       
    Jefferson    814691760    2    1    Br    b     -    -    5630    900    1200       
    Jefferson    814691773    3    3    r     -     -    -    5930    350     500       
    Jefferson    814691788    3    2    Bf    -     -    -    6080    100       0       
    Jefferson    814691797    3    1    Bf    -     -    -    5980     50       0       

where the column names (not included in files) are 

- player 
- timestamp 
- num_players
- position
- action (preflop)
- action (flop)
- action (turn)
- action (river)
- starting bankroll 
- total_bet
- total_win
- pocket_cards (if shown)

Taking a simple heads up for example:

hdb:
    
    820830094    20    1163    2    2/20    2/40    2/80    2/80    Qc 4s 6s 5d 4d

hroster:

    820830094    2    Jak    num

pdb.Jak:

    Jak    820830094    2    1    Bc    kc    kc    k    850    40    80    7c Ac

pdb.num:

    num    820830094    2    2    Bk    b     b     k    1420   40    0     9h Kh

What the above files record is a hand at timestamp 820830094 where we have 2 players at the table, Jak (starting bankroll $850) and num (starting bankroll $1420):

- At preflop, Jak makes a small blind (B) $5, num makes a big blind (B) $10, Jak calls (c) and num checks (k).
- At flop, we have 2 players and starting pot $20. Board sees Qc 4s 6s. Jak checks (k), num bets (b) $20, Jak calls (c).
- On the turn, we have 2 players and starting pot $40. Board sees 5d. Jak checks (k), num bets (b) $20, Jack calls (c).
- On the river, we have 2 players and starting pot $80. Board sees 4d. Jak checks (k), nums checks (k).
- At the showdown, we have 2 players and starting pot $80. Jak wins the hand with a pair of board 4's w/ Ace high versus num's board 4's w/ King high. Jak wins $80 in the end.

Note that we don't record the pocket cards of any players who fold before showdown.

The JSON record corresponding to the above example would be

    {
        '_id': 'holdem_199601_820830094',
        'board': ['Qc', '4s', '6s', '5d', '4d'],
        'dealer': 20,
        'game': 'holdem',
        'hand_num': 1163,
        'num_players': 2,
        'players': {
            'Jak': {
                'total_bet': 40,
                'bankroll': 850,
                'bets': [
                    {
                        'actions': ['B', 'c'],
                        'stage': 'p'
                    },
                    {
                        'actions': ['k', 'c'],
                        'stage': 'f'},
                    {
                        'actions': ['k', 'c'],
                        'stage': 't'
                    },
                    {
                        'actions': ['k'],
                        'stage': 'r'
                    }
                ],
                'pocket_cards': ['7c', 'Ac'],
                'position': 1,
                'total_win': 80
            },
            'num': {
                'total_bet': 40,
                'bankroll': 1420,
                'bets': [
                    {
                        'actions': ['B', 'k'],
                        'stage': 'p'
                    },
                    {
                        'actions': ['b'],
                        'stage': 'f'
                    },
                    {
                        'actions': ['b'],
                        'stage': 't'
                    },
                    {
                        'actions': ['k'],
                        'stage': 'r'
                    }
                ],
                'pocket_cards': ['9h', 'Kh'],
                'position': 2,
                'total_win': 0
            }
        },
        'pots': [
            {
                'num_players': 2,
                'stage': 'f',
                'size': 20
            },
            {
                'num_players': 2,
                'stage': 't',
                'size': 40
            },
            {
                'num_players': 2,
                'stage': 'r',
                'size': 80
            },
            {
                'num_players': 2,
                'stage': 's',
                'size': 80
            }
        ]
    }
"""

import json
import os
from functools import partial
from multiprocessing.pool import Pool
from tarfile import TarFile
from typing import Annotated, Iterator, Optional

import ijson
from pydantic import BaseModel, Field, ValidationError

from utils import logger, system

# a bunch of constants
VALID_GAME_TYPES = {
    "holdem",
    "holdem1",
    "holdem2",
    "holdem3",
    "holdemii",
    "holdempot",
    "nolimit",
    "tourney",
}
SLASH = "\\" if system == "Windows" else "/"
STAGES = ["preflop", "flop", "turn", "river", "showdown"]

# a bunch of annotated types for validation
Timestamp = Annotated[int, Field(ge=100000000, le=999999999)]
Stage = Annotated[str, Field(pattern=r"^[0-9]+\/[0-9]+$")]
Card = Annotated[str, Field(pattern=r"^[1-9,TJQKA][schd]$")]
Action = Annotated[str, Field(pattern=r"^[BfkbcrAQK-]+$")]


class HdbRecord(BaseModel):
    timestamp: Timestamp
    dealer: int
    hand_num: int
    num_players: int
    flop: Stage
    turn: Stage
    river: Stage
    showdown: Stage
    card1: Optional[Card] = None
    card2: Optional[Card] = None
    card3: Optional[Card] = None
    card4: Optional[Card] = None
    card5: Optional[Card] = None

    def __init__(self, *args):
        try:
            super().__init__(**dict(zip(self.model_fields, args)))
        except ValidationError:
            msg = f"Validation error for HdbRecord: fields={tuple(self.model_fields)} args={args}"
            logger.error(msg)
            raise

    @property
    def cards(self):
        cards = [self.card1, self.card2, self.card3, self.card4, self.card5]
        return [c for c in cards if c is not None]

    @property
    def pots(self):
        pots = []
        for stage in STAGES[1:]:
            n, s = getattr(self, stage).split("/")
            pots.append({"num_players": int(n), "stage": stage[0], "size": int(s)})
        return pots


class HrosterRecord(BaseModel):
    timestamp: Timestamp
    num_players: int
    players: list[str]

    def __init__(self, *args):
        try:
            super().__init__(timestamp=args[0], num_players=args[1], players=args[2:])
        except ValidationError:
            msg = f"Validation error for HrosterRecord: fields={tuple(self.model_fields)} args={args}"
            logger.error(msg)
            raise


class PdbRecord(BaseModel):
    player: str
    timestamp: Timestamp
    num_players: int
    position: int
    preflop: Action
    flop: Action
    turn: Action
    river: Action
    bankroll: int
    total_bet: int
    total_win: int
    card1: Optional[Card] = None
    card2: Optional[Card] = None

    def __init__(self, *args):
        try:
            super().__init__(**dict(zip(self.model_fields, args)))
        except ValidationError:
            msg = f"Validation error for PdbRecord: fields={tuple(self.model_fields)} args={args}"
            logger.error(msg)
            raise

    @property
    def cards(self):
        cards = [self.card1, self.card2]
        return [c for c in cards if c is not None]

    @property
    def bets(self):
        return [{"actions": getattr(self, stage), "stage": stage[0]} for stage in STAGES[:-1]]


class PokerHandsExtractor:
    def __init__(
        self,
        *,
        fname_in: Optional[str] = None,
        fname_out: Optional[str] = None,
        n_jobs: int = 1,
    ):
        """Extract poker hands data from an input file and optionally save to an output file

        Args:
            fname_in (Optional[str]): input filepath
            fname_out (Optional[str]): output filepath
            n_jobs (int): number of processes for extraction, default to 1, set to -1 to use all cores
        """
        if fname_in:
            assert fname_in.endswith(".tgz"), f"Input {fname_in} is not a tgz file"
            self.fname_in = fname_in

        if fname_out:
            assert fname_out.endswith(".json"), f"Output {fname_out} is not a json file"
            if os.path.isfile(fname_out) and n_jobs != 1:
                msg = f"Parameter n_jobs={n_jobs} will be ignored since fname_out={fname_out} exists"
                logger.warning(msg)
        self.fname_out = fname_out

        self.n_jobs = n_jobs if n_jobs > 0 else os.cpu_count()

    @staticmethod
    def _extract_single_group(name_group: str, fname_in: str) -> list[dict]:
        """Given an input filepath and specific group name, extract all poker hands data within

        Args:
            name_group (str): name of the group
            fname_in (str): input filepath

        Returns:
            list[dict]: a list of hand records in json
        """
        with TarFile.open(fname_in) as tar_in:
            split = lambda x: x.decode().strip().split()
            if not name_group.endswith(".tgz"):
                return []
            parts = name_group.rsplit(SLASH, 1)
            if len(parts) < 2:
                logger.error(f"Could not split {name_group} into two parts.")
            else:
                fname_group = parts[1]
            game_type = fname_group.split(".", 1)[0]
            if game_type not in VALID_GAME_TYPES:
                return []
            folder_group = fname_group.rstrip(".tgz").replace(".", SLASH)
            file_group = tar_in.extractfile(name_group)
            if file_group is None:
                logger.error(f"File {fname_group} not found")
                return []
            logger.info(f"Extracting {fname_group}")
            with TarFile.open(fileobj=file_group) as tar_group:
                hands = []
                fname_group = ""
                try:
                    # extract files
                    file_hdb = file_hroster = None
                    file_pdb = {}

                    fname_hdb = f"{folder_group}{SLASH}hdb"
                    file_hdb = tar_group.extractfile(fname_hdb)
                    if not file_hdb:
                        logger.error(f"File {fname_hdb} not found")
                        return []
                    iter_hdb = iter(file_hdb)
                    logger.debug(f"File {fname_hdb} extracted")

                    fname_hroster = f"{folder_group}{SLASH}hroster"
                    file_hroster = tar_group.extractfile(fname_hroster)
                    if not file_hroster:
                        logger.error(f"File {fname_hroster} not found")
                        file_hdb.close()
                        return []
                    iter_hroster = iter(file_hroster)
                    logger.debug(f"File {fname_hroster} extracted")

                    file_pdb = {}
                    iter_pdb = {}
                    delimiter = f"pdb{SLASH}pdb."
                    for fname in tar_group.getnames():
                        if delimiter in fname:
                            player = fname.split(delimiter)[-1]
                            file_pdb[player] = tar_group.extractfile(fname)
                            if file_pdb is None:
                                logger.error(f"File {fname} not found")
                                continue
                            iter_pdb[player] = iter(file_pdb[player])
                    msg = f"File {folder_group}{SLASH}pdb extracted, {len(iter_pdb)} files in total"
                    logger.debug(msg)

                    # iterate through timestamps
                    pdb = {k: PdbRecord(*[s for s in split(next(v)) if s]) for k, v in iter_pdb.items()}
                    while True:
                        try:
                            hdb = HdbRecord(*[s for s in split(next(iter_hdb)) if s])
                            while True:
                                hroster = HrosterRecord(*[s for s in split(next(iter_hroster)) if s])
                                if hroster.timestamp >= hdb.timestamp:
                                    break
                            if hdb.timestamp < hroster.timestamp:
                                continue
                            assert hdb.timestamp == hroster.timestamp
                            assert hdb.num_players == hroster.num_players
                            _id = f"{folder_group}{SLASH}{hdb.timestamp}".replace(SLASH, "_")

                            pdb_curr = {}
                            pdb_missing = False
                            for player in hroster.players:
                                if player not in pdb:
                                    msg = f"Record pdb.{player} missing at timestamp {hdb.timestamp}, skipping {_id}"
                                    logger.debug(msg)
                                    pdb_missing = True
                                    break
                                while pdb[player].timestamp < hdb.timestamp:
                                    pdb[player] = PdbRecord(*[s for s in split(next(iter_pdb[player])) if s])
                                if pdb[player].timestamp > hdb.timestamp:
                                    msg = f"Record pdb.{player} missing at timestamp {hdb.timestamp}, skipping {_id}"
                                    logger.debug(msg)
                                    pdb_missing = True
                                    break
                                pdb_curr[player] = pdb[player]
                            if pdb_missing:
                                continue
                            assert len(hroster.players) == len(pdb_curr)
                            assert all(v.timestamp == hdb.timestamp for v in pdb_curr.values())

                            hand = {
                                "_id": _id,
                                "board": hdb.cards,
                                "dealer": hdb.dealer,
                                "game": game_type,
                                "hand_num": hdb.hand_num,
                                "num_players": hdb.num_players,
                                "players": {
                                    k: {
                                        "total_bet": v.total_bet,
                                        "bankroll": v.bankroll,
                                        "bets": v.bets,
                                        "pocket_cards": v.cards,
                                        "position": v.position,
                                        "total_win": v.total_win,
                                    }
                                    for k, v in pdb_curr.items()
                                },
                                "pots": hdb.pots,
                            }
                            logger.debug(f"Hand {_id} extracted")
                            hands.append(hand)
                        except ValidationError:
                            continue
                except EOFError:
                    logger.error(f"EOFError, skipping {fname_group}")
                except StopIteration:
                    pass
                finally:
                    logger.debug(f"Closing all files for {folder_group}")
                    for file in [file_group, file_hdb, file_hroster, *file_pdb.values()]:  # type: ignore
                        if file is not None:
                            file.close()
                    return hands

    @staticmethod
    def _iter_helper(name_group: str, fname_in: str) -> tuple[list[dict], str]:
        """Helper function that extracts the hands and return with group name

        Args:
            name_group (str): name of the group
            fname_in (str): input filepath

        Returns:
            tuple[list[dict], str]: list of hand records, and group name
        """
        hands_group = PokerHandsExtractor._extract_single_group(name_group, fname_in)
        return hands_group, name_group

    def __iter__(self) -> Iterator[dict]:
        """Iterate through all hand records, save to fname_out in the end if specified

        Yields:
            dict: hand record in json
        """
        if self.fname_out and os.path.isfile(self.fname_out):
            with open(self.fname_out, "r") as f:
                for hand in ijson.items(f, "item"):
                    yield hand

        else:
            hands = []
            num_hands = 0
            func = partial(self._iter_helper, fname_in=self.fname_in)
            logger.info(f"Initializing poker hand data extraction from {self.fname_in}")
            with TarFile.open(self.fname_in) as tar_in:
                names = tar_in.getnames()
            with Pool(self.n_jobs) as pool:
                for hands_group, name_group in pool.imap(func, names):
                    if not hands_group:
                        continue
                    hands += hands_group
                    num_hands_group = len(hands_group)
                    num_hands += num_hands_group
                    msg = f"{num_hands_group} hands extracted from {name_group}, {num_hands} hands extracted by far"
                    logger.info(msg)
                    for hand in hands_group:
                        yield hand
            if self.fname_out:
                logger.info(f"Saving to {self.fname_out}")
                with open(self.fname_out, "w") as f:
                    json.dump(hands, f)


if __name__ == "__main__":
    extractor = PokerHandsExtractor(
        fname_in="IRCdata.tgz",
        fname_out="hands.json",
        n_jobs=12,
    )
    num_hands = 0
    for hand in extractor:
        num_hands += 1
    logger.info(f"{num_hands} extracted in total")
