import marimo

__generated_with = "unknown"
app = marimo.App(width="medium")


@app.cell
def _(pd):
    data = pd.read_csv("loadcomp.csv", index_col=list(range(5)))
    data.rename(
        {
            "MOTORA": "MA",
            "MOTORB": "MB",
            "MOTORC": "MC",
            "MOTORD": "MD",
            "PWRELEC": "PE",
            "STATPF": "SF"
        },
        inplace=True,
        axis=1,
    )
    return (data,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #NERC Load Model Model (2020 release)
    """)
    return


@app.cell
def _(
    area_data,
    area_plot,
    data,
    feeder,
    hour,
    mo,
    nomd,
    pie_data,
    pie_plot,
    ro,
    season,
    sector,
    show_column_summaries,
    show_data_types,
):
    _options = {
        "show_data_types": show_data_types.value,
        "show_column_summaries": show_column_summaries.value,
        "show_download": True,
    }
    mo.ui.tabs(
        {
            "Data": mo.ui.table(data, **_options, selection=None),
            "Shapes": mo.vstack(
                [
                    mo.hstack(
                        [ro, sector, feeder, season, hour, nomd], justify="start"
                    ),
                    area_plot,
                    mo.ui.table(
                        area_data,
                        **_options,
                        selection=None,
                        # selection="single",
                        # initial_selection=[hour.value],
                        page_size=24
                    ),
                ]
            ),
            "Fractions": mo.vstack(
                [
                    mo.hstack(
                        [ro, sector, feeder, season, hour, nomd], justify="start"
                    ),
                    mo.hstack(
                        [
                            pie_plot,
                            mo.ui.table(pie_data, **_options, selection=None),
                        ]
                    ),
                ]
            ),
            "Settings": mo.vstack(
                [mo.md("**Tables**"), show_data_types, show_column_summaries]
            ),
        },
        lazy=True,
    )
    return


@app.cell
def _(data, mo):
    _options = data.index.get_level_values(0).unique()
    ro = mo.ui.dropdown(options=_options, label="Region:", value=_options[0])
    return (ro,)


@app.cell
def _(data, mo, ro):
    _options = data.loc[[ro.value]].index.get_level_values(1).unique()
    _btype = sorted({x.split("_", 1)[0] for x in _options})
    sector = mo.ui.dropdown(options=_btype, label="City/Type:", value=_btype[0])
    return (sector,)


@app.cell
def _(data, mo, ro, sector):
    _options = data.loc[[ro.value]].index.get_level_values(1).unique()
    _ftype = sorted(
        {x.split("_", 1)[1] for x in _options if x.startswith(sector.value + "_")}
    )
    feeder = mo.ui.dropdown(options=_ftype, label="Sector/Load:", value=_ftype[0])
    return (feeder,)


@app.cell
def _(data, mo):
    _options = data.index.get_level_values(2).unique()
    season = mo.ui.dropdown(options=_options, label="Season:", value=_options[0])
    return (season,)


@app.cell
def _(mo):
    nomd = mo.ui.checkbox(label="No motor D", value=False)
    return (nomd,)


@app.cell
def _(mo):
    hour = mo.ui.slider(
        start=0, stop=23, label="Hour:", value=15, show_value=True, debounce=True
    )
    return (hour,)


@app.cell
def _(mo):
    # settings
    show_data_types = mo.ui.checkbox(label="Show data types")
    show_column_summaries = mo.ui.checkbox(label="Show column summaries")
    return show_column_summaries, show_data_types


@app.cell
def _(data, feeder, hour, nomd, np, plt, ro, season, sector):
    _data = data.loc[
        np.s_[
            ro.value,
            "_".join([sector.value, feeder.value]),
            season.value,
            1 if nomd.value else 0,
            :,
        ],
        ["MA", "MB", "MC", "MD", "PE", "ZP", "IP"],
    ]
    area_data = (
        _data.reset_index()
        .set_index("HOUR")
        .drop(["RO", "LOADTYPE", "SEASON", "NOMD"], axis=1)
    )
    area_plot = area_data.plot.area(
        figsize=(15, 5),
        grid=True,
        xlim=[0, 23],
        ylabel="Fraction of load",
        title=f"{ro.value} {feeder.value} {sector.value} {season.value} {'NO ' if nomd.value else 'W/'}MOTOR D",
    )
    area_plot.plot([hour.value, hour.value], [0, 1], linewidth=3, color="k")
    plt.legend(loc="right");
    return area_data, area_plot


@app.cell
def _(data, feeder, hour, nomd, ro, season, sector):
    _data = data.loc[
        [
            (
                ro.value,
                "_".join([sector.value, feeder.value]),
                season.value,
                1 if nomd.value else 0,
                hour.value,
            )
        ],
        ["MA", "MB", "MC", "MD", "PE", "ZP", "IP"],
    ]
    _data = (
        _data.stack()
        .reset_index()
        .rename({"level_5": "ENDUSE", 0: "VALUE"}, axis=1)
    )
    pie_data = _data.set_index("ENDUSE").drop(
        ["RO", "LOADTYPE", "SEASON", "HOUR", "NOMD"], axis=1
    )
    pie_plot = pie_data.plot(
        kind="pie",
        y="VALUE",
        x=pie_data.index,
        legend=False,
        autopct="%.1f%%",
        title=f"{ro.value} {feeder.value} {sector.value} {season.value} {hour.value}h {'NO ' if nomd.value else 'W/'}MOTOR D",
    )
    return pie_data, pie_plot


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Source: [NERC Load Model Data (2020)](https://urldefense.us/v3/__https://dev.azure.com/nerc/4dc7f7f3-e936-4308-8330-aa87f6d924fa/_apis/git/repositories/553cd3aa-8c2f-41ac-ba80-9a0748a7150f/items?path=*LMDT_Tool*LMWG*20LMDT*20Tool*20Examples*20and*20Hands*20On*20Training*20Resources.zip&versionDescriptor*5BversionOptions*5D=0&versionDescriptor*5BversionType*5D=0&versionDescriptor*5Bversion*5D=main&resolveLfs=true&*24format=octetStream&api-version=5.0&download=true__;Ly8lJSUlJSUlJSUlJSUlJSU!!G2kpM7uM-TzIFchu!1gJVnnjnUkeLKZ4d_cW3oAvZ5eyL0ouWvda9d0_ZooJWB_4aDgVH5u58M0xWSkdFDj4tWHZpeKDGwCjim2OTeIHPJcg$)
    """)
    return


@app.cell
def _():
    import marimo as mo
    import os
    import numpy as np
    import pandas as pd
    import matplotlib.pyplot as plt

    pd.options.display.width = None
    pd.options.display.max_columns = None
    return mo, np, pd, plt


if __name__ == "__main__":
    app.run()
