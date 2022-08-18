import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
from transformers import pipeline
import argparse
import re
from mlhub.pkg import get_cmd_cwd
import utils


def summarize_pipeline(text, summarizer, min_length, max_length):
    summarized_text = summarizer(text, min_length=min_length, max_length=max_length)
    return summarized_text


parser = argparse.ArgumentParser(description ='summarize a given piece of text')
  
parser.add_argument('text', metavar ='input_text', 
                    type = str,
                    help ='input text to be summarized')
  
parser.add_argument('--min_len',
                    type = int,
                    help ='minimum length of summarized text')

parser.add_argument('--max_len', 
                    type = int,
                    help ='maximum length of summarized text')  

parser.add_argument('--verbose',
                    type = bool,
                    help='returns all the warnings generated by the program')


  
args = parser.parse_args()
min_length = 20
max_length = 70
verbose_op = False

if(args.verbose):
    verbose_op = True

if(args.min_len):
    min_length = args.min_len
if(args.max_len):
    max_length = args.max_len

# Calling it globally so we only have to call it once
if(not verbose_op):
    import warnings
    warnings.filterwarnings('ignore')

if((max_length <= min_length) or (max_length - min_length) < 30):
    print("length mismatch! please ensure that max length is at least 30 words greater than max length for a meaningful result and try again!")
    exit()


# Validate URL
if (utils.check_url(args.text)):
    text_ip = utils.read_url(args.text)
else:
    text_ip = utils.read_file(args.text)
text_list = re.findall(r'\w+', text_ip)
if (len(text_list) > 1024):
    text_ip = re.findall(r'\w+', text_ip)[:980]
    text_ip = " ".join(text_ip)
    print("Your input text is greater than 1024 words. Results are calculated on the first 1024 words of the input. If you want more accurate results input a text file with lower than 1024 words.")
    summarizer = pipeline("summarization",model="sshleifer/distilbart-cnn-12-6",framework="pt")
else:
    summarizer = pipeline("summarization", model="t5-small", framework="pt")


summarized_text = summarize_pipeline(text_ip, summarizer=summarizer, min_length=min_length, max_length=max_length)
print(f"Summary of {args.text} between {min_length} and {max_length} words below:\n")
print(summarized_text[0]['summary_text'])



