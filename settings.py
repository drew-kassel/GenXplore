"""
Part of GenXplore software to process results of the GenX capacity expansion model.

Settings

Written by:
Drew Kassel
Webber Energy Group

"""


# Settings
def init():
    global root_dir, region, multi_stage, scenarios_dict, scenarios_bins, years_dict, model_year, hour1, hour2, technologies, tech_dict, tech_dict, tech_dict2, ERCOT_regions, ERCOT_lines, WECC_regions, WECC_lines, colors

    root_dir = "/Users/drew.kassel/Library/CloudStorage/Box-Box/META/Modeling/"

    region = "WECC"

    multi_stage = 1

    scenarios_dict = {
        "interconnect_2035_20zone_base_0.0gw": "0.0GW\n(base)",
        "interconnect_2035_20zone_base_1.5gw": "1.5GW\n(base)",
        "interconnect_2035_20zone_base_3.0gw": "3.0GW\n(base)",
        "interconnect_2035_20zone_base_6.0gw": "6.0GW\n(base)",
        "interconnect_2035_20zone_base_optimal": "Optimal\n(base)",
        "interconnect_2035_20zone_ws_0.0gw": "0.0GW\n(ws)",
        "interconnect_2035_20zone_ws_1.5gw": "1.5GW\n(ws)",
        "interconnect_2035_20zone_ws_3.0gw": "3.0GW\n(ws)",
        "interconnect_2035_20zone_ws_6.0gw": "6.0GW\n(ws)",
        "interconnect_2035_20zone_ws_optimal": "Optimal\n(ws)",
    }

    # scenarios_dict = {
    #     "interconnect_2035_20zone_base_0.0gw_restricted": "0.0GW (base)",
    #     "interconnect_2035_20zone_base_1.5gw_restricted": "1.5GW (base)",
    #     "interconnect_2035_20zone_base_3.0gw_restricted": "3.0GW (base)",
    #     "interconnect_2035_20zone_base_6.0gw_restricted": "6.0GW (base)",
    #     "interconnect_2035_20zone_base_optimal_restricted": "Optimal (base)",
    #     "interconnect_2035_20zone_ws_0.0gw_restricted": "0.0GW (ws)",
    #     "interconnect_2035_20zone_ws_1.5gw_restricted": "1.5GW (ws)",
    #     "interconnect_2035_20zone_ws_3.0gw_restricted": "3.0GW (ws)",
    #     "interconnect_2035_20zone_ws_6.0gw_restricted": "6.0GW (ws)",
    #     "interconnect_2035_20zone_ws_optimal_restricted": "Optimal (ws)",
    # }

    scenarios_bins = {
        "base": list(scenarios_dict)[0:5],
        "ws": list(scenarios_dict)[5:11],
    }

    years_dict = {
        "StartCap_p1": "2020",
        "EndCap_p1": "2022",
        "EndCap_p2": "2025",
        "EndCap_p3": "2030",
        "EndCap_p4": "2035",
    }
    model_year = {"Results_p4": "2035"}
    hour1 = 1032
    hour2 = 1152

    technologies = [
        "nuclear",
        "hydro",
        "coal",
        "ng",
        # "ngcc",
        # "ngct",
        # "ngst",
        "wind",
        "solar",
        "battery",
    ]

    tech_dict = {
        "Battery_*_Moderate": "battery",
        "Conventional Hydroelectric": "hydro",
        "Conventional Steam Coal": "coal",
        "Natural Gas Fired Combined Cycle": "ng",
        "Natural Gas Fired Combustion Turbine": "ng",
        "Natural Gas Steam Turbine": "ng",
        "NaturalGas_CCAvgCF_Moderate": "ng",
        "NaturalGas_CCCCSAvgCF_Conservative": "ng",
        "NaturalGas_CCS100_Moderate": "ng",
        "NaturalGas_CTAvgCF_Moderate": "ng",
        "Nuclear": "nuclear",
        "Onshore Wind Turbine": "wind",
        "Other_peaker": "other",
        "Solar Photovoltaic": "solar",
        "UtilityPV_Class1_Moderate_": "solar",
    }

    tech_dict2 = {
        "nuclear": "NUC",
        "hydro": "HYD",
        "coal": "COAL",
        "ng": "NG",
        # "ngcc": "NGCC",
        # "ngct": "NGCT",
        # "ngst": "NGST",
        "wind": "WIN",
        "solar": "SOL",
        "battery": "BAT",
    }

    ERCOT_regions = {
        "Zone1": "10_abilene",
        "Zone2": "11_wichitafalls",
        "Zone3": "12_amarillo",
        "Zone4": "13_lubbock",
        "Zone5": "14_midland",
        "Zone6": "15_fortstockton",
        "Zone7": "16_pecos",
        "Zone8": "1_dallas",
        "Zone9": "2_sanantonio",
        "Zone10": "3_houston",
        "Zone11": "4_corpuschristi",
        "Zone12": "5_mcallen",
        "Zone13": "6_laredo",
        "Zone14": "7_delrio",
        "Zone15": "8_sanangelo",
        "Zone16": "9_sansaba",
    }
    ERCOT_lines = [
        "1",
        "2",
        "3",
        "4",
        "5",
        "6",
        "7",
        "8",
        "9",
        "10",
        "11",
        "12",
        "13",
        "14",
        "15",
        "16",
        "17",
        "18",
        "19",
        "20",
        "21",
        "22",
        "23",
        "24",
        "25",
        "26",
        "27",
        # "32",
    ]

    WECC_regions = {
        "Zone17": "17_southwest",
        "Zone18": "18_camex",
        "Zone19": "19_northwest",
    }
    WECC_lines = [
        "28",
        "29",
        "30",
        "31",
    ]

    colors = {
        "nuclear": "#E7863C",
        "hydro": "#6360A4",
        "coal": "#5C6770",
        "ng": "#4AA8C4",
        "wind": "#69B77C",
        "solar": "#F6D149",
        "battery": "#7D2858",
        "nse": "red",
    }
