"""
Part of GenXplore software to process results of the GenX capacity expansion model.

Functions that analyze the transmission capacity built by the model.

Written by:
Drew Kassel
Webber Energy Group

"""

# Import packages
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from matplotlib import style

plt.style.use("default")
# plt.style.use("dark_background")

from matplotlib.lines import Line2D

pd.options.mode.chained_assignment = None

import settings

# Functions
def optimal_connection(scenario, line):
    new_line_cap_tot = []
    for i in range(4):
        if settings.multi_stage == 1:
            path = (
                settings.root_dir
                + scenario
                + "Results/Results_p%s/network_expansion.csv" % (scenario, str(i + 1))
            )
        elif settings.multi_stage == 0:
            path = settings.root_dir + scenario + "Results/network_expansion.csv"
        connect_i = pd.read_csv(path)
        new_line_cap = connect_i[connect_i["Line"] == line]["New_Trans_Capacity"].iloc[
            0
        ]
        if i == 0:
            lowerbound = round(new_line_cap / 1000)
            new_line_cap_tot.append(new_line_cap)
        else:
            new_line_cap_tot.append(new_line_cap)
    upperbound = round(sum(new_line_cap_tot) / 1000)
    return lowerbound, upperbound


def capacity_by_line():
    scenarios = list(settings.scenarios_dict)
    years = list(settings.years_dict.values())

    for i in range(len(scenarios)):
        scenario = scenarios[i]
        path = settings.root_dir + scenario

        trans_cap = pd.read_csv(path + "/Inputs/Inputs_p1/Network.csv")
        trans_cap = trans_cap[["Network_Lines", "Line_Max_Flow_MW"]]
        trans_cap.rename(
            {"Network_Lines": "Line", "Line_Max_Flow_MW": years[0]},
            axis=1,
            inplace=True,
        )

        for j in range(len(years) - 1):
            if settings.multi_stage == 1:
                path = (
                    settings.root_dir
                    + scenario
                    + "/Results/Results_p"
                    + str(j + 1)
                    + "/network_expansion.csv"
                )
            elif settings.multi_stage == 0:
                path = (
                    settings.root_dir + scenario + "/Results" + "/network_expansion.csv"
                )
            trans_loc = pd.read_csv(path)
            trans_loc = trans_loc[["Line", "New_Trans_Capacity"]]

            trans_cap = trans_cap.merge(
                trans_loc, how="inner", left_on="Line", right_on="Line"
            )
            trans_cap[years[j + 1]] = (
                trans_cap[years[j]] + trans_cap["New_Trans_Capacity"]
            )
            trans_cap.drop("New_Trans_Capacity", axis=1, inplace=True)

        trans_cap.set_index("Line", inplace=True)

        # Write to csv file
        path = (
            settings.root_dir + "GenXplore_results/" + scenario + "/" + settings.region
        )
        if os.path.exists(path):
            trans_cap.to_csv(path + "/" + "trans_cap_by_line.csv")
        else:
            os.makedirs(path)
            trans_cap.to_csv(path + "/" + "trans_cap_by_line.csv")
    return


def flow_across_line(scenario, line):
    year = list(settings.model_year.values())[0]

    path = (
        settings.root_dir
        + scenario
        + "/Results/%s/flow.csv" % list(settings.model_year)[0]
    )

    flow = pd.read_csv(path)
    flow = flow[line]
    flow = flow.T

    netsum = round(flow[0] / 1000, -2)

    flow = list(flow[1:])
    flow = [x / 1000 for x in flow]

    plt.figure(figsize=(15, 8))

    x = []
    for i in range(len(flow)):
        x.append(i)

    plt.plot(x, flow, linestyle="-", linewidth=4, color="#E7863C", zorder=3)

    plt.ylabel("Energy Flow [GWh]", fontweight="bold", fontsize=25, labelpad=25)
    plt.xticks([x[0], x[-1] + 1], [str(x[0]), str(x[-1] + 1)], fontsize=15)
    plt.xlim(0, 8760)
    plt.yticks(fontsize=25)

    ymax = abs(max(flow, key=abs))
    plt.ylim(-1.2 * ymax, 1.2 * ymax)

    plt.grid(axis="y", linestyle="-", color="0.5", zorder=0)
    plt.axhline(y=0, zorder=5, color="0")

    plt.text(
        x[-1] + 1 + 100,
        0,
        "Net Annual Sum\n%s [GWh]" % str(int(netsum)),
        fontsize=25,
        horizontalalignment="left",
        verticalalignment="center",
    )

    path = settings.root_dir + "/GenXplore_results/" + scenario + "/" + settings.region
    if os.path.exists(path):
        plt.savefig(
            path + "/%s_flow_in_%s.png" % (settings.region, year),
            bbox_inches="tight",
        )
        plt.clf()
    else:
        os.makedirs(path)
        plt.savefig(
            path + "/%s_flow_in_%s.png" % (settings.region, year),
            bbox_inches="tight",
        )
        plt.clf()
    return
