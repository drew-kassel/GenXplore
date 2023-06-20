"""
Part of GenXplore software to process results of the GenX capacity expansion model.

Functions to compile costs of investment, operation and maintenance, fuel, network expansion, etc.

Written by:
Drew Kassel
Webber Energy Group

"""

# Import packages
import os
from sys import exit
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from matplotlib import style

plt.style.use("default")
# plt.style.use("dark_background")

from matplotlib.lines import Line2D

pd.options.mode.chained_assignment = None

from capacity_expansion import capacity_by_type, capacity_by_type_per_scenario
from transmission_expansion import capacity_by_line

import settings


# Functions
def annual_fix_costs(scenario, years):
    cfix = []
    for i in range(len(years)):
        if settings.multi_stage == 1:
            path = (
                settings.root_dir
                + scenario
                + "/Results"
                + "/Results_p%s" % str(i + 1)
                + "/costs.csv"
            )
        elif settings.multi_stage == 0:
            path = settings.root_dir + scenario + "/Results" + "/costs.csv"
        cfix_i = pd.read_csv(path)
        cfix_i = cfix_i[cfix_i["Costs"] == "cFix"]
        cfix_i.drop(["Total", "Costs"], axis=1, inplace=True)
        if settings.region == "ERCOT":
            cfix_i = cfix_i[list(settings.ERCOT_regions)]
        elif settings.region == "WECC":
            cfix_i = cfix_i[list(settings.WECC_regions)]
        cfix_i = list(cfix_i.iloc[0])
        cfix_i = [float(x) for x in cfix_i]
        cfix.append(sum(cfix_i))
    return cfix


def annual_var_costs(scenario, years):
    cvar = []
    for i in range(len(years)):
        if settings.multi_stage == 1:
            path = (
                settings.root_dir
                + scenario
                + "/Results"
                + "/Results_p%s" % str(i + 1)
                + "/costs.csv"
            )
        elif settings.multi_stage == 0:
            path = settings.root_dir + scenario + "/Results" + "/costs.csv"
        cvar_i = pd.read_csv(path)
        cvar_i = cvar_i[cvar_i["Costs"] == "cVar"]
        cvar_i.drop(["Total", "Costs"], axis=1, inplace=True)
        if settings.region == "ERCOT":
            cvar_i = cvar_i[list(settings.ERCOT_regions)]
        elif settings.region == "WECC":
            cvar_i = cvar_i[list(settings.WECC_regions)]
        cvar_i = list(cvar_i.iloc[0])
        cvar_i = [float(x) for x in cvar_i]
        cvar.append(sum(cvar_i))
    return cvar


def annual_nse_costs(scenario, years):
    cnse = []
    for i in range(len(years)):
        if settings.multi_stage == 1:
            path = (
                settings.root_dir
                + scenario
                + "/Results"
                + "/Results_p%s" % str(i + 1)
                + "/costs.csv"
            )
        elif settings.multi_stage == 0:
            path = settings.root_dir + scenario + "/Results" + "/costs.csv"
        cnse_i = pd.read_csv(path)
        cnse_i = cnse_i[cnse_i["Costs"] == "cNSE"]
        cnse_i.drop(["Total", "Costs"], axis=1, inplace=True)
        if settings.region == "ERCOT":
            cnse_i = cnse_i[list(settings.ERCOT_regions)]
        elif settings.region == "WECC":
            cnse_i = cnse_i[list(settings.WECC_regions)]
        cnse_i = list(cnse_i.iloc[0])
        cnse_i = [float(x) for x in cnse_i]
        cnse.append(sum(cnse_i))
    return cnse


def annual_start_costs(scenario, years):
    cstart = []
    for i in range(len(years)):
        if settings.multi_stage == 1:
            path = (
                settings.root_dir
                + scenario
                + "/Results"
                + "/Results_p%s" % str(i + 1)
                + "/costs.csv"
            )
        elif settings.multi_stage == 0:
            path = settings.root_dir + scenario + "/Results" + "/costs.csv"
        cstart_i = pd.read_csv(path)
        cstart_i = cstart_i[cstart_i["Costs"] == "cStart"]
        cstart_i.drop(["Total", "Costs"], axis=1, inplace=True)
        if settings.region == "ERCOT":
            cstart_i = cstart_i[list(settings.ERCOT_regions)]
        elif settings.region == "WECC":
            cstart_i = cstart_i[list(settings.WECC_regions)]
        cstart_i = list(cstart_i.iloc[0])
        cstart_i = [float(x) for x in cstart_i]
        cstart.append(sum(cstart_i))
    return cstart


def annual_network_expansion_costs(scenario, years):
    cnetworkexpansion = []
    for i in range(len(years)):
        if settings.multi_stage == 1:
            path = (
                settings.root_dir
                + scenario
                + "/Results"
                + "/Results_p%s" % str(i + 1)
                + "/network_expansion.csv"
            )
        elif settings.multi_stage == 0:
            path = settings.root_dir + scenario + "/Results" + "/networkexpansion.csv"
        cnetworkexpansion_i = pd.read_csv(path)
        if settings.region == "ERCOT":
            cnetworkexpansion_i = cnetworkexpansion_i[
                cnetworkexpansion_i["Line"].isin([int(x) for x in settings.ERCOT_lines])
            ]
        elif settings.region == "WECC":
            cnetworkexpansion_i = cnetworkexpansion_i[
                cnetworkexpansion_i["Line"].isin([int(x) for x in settings.WECC_lines])
            ]
        cnetworkexpansion_i = list(cnetworkexpansion_i["Cost_Trans_Capacity"])
        cnetworkexpansion.append(sum(cnetworkexpansion_i))
    return cnetworkexpansion


def total_annual_cost(scenario, years):
    cfix = annual_fix_costs(scenario, years)
    cvar = annual_var_costs(scenario, years)
    cnse = annual_nse_costs(scenario, years)
    cstart = annual_start_costs(scenario, years)
    cnetworkexpansion = annual_network_expansion_costs(scenario, years)

    ctot = []
    for i in range(len(years)):
        ctot.append(cfix[i] + cvar[i] + cnse[i] + cstart[i] + cnetworkexpansion[i])
    return ctot


def cost_diff(scenario, years):
    ctot_base = total_annual_cost(list(settings.scenarios_dict)[0], years)
    ctot = total_annual_cost(scenario, years)

    cdiff = []
    for i in range(len(years)):
        cdiff.append(ctot[i] - ctot_base[i])
    return cdiff


def cost_diff_interpolation(cdiff, years):
    years_float = [float(x) for x in years]
    num_years = int(years_float[-1] - years_float[0])

    all_years = []
    for i in range(num_years + 1):
        all_years.append(years_float[0] + i)

    interpolated_diff = list(np.interp(all_years, years_float, cdiff))
    return interpolated_diff


def cost_diff_cumulation(interpolated_diff):
    cumulative_diff = []
    length = len(interpolated_diff)
    cumulative_diff = [sum(interpolated_diff[0:x:1]) for x in range(0, length + 1)]
    cumulative_diff = cumulative_diff[1:]
    return cumulative_diff


def cumulative_cost_diff_all_scenarios():
    scenarios = list(settings.scenarios_dict)
    years = list(settings.years_dict.values())[1:]

    zero_data = np.zeros(shape=(int(years[-1]) - int(years[0]) + 1, len(scenarios)))
    cost_diffs_df = pd.DataFrame(zero_data, columns=scenarios)

    for i in range(len(scenarios)):
        scenario = scenarios[i]
        cdiff = cost_diff(scenario, years)
        interpolated_diff = cost_diff_interpolation(cdiff, years)
        cumulative_diff = cost_diff_cumulation(interpolated_diff)

        cost_diffs_df[scenario] = [x / 10**9 for x in cumulative_diff]

    all_years = []
    for i in range(len(cost_diffs_df)):
        all_years.append(int(years[0]) + i)

    cost_diffs_df["Year"] = all_years
    cost_diffs_df.set_index("Year", inplace=True)

    path = (
        settings.root_dir
        + "/GenXplore_results"
        + "/all_scenarios"
        + "/"
        + str(settings.region)
    )
    if os.path.exists(path):
        cost_diffs_df.to_csv(
            path + "/" + str(settings.region) + "_" + "cost_differences_table.csv"
        )
    else:
        os.makedirs(path)
        cost_diffs_df.to_csv(
            path + "/" + str(settings.region) + "_" + "cost_differences_table.csv"
        )
    return cost_diffs_df


# Plotting
def cumulative_cost_difference_plotter(cost_diffs_df, year):
    scenarios = list(settings.scenarios_dict)

    cost_diffs_df = cost_diffs_df[cost_diffs_df.index == int(year)]
    cost_diffs_df.reset_index(inplace=True)
    cost_diffs_df.drop("Year", axis=1, inplace=True)
    cost_diffs_df = cost_diffs_df.T
    cost_diffs_df.reset_index(inplace=True)
    cost_diffs_df = cost_diffs_df.iloc[::-1]
    cost_diffs_df.columns = ["scenario", "cumulative_cost_difference"]
    cost_diffs_df.replace(settings.scenarios_dict, inplace=True)
    cost_diffs_df.set_index("scenario", inplace=True)

    plt.figure(figsize=(10, 8))

    barWidth = 0.3
    br = np.arange(len(cost_diffs_df))

    values = list(cost_diffs_df["cumulative_cost_difference"])
    for i in range(len(br)):
        value = values[i]
        if value > 0:
            plt.barh(
                br[i],
                value,
                color="#c32f27",
                height=barWidth,
                edgecolor="black",
                zorder=4,
            )
        elif value < 0:
            plt.barh(
                br[i],
                value,
                color="#7ae582",
                height=barWidth,
                edgecolor="black",
                zorder=4,
            )
        else:
            plt.barh(
                br[i],
                value,
                color="#00a5cf",
                height=barWidth,
                edgecolor="black",
                zorder=4,
            )

    plt.yticks(br, cost_diffs_df.index, fontsize=15)
    plt.xticks(fontsize=20)
    plt.xlim(-12, 30)
    # plt.xlim(
    #     -1.2 * abs(max(list(cost_diffs_df["cumulative_cost_difference"]), key=abs)),
    #     1.2 * abs(max(list(cost_diffs_df["cumulative_cost_difference"]), key=abs)),
    # )
    plt.grid(axis="x", linestyle="-", color="0.5", zorder=0)
    plt.axvline(x=0, zorder=5, color="0.5")

    plt.xlabel(
        "Cumulative cost differences\nfrom 2022 to 2035\n[$billion]",
        fontweight="bold",
        fontsize=20,
        labelpad=25,
    )

    for i in range(len(scenarios)):
        if i == len(scenarios) - 1:
            pass
        else:
            if values[i] > 0:
                plt.text(
                    values[i],
                    br[i],
                    "$" + str(round(values[i])) + "B",
                    horizontalalignment="left",
                    verticalalignment="center",
                    fontsize=15,
                )
            elif values[i] < 0:
                plt.text(
                    values[i],
                    br[i],
                    "$" + str(round(values[i])) + "B",
                    horizontalalignment="right",
                    verticalalignment="center",
                    fontsize=15,
                )
            else:
                plt.text(
                    values[i],
                    br[i],
                    "$0B",
                    horizontalalignment="left",
                    verticalalignment="center",
                    fontsize=15,
                )

    path = (
        settings.root_dir
        + "GenXplore_results"
        + "/all_scenarios"
        + "/"
        + str(settings.region)
    )
    if os.path.exists(path):
        plt.savefig(
            path + "/%s_cost_differences_to_%s.png" % (settings.region, str(year)),
            bbox_inches="tight",
        )
        plt.clf()
    else:
        os.makedirs(path)
        plt.savefig(
            path
            + "/%s_cost_differences_to_%s.png" % (settings.settings.region, str(year)),
            bbox_inches="tight",
        )
        plt.clf()
    return


# cost_diffs_df = cumulative_cost_diff_all_scenarios()
# cumulative_cost_difference_plotter(cost_diffs_df, list(settings.model_year.values())[0])
