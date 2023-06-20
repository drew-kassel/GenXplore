"""
Part of GenXplore software to process results of the GenX capacity expansion model.

Functions that analyze the generation capacity built by the model.

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
def capacity_by_type():
    # Defines scenarios and years from settings
    scenarios = list(settings.scenarios_dict)
    years = list(settings.years_dict)

    # Create big, total capacity dataframe (this is what I'm hoping to plot at the end)
    zero_data = np.zeros(shape=(len(settings.years_dict), len(scenarios)))
    tot_cap = pd.DataFrame(zero_data, columns=settings.scenarios_dict)

    # For loop to iterate over results from all scenarios
    # For each scenario this loop will find the results file, format it, and append it to the final dataframe
    for i in range(len(scenarios)):
        scenario = scenarios[i]
        if settings.multi_stage == 1:
            loc_cap = pd.read_csv(
                settings.root_dir + scenario + "/Results/capacities_multi_stage.csv"
            )
            loc_tech = pd.read_csv(
                settings.root_dir + scenario + "/Inputs/Inputs_p1/Generators_data.csv"
            )
        elif settings.multi_stage == 0:
            loc_cap = pd.read_csv(
                settings.root_dir + scenario + "/Results/capacity.csv"
            )
            loc_tech = pd.read_csv(
                settings.root_dir + scenario + "/Inputs/Generators_data.csv"
            )
        loc_tech = loc_tech[["Resource", "technology"]]
        loc_cap = loc_cap.merge(
            loc_tech, how="inner", left_on="Resource", right_on="Resource"
        )
        if settings.region == "ERCOT":
            for j in range(len(settings.WECC_regions)):
                loc_cap = loc_cap[
                    loc_cap["Resource"].str.contains(
                        list(settings.WECC_regions.values())[j]
                    )
                    == False
                ]
        elif settings.region == "WECC":
            for j in range(len(settings.ERCOT_regions)):
                loc_cap = loc_cap[
                    loc_cap["Resource"].str.contains(
                        list(settings.ERCOT_regions.values())[j]
                    )
                    == False
                ]
        loc_cap["technology"] = loc_cap["technology"].replace(settings.tech_dict)
        keep_col = ["technology"]
        for j in range(len(years)):
            keep_col.append(years[j])
        loc_cap = loc_cap[keep_col]
        loc_cap = loc_cap.groupby("technology", as_index=False).agg("sum")
        loc_cap = loc_cap[loc_cap["technology"].isin(settings.technologies)]
        sorting = pd.DataFrame({"tech": settings.technologies})
        sorting = sorting.reset_index().set_index("tech")
        loc_cap["sorting"] = loc_cap["technology"].map(sorting["index"])
        loc_cap.sort_values("sorting", inplace=True)
        loc_cap.set_index("sorting", inplace=True)
        for k in range(len(years)):
            loc_cap_df = loc_cap[["technology", years[k]]]
            loc_cap_df.rename(settings.years_dict, axis=1, inplace=True)
            tot_cap[scenario].iloc[k] = loc_cap_df
    tot_cap = tot_cap.T
    tot_cap.columns = years
    tot_cap.rename(settings.years_dict, axis=1, inplace=True)
    tot_cap.reset_index(inplace=True)
    tot_cap.rename({"index": "scenario"}, axis=1, inplace=True)
    return tot_cap


def capacity_by_type_per_scenario(tot_cap):
    # Find settings.technologies and years
    technologies_i = list(tot_cap.iloc[0, 1]["technology"])
    years = list(tot_cap.columns[1:])

    # Create zero dataframe
    zero_data = np.zeros(shape=(len(technologies_i), len(years)))

    # Loop through all scenarios, build dataframes for each individual scenario
    for i in range(len(tot_cap)):
        scenario = tot_cap.iloc[i, 0]
        cap_by_type = pd.DataFrame(zero_data, columns=years)
        cap_by_type["technology"] = technologies_i
        for j in range(len(years)):
            cap_by_type[years[j]] = tot_cap[years[j]].iloc[i][years[j]]
        cap_by_type.set_index("technology", inplace=True)

        # Write to csv file
        path = (
            settings.root_dir + "/GenXplore_results/" + scenario + "/" + settings.region
        )
        if os.path.exists(path):
            cap_by_type.to_csv(path + "/" + "gen_cap_by_type.csv")
        else:
            os.makedirs(path)
            cap_by_type.to_csv(path + "/" + "gen_cap_by_type.csv")
    return


def capacity_by_type_plotter(tot_cap):
    technologies_i = list(tot_cap.iloc[0, 1]["technology"])
    years = list(tot_cap.columns[3:])
    year = list(settings.model_year.values())[0]
    scenarios = list(tot_cap["scenario"])

    plt.figure(figsize=(20, 10))

    barWidth = 0.15
    cushion = 1.1
    br = np.arange(len(tot_cap))
    br_years = {}

    for j in range(len(years)):
        br_years[j] = [x + (cushion * j * barWidth) for x in br]

    for k in range(len(years)):
        bottom = []
        for i in range(len(tot_cap)):
            bottom.append(0)
        for j in range(len(technologies_i)):
            bar = []
            for l in range(len(tot_cap)):
                bar.append(
                    tot_cap[years[k]]
                    .iloc[l][
                        tot_cap[years[k]].iloc[l]["technology"] == technologies_i[j]
                    ][years[k]]
                    .iloc[0]
                    / 1000
                )
            plt.bar(
                br_years[k],
                bar,
                color=settings.colors[technologies_i[j]],
                width=barWidth,
                label=years[k],
                edgecolor="black",
                bottom=bottom,
                zorder=4,
            )
            bottom = list(np.add(bottom, bar))

    initial_year = settings.years_dict["StartCap_p1"]
    bottom = []
    bottom.append(0)
    for j in range(len(technologies_i)):
        bar = []
        bar.append(
            tot_cap[initial_year]
            .iloc[0][tot_cap[initial_year].iloc[0]["technology"] == technologies_i[j]][
                initial_year
            ]
            .iloc[0]
            / 1000
        )
        plt.bar(
            -1,
            bar,
            color=settings.colors[technologies_i[j]],
            width=barWidth,
            label=years[k],
            edgecolor="black",
            bottom=bottom,
            zorder=4,
        )
        bottom = list(np.add(bottom, bar))

    count = 0
    xticks = []
    xlabels = []

    xticks.append(-1)
    xlabels.append(initial_year)
    for r in range(len(br)):
        for s in range(len(years)):
            xticks.append(count + (cushion * s * barWidth))
            xlabels.append(years[s])
        count += 1

    legend_elements = []
    for r in range(len(technologies_i)):
        tech = technologies_i[r]
        legend_elements.append(
            Line2D([0], [0], color=settings.colors[tech], linewidth=15)
        )

    plt.ylabel(
        "%s Generation Capacity [GW]" % settings.region,
        fontweight="bold",
        fontsize=24,
        labelpad=25,
    )
    plt.xticks(xticks, xlabels, fontsize=15, rotation="vertical")
    plt.yticks(fontsize=20)
    plt.xlim((-2 + (cushion * (len(years) - 1) * barWidth)), len(scenarios))
    plt.ylim(0, 400)
    plt.grid(axis="y", linestyle="-", color="0.5", zorder=0)
    plt.legend(
        legend_elements,
        settings.tech_dict2.values(),
        loc="lower center",
        bbox_to_anchor=(0.5, -0.26),
        ncol=len(technologies_i),
        frameon=False,
        fontsize=15,
    )

    for i in range(len(scenarios)):
        plt.text(
            xticks[i * 3 + 2],
            -65,
            list(settings.scenarios_dict.values())[i],
            horizontalalignment="center",
            fontsize=15,
        )

        ytick = sum(list(tot_cap.iloc[i][year][year])) / 1000
        ytick = round(ytick, 0)
        plt.text(
            xticks[i * 3 + 3],
            ytick,
            str(int(ytick)),
            horizontalalignment="center",
            verticalalignment="bottom",
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
            path + "/%s_capacityexpansion_stacked_bar_plot.png" % settings.region,
            bbox_inches="tight",
        )
        plt.clf()
    else:
        os.makedirs(path)
        plt.savefig(
            path + "/%s_capacityexpansion_stacked_bar_plot.png" % settings.region,
            bbox_inches="tight",
        )
        plt.clf()
    return


def spec_capacity_hbar_plotter(tech):
    # Working on tech capacity bar plots in specific year
    # Defines scenarios and model year to plot
    scenarios = list(settings.scenarios_dict)
    year = list(settings.model_year)

    # Create big, total capacity dataframe (this is what I'm hoping to plot at the end)
    zero_data = np.zeros(
        shape=(len(settings.scenarios_dict), len(settings.technologies))
    )
    tot_cap = pd.DataFrame(zero_data, columns=settings.technologies)

    cap_dict = {}
    for i in range(len(settings.technologies)):
        cap_dict[settings.technologies[i]] = []
    diff_dict = {}
    for i in range(len(settings.technologies)):
        diff_dict[settings.technologies[i]] = []

    for i in range(len(scenarios)):
        scenario = scenarios[i]
        if settings.multi_stage == 1:
            loc_cap = pd.read_csv(
                settings.root_dir + scenario + "/Results/" + year[0] + "/capacity.csv"
            )
            loc_tech = pd.read_csv(
                settings.root_dir + scenario + "/Inputs/Inputs_p1/Generators_data.csv"
            )
        elif settings.multi_stage == 0:
            loc_cap = pd.read_csv(
                settings.root_dir + scenario + "/Results/capacity.csv"
            )
            loc_tech = pd.read_csv(
                settings.root_dir + scenario + "/Inputs/Generators_data.csv"
            )
        loc_tech = loc_tech[["Resource", "technology"]]
        loc_cap = loc_cap.merge(
            loc_tech, how="inner", left_on="Resource", right_on="Resource"
        )
        if settings.region == "ERCOT":
            for j in range(len(settings.WECC_regions)):
                loc_cap = loc_cap[
                    loc_cap["Resource"].str.contains(
                        list(settings.WECC_regions.values())[j]
                    )
                    == False
                ]
        elif settings.region == "WECC":
            for j in range(len(settings.ERCOT_regions)):
                loc_cap = loc_cap[
                    loc_cap["Resource"].str.contains(
                        list(settings.ERCOT_regions.values())[j]
                    )
                    == False
                ]
        loc_cap["technology"] = loc_cap["technology"].replace(settings.tech_dict)
        keep_col = ["technology", "EndCap"]
        loc_cap = loc_cap[keep_col]
        loc_cap = loc_cap.groupby("technology", as_index=False).agg("sum")
        loc_cap = loc_cap[loc_cap["technology"].isin(settings.technologies)]
        sorting = pd.DataFrame({"tech": settings.technologies})
        sorting = sorting.reset_index().set_index("tech")
        loc_cap["sorting"] = loc_cap["technology"].map(sorting["index"])
        loc_cap.sort_values("sorting", inplace=True)
        loc_cap.set_index("sorting", inplace=True)
        for k in range(len(settings.technologies)):
            cap_dict[settings.technologies[k]].append(
                loc_cap[loc_cap["technology"] == settings.technologies[k]][
                    "EndCap"
                ].iloc[0]
            )
    for k in range(len(settings.technologies)):
        diff_dict[settings.technologies[k]] = [
            round(
                (
                    100
                    * (x - cap_dict[settings.technologies[k]][0])
                    / cap_dict[settings.technologies[k]][0]
                ),
                1,
            )
            for x in cap_dict[settings.technologies[k]]
        ]
    for k in range(len(settings.technologies)):
        tot_cap[settings.technologies[k]] = [
            x / 1000 for x in cap_dict[settings.technologies[k]]
        ]
    tot_cap["scenario"] = settings.scenarios_dict.values()
    tot_cap = tot_cap.iloc[::-1]
    tot_cap.set_index("scenario", inplace=True)

    # Create plot
    plt.figure(figsize=(10, 6))

    barWidth = 0.3
    br = np.arange(len(tot_cap))

    plt.barh(
        br,
        list(tot_cap[tech]),
        color=settings.colors[tech],
        height=barWidth,
        edgecolor="black",
    )

    plt.title(
        "%s %s %s Capacity (GW)"
        % (
            settings.region,
            list(settings.model_year.values())[0],
            settings.tech_dict2[tech],
        ),
        fontsize=25,
    )
    plt.yticks(br, tot_cap.index, fontsize=18)
    plt.xticks(fontsize=20)
    plt.xlim(0, 160)
    # plt.xlim(0, 1.2 * max(list(tot_cap[tech])))

    for i in range(len(scenarios)):
        if i == len(scenarios) - 1:
            pass
        else:
            if diff_dict[tech][len(scenarios) - i - 1] > 0:
                plt.text(
                    tot_cap[tech][i],
                    br[i],
                    "+" + str(diff_dict[tech][len(scenarios) - i - 1]) + "%",
                    horizontalalignment="left",
                    verticalalignment="center",
                    fontsize=15,
                )
            elif diff_dict[tech][len(scenarios) - i - 1] < 0:
                plt.text(
                    tot_cap[tech][i],
                    br[i],
                    str(diff_dict[tech][len(scenarios) - i - 1]) + "%",
                    horizontalalignment="left",
                    verticalalignment="center",
                    fontsize=15,
                )
            else:
                plt.text(
                    tot_cap[tech][i],
                    br[i],
                    "0%",
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
        + "/technologies/"
    )
    if os.path.exists(path):
        plt.savefig(
            path + "%s_capacity_bar_plot.png" % tech,
            bbox_inches="tight",
        )
        plt.clf()
    else:
        os.makedirs(path)
        plt.savefig(
            path + "%s_capacity_bar_plot.png" % tech,
            bbox_inches="tight",
        )
        plt.clf()
    return


def tot_capacity_plotter(tot_cap):
    scenarios = list(settings.scenarios_dict)
    year = list(settings.model_year.values())[0]

    cap_dict = {}
    for i in range(len(settings.scenarios_bins)):
        cap_dict[list(settings.scenarios_bins)[i]] = []

    for i in range(len(scenarios)):
        scenario = scenarios[i]
        loc_cap = list(tot_cap.iloc[i][year][year])
        loc_tot_cap = sum(loc_cap) / 1000

        for j in range(len(cap_dict)):
            if list(cap_dict)[j] in scenario:
                cap_dict[list(cap_dict)[j]].append(loc_tot_cap)

    tot_cap_plotting = pd.DataFrame.from_dict(cap_dict)

    # Create plot
    plt.figure(figsize=(20, 10))

    barWidth = 0.3
    cushion = 1
    br = np.arange(len(tot_cap_plotting))
    br_bins = {}
    for j in range(len(cap_dict)):
        br_bins[j] = [x + (cushion * j * barWidth) for x in br]

    colors = []
    for j in range(len(cap_dict)):
        colors.append(str(0.4 + (j * 0.2)))
        plt.bar(
            br_bins[j],
            list(tot_cap_plotting[list(cap_dict)[j]]),
            color=colors[j],
            width=barWidth,
            edgecolor="black",
            zorder=4,
        )

        line_types = ["-", "--"]
        plt.plot(
            br_bins[j],
            list(tot_cap_plotting[list(cap_dict)[j]]),
            color="#E7863C",
            linestyle=line_types[j],
            linewidth=5,
            zorder=5,
        )

    count = 0
    xticks = []
    xlabels = [
        "No Connect",
        "1.5GW Connect",
        "3.0GW Connect",
        "6.0GW Connect",
        "Optimal Connect",
    ]
    # xlabels = ["No Connect", "1.5GW Connect", "Optimal Connect"]
    for r in range(len(br)):
        xticks.append(count + (barWidth / 2))
        count += 1

    legend_elements = []
    for r in range(len(settings.scenarios_bins)):
        legend_elements.append(Line2D([0], [0], color=colors[r], linewidth=15))
    weather_scenarios = ["Base Weather", "Extreme Winter Weather"]

    plt.ylabel("Generation Capacity [GW]", fontweight="bold", fontsize=24, labelpad=25)
    plt.xticks(xticks, xlabels, fontsize=20)
    plt.yticks(fontsize=20)
    plt.ylim(0, 700)
    plt.grid(axis="y", linestyle="-", color="0.5", zorder=0)
    plt.legend(
        legend_elements,
        weather_scenarios,
        loc="lower center",
        bbox_to_anchor=(0.5, -0.15),
        ncols=len(weather_scenarios),
        frameon=False,
        fontsize=20,
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
            path + "/%s_total_capacity_expansion.png" % settings.region,
            bbox_inches="tight",
        )
        plt.clf()
    else:
        os.makedirs(path)
        plt.savefig(
            path + "/%s_total_capacity_expansion.png" % settings.region,
            bbox_inches="tight",
        )
        plt.clf()
    return
