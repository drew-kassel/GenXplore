"""
Part of GenXplore software to process results of the GenX capacity expansion model.

Functions that analyze the energy consumed by the model.

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
def energy_consumed_by_type():
    scenarios = list(settings.scenarios_dict)
    years = list(settings.years_dict.values())[1:]

    zero_data = np.zeros(shape=(len(years), len(scenarios)))
    tot_energy = pd.DataFrame(zero_data, columns=scenarios)

    for i in range(len(scenarios)):
        scenario = scenarios[i]

        zero_data = np.zeros(shape=(len(settings.technologies), len(years)))
        loc_energy = pd.DataFrame(zero_data, columns=years)
        loc_energy["technology"] = settings.technologies

        if settings.multi_stage == 1:
            loc_tech = pd.read_csv(
                settings.root_dir + scenario + "/Inputs/Inputs_p1/Generators_data.csv"
            )
        elif settings.multi_stage == 0:
            loc_tech = pd.read_csv(
                settings.root_dir + scenario + "/Generators_data.csv"
            )
        loc_tech = loc_tech[["Resource", "technology"]]

        for j in range(len(years)):
            year = years[j]
            if settings.multi_stage == 1:
                loc_energy_p = pd.read_csv(
                    settings.root_dir
                    + scenario
                    + "/Results/Results_p%s/power.csv" % str(j + 1)
                )
            elif settings.multi_stage == 0:
                loc_energy_p = pd.read_csv(
                    settings.root_dir + scenario + "/Results/power.csv"
                )
            loc_energy_p = loc_energy_p.T
            loc_energy_p.reset_index(inplace=True)
            loc_energy_p.columns = loc_energy_p.iloc[0]
            loc_energy_p.drop(
                index=loc_energy_p.iloc[:1, :].index.tolist(), inplace=True
            )
            loc_energy_p = loc_energy_p[["Resource", "AnnualSum"]]
            if settings.region == "ERCOT":
                for j in range(len(settings.WECC_regions)):
                    loc_energy_p = loc_energy_p[
                        loc_energy_p["Resource"].str.contains(
                            list(settings.WECC_regions.values())[j]
                        )
                        == False
                    ]
            elif settings.region == "WECC":
                for j in range(len(settings.ERCOT_regions)):
                    loc_energy_p = loc_energy_p[
                        loc_energy_p["Resource"].str.contains(
                            list(settings.ERCOT_regions.values())[j]
                        )
                        == False
                    ]
            loc_energy_p = loc_energy_p.merge(
                loc_tech, how="inner", left_on="Resource", right_on="Resource"
            )

            loc_energy_p["technology"] = loc_energy_p["technology"].replace(
                settings.tech_dict
            )
            loc_energy_p = loc_energy_p.groupby("technology", as_index=False).agg("sum")
            loc_energy_p = loc_energy_p[
                loc_energy_p["technology"].isin(settings.technologies)
            ]
            sorting = pd.DataFrame({"tech": settings.technologies})
            sorting = sorting.reset_index().set_index("tech")
            loc_energy_p["sorting"] = loc_energy_p["technology"].map(sorting["index"])
            loc_energy_p.sort_values("sorting", inplace=True)
            loc_energy_p.set_index("sorting", inplace=True)
            loc_energy_p = list(loc_energy_p["AnnualSum"])
            loc_energy[year] = loc_energy_p
        for k in range(len(years)):
            loc_energy_df = loc_energy[["technology", years[k]]]
            loc_energy_df.rename(settings.years_dict, axis=1, inplace=True)
            tot_energy[scenario].iloc[k] = loc_energy_df
    tot_energy = tot_energy.T
    tot_energy.columns = years
    tot_energy.reset_index(inplace=True)
    tot_energy.rename({"index": "scenario"}, axis=1, inplace=True)

    return tot_energy


def energy_consumed_by_type_per_scenario(tot_energy):
    # Find settings.technologies and years
    settings.technologies = list(tot_energy.iloc[0, 1]["technology"])
    years = list(tot_energy.columns[1:])

    # Create zero dataframe
    zero_data = np.zeros(shape=(len(settings.technologies), len(years)))

    # Loop through all scenarios, build dataframes for each individual scenario
    for i in range(len(tot_energy)):
        scenario = tot_energy.iloc[i, 0]
        energy_by_type = pd.DataFrame(zero_data, columns=years)
        energy_by_type["technology"] = settings.technologies
        for j in range(len(years)):
            energy_by_type[years[j]] = tot_energy[years[j]].iloc[i][years[j]]
        energy_by_type.set_index("technology", inplace=True)

        # Write to csv file
        path = (
            settings.root_dir + "GenXplore_results/" + scenario + "/" + settings.region
        )
        if os.path.exists(path):
            energy_by_type.to_csv(path + "/energy_consumed_by_type.csv")
        else:
            os.makedirs(path)
            energy_by_type.to_csv(path + "/energy_consumed_by_type.csv")
    return


def energy_consumed_by_type_plotter(tot_energy):
    settings.technologies = list(tot_energy.iloc[0, 1]["technology"])
    years = list(settings.model_year.values())
    scenarios = list(settings.scenarios_dict.values())

    plt.figure(figsize=(20, 10))

    barWidth = 0.5
    cushion = 1.1
    br = np.arange(len(tot_energy))
    br_years = {}
    for j in range(len(years)):
        br_years[j] = [x + (cushion * j * barWidth) for x in br]

    for k in range(len(years)):
        zero_data = np.zeros(shape=(len(scenarios), len(settings.technologies)))
        prop = pd.DataFrame(zero_data, columns=settings.technologies)

        bottom = []
        for i in range(len(tot_energy)):
            bottom.append(0)
        for j in range(len(settings.technologies)):
            bar = []
            for l in range(len(tot_energy)):
                total = sum(tot_energy[years[k]].iloc[-(l + 1)][years[k]])
                value = (
                    tot_energy[years[k]]
                    .iloc[-(l + 1)][
                        tot_energy[years[k]].iloc[-(l + 1)]["technology"]
                        == settings.technologies[j]
                    ][years[k]]
                    .iloc[0]
                    / total
                )
                bar.append(value)
                # print(scenarios[-(l + 1)])
            plt.barh(
                br_years[k],
                bar,
                color=settings.colors[settings.technologies[j]],
                height=barWidth,
                label=years[k],
                edgecolor="black",
                left=bottom,
                zorder=4,
            )
            bottom = list(np.add(bottom, bar))
            prop[settings.technologies[j]] = bar

    count = 0
    yticks = []
    ylabels = []
    for r in range(len(br)):
        yticks.append(br[r])
        ylabels.append(scenarios[-(r + 1)])
        count += 1

    legend_elements = []
    for r in range(len(settings.technologies)):
        tech = settings.technologies[r]
        legend_elements.append(
            Line2D([0], [0], color=settings.colors[tech], linewidth=15)
        )

    plt.title("%s %s Fuel Mix" % (settings.region, list(settings.model_year.values())[0]), fontweight="bold", fontsize=24)
    # plt.xlabel("Fuel Mix [%]", fontweight="bold", fontsize=24, labelpad=15)
    plt.yticks(yticks, ylabels, fontsize=20)
    plt.xticks([0, 1], [0, 1], fontsize=20)
    plt.ylim((-1 + (cushion * (len(years) - 1) * barWidth)), len(scenarios))
    plt.xlim(0, 1.0)
    # plt.axvline(x=0, zorder=5, color="white")
    # plt.axvline(x=1, zorder=5, color="white")
    plt.legend(
        legend_elements,
        settings.tech_dict2.values(),
        loc="lower center",
        bbox_to_anchor=(0.5, -0.15),
        ncol=len(settings.technologies),
        frameon=False,
        fontsize=20,
    )

    for n, x in enumerate([*prop.index.values]):
        cumulative = 0
        for proportion in prop.loc[x]:
            cumulative = cumulative + proportion
            middle = cumulative - proportion / 2
            string = str(np.round(proportion * 100, 1)) + "%"
            plt.text(
                x=middle,
                y=n,
                s=string,
                color="white",
                fontsize=15,
                fontweight="bold",
                horizontalalignment="center",
                verticalalignment="center",
                zorder=6,
            )

    path = (
        settings.root_dir
        + "/GenXplore_results"
        + "/all_scenarios"
        + "/"
        + str(settings.region)
    )
    if os.path.exists(path):
        plt.savefig(
            path + "/%s_fuelmix_stacked_bar_plot.png" % settings.region,
            bbox_inches="tight",
        )
        plt.clf()
    else:
        os.makedirs(path)
        plt.savefig(
            path + "/%s_fuelmix_stacked_bar_plot.png" % settings.region,
            bbox_inches="tight",
        )
        plt.clf()
    return


def dispatch_plot_builder():
    scenarios = list(settings.scenarios_dict)
    year = list(settings.model_year.keys())[0]

    for i in range(len(scenarios)):
        scenario = scenarios[i]

        if settings.multi_stage == 1:
            loc_tech = pd.read_csv(
                settings.root_dir + scenario + "/Inputs/Inputs_p1/Generators_data.csv"
            )
            loc_energy_p = pd.read_csv(
                settings.root_dir + scenario + "/Results/%s/power.csv" % year
            )
        elif settings.multi_stage == 0:
            loc_tech = pd.read_csv(
                settings.root_dir + scenario + "/Generators_data.csv"
            )
            loc_energy_p = pd.read_csv(
                settings.root_dir + scenario + "/Results/power.csv"
            )
        loc_tech = loc_tech[["Resource", "technology"]]

        loc_energy_p = loc_energy_p.T
        loc_energy_p.reset_index(inplace=True)
        loc_energy_p.columns = loc_energy_p.iloc[0]
        loc_energy_p.drop(index=loc_energy_p.iloc[:1, :].index.tolist(), inplace=True)
        loc_energy_p.drop(["Zone", "AnnualSum"], axis=1, inplace=True)
        if settings.region == "ERCOT":
            for j in range(len(settings.WECC_regions)):
                loc_energy_p = loc_energy_p[
                    loc_energy_p["Resource"].str.contains(
                        list(settings.WECC_regions.values())[j]
                    )
                    == False
                ]
        elif settings.region == "WECC":
            for j in range(len(settings.ERCOT_regions)):
                loc_energy_p = loc_energy_p[
                    loc_energy_p["Resource"].str.contains(
                        list(settings.ERCOT_regions.values())[j]
                    )
                    == False
                ]
        loc_energy_p = loc_energy_p.merge(
            loc_tech, how="inner", left_on="Resource", right_on="Resource"
        )

        loc_energy_p["technology"] = loc_energy_p["technology"].replace(
            settings.tech_dict
        )
        loc_energy_p = loc_energy_p.groupby("technology", as_index=False).agg("sum")
        loc_energy_p = loc_energy_p[
            loc_energy_p["technology"].isin(settings.technologies)
        ]
        sorting = pd.DataFrame({"tech": settings.technologies})
        sorting = sorting.reset_index().set_index("tech")
        loc_energy_p["sorting"] = loc_energy_p["technology"].map(sorting["index"])
        loc_energy_p.sort_values("sorting", inplace=True)
        loc_energy_p.set_index("sorting", inplace=True)
        loc_energy_p.drop(["Resource"], axis=1, inplace=True)
        loc_energy_p = loc_energy_p.T
        loc_energy_p.reset_index(inplace=True, drop=True)
        loc_energy_p.columns = loc_energy_p.iloc[0]
        loc_energy_p.drop(index=loc_energy_p.iloc[:1, :].index.tolist(), inplace=True)
        loc_energy_p = loc_energy_p.iloc[
            range(int(settings.hour1), int(settings.hour2) + 1)
        ]
        loc_energy_p.reset_index(inplace=True)
        loc_energy_p.drop("index", axis=1, inplace=True)
        loc_energy_p = loc_energy_p.astype(float)
        loc_energy_p.rename(settings.tech_dict2, axis=1, inplace=True)

        ## NSE and Lost Load
        df = pd.read_csv(
            "/Users/drew.kassel/Library/CloudStorage/Box-Box/Project3/GenX/Misc./nse_and_lostload.csv"
        )
        nse = df["nse"]
        total_load = df["total_load(gw)"]

        loc_energy_p["NSE"] = nse

        # Plotting
        plt.figure(figsize=[12, 8])
        plt.stackplot(
            loc_energy_p.index,
            loc_energy_p.values.T / 1000,
            labels=list(loc_energy_p),
            colors=list(settings.colors.values()),
            edgecolor="black",
        )
        plt.plot(
            loc_energy_p.index,
            total_load,
            label="Load",
            linestyle="-",
            color="black",
            linewidth=3,
        )
        plt.xlabel(
            "Time Since Start Of Storm [hours]",
            fontweight="bold",
            fontsize=20,
            labelpad=5,
        )
        plt.ylabel(
            "Dispatched Power [GW]",
            fontweight="bold",
            fontsize=20,
            labelpad=20,
        )
        plt.xticks(fontsize=15)
        plt.yticks(fontsize=15)
        plt.xlim(0, 120)
        plt.ylim(0, 120)
        plt.legend(
            loc="lower center",
            bbox_to_anchor=(0.5, -0.3),
            ncol=5,
            frameon=False,
            fontsize=15,
        )

        path = (
            settings.root_dir + "GenXplore_results/" + scenario + "/" + settings.region
        )
        if os.path.exists(path):
            plt.savefig(
                path
                + "/%s_dispatch_%s.png"
                % (settings.region, list(settings.model_year.values())[0]),
                bbox_inches="tight",
            )
            plt.clf()
        else:
            os.makedirs(path)
            plt.savefig(
                path
                + "/%s_dispatch_%s.png"
                % (settings.region, list(settings.model_year.values())[0]),
                bbox_inches="tight",
            )
            plt.clf()
    return
