# Calculate the accuracy of a baseline that simply predicts "London" for every
#   example in the dev set.
# Hint: Make use of existing code.
# Your solution here should only be a few lines.

from utils import evaluate_places

with open("birth_dev.tsv") as tsv:
    lines = tsv.readlines()

preds = ["London"] * len(lines)
accuracy = evaluate_places("birth_dev.tsv", preds)
print(f"accuracy: {accuracy[1]/100}")