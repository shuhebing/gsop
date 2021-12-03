Procedures for determining ordered ground states by group-subgroup transformation

1.Convert the format of CIF file to the format of POSCAR file 
Read all CIF files from the folder of cifs, and then convert CIF file format to POSCAR format because VASP calculations require POSCAR as the input of structural information. POSCAR files are automatically saved to the folder of poscars.

2. Generate various ordered phases
Read out all poscar files from the poscars folder. Generate various ordered phases with different Li concentrations and these configurations will be stored in concs folder.

3. Obtain non-identical arrangements
Read out ordered phases from the concs folder. After that, StructureMatcher utility in Pymatgen is employed to exclude identical arrangements

4. Generate hierarchical directories for DFT calculations
Read all non-indentical structures in uniqk folder. Update hierarchical directories  for DFT calculations.     

5. Configure inputs files for DFT calculations.
update INCAR, POTCAR, KPOINTS and vasp.lsf for each POSCAR.

6. Extract DFT calculation results
information of free energies, supercell size, Li concentration will be read from output files of DFT calculations.

7. Phase diagram determination
Formation energies of all ordered phase are calculated, Ordered ground states are obtained by convex hull.

The detailed algorithm of gsop is describted the following article:
(1)Ran, Y.; Zou, Z.; Liu, B.; Wang, D.; Pu, B.; Mi, P.; Shi, W.; Li, Y.; He, B.; Lu, Z.; Lu, X.; Li, B.; Shi, S. Towards Prediction of Ordered Phases in Rechargeable Battery Chemistry via Group–Subgroup Transformation. npj Comput Mater 2021, 7 (1), 1–11. https://doi.org/10.1038/s41524-021-00653-y.

If you use gsop in your research, please consider citing the article.
