"""Reconstruction du combustible de sous-étage (< 2 m) en voxels 1 m³ à partir du lidar NEON.

C'est le cœur de notre différenciation : FastFuels modélise bien la canopée mais mal la strate
de surface. On normalise la hauteur au-dessus du sol, on ne garde que les retours sous 2 m, et on
agrège la densité de retours dans une grille 1 m³ comme proxy de charge de combustible fin.

Sortie : xarray.Dataset (x, y, z) exportable en NetCDF/GeoTIFF pour le concours.

Ce module fait tourner du calcul réel sur des nuages de points de plusieurs millions de points ;
prévoir de la RAM et lancer par tuile.
"""
from __future__ import annotations

import argparse
import pathlib

import numpy as np
import xarray as xr

try:
    import laspy
except ImportError as e:  # message d'aide clair plutôt qu'un traceback obscur
    raise SystemExit("Installez laspy :  pip install 'laspy[laz]'") from e

VOXEL = 1.0            # taille de voxel en mètres (résolution imposée : 1 m³)
UNDERSTORY_MAX = 2.0   # plafond de la strate de surface/sous-étage en mètres


def height_above_ground(las: "laspy.LasData") -> np.ndarray:
    """Hauteur normalisée au-dessus du sol.

    Si le nuage est déjà classé (classification 2 = sol, convention ASPRS), on interpole une
    surface de sol par cellule et on soustrait. Sinon, on rabat sur un minimum local grossier.
    """
    x, y, z = np.asarray(las.x), np.asarray(las.y), np.asarray(las.z)
    cls = np.asarray(las.classification)
    ground = cls == 2

    # Surface de sol par cellule 1 m : moyenne des points-sol si classés, sinon minimum
    # local (approximation ; pour la version finale, préférer PDAL filters.hag_nn).
    allx = np.floor(x / VOXEL).astype(np.int64)
    ally = np.floor(y / VOXEL).astype(np.int64)
    if ground.sum() >= 100:
        sx, sy, sz = allx[ground], ally[ground], z[ground]
        reducer = np.mean
    else:
        sx, sy, sz = allx, ally, z
        reducer = np.min

    import pandas as pd
    surf = (
        pd.DataFrame({"cx": sx, "cy": sy, "z": sz})
        .groupby(["cx", "cy"])["z"]
        .agg(reducer)
    )
    default = float(surf.median())
    gsurf = surf.reindex(
        list(zip(allx.tolist(), ally.tolist()))
    ).fillna(default).to_numpy()
    return z - gsurf


def voxelize_understory(las_path: pathlib.Path) -> xr.Dataset:
    las = laspy.read(str(las_path))
    x, y = np.asarray(las.x), np.asarray(las.y)
    hag = height_above_ground(las)

    mask = (hag >= 0.05) & (hag < UNDERSTORY_MAX)   # exclut le sol nu, garde le sous-étage
    x, y, h = x[mask], y[mask], hag[mask]
    if x.size == 0:
        raise SystemExit("Aucun retour sous 2 m après filtrage — vérifier la normalisation sol.")

    x0, y0 = np.floor(x.min()), np.floor(y.min())
    ix = np.floor((x - x0) / VOXEL).astype(np.int64)
    iy = np.floor((y - y0) / VOXEL).astype(np.int64)
    iz = np.floor(h / VOXEL).astype(np.int64)
    nx, ny, nz = ix.max() + 1, iy.max() + 1, int(UNDERSTORY_MAX / VOXEL)
    iz = np.clip(iz, 0, nz - 1)

    grid = np.zeros((nx, ny, nz), dtype=np.float32)
    np.add.at(grid, (ix, iy, iz), 1.0)             # densité de retours par voxel

    # proxy de charge de combustible : densité normalisée (à calibrer contre terrain — voir validate.py)
    ds = xr.Dataset(
        {"return_density": (("x", "y", "z"), grid)},
        coords={
            "x": x0 + (np.arange(nx) + 0.5) * VOXEL,
            "y": y0 + (np.arange(ny) + 0.5) * VOXEL,
            "z": (np.arange(nz) + 0.5) * VOXEL,
        },
        attrs={
            "title": "Understory fuel voxels (<2m), 1m3",
            "source": "NEON discrete-return lidar DP1.30003.001",
            "voxel_m": VOXEL,
            "note": "return_density is a proxy; calibrate to fuel load with field plots",
        },
    )
    return ds


def main() -> None:
    p = argparse.ArgumentParser(description="Voxelise le sous-étage <2m depuis un .laz NEON")
    p.add_argument("las", type=pathlib.Path, help="Fichier lidar .laz/.las")
    p.add_argument("--out", type=pathlib.Path, default=pathlib.Path("outputs/understory.nc"))
    args = p.parse_args()
    ds = voxelize_understory(args.las)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    ds.to_netcdf(args.out)
    print(f"écrit {args.out}  grille {dict(ds.sizes)}")


if __name__ == "__main__":
    main()
