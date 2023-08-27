# TF2 Market Scraper

## Overview

This scraper targets the **Team Fortress 2** (TF2) market, specifically aiming at tracking unusual visual effects (VFX) on items.

## How It Works

1. **Data Source**: 
   - The script interfaces with the market through the `market_search` utility to retrieve VFX-related item listings.
   
2. **VFX Categories**: 
   - Different unusual effect types, like `ROBO`, `EOTL`, `SFXIII`, etc., are predefined in the `VFX_DICT`.
   
3. **Comparison Mechanism**:
   - The scraper compares the current data with the previous state (stored as `.csv` files).
   - If there are any differences or changes in the market listings between runs, they are flagged and displayed (Pending backpack tf api checks for pricing comparisons)
   
4. **Storage**: 
   - Results are saved under the `data/` directory, with each VFX category stored as a separate `.csv` file.

## Usage

Run the script, and it will iterate over each VFX category, tracking changes and saving updates. If market changes are detected for a particular VFX, they'll be printed on the console.
