# generate_bat.py

def generate_bat_file(filename="data.bat"):
    # List of .bat commands you want to add
    bat_lines = [
        "@echo off",
        "echo Hello, this is an auto-generated batch file!",
        "echo Current directory: %cd%",
        "pause"
    ]

    # Write lines into the .bat file
    with open(filename, "w") as f:
        for line in bat_lines:
            f.write(line + "\n")

    print(f"Batch file '{filename}' generated successfully.")


if __name__ == "__main__":
    generate_bat_file()
