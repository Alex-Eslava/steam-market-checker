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
    return market_search(params)


def fetch_previous_data(file_path):
    try:
        return pd.read_csv(file_path, sep='|')
    except FileNotFoundError:
        return pd.DataFrame()


def detect_market_changes(current_df, previous_df):
    return pd.concat([current_df, previous_df]).drop_duplicates(keep=False)


def main():
    for vfx_key, vfx_values in VFX_DICT.items():
        vfx_results_list = [get_search_results(vfx) for vfx in vfx_values if get_search_results(vfx)]
        
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
