import argparse
import numpy as np
import matplotlib.pyplot as plt
import math


parser = argparse.ArgumentParser()
parser.add_argument('-c', metavar="client_file", default='', help="File which has client probabilities")
parser.add_argument('-i', metavar="impostor_file", default='', help="File which has impostor probabilities")
parser.add_argument('-fn', metavar="false negative", help="Specification of false negatives")
parser.add_argument('-fp', metavar="false positive", help="Specification of false positives")
parsed_args = parser.parse_args()
args = vars(parsed_args)

clients = []
impostors = []

# Read client and impostor files
with open(args['c'], 'r') as fc:
    for line in fc:
        parts = line.split()
        clients.append(float(parts[1]))

with open(args['i'], 'r') as fi:
    for line in fi:
        parts = line.split()
        impostors.append(float(parts[1]))

# Initialize variables
clients = list(sorted(clients))
impostors = list(sorted(impostors))

x_point = []
y_point = []

idx_cli = 0
idx_imp = 0
dist = math.inf

if args['fn']:
    specific_fn = float(args['fn'])
    closest_fn = math.inf

if args['fp']:
    specific_fp = float(args['fp'])
    closest_fp = math.inf

# Compute FP and FN for each score
# Values from threshold = 0
FP = len(impostors)
FN = 0
x_point.append(FP/len(impostors))
y_point.append(1-FN/len(clients))

# Values from different thresholds
while idx_cli < len(clients) and idx_imp < len(impostors):
    th = min(clients[idx_cli], impostors[idx_imp])

    if clients[idx_cli] < impostors[idx_imp]:
        FN += 1
        idx_cli += 1
    elif clients[idx_cli] > impostors[idx_imp]:
        FP -= 1
        idx_imp += 1
    else:
        FN += 1
        FP -= 1
        idx_cli += 1
        idx_imp += 1

    fp_norm = FP/len(impostors)
    fn_norm = FN/len(clients)
    
    if args['fp'] and abs(fp_norm - specific_fp) < closest_fp:
        target_fn = fn_norm
        fn_threshold = th
        closest_fp = abs(fp_norm - specific_fp)

    if args['fn'] and abs(fn_norm - specific_fn) < closest_fn:
        target_fp = fp_norm
        fp_threshold = th
        closest_fn = abs(fn_norm - specific_fn)
    
    if abs(fp_norm - fn_norm) < dist:
        dist = abs(fp_norm - fn_norm)
        threshold_equal = th
        f_equal = fp_norm

    x_point.append(FP/len(impostors))
    y_point.append(1-FN/len(clients))

while idx_cli < len(clients):
    th = clients[idx_cli]
    FN += 1
    idx_cli += 1

    fp_norm = FP/len(impostors)
    fn_norm = FN/len(clients)
    
    if args['fp'] and abs(fp_norm - specific_fp) < closest_fp:
        target_fn = fn_norm
        fn_threshold = th
        closest_fp = abs(fp_norm - specific_fp)

    if args['fn'] and abs(fn_norm - specific_fn) < closest_fn:
        target_fp = fp_norm
        fp_threshold = th
        closest_fn = abs(fn_norm - specific_fn)
    
    if abs(fp_norm - fn_norm) < dist:
        dist = abs(fp_norm - fn_norm)
        threshold_equal = th

    x_point.append(FP/len(impostors))
    y_point.append(1-FN/len(clients))

while idx_imp < len(impostors):
    th = impostors[idx_imp]
    FP -= 1
    idx_imp += 1

    fp_norm = FP/len(impostors)
    fn_norm = FN/len(clients)
    
    if args['fp'] and abs(fp_norm - specific_fp) < closest_fp:
        target_fn = fn_norm
        fn_threshold = th
        closest_fp = abs(fp_norm - specific_fp)

    if args['fn'] and abs(fn_norm - specific_fn) < closest_fn:
        target_fp = fp_norm
        fp_threshold = th
        closest_fn = abs(fn_norm - specific_fn)
    
    if abs(fp_norm - fn_norm) < dist:
        dist = abs(fp_norm - fn_norm)
        threshold_equal = th

    x_point.append(FP/len(impostors))
    y_point.append(1-FN/len(clients))

# Values from threshold = 1
FP = 0
FN = len(clients)
x_point.append(FP/len(impostors))
y_point.append(1-FN/len(clients))

# Plot ROC curve
plt.plot(x_point, y_point)
plt.title('ROC CURVE')
plt.xlabel('FP')
plt.ylabel('1-FN')
plt.show()

# Retrieve threshold when they are equal
print("Threshold when FN == FP is %.5f. FN == FP == %.5f" % (threshold_equal, f_equal))

# Mann–Whitney U test
def H(c,i):
    if c>i:
        return 1
    elif c<i:
        return 0
    else:
        return 0.5

auc = 0
for c in clients:
    for i in impostors:
        auc += H(c,i)

auc = auc / (len(clients) * len(impostors))
print("Area found under ROC-curve: %.5f\n" % auc)

# D-prime calculation
pos = np.array(clients)
neg = np.array(impostors)

upos = np.mean(pos)
uneg = np.mean(neg)

varpos= np.var(pos)
varneg = np.var(neg)

d_comp = (upos - uneg) / np.sqrt(varpos + varneg)
print("D-prime value: %.5f\n" % d_comp)

# Retrieve FP and threshold when FN is specified
if args['fn']:
    print("FP(FN = %.5f) = %.5f and threshold is %.5f\n" % (specific_fn, target_fp, fp_threshold))

# Retrieve FN and threshold when FP is specified
if args['fp']:
    print("FN(FP = %.5f) = %.5f and threshold is %.5f\n" % (specific_fp, target_fn, fn_threshold))