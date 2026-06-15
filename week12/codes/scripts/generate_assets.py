from __future__ import annotations

import csv
import subprocess
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
FRAMES = DATA / "frames"


def ensure_dirs() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    FRAMES.mkdir(parents=True, exist_ok=True)


def projectile_data() -> list[dict[str, float]]:
    g = 9.81
    x0, y0 = 0.25, 0.25
    vx0, vy0 = 2.35, 4.15
    fps = 20
    n_frames = 34
    radius_m = 0.055
    rows = []
    for k in range(n_frames):
        t = k / fps
        x = x0 + vx0 * t
        y = y0 + vy0 * t - 0.5 * g * t * t
        if y < 0:
            break
        rows.append({
            "frame": float(k), "t_s": t, "x_m": x, "y_m": y,
            "vx_m_s": vx0, "vy_m_s": vy0 - g * t,
            "ax_m_s2": 0.0, "ay_m_s2": -g, "radius_m": radius_m,
        })
    return rows


def write_ground_truth(rows: list[dict[str, float]]) -> None:
    out = DATA / "ground_truth.csv"
    with out.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def draw_frames(rows: list[dict[str, float]]) -> None:
    width, height = 960, 540
    px_per_m = 140.0
    origin_px = (70, height - 58)
    rng = np.random.default_rng(261)
    for old in FRAMES.glob("frame_*.png"):
        old.unlink()
    for row in rows:
        img = Image.new("RGB", (width, height), (248, 250, 252))
        draw = ImageDraw.Draw(img)
        for xm in np.arange(0, 7.0, 0.5):
            xpx = origin_px[0] + int(round(xm * px_per_m))
            draw.line([(xpx, 0), (xpx, height)], fill=(226, 232, 240), width=1)
        for ym in np.arange(0, 4.0, 0.5):
            ypx = origin_px[1] - int(round(ym * px_per_m))
            draw.line([(0, ypx), (width, ypx)], fill=(226, 232, 240), width=1)
        draw.line([(origin_px[0], 0), origin_px], fill=(71, 85, 105), width=3)
        draw.line([origin_px, (width, origin_px[1])], fill=(71, 85, 105), width=3)
        draw.line([(origin_px[0], height - 28), (origin_px[0] + int(px_per_m), height - 28)], fill=(15, 23, 42), width=5)
        draw.text((origin_px[0] + 35, height - 50), "1 m", fill=(15, 23, 42))
        xpx = origin_px[0] + row["x_m"] * px_per_m + rng.normal(0, 0.45)
        ypx = origin_px[1] - row["y_m"] * px_per_m + rng.normal(0, 0.45)
        rpx = row["radius_m"] * px_per_m
        draw.ellipse([xpx - rpx, ypx - rpx, xpx + rpx, ypx + rpx], fill=(220, 38, 38), outline=(127, 29, 29), width=2)
        draw.ellipse([xpx - 0.25 * rpx, ypx - 0.25 * rpx, xpx + 0.25 * rpx, ypx + 0.25 * rpx], fill=(254, 202, 202))
        img.save(FRAMES / f"frame_{int(row['frame']):03d}.png")


def make_video() -> None:
    out = DATA / "projectile_synthetic.mp4"
    cmd = ["ffmpeg", "-y", "-framerate", "20", "-i", str(FRAMES / "frame_%03d.png"), "-pix_fmt", "yuv420p", "-vcodec", "libx264", str(out)]
    try:
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except Exception:
        print("No se pudo generar el video; los frames estan disponibles.")


def main() -> None:
    ensure_dirs()
    rows = projectile_data()
    write_ground_truth(rows)
    draw_frames(rows)
    make_video()
    print(f"Datos generados en {DATA}")
    print(f"Frames: {len(list(FRAMES.glob('frame_*.png')))}")


if __name__ == "__main__":
    main()
