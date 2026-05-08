"""Load Composition Data

Compile load composition data
"""

import os
import sys
import pandas as pd

class LoadComp(pd.DataFrame):
    """Load composition dataframe"""

    def __init__(self,
        path:str="data",
        region:str|list[str]|None=None,
        season:str|list[str]|None=None,
        nomd:bool|None=None,
        ):
        """Construct load composition dataframe

        Arguments
        ---------

        - `path`: path to data LC files

        - `region`: regions to include
        """
        data = []
        for file in sorted(os.listdir(path)):
            if not file.startswith("LoadComp_") or not file.endswith(".xlsx"):
                continue
            spec = os.path.splitext(file.upper())[0].split("_", 3)

            if isinstance(region,str): region = region.split(",")
            if region is not None and spec[1] not in map(str.upper,region):
                continue
            
            if isinstance(season,str): season = season.split(",")
            if season is not None and spec[2] not in map(str.upper,season):
                continue

            if nomd != None and nomd == ( len(spec) < 4 ):
                continue

            pathname = f"{path}/{file}"
            try:
                print(file, end="... ", flush=True)
                xlsx = pd.ExcelFile(pathname,
                    engine='openpyxl', 
                    engine_kwargs={'data_only': True, 'read_only': True},
                    )
                sheet_names = sorted(xlsx.sheet_names)
                xlsx.close()
                for sheet in sheet_names:
                    if not sheet.upper()[:4] == "HOUR":
                        continue
                    lcdata = pd.read_excel(
                        f"{path}/{file}",
                        sheet_name=sheet,
                        engine="openpyxl",
                        engine_kwargs={"data_only": True, "read_only": True},
                    )
                    lcdata[["RO", "SEASON", "NOMD", "HOUR"]] = (
                        spec[1].upper(),
                        spec[2].upper(),
                        1 if len(spec) > 3 else 0,
                        int(sheet.replace("Hour", "")) - 1,
                    )
                    lcdata.rename({"#AREA": "LOADTYPE"}, axis=1, inplace=True)
                    lcdata.drop(
                        [x for x in lcdata.columns if x.startswith("ID_")],
                        inplace=True,
                        axis=1,
                    )
                    lcdata.columns = [x.upper().replace("LC_","") for x in lcdata.columns]
                    data.append(
                        lcdata.set_index(
                            ["RO", "LOADTYPE", "SEASON", "NOMD", "HOUR"]
                        ).round(6)
                    )
                print("ok",flush=True)
            except Exception as err:
                print(f"ERROR [{file}]: {err}", flush=True, file=sys.stderr)
        if not data:
            raise RuntimeError("no data")
        super().__init__(pd.concat(data).sort_index())

def main(*args,**kwargs):

    lc = LoadComp()
    lc.to_csv("loadcomp.csv",index=True,header=True)

if __name__ == '__main__':
    main()
