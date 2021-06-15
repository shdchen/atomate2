"""Core VASP flows."""

from __future__ import annotations

import typing
from dataclasses import dataclass, field

from jobflow import Flow, Maker

from atomate2.vasp.jobs.core import RelaxMaker

if typing.TYPE_CHECKING:
    from pathlib import Path
    from typing import Union

    from pymatgen.core.structure import Structure

    from atomate2.vasp.jobs.base import BaseVaspMaker


@dataclass
class DoubleRelaxMaker(Maker):
    """Maker to perform a double VASP relaxation."""

    name: str = "double relax"
    relax_maker: BaseVaspMaker = field(default_factory=RelaxMaker)

    def make(self, structure: Structure, prev_vasp_dir: Union[str, Path] = None):
        """
        Create a flow with two chained relaxations.

        Parameters
        ----------
        structure
            A pymatgen structure object.
        prev_vasp_dir
            A previous VASP calculation directory to copy output files from.

        Returns
        -------
        Flow
            A flow containing two relaxations.
        """
        relax1 = self.relax_maker.make(structure, prev_vasp_dir=prev_vasp_dir)
        relax1.name += " 1"

        relax2 = self.relax_maker.make(
            relax1.output.structure, prev_vasp_dir=relax1.output.dir_name
        )
        relax2.name += " 2"

        return Flow([relax1, relax2], relax2.output, name=self.name)