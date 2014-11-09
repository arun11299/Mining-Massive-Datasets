import copy
import math
"""
https://class.coursera.org/mmds-001/forum/thread?thread_id=753#comment-1339

[Dmitry Nozhnin]
Hint: CTRs are there not purely for ranking the advertisers.

Users click only one ad per page view, that's kinda bottomline assumption, and there is a certain CTR for each of the slots depending on the ad being shown. Take CTRs into account and then you get the right number of clicks for B and C. A runs out of budget in 10 clicks, that's right btw.

[low yi xiang]
i did not use that formula though, i tried ashic's approach, it did not seem to work out. what i did was if A had 10 click throughs, with a click through rate of x, that means there must be a total of 10/x impressions. so with that impressions, i then multiply by the click through rate of C and E to find out what is the number of clicks they have, rounded to the nearest integer.
"""

all_advertisers = []
top_3_advertisers = []

class Advertiser:
    def __init__(self, name, bid, ctr1, ctr2, ctr3, budget):
        self.name = name
        self.bid = bid # bid price in dollars
        self.ctr1 = ctr1 # click through rate for position 1
        self.ctr2 = ctr2 # click through rate for position 2
        self.ctr3 = ctr3 # click through rate for position 3
        self.budget = budget # total budget for the advertiser
        # List of expected revenue
        self.er = [bid * ctr1, bid * ctr2, bid * ctr3]

        # List of CTR's
        self.ctr = [ctr1, ctr2, ctr3]

        self.act_clicks = 0 # Expected clicks using CTR
        self.clicks = 0 # No. of clicks made for this Advertiser

    def remove(self):
        ## Will not come on top while sorting
        self.er = [-1, -1, -1]

    def __repr__(self):
        print "repr"
        return str(self.er)

## Functions for sorting
def get_key_ctr1(advertiser):
    return advertiser.er[0]

def get_key_ctr2(advertiser):
    return advertiser.er[1]

def get_key_ctr3(advertiser):
    return advertiser.er[2]

def find(advertiser):
    global all_advertisers

    for idx, obj in enumerate(all_advertisers):
        if advertiser.name == obj.name:
            return idx

def compute_top_3():
    global all_advertisers, top_3_advertisers

    ## Initialize the list
    top_3_advertisers = []
    tmp_adv = copy.deepcopy(all_advertisers)
    # top advertiser for CRT1
    tmp = sorted(tmp_adv, key=get_key_ctr1)[-1]
    print tmp
    top_3_advertisers.append(find(tmp))
    tmp_adv.remove(tmp)

    # top advertiser for CRT2
    tmp = sorted(tmp_adv, key=get_key_ctr2)[-1]
    print tmp
    top_3_advertisers.append(find(tmp))
    tmp_adv.remove(tmp)

    # top advertiser for CRT3
    tmp = sorted(tmp_adv, key=get_key_ctr3)[-1]
    print tmp
    top_3_advertisers.append(find(tmp))
    tmp_adv.remove(tmp)

    print "==============="

    print top_3_advertisers


def start_main():
    global all_advertisers, top_3_advertisers

    compute_top_3()

    total_clicks = 101
    clicks = 0
    loop_stop_cond = False

    while not loop_stop_cond:
        if clicks > total_clicks:
            break

        for ind, idx in enumerate(top_3_advertisers):
            all_advertisers[idx].budget -= all_advertisers[idx].bid

            if all_advertisers[idx].budget <= 0:
                # Recalculate top 3 advertisers
                all_advertisers[idx].act_clicks += all_advertisers[idx].clicks

                impressions = all_advertisers[idx].act_clicks / all_advertisers[idx].ctr[ind]
                impressions = math.ceil(impressions)

                all_advertisers[idx].remove()

                # update the click using CTR for other two
                denom = 0
                for index, id in enumerate(top_3_advertisers):
                    denom += all_advertisers[id].ctr[index]

                for index, id in enumerate(top_3_advertisers):
                    if id != idx:
                        all_advertisers[id].act_clicks += math.ceil(impressions * all_advertisers[id].ctr[index])
                        #all_advertisers[id].act_clicks += math.ceil(all_advertisers[idx].clicks * all_advertisers[id].ctr[index]/ denom)

                compute_top_3() 
                break

            all_advertisers[idx].clicks += 1

            clicks += 1

            ## Print
        disp = ""
        for obj in all_advertisers:
            disp += " " + str(obj.act_clicks)
        print disp


if __name__ == "__main__":
    A = Advertiser("A", 0.10, 0.015, 0.010, 0.005, 1)
    B = Advertiser("B", 0.09, 0.016, 0.012, 0.006, 2)
    C = Advertiser("C", 0.08, 0.017, 0.014, 0.007, 3)
    D = Advertiser("D", 0.07, 0.018, 0.015, 0.008, 4)
    E = Advertiser("E", 0.06, 0.019, 0.016, 0.010, 5)

    for obj in [A, B, C, D, E]:
        all_advertisers.append(obj)

    start_main()
