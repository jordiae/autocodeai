#!/usr/bin/env bash

FAIRSEQ=src/fairseq

TEXT=data/corpora/urls-2019-09-24-21:07:51
BIN=data-bin/urls-2019-09-24
BPESIZE=5000
TRAIN_MINLEN=1  # remove sentences with <1 BPE token
TRAIN_MAXLEN=250
source venv/bin/activate

#python $FAIRSEQ/scripts/spm_train.py \
#  --input=$TEXT/train.txt \
#  --model_prefix=$BIN/sentencepiece.bpe \
#  --vocab_size=$BPESIZE \
#  --character_coverage=1.0 \
#  --model_type=bpe

python $FAIRSEQ/scripts/spm_encode.py \
  --model $BIN/sentencepiece.bpe.model \
  --output_format=piece \
  --inputs $TEXT/train.txt \
  --outputs $TEXT/train.bpe.txt \
  --min-len $TRAIN_MINLEN --max-len $TRAIN_MAXLEN
for SPLIT in "valid" "test"; do \
  python $FAIRSEQ/scripts/spm_encode.py \
    --model $BIN/sentencepiece.bpe.model \
    --output_format=piece \
    --inputs $TEXT/$SPLIT.txt $TEXT/$SPLIT.txt \
    --outputs $TEXT/$SPLIT.bpe.txt $TEXT/$SPLIT.bpe.txt
done

python $FAIRSEQ/preprocess.py \
    --only-source \
    --trainpref $TEXT/train.bpe.txt \
    --validpref $TEXT/valid.bpe.txt \
    --testpref $TEXT/test.bpe.txt \
    --destdir $BIN \
    --workers 20

