#!/usr/bin/env python3 

import argparse
import json
import lxml
import lxml.html
import requests
import os

import numpy as np
import pandas as pd


def search(base_url, base_pattern):

    ## TODO automate search for dataset urls
    #page = requests.get(url=base_url)
    
    #urls = page.content().xpath(base_pattern)
    #return urls
    
    datasetUrls = ["https://www.inptdat.de/dataset/verified-modeling-low-pressure-hydrogen-plasma-generated-electron-cyclotron-resonance", 
            "https://www.inptdat.de/dataset/effect-spatially-fluctuating-heating-particles-plasma-spray-process-dataset",
            "https://www.inptdat.de/dataset/upscaling-single-multi-filament-dielectric-barrier-discharges-pulsed-operation-dataset",
            "https://www.inptdat.de/dataset/effect-oxygen-admixture-properties-microwave-generated-plasma-ar-o%E2%82%82-modelling-study-dataset",
            "https://www.inptdat.de/dataset/modelling-and-experimental-evidence-cathode-erosion-plasma-spray-torch",
            "https://www.inptdat.de/dataset/electron-swarm-parameters-c2h6-measurements-and-kinetic-calculations",
            "https://www.inptdat.de/dataset/electron-swarm-parameters-c2h4-measurements-and-kinetic-calculations",
            "https://www.inptdat.de/dataset/electron-swarm-parameters-c2h2-measurements-and-kinetic-calculations",
            "https://www.inptdat.de/dataset/electrical-characteristics-atmospheric-pressure-dbd-argon-small-admixtures-tms-measured-and",
            "https://www.inptdat.de/dataset/streamer-surface-interaction-atmospheric-pressure-dielectric-barrier-discharge-argon-dataset",
            "https://www.inptdat.de/dataset/impact-electrode-proximity-streamer-breakdown-and-development-pulsed-dielectric-barrier",
            "https://www.inptdat.de/dataset/evidence-dominant-production-mechanism-ammonia-hydrogen-plasma-parts-million-nitrogen",
            "https://www.inptdat.de/dataset/self-consistent-cathode-plasma-coupling-and-role-fluid-flow-approach-torch-modelling-dataset",
            "https://www.inptdat.de/dataset/spatial-distribution-ho%E2%82%82-atmospheric-pressure-plasma-jet-investigated-cavity-ring-down",
            "https://www.inptdat.de/dataset/ar-metastable-densities-%C2%B3p%E2%82%82-effluent-filamentary-atmospheric-pressure-plasma-jet-humidified",
            "https://www.inptdat.de/dataset/effect-bidirectional-coupling-lte-arc-column-refractory-cathode-atmospheric-pressure-argon",
            "https://www.inptdat.de/dataset/unified-modelling-low-current-short-length-arcs-between-copper-electrodes",
            "https://www.inptdat.de/dataset/simplified-voltage-model-gmaw",
            "https://www.inptdat.de/dataset/benchmark-data-fluid-modelling-low-pressure-ccrf-discharge-plasmas",
            "https://www.inptdat.de/dataset/plasma-parameters-microarcs-towards-minuscule-discharge-gap-dataset",
            "https://www.inptdat.de/dataset/spatial-distribution-hydrogen-and-oxygen-atoms-cold-atmospheric-pressure-plasma-jet-dataset",
            "https://www.inptdat.de/dataset/study-anode-energy-gas-metal-arc-welding",
            "https://www.inptdat.de/dataset/correlation-helicality-and-rotation-frequency-filaments-ntappj",
            "https://www.inptdat.de/dataset/relationship-between-sif4-plasma-species-and-sample-properties-ultra-low-k-etching-processes",
            "https://www.inptdat.de/dataset/influence-surface-parameters-dielectric-barrier-discharges-argon-subatmospheric-pressure",
            "https://www.inptdat.de/dataset/benchmark-calculations-electron-velocity-distribution-function-obtained-monte-carlo-flux",
            "https://www.inptdat.de/dataset/non-thermal-plasma-contact-water-origin-species",
            "https://www.inptdat.de/dataset/plasma-parameters-ar-hmdso-dbd-atmospheric-pressure-plasma-polymerization-experiments",
            "https://www.inptdat.de/dataset/high-speed-thermal-microscopy-plasma-microprinting-atmospheric-pressure",
            "https://www.inptdat.de/dataset/comparison-six-simulation-codes-positive-streamers-air"
            ]

    sourceUrls = ["https://www.inptdat.de/non-thermal-atmospheric-pressure-plasma-jet-ntappj",
            "https://www.inptdat.de/helixjet",
            "https://www.inptdat.de/kinpen-ind",
            "https://www.inptdat.de/ion-wind-dbd",
            "https://www.inptdat.de/hairline-plasma-jet-hairlineplasma",
            "https://www.inptdat.de/biofilm-jet",
            "https://www.inptdat.de/venturi-dbd-vdbd",
            "https://www.inptdat.de/aura-wave-sairem",
            "https://www.inptdat.de/plasmaskop-jet",
            "https://www.inptdat.de/minimip",
            "https://www.inptdat.de/miller-auto-axcess-450"]

    return sourceUrls
    #return datasetUrls 


def scrape(content, mappingDict):
    root = lxml.html.fromstring(content)
    result = dict()

    for k,v in mappingDict["fixed"].items():
        node = root.xpath(v)
        result[k] = '; '.join([x.strip() for x in node[0].itertext() if len(x.strip()) > 0]) if len(node) > 0 else np.nan

    for item in mappingDict["dynamic"]:
        nodes = root.xpath(item["query"])
        for node in nodes:
            result[node.xpath(item["key"])[0].text_content()] = "; ".join(node.xpath(item["value"])[0].itertext())

    return result

def export(input_file, output_file):
    
    with open(input_file, "r") as input_handle:
        mappingDict = json.load(input_handle)
   
    data_list = []
    with open(output_file + ".json", "w") as output_handle:
        for url in search(mappingDict["baseurl"], mappingDict["basepattern"]):
            page = requests.get(url=url)
            data = scrape(page.content, mappingDict)
            data_list += [data]
            json.dump(data, output_handle)
            output_handle.write("\n")

    data_pd = pd.DataFrame(data_list)
    data_pd.to_csv(output_file + ".csv", index=False, sep=";")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_file", required=True, help="")
    parser.add_argument("--output_file", required=True, help="")
    args = parser.parse_args()

    input_file = args.input_file
    output_file = args.output_file

    export(input_file, output_file)

if __name__ == "__main__":
    main()
