import pandas as pd

fe = pd.read_csv('fullevents.csv')
pe = pd.read_csv('passingevents.csv')
m = pd.read_csv('matches.csv')


# 将坐标统一！
def convert_coor(row):
    if row[1].startswith('Opponent'):
        for i in range(1, 5):
            row[-i] = 100 - row[-i]
    return row


def convert_goal_keeper(row):
    if row[6] != 'Pass':
        if str(row[2])[:-1].endswith('G'):
            row[-3] = 50
            if row[1].startswith('Opponent'):
                row[-4] = 100
        elif str(row[3])[:-1].endswith('G'):
            row[-1] = 50
            if row[1].startswith('Opponent'):
                row[-2] = 100
    return row


fe = fe.apply(func=convert_coor, axis=1)
fe = fe.apply(func=convert_goal_keeper, axis=1)
fe.loc[fe.EventSubType == 'Goal kick', 'EventOrigin_y'] = 50
pe = pe.apply(func=convert_coor, axis=1)


def phrase_srtuct(players):
    st = [0, 0, 0]
    for p in players:
        if 'F' in p:
            st[0] += 1
        elif 'M' in p:
            st[1] += 1
        elif 'D' in p:
            st[2] += 1
    if sum(st) != 10:
        print('aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
    return st


def struct(matches):
    for m in matches:
        print('Match %d' % m)
        for p in ['1H', '2H']:
            me = fe[(fe.MatchID == m) & (fe.MatchPeriod == p) & (fe.TeamID == 'Huskies')]
            print(p)
            on_court = set()
            sub = {}
            for i in range(len(me)):
                if len(on_court) < 11:
                    if me['EventType'].iloc[i] != 'Substitution':
                        if type(me['OriginPlayerID'].iloc[i]) is str and me['OriginPlayerID'].iloc[
                                i] not in sub.values():
                            on_court.add(me['OriginPlayerID'].iloc[i])
                        if type(me['DestinationPlayerID'].iloc[i]) is str and me['DestinationPlayerID'].iloc[
                                i] not in sub.values():
                            on_court.add(me['DestinationPlayerID'].iloc[i])
                    else:
                        # on_court.add(me['OriginPlayerID'].iloc[i])
                        sub[me['OriginPlayerID'].iloc[i]] = me['DestinationPlayerID'].iloc[i]
                    if len(on_court) == 11:
                        print(on_court)
                        print('%s First:' % p, phrase_srtuct(on_court))
                    elif len(on_court) > 11:
                        print('大于11')
                else:
                    if len(sub) != 0:
                        for k, v in sub.items():
                            on_court.remove(k)
                            on_court.add(v)
                            print(k, v)
                            print('Then1:', phrase_srtuct(on_court))
                        sub = {}
                    if me['EventType'].iloc[i] == 'Substitution':
                        on_court.remove(me['OriginPlayerID'].iloc[i])
                        on_court.add(me['DestinationPlayerID'].iloc[i])
                        print('Then2:', phrase_srtuct(on_court))


struct([19])
