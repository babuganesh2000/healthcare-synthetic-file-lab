import subprocess
import sys

GENERATORS = [
    "src/generators/generate_hl7.py",
    "src/generators/generate_x12.py",
    "src/generators/generate_eob.py",
    "src/generators/generate_pharmacy.py",
    "src/generators/generate_labs.py",
    "src/generators/generate_imaging.py",
    "src/generators/generate_rcm.py",
    "src/generators/generate_interoperability.py",
]


def main():
    for script in GENERATORS:
        print(f"\nRunning {script}")
        subprocess.run([sys.executable, script], check=True)

    print("\nAll healthcare standard files generated successfully.")


if __name__ == "__main__":
    main()