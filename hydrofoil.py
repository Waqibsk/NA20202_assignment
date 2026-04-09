import sys

import matplotlib.pyplot as plt
import numpy as np


def generate_hydrofoil():
    print("=" * 55)
    print(" Joukowski Hydrofoil Generator ")
    print("=" * 55)

    # -----------------------------
    # INPUT (x0, y0)
    # -----------------------------
    try:
        a = float(input("Enter radius a: "))
        x0 = float(input("Enter x0 (x-offset): "))
        y0 = float(input("Enter y0 (y-offset, 0 = symmetric): "))
    except ValueError:
        print("Invalid input.")
        sys.exit(1)

    # z0 = x0 + iy0 (Center of the circle in the z-plane)
    z0 = x0 + 1j * y0

    # -----------------------------
    # VALIDATION
    # -----------------------------
    if a <= abs(y0):
        print("Error: a must be > |y0| for valid hydrofoil.")
        sys.exit(1)

    # -----------------------------
    # TRAILING EDGE CONDITION
    # |b - z0| = a  -> b is real
    # b is the transformation parameter
    # -----------------------------
    b = x0 + np.sqrt(a**2 - y0**2)

    # -----------------------------
    # CIRCLE IN z-PLANE
    # z = z0 + a * e^{i*theta}
    # -----------------------------
    theta = np.linspace(0, 2 * np.pi, 800)
    z_circle = z0 + a * np.exp(1j * theta)

    # z = x + iy
    x = np.real(z_circle)
    y = np.imag(z_circle)

    # -----------------------------
    # JOUKOWSKI TRANSFORMATION
    # zeta = z + b^2 / z
    # -----------------------------

    zeta_foil = z_circle + (b**2) / z_circle

    # zeta = xi + i*eta
    xi = np.real(zeta_foil)
    eta = np.imag(zeta_foil)

    foil_type = "Symmetric" if abs(y0) < 1e-6 else "Cambered"

    # -----------------------------
    # THICKNESS & CAMBER
    # -----------------------------

    thickness = max(eta) - min(eta)
    camber_line = (max(eta) + min(eta)) / 2

    # -----------------------------
    # PLOTTING
    # -----------------------------
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

    # z-plane (Circle)
    ax1.plot(x, y, "b-", label="Circle")
    ax1.plot(x0, y0, "ro", label="Center z0")
    ax1.plot(b, 0, "kx", label="Point b (maps to TE)")
    ax1.set_title(r"$z$-plane (Physical): $z = x + iy$")
    ax1.set_xlabel("x")
    ax1.set_ylabel("y")
    ax1.axis("equal")
    ax1.grid(True)
    ax1.legend()

    # zeta-plane (Hydrofoil)
    ax2.plot(xi, eta, "g-", linewidth=2, label="Hydrofoil")

    # thickness bounds
    ax2.axhline(max(eta), linestyle="--", alpha=0.5)
    ax2.axhline(min(eta), linestyle="--", alpha=0.5)

    # camber line
    ax2.axhline(camber_line, linestyle=":", color="black", label="Camber line")

    ax2.set_title(r"$\zeta$-plane (Transformed): $\zeta = \xi + i\eta$")
    ax2.set_xlabel(r"$\xi$")
    ax2.set_ylabel(r"$\eta$")
    ax2.axis("equal")
    ax2.grid(True)
    ax2.legend()

    # -----------------------------
    # OUTPUT
    # -----------------------------
    print("\n--- RESULTS ---")
    print(f"Type: {foil_type}")
    print(f"z0 = {x0} + i{y0}")
    print(f"b = {b:.4f}")
    print(f"Max thickness ≈ {thickness:.4f}")
    print(f"Camber line ≈ {camber_line:.4f}")

    if foil_type == "Symmetric":
        print("-> y0 = 0 => symmetric hydrofoil")
    else:
        print("-> y0 != 0 => cambered hydrofoil")

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    generate_hydrofoil()
