import struct
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import argparse
import sys
import os


def read_trajectory(filename):
    """
    Reads the binary trajectory file.
    Format:
    - Magic (4 bytes): "SCHR"
    - Width (int32)
    - Height (int32)
    - FrameCount (int32)
    - Frames: [FrameCount * Width * Height * 2 * double] (Real, Imag)
      Note: Original C++ uses double for complex.
    """
    if not os.path.exists(filename):
        print(f"Error: File {filename} not found.")
        sys.exit(1)

    with open(filename, "rb") as f:
        magic = f.read(4)
        if magic != b"SCHR":
            print("Error: Invalid file format (Magic header mismatch).")
            sys.exit(1)

        width, height, frame_count = struct.unpack("iii", f.read(12))
        print(f"Loading {filename}: {width}x{height}, {frame_count} frames")

        frames = []
        num_pixels = width * height
        # Each complex<double> is 16 bytes (8 bytes real, 8 bytes imag)
        frame_size_bytes = num_pixels * 16

        for i in range(frame_count):
            data = f.read(frame_size_bytes)
            if len(data) != frame_size_bytes:
                print(f"Warning: Incomplete frame {i}")
                break

            # Read as complex128 (double precision complex)
            # stored as real, imag interleaved
            arr = np.frombuffer(data, dtype=np.complex128)
            frames.append(arr.reshape((height, width)))

    return width, height, frames


def complex_to_rgb(z):
    """
    Maps a complex array to RGB values, matching the C++ visualization logic.
    """
    a = np.abs(z)

    # Avoid division by zero
    valid_mask = a > 1e-9

    y = np.zeros_like(a)
    y[valid_mask] = np.arctan(a[valid_mask]) / np.pi

    # z *= 0.5 * y / a
    # We perform this calculation carefully to operate on the array
    scaled_z = np.zeros_like(z)
    scaled_z[valid_mask] = z[valid_mask] * (0.5 * y[valid_mask] / a[valid_mask])

    u = scaled_z.real
    v = scaled_z.imag

    r = y + 1.5748 * v
    g = y - 0.1873 * u - 0.4681 * v
    b = y + 1.8556 * u

    rgb = np.dstack((r, g, b))

    # Clip to [0, 1] for matplotlib
    return np.clip(rgb, 0, 1)


def main():
    parser = argparse.ArgumentParser(description="Visualize Schrödinger 2D Trajectory")
    parser.add_argument("file", help="Path to the binary trajectory file")
    parser.add_argument(
        "--fps", type=int, default=30, help="Frames per second for playback"
    )
    parser.add_argument("--save", help="Save animation to file (e.g. out.mp4)")
    args = parser.parse_args()

    width, height, frames = read_trajectory(args.file)

    if not frames:
        print("No frames loaded.")
        return

    fig = plt.figure(figsize=(8, 6))
    ax = plt.axes()
    ax.set_title(f"Frame 0/{len(frames)}")

    img = ax.imshow(
        complex_to_rgb(frames[0]), origin="lower", extent=[0, width, 0, height]
    )
    plt.axis("off")

    def update(frame_idx):
        img.set_data(complex_to_rgb(frames[frame_idx]))
        ax.set_title(f"Frame {frame_idx}/{len(frames)}")
        return [img]

    ani = animation.FuncAnimation(
        fig, update, frames=len(frames), interval=1000 / args.fps, blit=False
    )

    if args.save:
        print(f"Saving animation to {args.save}...")
        ani.save(args.save, fps=args.fps)
    else:
        plt.show()


if __name__ == "__main__":
    main()
