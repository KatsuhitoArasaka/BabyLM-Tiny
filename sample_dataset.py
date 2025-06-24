import random
import os

TARGET_WORDS = 1_000_000
DEV_WORDS = int(0.2 * TARGET_WORDS)
SNIPPET_SIZE = 10_000
NUM_SNIPPETS = (TARGET_WORDS + DEV_WORDS) // SNIPPET_SIZE
def sample_from_single_file(file_path, target_words):
    files = os.listdir(file_path)
    for file in files:
        with open(f"./datasets/train_100M/{file}", "r", encoding="utf-8") as f:
            words = f.read().split()
        total_words = len(words)

        if (total_words > target_words + DEV_WORDS):
            max_start = total_words - SNIPPET_SIZE
            starts = random.sample(range(max_start), NUM_SNIPPETS)

            snippets = [words[start:start + SNIPPET_SIZE] for start in starts]

            sampled_words = [word for snippet in snippets for word in snippet]

            train_words = sampled_words[:target_words]
            dev_words = sampled_words[target_words:]

            with open(f"./datasets/train_1M/{file}", "w+", encoding="utf-8") as f:
                f.write(" ".join(sampled_words))
            with open(f"./datasets/train_1M/{file[:-6]}_dev.train", "w+", encoding="utf-8") as f:
                f.write(" ".join(dev_words))
        else: 
            print(f"File {file} has only {total_words} words, not enough to sample {target_words} words.")

    
def sample_proportional (output_name, no_words, bnc_spoken, childes, gutenberg, open_subtitles, simple_wiki, switchboard):
    if bnc_spoken + childes + gutenberg + open_subtitles + simple_wiki + switchboard != 1:
        raise ValueError("Proportions must sum to 1.")

    files = ["bnc_spoken.train", "childes.train", "gutenberg.train", "open_subtitles.train", "simple_wiki.train", "switchboard.train"]
    proportions = [bnc_spoken, childes, gutenberg, open_subtitles, simple_wiki, switchboard]

    sampled_words = []
    for i in range(len(files)):
        file = files[i]
        nr_words = int((no_words + DEV_WORDS) * proportions[i])  # Include dev words in sampling
        if nr_words == 0:
            continue
            
        with open(f"./datasets/train_100M/{file}", "r", encoding="utf-8") as f:
            words = f.read().split()
        total_words = len(words)

        if total_words < nr_words:
            print(f"File {file} has only {total_words} words, not enough to sample {nr_words} words.")
            continue

        # Calculate snippets needed for this file specifically
        snippets_needed = (nr_words + SNIPPET_SIZE - 1) // SNIPPET_SIZE  # Ceiling division
        max_start = total_words - SNIPPET_SIZE
        starts = random.sample(range(max_start), min(snippets_needed, max_start))
        snippets = [words[start:start + SNIPPET_SIZE] for start in starts]
        file_words = [word for snippet in snippets for word in snippet][:nr_words]
        sampled_words.extend(file_words)
    
    random.shuffle(sampled_words)
    train_words = sampled_words[:no_words]
    dev_words = sampled_words[no_words:]
        
    print(f"Total sampled words: {len(sampled_words)}")
    print(f"Train words: {len(train_words)}")
    print(f"Dev words: {len(dev_words)}")
    
    with open(f"./datasets/train_1M/{output_name}.train", "w+", encoding="utf-8") as f:
        f.write(" ".join(train_words))
    with open(f"./datasets/train_1M/{output_name}_dev.train", "w+", encoding="utf-8") as f:
        f.write(" ".join(dev_words))
    
sample_proportional("gutenberg_x_bnc_spoken", TARGET_WORDS, 0.5, 0, 0.5, 0, 0, 0)