import pandas as pd
from utils import market_search
from sm_constants import VFX_DICT

def main():

    for vfx_key in VFX_DICT.keys():
        vfx_results_list = []
        for vfx in VFX_DICT[vfx_key]:
            params = {
                'query': vfx,
                'appid': 440,  # This is for TF2.
                'count': 50,   # Number of results. You can adjust this.
                'search_descriptions': 1,  # This will search the description as well.
                'category_440_Quality[]': 'tag_rarity4',  # Searching Unusuals
            }
            vfx_results_list.extend(market_search(params))
        vfx_results_list
        # Transform list of dictionaries into pandas dataframe
        current_df = pd.DataFrame(vfx_results_list)
        # Read previous f"{vfx_key}_df.csv (using sep='|') 
        try:
            previous_df = pd.read_csv(f"{vfx_key}_df.csv", sep='|')
        except FileNotFoundError:
            previous_df = pd.DataFrame()
        # Compare the previous dataframe to the new one and store in another dataframe the differences
        diff_df = pd.concat([current_df, previous_df]).drop_duplicates(keep=False)
        current_df.to_csv(f"{vfx_key}_df.csv", sep='|', index=False)
        if len(diff_df)>0:
            print(f"[X] - For {vfx_key} we detected market changes:")
            print(diff_df)
        else: 
            print(f"[_] No market changes for {vfx_key}")
    return True


if __name__ == "__main__":
    main()