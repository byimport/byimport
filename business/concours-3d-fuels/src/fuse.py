"""Fusion canopée (FastFuels) + sous-étage (notre reconstruction lidar) en un cube unique.

Choix d'ingénierie honnête : le SDK FastFuels ne publie pas de signatures stables et lisibles,
donc on n'appelle PAS son API en direct ici (pas d'appels inventés). Le flux réel du concours est :

  1. Générer/exporter la grille de canopée depuis la plateforme FastFuels → fichier NetCDF/zarr.
  2. Ce module ingère cet export, le rééchantillonne sur notre grille 1 m³, et le fusionne
     avec les voxels de sous-étage produits par ``understory_voxelize.py``.

Résultat : un cube de propriétés de combustible du sol jusqu'à la canopée, aux formats exigés.
"""
from __future__ import annotations

import argparse
import pathlib

import numpy as np
import xarray as xr

VOXEL = 1.0
UNDERSTORY_MAX = 2.0


def load_grid(path: pathlib.Path, var_hint: str | None = None) -> xr.DataArray:
    """Charge une grille 3D depuis un NetCDF/zarr et renvoie une DataArray (x, y, z)."""
    ds = xr.open_zarr(path) if path.suffix == ".zarr" else xr.open_dataset(path)
    if var_hint and var_hint in ds:
        da = ds[var_hint]
    else:
        # prend la première variable 3D
        da = next(v for v in ds.data_vars.values() if v.ndim == 3)
    return da.rename({d: n for d, n in zip(da.dims, ("x", "y", "z"))})


def regrid_to(reference: xr.DataArray, moving: xr.DataArray) -> xr.DataArray:
    """Rééchantillonne ``moving`` sur les coordonnées de ``reference`` (interp linéaire + 0 hors champ)."""
    return moving.interp(
        x=reference.x, y=reference.y, z=reference.z, method="linear"
    ).fillna(0.0)


def fuse(understory: xr.DataArray, canopy: xr.DataArray) -> xr.Dataset:
    """Empile sous-étage (<2 m) et canopée (>=2 m) sur une grille commune.

    On privilégie notre reconstruction sous 2 m (c'est notre valeur ajoutée) et la canopée
    FastFuels au-dessus, avec une zone de recouvrement moyennée pour éviter une discontinuité.
    """
    canopy_on_ref = regrid_to(understory, canopy)
    z = understory.z
    w_under = np.clip((UNDERSTORY_MAX - z) / UNDERSTORY_MAX, 0.0, 1.0)  # 1 au sol → 0 à 2 m
    w_canopy = 1.0 - w_under
    fused = understory * w_under + canopy_on_ref * w_canopy

    return xr.Dataset(
        {
            "bulk_density": fused.astype("float32"),
            "understory": understory.astype("float32"),
            "canopy": canopy_on_ref.astype("float32"),
        },
        attrs={
            "title": "Fused 3D fuel voxels (surface→canopy), 1m3",
            "understory_source": "NEON discrete-return lidar reconstruction (<2m)",
            "canopy_source": "FastFuels export (>=2m)",
            "blend": "linear ramp over 0-2m overlap",
        },
    )


def footprint_geojson(ds: xr.Dataset, epsg: int, out: pathlib.Path) -> None:
    """Écrit le polygone d'emprise (rectangle englobant) en GeoJSON projeté — livrable exigé."""
    import geopandas as gpd
    from shapely.geometry import box

    minx, maxx = float(ds.x.min()), float(ds.x.max())
    miny, maxy = float(ds.y.min()), float(ds.y.max())
    gdf = gpd.GeoDataFrame(
        {"name": ["challenge_area"]},
        geometry=[box(minx, miny, maxx, maxy)],
        crs=f"EPSG:{epsg}",
    )
    gdf.to_file(out, driver="GeoJSON")


def main() -> None:
    p = argparse.ArgumentParser(description="Fusionne canopée FastFuels + sous-étage lidar")
    p.add_argument("--understory", type=pathlib.Path, required=True, help="NetCDF de understory_voxelize")
    p.add_argument("--canopy", type=pathlib.Path, required=True, help="Export FastFuels (NetCDF/zarr)")
    p.add_argument("--canopy-var", help="Nom de variable canopée si ambigu (ex. bulkDensity)")
    p.add_argument("--epsg", type=int, default=32611, help="EPSG projeté de la zone (déf. UTM 11N)")
    p.add_argument("--out", type=pathlib.Path, default=pathlib.Path("outputs/fused.nc"))
    args = p.parse_args()

    under = load_grid(args.understory)
    can = load_grid(args.canopy, args.canopy_var)
    ds = fuse(under, can)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    ds.to_netcdf(args.out)
    footprint_geojson(ds, args.epsg, args.out.with_name("footprint.geojson"))
    print(f"écrit {args.out} + footprint.geojson  grille {dict(ds.sizes)}")


if __name__ == "__main__":
    main()
