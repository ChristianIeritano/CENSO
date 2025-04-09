# CENSO Setup and Usage (currently for DRAC clusters)

The following is an overview of using the subCENSO submission module for submitting CENSO jobs to DRAC clusters. Note that configurations specific to the Hopkins/Ieritano lab are currently implemented, so the subCENSO code will need to be modified for your own use. The next update will include a config file. 

``subCENSO`` is distributed in the hope that it will be useful, but without any warranty; without even the implied warranty of merchantability or fitness for a particular purpose. See the GNU Lesser General Public License for more details.

## 1. Clone the subCENSO repo

Clone the repo to a location on the DRAC cluster that's in your system's PATH, like `home/YOUR_USERNAME/bin/CENSO`. Please note that the contents of this repository outside of the subCENSO script are the work of the [Grimme lab](https://github.com/grimme-lab/CENSO) and must be cited accordingly. 

Clone via the command:

```
cd /location/of/CENSO (like `home/YOUR_USERNAME/bin/CENSO)
git clone https://github.com/ChristianIeritano/CENSO
```

**Note:** The repo URL may change over time, but this is unlikely.

If this completes successfully, you'll see a folder called `CENSO` with all the files found on the CENSO GitHub repo as of the date you cloned it.

---

## 2. Move the subCENSO folder 

The subCENSO submission script folder /subCENSO_scripts should be moved to a location where you typically store your scripts, like `home/YOUR_USERNAME/bin/CENSO`, and change its permissions to be executable by

```
cd /location/of/subCENSO_scripts
chmod a+x subCENSO
```

## 2. Install xtb (not DRAC cluster users or any user when xtb is not natively available)

Install the latest version of [xtb](https://github.com/grimme-lab/xtb) using instructions provided on the xtb GitHub. We use [v6.7.1](https://github.com/grimme-lab/xtb/releases/tag/v6.7.1). 

## 3. Add CENSO/subCENSO/xtb to PATH and install modules

Add the following lines to your `.bashrc`. This puts the required ".exe" files and Python modules in your PATH:

```
export PYTHONPATH="$PYTHONPATH:/home/YOUR_USERNAME/bin/CENSO/src"
export PATH="$PATH:/home/YOUR_USERNAME/bin/CENSO/bin"
export PATH="$PATH:/home/YOUR_USERNAME/bin/subCENSO_scripts/subCENSO"
```

and if you needed to install xtb, add the following line to your `.bashrc`:

```
export PATH="$PATH:/PATH_TO_XTB_EXE/bin"

```

Then run:

```
cd /location/of/CENSO
pip install .
cd /location/of/CENSO/bin
chmod a+x censo
```

At this point, you can verify that CENSO works correctly by reloading your .bashrc via:

```
source ~/.bashrc
```

and then running CENSO via:

```
censo
```

which should print the following header (note that the version should match the printout below)

```
         ______________________________________________________________
        |                                                              |
        |                                                              |
        |                   CENSO - Commandline ENSO                   |
        |               v 2.1.3.dev54+g216ca3a.d20250409               |
        |    energetic sorting of CREST Conformer Rotamer Ensembles    |
        |                    University of Bonn, MCTC                  |
        |                           Oct 2024                           |
        |                 based on ENSO version 2.0.1                  |
        |             L. M. Seidler, F. Bohle and S. Grimme            |
        |                                                              |
        |______________________________________________________________|

        Please cite:
        (TBA)
        S. Grimme, F. Bohle, A. Hansen, P. Pracht, S. Spicher, and M. Stahn
        J. Phys. Chem. A 2021, 125, 19, 4039-4054.
        DOI: https://doi.org/10.1021/acs.jpca.1c00971

        This program is distributed in the hope that it will be useful,
        but WITHOUT ANY WARRANTY; without even the implied warranty of
        MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.

You must provide an input file via '-i' and provide number of cores via '--maxcores'.
```

---

## 5. Prepare ensemble input files

Move your `.xyz` file(s) containing each ensemble (e.g., the output from ORCA's GOAT) to a directory in either `/project` or `/scratch` on the DRAC cluster.

Also copy the following files from the `subCENSO_scripts` GitHub folder into the same directory:

- `censo_config.py` – this file tells CENSO what subroutines to run
- `gas.censo2rc` or `solv.censo2rc` – depending on whether you want to run in gas or solvent

---

## 6. Modify `censo_config.py` (if needed)

Look for the following line in `censo_config.py`:

```python
results, timings = zip(*[part.run(ensemble) for part in [Screening, Optimization]])
```

This line controls which subroutines will be run with CENSO. In general, you shouldn't need to change it.

If you want to run additional routines or prescreening steps, see the terms you can add to `[Screening, Optimization]` in the `.censo2rc` file, which you'll modify next.

---

## 7. Modify the `.censo2rc` file

Edit `gas.censo2rc` or `solv.censo2rc` as needed. See the [CENSO documentation](https://xtb-docs.readthedocs.io/en/latest/CENSO_docs/censorc.html) for what each keyword does.

**Important:** You must update the `orcapath` and `xtbpath` variables to match the system you're using. Since its paralellized, you must give the true path of both orca and xtb. It's recommended to have copies of `.censo2rc` in your system’s `bin` for each setup. One day there’ll be a proper config file...

---

## 8. Run `subCENSO`

Run `subCENSO` in a directory containing `.xyz` files with the coordinates of all ensembles.

The script will:

- Create a subdirectory for each `.xyz` file based on its basename
- Submit a CENSO job for each one

### Example usage:

```
subCENSO -n 64 -m 1500mb -t 2d12h30m12s -c 1 -u 0 -s gas -a def
```

### Arguments:

- `-n`: number of cores. Must be an integer.
- `-m`: memory. Must be an integer suffixed with `mb` or `gb`.
- `-t`: time. Format is `XdYhZmWs` — hopefully self-explanatory.
- `-c`: charge of the molecule. Must be an integer.  
  **Note:** You can't mix charges in one run. If you have neutral, cation, and anion ensembles, separate them into different folders and run `subCENSO` on each one.
- `-u`: number of unpaired electrons. Must be an integer.
- `-s`: solvent. Accepted inputs are `gas` or `h2o`. Anything else defaults to `gas`.
- `-a`: account. If you're in the Hopkins/Ieritano lab, use `def` or `rrg`.




