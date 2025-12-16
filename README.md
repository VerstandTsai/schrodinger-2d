# PP Final Project

This project is a **CUDA‑parallelized implementation** of the 2D Schrödinger Simulator, adapted from [Verstand's original code](https://github.com/VerstandTsai/schrodinger-2d).
Because I do not have access to a Linux environment, and using SDL2 in WSL2 provides a poor experience, so I make it support both **Windows** and **Linux** platforms.

---

## Linux

Navigate to the `linux` directory and run:

```bash
make cuda       # build the CUDA version
make sequential # build the sequential CPU version
make # build both CUDA and CPU version
```

## Windows
Requirment:
- Microsoft cl compiler
- nvcc
- SDL2

```Powershell
nmake cuda       # build the CUDA version
nmake sequential # build the sequential CPU version
nmake # build all
```

> Note: Windows paths may vary depending on your setup. Make sure to update the Makefile with the correct include/library paths for SDL2 and CUDA on your machine.

## Batch Mode & Visualization

You can run the simulation in batch mode to generate a trajectory file without opening a window (useful for benchmarking or headless servers).

```bash
./sequential --batch out.bin 100 50
./cuda --batch out.bin 100 50
```
Arguments: `output_file`, `num_frames`, `steps_per_frame`.

To visualize the result:
```bash
python3 visualizer.py out.bin
```

## Troubleshooting

If you are on a system without SDL2 installed (e.g., a server), you can compile in **Headless Mode**:

```bash
make sequential HEADLESS=1
make cuda HEADLESS=1
```
This disables the GUI window code entirely.
