"""Map plates M1 and M2 -- angular change, registration and deferral, per region.

Everything is read from the GeoTIFFs already written to `data/products/` (P5, P5b), so the
plates cost no Earth Engine work.  Each map carries a graticule, a scale bar and a locator
inset drawn from the cached country outlines.
"""
import glob, json
import numpy as np
import rasterio
from rasterio.merge import merge
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap, ListedColormap
from matplotlib.patches import Rectangle, Patch
from figstyle import W2, C, INK, INK2, SEQ_BLUE, save, panel_tag

PROD = "data/products"
OUTLINES = "aef_explore/paper/code/outlines.geojson"
REGIONS = {"M1": dict(key="ParaBR163", label="Pará / BR-163", tau=12.73,
                      inset=[-82, -57, -34, 13], focus="south_america"),
           "M2": dict(key="Roraima_S", label="Roraima (south)", tau=19.54,
                      inset=[-82, -57, -34, 13], focus="south_america")}
ANG = LinearSegmentedColormap.from_list("ang", SEQ_BLUE)


def mosaic(pattern):
    files = sorted(glob.glob(f"{PROD}/{pattern}"))
    if not files:
        raise FileNotFoundError(pattern)
    srcs = [rasterio.open(f) for f in files]
    arr, tr = merge(srcs)
    b = srcs[0].bounds
    xs = [s.bounds for s in srcs]
    ext = (min(x.left for x in xs), max(x.right for x in xs),
           min(x.bottom for x in xs), max(x.top for x in xs))
    for s in srcs:
        s.close()
    return arr[0], ext


def _walk(g, segs):
    t = g.get("type")
    if t == "GeometryCollection":
        for sub in g["geometries"]:
            _walk(sub, segs)
    elif t == "Polygon":
        for ring in g["coordinates"]:
            segs.append(np.asarray(ring))
    elif t == "MultiPolygon":
        for poly in g["coordinates"]:
            for ring in poly:
                segs.append(np.asarray(ring))
    elif t == "LineString":
        segs.append(np.asarray(g["coordinates"]))
    elif t == "MultiLineString":
        for line in g["coordinates"]:
            segs.append(np.asarray(line))


def outlines():
    """Country outlines as plain coordinate arrays, for the locator inset."""
    gj = json.load(open(OUTLINES))
    segs = []
    for f in gj["features"]:
        _walk(f["geometry"], segs)
    return [s for s in segs if len(s) > 2]


def scalebar(ax, ext, km=None, xfrac=0.06):
    """Scale bar in km, converted to degrees at the panel's own latitude."""
    lat = (ext[2] + ext[3]) / 2
    if km is None:                       # ~20 % of the panel, rounded to a tidy value
        span = (ext[1] - ext[0]) * 111.32 * np.cos(np.radians(lat))
        km = min([x for x in (10, 20, 25, 50, 100) if x >= 0.18 * span] or [100])
    deg = km / (111.32 * np.cos(np.radians(lat)))
    x0 = ext[0] + xfrac * (ext[1] - ext[0])
    y0 = ext[2] + 0.06 * (ext[3] - ext[2])
    ax.add_patch(Rectangle((x0, y0), deg, 0.012 * (ext[3] - ext[2]),
                           facecolor=INK, edgecolor="white", lw=0.4, zorder=6))
    ax.text(x0 + deg / 2, y0 + 0.03 * (ext[3] - ext[2]), f"{km} km", ha="center",
            va="bottom", fontsize=7.0, color=INK, zorder=6)


def north(ax, ext):
    x = ext[1] - 0.07 * (ext[1] - ext[0])
    y0 = ext[3] - 0.19 * (ext[3] - ext[2])
    h = 0.09 * (ext[3] - ext[2])
    ax.annotate("", xy=(x, y0 + h), xytext=(x, y0),
                arrowprops=dict(arrowstyle="-|>", color=INK, lw=0.8), zorder=6)
    ax.text(x, y0 + h * 1.05, "N", ha="center", va="bottom", fontsize=7.0, color=INK)


def graticule(ax, ext, step=0.5):
    xt = np.arange(np.ceil(ext[0] / step) * step, ext[1] + 1e-9, step)
    yt = np.arange(np.ceil(ext[2] / step) * step, ext[3] + 1e-9, step)
    for x in xt:
        ax.axvline(x, color="white", lw=0.3, alpha=0.55, zorder=4)
    for y in yt:
        ax.axhline(y, color="white", lw=0.3, alpha=0.55, zorder=4)
    ax.set_xticks(xt)
    ax.set_yticks(yt)
    ax.set_xticklabels([f"{abs(v):.1f}°{'W' if v < 0 else 'E'}" for v in xt], fontsize=7.0)
    ax.set_yticklabels([f"{abs(v):.1f}°{'S' if v < 0 else 'N'}" for v in yt], fontsize=7.0)
    ax.tick_params(length=1.6, pad=1.2)


def locator(fig, rect, ext, box_ext, segs):
    ax = fig.add_axes(rect)
    for s in segs:
        ax.plot(s[:, 0], s[:, 1], color="#9aa2ab", lw=0.3)
    ax.add_patch(Rectangle((box_ext[0], box_ext[2]), box_ext[1] - box_ext[0],
                           box_ext[3] - box_ext[2], facecolor="none",
                           edgecolor=C["flag"], lw=0.9))
    ax.plot(np.mean(box_ext[:2]), np.mean(box_ext[2:]), marker="o", ms=2.4,
            color=C["flag"])
    ax.set_xlim(ext[0], ext[1]); ax.set_ylim(ext[2], ext[3])
    ax.set_xticks([]); ax.set_yticks([])
    ax.set_facecolor("#f7f9fa")
    for s in ax.spines.values():
        s.set_color("#aab1b8"); s.set_linewidth(0.5)
    return ax


def plate(tag, cfg):
    key = cfg["key"]
    ang, ext = mosaic(f"{key}_ang2021_x100_100m_r*.tif")
    reg, _ = mosaic(f"{key}_reg2021_100m_r*.tif")
    dfr, _ = mosaic(f"{key}_defer2022_100m_r*.tif")
    ang = np.where(ang <= -32000, np.nan, ang / 100.0)
    aspect = (ext[3] - ext[2]) / (ext[1] - ext[0])
    fig = plt.figure(figsize=(W2, W2 * aspect / 3 * 1.30))
    segs = outlines()
    panels = [("a", ang, "2020→2021 angular change (°)"),
              ("b", reg, f"registered (change > τ = {cfg['tau']:.2f}°)"),
              ("c", dfr, "registers in 2022 (unregistered in 2021)")]
    for i, (t, arr, title) in enumerate(panels):
        ax = fig.add_axes([0.045 + i * 0.300, 0.165, 0.245, 0.760])
        if t == "a":
            im = ax.imshow(arr, extent=ext, cmap=ANG, vmin=0, vmax=30,
                           interpolation="nearest", zorder=1)
        else:
            cmap = ListedColormap(["#eef1f4", C["2021"] if t == "b" else C["congo"]])
            im = ax.imshow(np.clip(arr, 0, 1), extent=ext, cmap=cmap, vmin=0, vmax=1,
                           interpolation="nearest", zorder=1)
        graticule(ax, ext)
        if i:
            ax.set_yticklabels([])
        scalebar(ax, ext, xfrac=0.06)
        if i == 0:
            north(ax, ext)
        ax.set_title(title, fontsize=7.5, color=INK, pad=2.5)
        panel_tag(ax, f"({t})", dx=-0.01, dy=1.13)
        if t == "a":
            first = (ax, im)
        if t == "c":
            ax.legend(handles=[Patch(facecolor=C["congo"], edgecolor="none",
                                     label="registers in 2022")],
                      frameon=True, facecolor="white", edgecolor="#cdd3d9", framealpha=0.85,
                      loc="lower right", fontsize=7.0, handlelength=1.1,
                      borderpad=0.35, handletextpad=0.5).get_frame().set_linewidth(0.4)
        ax.set_xlim(ext[0], ext[1]); ax.set_ylim(ext[2], ext[3])
        if t == "c":
            axes_c = ax
    # the panels keep their geographic aspect, so matplotlib shrinks each axes box to fit;
    # read the settled geometry back before hanging the colourbar and the locator off it
    fig.canvas.draw()
    pos_a = first[0].get_position()
    pos_c = axes_c.get_position()
    cax = fig.add_axes([pos_a.x0, max(pos_a.y0 - 0.105, 0.02), pos_a.width, 0.020])
    cb = fig.colorbar(first[1], cax=cax, orientation="horizontal")
    cb.set_label("angular change (°)", fontsize=7.0, color=INK2, labelpad=1.5)
    cb.ax.tick_params(labelsize=7.0, length=1.5, pad=1.5)
    cb.outline.set_visible(False)
    locator(fig, [0.905, pos_c.y0 + pos_c.height * 0.30, 0.080,
                  pos_c.height * 0.55], cfg["inset"], ext, segs)
    fig.text(0.045, 0.972, f"{tag}  {cfg['label']}   {ext[0]:.2f}–{ext[1]:.2f}°E, "
             f"{ext[2]:.2f}–{ext[3]:.2f}°N   (100 m)", fontsize=8, color=INK)
    save(fig, f"{tag}_{key}.png")


if __name__ == "__main__":
    for tag, cfg in REGIONS.items():
        plate(tag, cfg)
