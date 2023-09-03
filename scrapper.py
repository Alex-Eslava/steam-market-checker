import os
import pandas as pd
from utils import market_search
from sm_constants import VFX_DICT, UNUS_COLS


def get_search_results(vfx, appid=440, count=100):
    # TF2's appid is 440
    params = {
        "query": vfx,
        "appid": appid,
        "count": count,
        "search_descriptions": 1,
        "category_440_Quality[]": "tag_rarity4",
        "norender": 1,  # No need for beautifulsoups
    }
    return market_search(params) or []


def fetch_previous_data(file_path):
    try:
        return pd.read_csv(file_path, sep="|")
    except FileNotFoundError:
        print("No market history db fount. Creating one...")
        return pd.DataFrame()


def detect_market_changes(current_df, previous_df):
    if previous_df is None or previous_df.empty:
        return current_df
    # We noticed small FX change differences on a daily basis so we will ignore +-0.99 usd differences
    current_df["truncated_price"] = current_df["sell_price_text"].str[:-3]
    previous_df["truncated_price"] = previous_df["sell_price_text"].str[:-3]
    filtered_df = current_df[
        ~current_df.set_index(["name", "truncated_price"]).index.isin(
            previous_df.set_index(["name", "truncated_price"]).index
        )
    ].drop(columns=["truncated_price"])
    return filtered_df


def main():
    for vfx_key, vfx_values in VFX_DICT.items():
        vfx_results_list = [
            result for vfx in vfx_values for result in get_search_results(vfx)
        ]
        file_path = os.path.join("data", f"{vfx_key}_df.csv")
        current_df = pd.DataFrame(vfx_results_list)
        previous_df = fetch_previous_data(file_path)
        diff_df = detect_market_changes(current_df, previous_df)
        current_df[UNUS_COLS].to_csv(file_path, sep="|", index=False)

        if not diff_df.empty:
            print(f"[X] - For {vfx_key} we detected market changes:")
            print(diff_df[["unusual_effect", "name", "sale_price_text"]])
        else:
            print(f"[_] No market changes for {vfx_key}")
    return True


if __name__ == "__main__":
    main()
