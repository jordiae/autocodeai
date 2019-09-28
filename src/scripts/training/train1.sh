#!/usr/bin/env bash

FAIRSEQ=src/fairseq

BIN=data-bin/urls-2019-09-24
source venv/bin/activate
python $FAIRSEQ/train.py \
    --task language_modeling \
    $BIN \
    --save-dir models/checkpoints/transformer_gpt_1 \
    --arch transformer_lm_gpt \
    --max-update 286000 --max-lr 1.0 --t-mult 2 --lr-period-updates 270000 --lr-scheduler cosine --lr-shrink 0.75 \
    --warmup-updates 16000 --warmup-init-lr 1e-07 --min-lr 1e-09 --optimizer nag --lr 0.0001 --clip-norm 0.1 \
    --max-tokens 3072 --update-freq 3 --tokens-per-sample 3072 --seed 1 \
    --sample-break-mode complete_doc --skip-invalid-size-inputs-valid-test --ddp-backend=no_c10d
#python $FAIRSEQ/train.py \
#    --task language_modeling \
#    $BIN \
#    --save-dir models/checkpoints/transformer_gpt_1 \
#    --arch transformer_lm_gpt \
#    --max-update 286000 --max-lr 1.0 --t-mult 2 --lr-period-updates 270000 --lr-scheduler cosine --lr-shrink 0.75 \
#    --warmup-updates 16000 --warmup-init-lr 1e-07 --min-lr 1e-09 --optimizer nag --lr 0.0001 --clip-norm 0.1 \
#    --criterion adaptive_loss --max-tokens 3072 --update-freq 3 --tokens-per-sample 3072 --seed 1 \
#    --sample-break-mode complete_doc --skip-invalid-size-inputs-valid-test --ddp-backend=no_c10d