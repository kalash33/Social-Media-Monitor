import argparse
parser = argparse.ArgumentParser()
from transformers import pipeline

pipe = pipeline("text-classification", model="Hate-speech-CNERG/indic-abusive-allInOne-MuRIL")

# Add arguments
parser.add_argument("text", type=str, help="toxicity text tester")
# Parse the arguments
args = parser.parse_args()
print(pipe(args.text))