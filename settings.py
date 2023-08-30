"""
Part of GenXplore software to process results of the GenX capacity expansion model.

Settings

Written by:
Drew Kassel
Webber Energy Group

"""


# Settings
def init():
    global root_dir, region, multi_stage, scenarios_dict, scenarios_bins, years_dict, model_year, hour1, hour2, technologies, tech_dict, tech_dict, tech_dict2, ERCOT_regions, ERCOT_lines, EAST_regions, EAST_lines, WECC_regions, WECC_lines, colors

    # root_dir = "/Users/drew.kassel/Library/CloudStorage/Box-Box/Modeling/GenX/ERCOT_WECC_Interconnect/Optimize_ERCOT_and_WECC/"
    root_dir = (
        "/Users/drew.kassel/Library/CloudStorage/Box-Box/Modeling/GenX/TEXAS_COUNTIES/"
    )

    region = "ALL"

    multi_stage = 1

    # scenarios_dict = {"US_base_v2": "US (base)"}
    scenarios_dict = {"TEXAS_COUNTIES_2050_16zone_BAU": "Texas Counties"}

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

    # scenarios_bins = {
    #     "base": list(scenarios_dict)[0:5],
    #     "ws": list(scenarios_dict)[5:11],
    # }
    scenarios_bins = {
        "base": list(scenarios_dict)[0],
    }

    years_dict = {
        "StartCap_p1": "2020",
        "EndCap_p1": "2022",
        "EndCap_p2": "2025",
        "EndCap_p3": "2030",
        "EndCap_p4": "2040",
        "EndCap_p5": "2050",
    }
    model_year = {"Results_p5": "2050"}
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
        "UtilityPV_Class1_Moderate": "solar",
        "LandbasedWind_Class3_Moderate": "wind",
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
        # "1",
        # "2",
        # "3",
        # "4",
        # "5",
        # "6",
        # "7",
        # "8",
        # "9",
        # "10",
        # "11",
        # "12",
        # "13",
        # "14",
        # "15",
        # "16",
        # "17",
        # "18",
        # "19",
        # "20",
        # "21",
        # "22",
        # "23",
        # "24",
        # "25",
        # "26",
        # "27",
        # "32",
    ]

    EAST_regions = {
        "Zone1": "18_newengland",
        "Zone2": "19_newyork",
        "Zone3": "20_pjm",
        "Zone4": "21_miso",
        "Zone5": "22_spp",
        "Zone7": "24_southeast",
        "Zone8": "25_florida",
    }
    EAST_lines = [
        "1",
        "2",
        "3",
        "4",
        "5",
        "6",
    ]

    WECC_regions = {
        "Zone6": "23_caiso",
        "Zone9": "26_southwest",
        "Zone10": "27_northwest",
        "Zone11": "28_rockymountains",
    }
    WECC_lines = [
        "7",
        "8",
        "9",
        "10",
        "11",
        "12",
        "13",
        "14",
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
