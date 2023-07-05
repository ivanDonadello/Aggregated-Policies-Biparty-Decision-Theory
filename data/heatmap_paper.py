import numpy as np
import matplotlib.pyplot as plt

def SDM(q_prop, q_opp, w):
    score = ((1-w) * (q_prop + q_opp)) - (w * abs(q_prop - q_opp))
    return score

def DON(U, w):
    func = (w * (np.linalg.norm(U, ord=1)**2)) - ((1-w) * np.linalg.norm(U, ord=1))
    #func = w * np.sqrt(np.sum(np.power(value, 2))) - (1-w) * np.sqrt(np.sum(np.power(value, 2)))**2
    return func #* -1

def aggregation(q_prop, q_opp, p):
    q_prop = float(q_prop)
    q_opp = float(q_opp)
    return ((1 / 2) * (q_prop ** p + q_opp ** p)) ** (1 / p)

# ((1 / 2) * (self.utility_proponent ** p + self.utility_opponent ** p)) ** (1 / p)

def bimaximax(q_prop, q_opp, p):
    return q_prop


def run_policy(q_prop, q_opp, p_value, name):
    if p_value == 0:
        return bimaximax(q_prop, q_opp, p_value)
    elif p_value == -1:
        return aggregation(q_prop,q_opp, p_value)

    else:
        if "DON" in name:
            return DON([q_prop,q_opp], p_value)
        if "SDM" in name:
            return SDM(q_prop, q_opp, p_value)


# data generation
x = np.arange(1, 11)
y = np.arange(1, 11)
data = np.zeros((10, 10))
# data_agg = np.zeros((10, 10))
# data_bimax = np.zeros((10, 10))
print(data)

policies = [0.1, 0.5, 0.9, 0.1, 0.5, 0.9, -1, 0]
titles = [f'SDM. w={policies[0]}',f'SDM. w={policies[1]}',f'SDM. w={policies[2]}',
          f'DON. w={policies[3]}',f'DON. w={policies[4]}',f'DON. w={policies[5]}',
          f'Aggregation. p={policies[6]}',f'Bimaximax' ]
names = ['policy_SDM_1','policy_SDM_2','policy_SDM_3', 'policy_DON_1','policy_DON_2','policy_DON_3','policy_aggregation','policy_bimax']
#title = f'Policy: OverallScore. w={w}'

for index, policy in enumerate(policies):
    print(titles[index])
    print(policy)
    data = np.zeros((10, 10))
    for i in range(10):
        for j in range(10):
            data[i][j] = run_policy(x[i],y[j], policy, titles[index])

    # flip/rotate the data vertically
    data = np.flip(data, 0)
    start = 0
    end = 10
    width = end - start
    data = (data - data.min()) / (data.max() - data.min()) * width + start
    #data = np.log1p(data)

    # heatmap definition
    fig, ax = plt.subplots()
    im = ax.imshow(data, cmap='YlOrRd')

    # tick labels and show the colorbar
    ax.set_xticks(np.arange(10))
    ax.set_yticks(np.arange(10))
    ax.set_xticklabels(x)
    ax.set_yticklabels(y[::-1]) # rotate/change the y vector order
    cbar = ax.figure.colorbar(im, ax=ax)

    # axis labels
    ax.set_xlabel('Q_opp')
    ax.set_ylabel('Q_prop')

    # title
    ax.set_title('Policy: '+titles[index])

    # rotate and align the tick labels
    plt.setp(ax.get_xticklabels(), rotation=0, ha="right",
             rotation_mode="anchor")

    # loop over data to create the annotations
    for i in range(10):
        for j in range(10):
            text = ax.text(j, i, round(data[i, j], 2),
                           ha="center", va="center", color="black", size="8")

    plt.savefig(f'heatmaps_paper/{names[index]}.pdf')

#plt.show()











