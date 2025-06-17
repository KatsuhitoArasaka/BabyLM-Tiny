import random
import os

TARGET_WORDS = 1_000_000
DEV_WORDS = int(0.2 * TARGET_WORDS)
SNIPPET_SIZE = 10_000
NUM_SNIPPETS = (TARGET_WORDS + DEV_WORDS) // SNIPPET_SIZE

files = os.listdir("./datasets/train_100M")
for file in files:
    with open(f"./datasets/train_100M/{file}", "r", encoding="utf-8") as f:
        words = f.read().split()
    total_words = len(words)

    if (total_words > TARGET_WORDS + DEV_WORDS):
        max_start = total_words - SNIPPET_SIZE
        starts = random.sample(range(max_start), NUM_SNIPPETS)

        snippets = [words[start:start + SNIPPET_SIZE] for start in starts]

        sampled_words = [word for snippet in snippets for word in snippet]

        train_words = sampled_words[:TARGET_WORDS]
        dev_words = sampled_words[TARGET_WORDS:]

        with open(f"./datasets/train_1M/{file}", "w+", encoding="utf-8") as f:
            f.write(" ".join(sampled_words))
        with open(f"./datasets/train_1M/{file[:-6]}_dev.train", "w+", encoding="utf-8") as f:
            f.write(" ".join(dev_words))
    else: 
        print(f"File {file} has only {total_words} words, not enough to sample {TARGET_WORDS} words.")

    
