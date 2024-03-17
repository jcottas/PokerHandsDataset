"""
This module provides the class that allows browsing extracted poker hands data in consoles. The expected format of a game would be:

########################################################
#    time : 199504_797212996   hand# : 27              #
#   board : ['Tc', '5s', '6h', '7h', 'Th']             #
#    pots : [(3, 60), (3, 120), (3, 180), (2, 280)]    #
# players :                                            #
#                      derek (#1)                      #
###   total_bet : 100                                ###
###    bankroll : 900                                ###
###        bets : [{'actions': 'Br', 'stage': 'p'},  ###
###                {'actions': 'bc', 'stage': 'f'    ###
###                {'actions': 'kc', 'stage': 't'    ###
###                {'actions': 'kr', 'stage': 'r'}]  ###
###      pocket : ['Ah', 'Kh']                       ###
###   total_win : 280                                ###
# . . . . . . . . . . . . . . . . . . . . . . . . . . .#
#                    deadhead (#2)                     #
###   total_bet : 80                                 ###
###    bankroll : 1343                               ###
###        bets : [{'actions': 'Bc', 'stage': 'p'},  ###
###                {'actions': 'cc', 'stage': 'f'    ###
###                {'actions': 'b', 'stage': 't'     ###
###                {'actions': 'bf', 'stage': 'r'}]  ###
###      pocket : []                                 ###
###   total_win : 0                                  ###
# . . . . . . . . . . . . . . . . . . . . . . . . . . .#
#                      Snerd (#3)                      #
###   total_bet : 0                                  ###
###    bankroll : 972                                ###
###        bets : [{'actions': 'f', 'stage': 'p'},   ###
###                {'actions': '-', 'stage': 'f'     ###
###                {'actions': '-', 'stage': 't'     ###
###                {'actions': '-', 'stage': 'r'}]   ###
###      pocket : []                                 ###
###   total_win : 0                                  ###
# . . . . . . . . . . . . . . . . . . . . . . . . . . .#
#                    sagerbot (#4)                     #
###   total_bet : 0                                  ###
###    bankroll : 1940                               ###
###        bets : [{'actions': 'f', 'stage': 'p'},   ###
###                {'actions': '-', 'stage': 'f'     ###
###                {'actions': '-', 'stage': 't'     ###
###                {'actions': '-', 'stage': 'r'}]   ###
###      pocket : []                                 ###
###   total_win : 0                                  ###
# . . . . . . . . . . . . . . . . . . . . . . . . . . .#
#                       tpm (#5)                       #
###   total_bet : 0                                  ###
###    bankroll : 1070                               ###
###        bets : [{'actions': 'f', 'stage': 'p'},   ###
###                {'actions': '-', 'stage': 'f'     ###
###                {'actions': '-', 'stage': 't'     ###
###                {'actions': '-', 'stage': 'r'}]   ###
###      pocket : []                                 ###
###   total_win : 0                                  ###
# . . . . . . . . . . . . . . . . . . . . . . . . . . .#
#                      greg (#6)                       #
###   total_bet : 100                                ###
###    bankroll : 1245                               ###
###        bets : [{'actions': 'cc', 'stage': 'p'},  ###
###                {'actions': 'r', 'stage': 'f'     ###
###                {'actions': 'c', 'stage': 't'     ###
###                {'actions': 'cc', 'stage': 'r'}]  ###
###      pocket : ['Jd', 'Ts']                       ###
###   total_win : 0                                  ###
# . . . . . . . . . . . . . . . . . . . . . . . . . . .#
#                    justnuts (#7)                     #
###   total_bet : 0                                  ###
###    bankroll : 980                                ###
###        bets : [{'actions': 'f', 'stage': 'p'},   ###
###                {'actions': '-', 'stage': 'f'     ###
###                {'actions': '-', 'stage': 't'     ###
###                {'actions': '-', 'stage': 'r'}]   ###
###      pocket : []                                 ###
###   total_win : 0                                  ###
########################################################
"""

from textwrap import dedent
from typing import Optional

from extract import VALID_GAME_TYPES, PokerHandsExtractor


class PokerHandsBrowser:
    def __init__(self, fname: str):
        """Browse poker hands in console

        Args:
            fname (str): extracted poker hands filepath
        """
        assert fname.endswith(".json"), f"Input {fname} is not a json file"
        self.fname = fname

    def run(self, game_type: Optional[str] = None, manual_mode: bool = False):
        """Start browsing automatically or manually, optionally filter based on a certain game type

        Args:
            game_type (Optional[str]): set to a specific game type if needed, default is None
            manual_mode (bool): set to true to go to the next hand only when ENTER is pressed
        """
        assert (not game_type) or (game_type in VALID_GAME_TYPES)
        extractor = PokerHandsExtractor(fname_out=self.fname)
        hand_counter = 0
        for hand in extractor:
            if game_type and (not hand["_id"].startswith(game_type)):
                continue
            try:
                timestamp = hand["_id"].split("_", 1)[1]
                pots = [(p["num_players"], p["size"]) for p in hand["pots"]]
                playerstr = []
                players = hand["players"]
                pos = [v["position"] for _, v in players.items()]
                assert len(pos) == hand["num_players"], (pos, hand["num_players"])
                for i, name in enumerate(sorted(players, key=lambda x: players[x]["position"])):
                    player = players[name]
                    bets = str(player["bets"]).split("}, ")
                    bets[0] = "{:<34} ###".format(bets[0] + "},")
                    for j in range(1, len(bets)):
                        bets[j] = "###" + " " * 16 + f"{bets[j]:<33} ###"
                    betstr = "\n".join(bets)
                    pstr = (
                        f"# {name + ' (#' + str(i + 1) + ')':^52} #"
                        + dedent("""
                        ###   total_bet : {:<34} ###
                        ###    bankroll : {:<34} ###
                        ###        bets : {}
                        ###      pocket : {:<34} ###
                        ###   total_win : {:<34} ###
                        """).format(
                            player["total_bet"],
                            player["bankroll"],
                            betstr,
                            str(player["pocket_cards"]),
                            player["total_win"],
                        )
                    )
                    playerstr.append(pstr)
                playerstr = ("# {}.#\n".format(". " * 26)).join(playerstr)
                handstr = dedent("""
                #    time : {}   hand# : {:<15} #
                #   board : {:<42} #
                #    pots : {:<42} #
                # players :                                            #
                """[1:-1]).format(
                    timestamp,
                    hand_counter,
                    str(hand["board"]),
                    str(pots),
                )
                print("#" * 56 + "\n" + handstr + playerstr + "#" * 56)
                hand_counter += 1
                if manual_mode:
                    input()
                else:
                    print()
            except KeyboardInterrupt:
                break


if __name__ == "__main__":
    browser = PokerHandsBrowser("hands.json")
    browser.run(manual_mode=False)
