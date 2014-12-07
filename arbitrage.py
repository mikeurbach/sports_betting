from itertools import combinations

class Arbitrage:
    def __init__(self, lines):
        self.lines = lines
        self.has_arbitrage = False
        self.arbitrage_opportunities = {}

    def __repr__(self):
        s = ''
        if self.has_arbitrage:
            s += 'YES '
            s += str(self.arbitrage_opportunities)
        else:
            s += 'NO'
        return s

    # returns yes/no, if yes the sites and games
    def check(self):
        # find the take and lay
        T = {}
        best_t = -float('inf')
        L = {}
        best_l = float('inf')

        # for each site
        for site, lines in self.lines.iteritems():
            # check each game
            for game_id, (awayline, homeline) in lines.iteritems():
                # find possible take and lay
                if awayline > homeline:
                    c = awayline
                    c_team = 'away'
                    d = homeline
                    d_team = 'home'
                else :
                    c = homeline
                    c_team = 'home'
                    d = awayline
                    d_team = 'away'

                # lookup the best take
                if game_id in T:
                    _, best_t, _ = T[game_id]

                # is this the new best take?
                if c > best_t:
                    T[game_id] = (site._id, c, c_team)

                # lookup the best lay
                if game_id in L:
                    _, best_l, _ = L[game_id]

                # is this the new best take?
                if abs(d) < best_l:
                    L[game_id] = (site._id, abs(d), d_team)

        # compute the rewards
        Rt = {}
        Rl = {}

        # for each take
        for game_id, (_id, t, team) in T.iteritems():
            Rt[game_id] = (_id, t, 100.0 / (100.0 + t), team)

        # for each lay
        for game_id, (_id, l, team) in L.iteritems():
            Rl[game_id] = (_id, l, l / (100.0 + l), team)

        # check for arbitrage
        for game_id in Rt:
            sitet, t, rt, teamt = Rt[game_id]
            sitel, l, rl, teaml = Rl[game_id]
            if rt + rl < 1:
                self.has_arbitrage = True
                self.arbitrage_opportunities[game_id] = { 'take': (sitet, teamt, t, rt), 'lay': (sitel, teaml, l, rl) }
