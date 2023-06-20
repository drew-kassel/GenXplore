"""
Part of GenXplore software to process results of the GenX capacity expansion model.

Functions to compile C02 emissions.

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

import settings


# Functions
def total_annual_emissions(scenario, years):
    etot = []
    for i in range(len(years)):
        if settings.multi_stage == 1:
            path = (
                settings.root_dir
                + scenario
                + "/Results"
                + "/Results_p%s" % str(i + 1)
                + "/emissions.csv"
            )
        elif settings.multi_stage == 0:
            path = settings.root_dir + scenario + "/Results" + "/emissions.csv"
        etot_i = pd.read_csv(path)
        etot_i = etot_i.T
        etot_i.columns = etot_i.iloc[0]
        etot_i.drop(index=etot_i.iloc[:1, :].index.tolist(), inplace=True)
        etot_i.drop("Total", axis=0, inplace=True)
        etot_i = etot_i[["AnnualSum"]]

        zone_dict = {}
        for i in range(len(etot_i)):
            zone_dict[str(i + 1)] = "Zone%s" % str(i + 1)

        etot_i.rename(zone_dict, axis=0, inplace=True)

        if settings.region == "ERCOT":
            etot_i = etot_i[etot_i.index.isin(list(settings.ERCOT_regions))]
        elif settings.region == "WECC":
            etot_i = etot_i[etot_i.index.isin(list(settings.WECC_regions))]
        etot_i = list(etot_i["AnnualSum"])
        etot.append(sum(etot_i) / (10**3))
    return etot


def emissions_interpolation(etot, years):
    years_float = [float(x) for x in years]
    num_years = int(years_float[-1] - years_float[0])

    all_years = []
    for i in range(num_years + 1):
        all_years.append(years_float[0] + i)

    interpolated_e = list(np.interp(all_years, years_float, etot))
    return interpolated_e


def emissions_cumulation(interpolated_e):
    cumulative_e = []
    length = len(interpolated_e)
    cumulative_e = [sum(interpolated_e[0:x:1]) for x in range(0, length + 1)]
    cumulative_e = cumulative_e[1:]
    return cumulative_e


def cumulative_emissions_all_scenarios():
    scenarios = list(settings.scenarios_dict)
    years = list(settings.years_dict.values())[1:]

    zero_data = np.zeros(shape=(int(years[-1]) - int(years[0]) + 1, len(scenarios)))
    emissions_df = pd.DataFrame(zero_data, columns=scenarios)

    for i in range(len(scenarios)):
        scenario = scenarios[i]
        etot = total_annual_emissions(scenario, years)
        interpolated_e = emissions_interpolation(etot, years)
        cumulative_e = emissions_cumulation(interpolated_e)

        emissions_df[scenario] = [x for x in cumulative_e]

    all_years = []
    for i in range(len(emissions_df)):
        all_years.append(int(years[0]) + i)

    emissions_df["Year"] = all_years
    emissions_df.set_index("Year", inplace=True)

    path = (
        settings.root_dir
        + "/GenXplore_results"
        + "/all_scenarios"
        + "/"
        + str(settings.region)
    )
    if os.path.exists(path):
        emissions_df.to_csv(
            path + "/" + str(settings.region) + "_" + "emissions_table.csv"
        )
    else:
        os.makedirs(path)
        emissions_df.to_csv(
            path + "/" + str(settings.region) + "_" + "emissions_table.csv"
        )
    return emissions_df


# Plotting
def cumulative_emissions_diff_plotter(emissions_df, year):
    scenarios = list(settings.scenarios_dict)

    emissions_df = emissions_df[emissions_df.index == int(year)]
    emissions_df.reset_index(inplace=True)
    emissions_df.drop("Year", axis=1, inplace=True)
    emissions_df = emissions_df.T
    emissions_df.reset_index(inplace=True)

    etot_base = emissions_df[emissions_df["index"] == list(settings.scenarios_dict)[0]][
        0
    ][0]
    etot = list(emissions_df[0])
    ediff = []
    for i in range(len(etot)):
        ediff.append(etot[i] - etot_base)

    emissions_df.drop(0, axis=1)
    emissions_df[0] = ediff
    emissions_df = emissions_df.iloc[::-1]
    emissions_df.columns = ["scenario", "cumulative_emissions"]
    emissions_df.replace(settings.scenarios_dict, inplace=True)
    emissions_df.set_index("scenario", inplace=True)

    plt.figure(figsize=(10, 8))

    barWidth = 0.3
    br = np.arange(len(emissions_df))

    values = list(emissions_df["cumulative_emissions"])
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

    plt.yticks(br, emissions_df.index, fontsize=15)
    plt.xticks(fontsize=20)
    plt.xlim(-260, 50)
    # plt.xlim(
    #     -1.2 * abs(max(list(emissions_df["cumulative_emissions"]), key=abs)),
    #     1.2 * abs(max(list(emissions_df["cumulative_emissions"]), key=abs)),
    # )
    plt.grid(axis="x", linestyle="-", color="0.5", zorder=0)
    plt.axvline(x=0, zorder=5, color="0.5")

    plt.xlabel(
        "Cumulative CO2 emission differences\nfrom 2022 to 2035\n[million metric tons]",
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
                    str(round(values[i])) + "MMT",
                    horizontalalignment="left",
                    verticalalignment="center",
                    fontsize=15,
                )
            elif values[i] < 0:
                plt.text(
                    values[i],
                    br[i],
                    str(round(values[i])) + "MMT",
                    horizontalalignment="right",
                    verticalalignment="center",
                    fontsize=15,
                )
            else:
                plt.text(
                    values[i],
                    br[i],
                    "0MMT",
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
            path + "/%s_emission_differences_to_%s.png" % (settings.region, str(year)),
            bbox_inches="tight",
        )
        plt.clf()
    else:
        os.makedirs(path)
        plt.savefig(
            path + "/%s_emission_differences_to_%s.png" % (settings.region, str(year)),
            bbox_inches="tight",
        )
        plt.clf()
    return


# emissions_df = cumulative_emissions_all_scenarios()
# cumulative_emissions_diff_plotter(emissions_df, list(settings.model_year.values())[0])
