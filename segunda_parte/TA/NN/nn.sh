export TA=${PWD}
export INSTALLATION_PATH=${TA}
export NMT=${INSTALLATION_PATH}/NMT_TA
export PATH=${NMT}/miniconda/bin/:${PATH}
export PYTHONPATH=${PYTHONPATH}:${NMT}/nmt-keras/keras:${NMT}/nmt-keras/coco-caption:${NMT}/nmt-keras/multimodal_keras_wrapper

# python ${NMT}/nmt-keras/main.py -c config.py

python ${NMT}/nmt-keras/sample_ensemble.py --models trained_models/final/epoch_14 --dataset datasets/Dataset_europarl_enes.pkl \
--text Practica2/Data/europarl/test.en --dest hyp.test.es --config config.py


${NMT}/nmt-keras/utils/multi-bleu.perl -lc Practica2/Data/europarl/test.es < hyp.test.es