from numpy import mean

def my_dist(v1, v2):
    # select the votes in which both deputies participated
    idx = (v1 != 0) & (v2 != 0)
    # TODO add attendence correction/weight
    k = mean(idx)  ## k=1 -> 1 ----------------  k<1 ->
    if k > 0:
        discordance = mean(v1[idx] != v2[idx])
    else:
        discordance = .75
    return discordance