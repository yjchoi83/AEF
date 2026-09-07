"""P5b item 2, step 4 -- stamp the retirement of P5 map layer (d) onto the committed plates.

Layer (d) rendered sigma(2.1413 + 0.0552 * annual clear count) as "attribution confidence".
Two things are wrong with it and both are now on record: the model is fitted on `clear_post`
(a post-event count) but the map feeds it an annual count, whose measured skill at predicting
deferral is AUC 0.599 (P5 section 3); and the raw-count link is mis-calibrated at the low end,
predicting 0.91 registration where one post-event clear observation actually yields 0.59.
The plates are stamped rather than re-rendered because the P5 map script was not retained;
the replacement layers are P5b figures F7 and F8.
"""
from PIL import Image, ImageDraw, ImageFont

PLATES = {"aef_explore/stage5/TB01/P5/figures/M_ParaBR163.png": 985,
          "aef_explore/stage5/TB01/P5/figures/M_Roraima_S.png": 895}
W = 911
MSG1 = "d  RETIRED — was “attribution confidence”; it is a mid-year-event prior only"
MSG2 = ("σ(β₀+β₁·count) fitted on post-event counts but fed the ANNUAL count; skill at predicting "
        "deferral AUC 0.599, and mis-calibrated at low counts (predicts .91 where the data give .59).")
MSG3 = "Superseded by P5b F7 (observation supply) and F8 (deferral risk by event month)."


def font(sz):
    for p in ("/usr/share/fonts/dejavu/DejaVuSans-Bold.ttf",
              "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"):
        try:
            return ImageFont.truetype(p, sz)
        except OSError:
            continue
    return ImageFont.load_default()


def main():
    for path, y0 in PLATES.items():
        im = Image.open(path).convert("RGB")
        d = ImageDraw.Draw(im, "RGBA")
        d.rectangle([0, y0 - 6, W, y0 + 96], fill=(255, 255, 255, 240))
        d.rectangle([0, y0 - 6, W, y0 + 96], outline=(178, 34, 34), width=3)
        d.text((10, y0 + 2), MSG1, fill=(178, 34, 34), font=font(19))
        d.text((10, y0 + 28), MSG2[:78], fill=(60, 60, 60), font=font(13))
        d.text((10, y0 + 46), MSG2[78:], fill=(60, 60, 60), font=font(13))
        d.text((10, y0 + 70), MSG3, fill=(60, 60, 60), font=font(13))
        d.text((int(W * 0.18), y0 + int(W * 0.42)), "RETIRED", fill=(178, 34, 34, 190),
               font=font(96))
        im.save(path)
        print("stamped", path)


if __name__ == "__main__":
    main()
