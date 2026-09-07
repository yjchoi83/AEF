"""Figure 1 -- study area.

Legal Amazon state boundaries, the density of 2021 DETER clearing events, the two
demonstration regions whose map products appear later in the paper, and the two Congo Basin
boxes as an inset. Drawn in EPSG:4326; densities are computed per unit ground area, so the
latitudinal narrowing of a degree cell is divided out rather than displayed.
"""
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap, BoundaryNorm
from matplotlib.patches import Rectangle
from figstyle import W2, C, INK, INK2, SEQ_BLUE, save

P2 = "aef_explore/stage5/TB01/P2/P2_events.csv"
STATES = "aef_explore/paper/code/legal_amazon_states.geojson"
BOUNDARY = "aef_explore/paper/code/legal_amazon_boundary.geojson"
OUTLINES = "aef_explore/paper/code/outlines.geojson"
DEMO = {"Pará / BR-163": (-56.8409, -5.7426, -55.0379, -3.9339),
        "Roraima (south)": (-61.30, 1.20, -60.30, 2.10)}
CONGO = {"CG1": (28.679, 0.426, 29.578, 1.331), "CG2": (23.301, -4.096, 24.201, -3.191)}
EVENT_STATES = ["AC", "AM", "AP", "MA", "MT", "PA", "RO", "RR", "TO"]
CELL = 0.25
BLUE = LinearSegmentedColormap.from_list("b", SEQ_BLUE)


def rings(geom):
    t = geom["type"]
    if t == "Polygon":
        return [np.asarray(r) for r in geom["coordinates"]]
    if t == "MultiPolygon":
        return [np.asarray(r) for p in geom["coordinates"] for r in p]
    return []


def cell_area_km2(lat0, lat1, dlon):
    """Exact spherical area of a lon/lat cell, in km²."""
    R = 6371.0088
    return (np.radians(dlon) * R ** 2 *
            (np.sin(np.radians(lat1)) - np.sin(np.radians(lat0))))


def density_grid(lon, lat, ext):
    x = np.arange(ext[0], ext[1] + CELL, CELL)
    y = np.arange(ext[2], ext[3] + CELL, CELL)
    cnt, _, _ = np.histogram2d(lat, lon, bins=[y, x])
    area = cell_area_km2(y[:-1], y[1:], CELL)[:, None]
    dens = cnt / area * 1000.0                     # events per 1,000 km²
    return np.where(cnt > 0, dens, np.nan), (x[0], x[-1], y[0], y[-1])


def scalebar(ax, ext, km, y_frac=0.055, x_frac=0.055):
    lat = ext[2] + 0.25 * (ext[3] - ext[2])
    deg = km / (111.32 * np.cos(np.radians(lat)))
    x0 = ext[0] + x_frac * (ext[1] - ext[0])
    y0 = ext[2] + y_frac * (ext[3] - ext[2])
    ax.add_patch(Rectangle((x0, y0), deg, 0.011 * (ext[3] - ext[2]), facecolor=INK,
                           edgecolor="white", lw=0.4, zorder=8))
    ax.text(x0 + deg / 2, y0 + 0.022 * (ext[3] - ext[2]), f"{km:,} km", ha="center",
            va="bottom", fontsize=7.0, color=INK, zorder=8)


def main():
    d = pd.read_csv(P2)
    states = json.load(open(STATES))["features"]
    boundary = json.load(open(BOUNDARY))
    world = json.load(open(OUTLINES))["features"]

    ext = (-74.5, -43.5, -18.5, 5.8)
    dens, dext = density_grid(d["lon"].values, d["lat"].values, ext)

    fig = plt.figure(figsize=(W2, W2 * 0.60))
    ax = fig.add_axes([0.055, 0.165, 0.66, 0.815])
    vmax = float(np.nanpercentile(dens, 98))
    im = ax.imshow(dens, extent=dext, origin="lower", cmap=BLUE, vmin=0, vmax=vmax,
                   interpolation="nearest", zorder=2)
    for f in states:
        emph = f["properties"]["sigla"] in EVENT_STATES
        for r in rings(f["geometry"]):
            ax.plot(r[:, 0], r[:, 1], color="#8f979f" if emph else "#c8ced4",
                    lw=0.45 if emph else 0.3, zorder=3)
    for r in rings(boundary["geometry"]):
        ax.plot(r[:, 0], r[:, 1], color=INK, lw=0.9, zorder=4)
    for f in states:
        s = f["properties"]["sigla"]
        if s not in EVENT_STATES:
            continue
        pts = np.concatenate(rings(f["geometry"]))
        ax.text(pts[:, 0].mean(), pts[:, 1].mean(), s, fontsize=7.0, color=INK2,
                ha="center", va="center", zorder=6,
                bbox=dict(boxstyle="round,pad=0.12", fc="white", ec="none", alpha=0.55))
    for lab, (x0, y0, x1, y1) in DEMO.items():
        ax.add_patch(Rectangle((x0, y0), x1 - x0, y1 - y0, facecolor="none",
                               edgecolor=C["flag"], lw=1.0, zorder=7))
        para = "Pará" in lab
        pos = ((x0 + x1) / 2, y1) if para else (x0, (y0 + y1) / 2)
        off, ha = ((0, 3), "center") if para else ((-5, 0), "right")
        ax.annotate(lab, pos, textcoords="offset points", xytext=off, ha=ha,
                    va="bottom" if para else "center", fontsize=7.0, color=C["flag"],
                    zorder=7)
    xt = np.arange(-72, -43, 6.0)
    yt = np.arange(-18, 6, 6.0)
    ax.set_xticks(xt); ax.set_yticks(yt)
    ax.set_xticklabels([f"{abs(v):.0f}°W" for v in xt], fontsize=7.0)
    ax.set_yticklabels([f"{abs(v):.0f}°{'S' if v < 0 else 'N'}" for v in yt], fontsize=7.0)
    for v in xt:
        ax.axvline(v, color="#e9edf0", lw=0.3, zorder=1)
    for v in yt:
        ax.axhline(v, color="#e9edf0", lw=0.3, zorder=1)
    ax.tick_params(length=1.6, pad=1.5)
    ax.set_xlim(ext[0], ext[1]); ax.set_ylim(ext[2], ext[3])
    ax.set_aspect(1 / np.cos(np.radians(-6.0)))
    for s in ax.spines.values():
        s.set_color("#aab1b8")
    scalebar(ax, ext, 500)
    ax.annotate("", xy=(-72.6, 3.6), xytext=(-72.6, 1.4),
                arrowprops=dict(arrowstyle="-|>", color=INK, lw=0.8), zorder=8)
    ax.text(-72.6, 3.8, "N", ha="center", fontsize=7.0, color=INK)

    cax = fig.add_axes([0.055, 0.075, 0.28, 0.022])
    cb = fig.colorbar(im, cax=cax, orientation="horizontal")
    cb.set_label("2021 DETER clearing events per 1,000 km²", fontsize=7.0, color=INK2,
                 labelpad=1.5)
    cb.ax.tick_params(labelsize=7.0, length=1.5)
    cb.outline.set_visible(False)

    # locator: South America
    axl = fig.add_axes([0.735, 0.60, 0.245, 0.375])
    for f in world:
        for r in rings(f["geometry"]) or []:
            axl.plot(r[:, 0], r[:, 1], color="#b8bfc6", lw=0.3)
        g = f["geometry"]
        if g.get("type") == "GeometryCollection":
            for sub in g["geometries"]:
                for r in rings(sub):
                    axl.plot(r[:, 0], r[:, 1], color="#b8bfc6", lw=0.3)
    for r in rings(boundary["geometry"]):
        axl.plot(r[:, 0], r[:, 1], color=INK, lw=0.6)
    axl.set_xlim(-82, -33); axl.set_ylim(-56, 13)
    axl.set_xticks([]); axl.set_yticks([])
    axl.set_facecolor("#f7f9fa")
    axl.set_title("Legal Amazon", fontsize=7.0, color=INK, pad=2)
    for s in axl.spines.values():
        s.set_color("#aab1b8"); s.set_linewidth(0.5)

    # inset: the Congo Basin boxes
    axc = fig.add_axes([0.735, 0.115, 0.245, 0.375])
    for f in world:
        g = f["geometry"]
        subs = g["geometries"] if g.get("type") == "GeometryCollection" else [g]
        emph = f["properties"].get("name") == "Dem Rep of the Congo"
        for sub in subs:
            for r in rings(sub):
                axc.plot(r[:, 0], r[:, 1], color=INK if emph else "#b8bfc6",
                         lw=0.6 if emph else 0.3)
    for lab, (x0, y0, x1, y1) in CONGO.items():
        axc.add_patch(Rectangle((x0, y0), x1 - x0, y1 - y0, facecolor=C["flag"],
                                edgecolor=C["flag"], lw=0.8, alpha=0.85))
        axc.annotate(lab, ((x0 + x1) / 2, y1), textcoords="offset points", xytext=(0, 2),
                     ha="center", fontsize=7.0, color=C["flag"])
    axc.set_xlim(11, 33); axc.set_ylim(-14, 7)
    axc.set_xticks([]); axc.set_yticks([])
    axc.set_facecolor("#f7f9fa")
    axc.set_title("Congo Basin comparison", fontsize=7.0, color=INK, pad=2)
    for s in axc.spines.values():
        s.set_color("#aab1b8"); s.set_linewidth(0.5)

    save(fig, "F1_study_area.png")
    print("events gridded:", len(d), "max density %.1f" % np.nanmax(dens),
          "p98 %.1f" % vmax)


if __name__ == "__main__":
    main()
