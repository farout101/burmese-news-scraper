import pandas as pd
import argparse

def split_burmese_sentences(input_csv, output_csv, category="default", min_length=80):
    """
    Reads a CSV, splits sentences in the 'text' column by Burmese sentence ending '။',
    merges short sentences under min_length, removes newlines, and writes a new CSV 
    with 'category' and 'sentence' columns.
    
    Args:
        input_csv (str): Path to the input CSV file.
        output_csv (str): Path to save the output CSV file.
        category (str): Category name to assign for all sentences.
        min_length (int): Minimum sentence length. Short sentences are merged.
    """
    df = pd.read_csv(input_csv)
    data = []

    for text in df['text'].dropna():
        # Remove newlines
        text = text.replace('\n', ' ').replace('\r', ' ')
        # Split by Burmese sentence ending
        sentences = [s.strip() for s in text.split('။') if s.strip()]
        
        merged_sentences = []
        buffer = ""
        for i, sentence in enumerate(sentences):
            sentence = sentence + "။"  # add the symbol back
            if buffer:
                sentence = buffer + " " + sentence
                buffer = ""

            if len(sentence) < min_length:
                # If not last sentence, merge with next
                if i < len(sentences) - 1:
                    buffer = sentence
                else:
                    # If last sentence, merge with previous if possible
                    if merged_sentences:
                        merged_sentences[-1] += " " + sentence
                    else:
                        merged_sentences.append(sentence)
            else:
                merged_sentences.append(sentence)

        for sent in merged_sentences:
            data.append({'category': category, 'text': sent})

    new_df = pd.DataFrame(data)
    new_df.to_csv(output_csv, index=False, encoding='utf-8-sig')
    print(f"Processed {len(data)} sentences. Output saved to {output_csv}")


def main():
    parser = argparse.ArgumentParser(description="Split Burmese sentences in a CSV file with min length merging.")
    parser.add_argument("input_csv", help="Path to input CSV file")
    parser.add_argument("output_csv", help="Path to output CSV file")
    parser.add_argument("--category", default="default", help="Category to assign to sentences")
    parser.add_argument("--min_length", type=int, default=80, help="Minimum sentence length")
    
    args = parser.parse_args()
    
    split_burmese_sentences(args.input_csv, args.output_csv, args.category, args.min_length)


if __name__ == "__main__":
    main()
