import nltk

packages = [
    "punkt",
    "punkt_tab",
    "words",
    "averaged_perceptron_tagger",
    "averaged_perceptron_tagger_eng",
]

for package in packages:
    try:
        nltk.download(package, quiet=False)
    except Exception as exc:
        print(f"Could not download {package}: {exc}")

print("\nNLTK data setup completed.")
