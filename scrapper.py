import os
import pandas as pd
from utils import market_search
from sm_constants import VFX_DICT


def get_search_results(vfx, appid=440, count=50):
    # TF2's appid is 440
    params = {
        'query': vfx,
        'appid': appid,
        'count': count,
        'search_descriptions': 1,
        'category_440_Quality[]': 'tag_rarity4',
    }
    return market_search(params) or [] 


def fetch_previous_data(file_path):
    try:
        return pd.read_csv(file_path, sep='|')
    except FileNotFoundError:
        return pd.DataFrame()


def detect_market_changes(current_df, previous_df):
    # Merge based on the specific columns
    merged_df = current_df.merge(previous_df, on=['unusual_effect', 'item_name', 'sale_price'], indicator=True, how='outer')
    # Filter to only get rows present in `current_df` but not in `previous_df`
    new_entries = merged_df[merged_df['_merge'] == 'left_only']
    # Drop the _merge column before returning
    return new_entries.drop(columns=['_merge'])



def main():
    for vfx_key, vfx_values in VFX_DICT.items():
        vfx_results_list = [result for vfx in vfx_values for result in get_search_results(vfx)]
        
        current_df = pd.DataFrame(vfx_results_list)
        file_path = os.path.join("data", f"{vfx_key}_df.csv")
        
        previous_df = fetch_previous_data(file_path)
        
        diff_df = detect_market_changes(current_df, previous_df)
        current_df.to_csv(file_path, sep='|', index=False)

        if not diff_df.empty:
            print(f"[X] - For {vfx_key} we detected market changes:")
            print(diff_df)
        else:
            print(f"[_] No market changes for {vfx_key}")
    return True


if __name__ == "__main__":
    main()
