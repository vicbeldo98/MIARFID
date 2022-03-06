cd /home/victoria/Desktop/TA-FINAL

export PATH=$PATH:/opt/moses-4/bin/
export PATH=$PATH:/opt/moses-4/scripts/training/
export PATH=$PATH:/opt/srilm-1.7.3/bin/i686-m64
export SCRIPTS_ROOTDIR=/opt/moses-4/scripts/
export GIZA=/opt/mgiza/mgizapp/bin/
export MOSES=/opt/moses-4/

cd $PWD/MOSES
echo $PWD
mkdir final
cd final

# Entrenar modelo de lenguaje
mkdir lm
ngram-count -order 4 -unk -interpolate -ukndiscount -text ../europarl/train.es -lm lm/europarl.lm
export LM=$PWD/lm/europarl.lm

# Entrenar el modelo de alineamiento
export CPU=1
$SCRIPTS_ROOTDIR/training/train-model.perl -root-dir work -mgiza -mgiza-cpus $CPU \
-corpus ../europarl/train -f en -e es -alignment grow-diag-final-and \
-reordering msd-bidirectional-fe -lm 0:4:$LM -external-bin-dir $GIZA

# Entrenar el modelo log-linear
$MOSES/scripts/training/mert-moses.pl ../europarl/dev.en ../europarl/dev.es \
$MOSES/bin/moses work/model/moses.ini --maximum-iterations=200 --mertdir $MOSES/bin/

# Generate predictions
$MOSES/bin/moses -f mert-work/moses.ini < ../europarl/test.en > hyp.hyp

# Evaluate predictions
$MOSES/scripts/generic/multi-bleu.perl -lc ../europarl/test.es < hyp.hyp > ../pruebas/final.txt
cd ..
