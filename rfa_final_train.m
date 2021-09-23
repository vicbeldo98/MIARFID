#!/usr/bin/octave -qf
datapath = "datos/videos";
w_path = "videos_w";
load(datapath);
a=100000;
b =1000;
[w,E,k]=perceptron(data,b,a);
save_precision(4);
save(w_path,"w"); # nomfichero = nomcorpus_w