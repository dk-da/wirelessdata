import sys, os
from rpy import *
from scipy import *

def create_data(data, is_square_root=False):
    """Create distance data.
    Arguments:
      data:           position data
      is_square_root: whether to apply square root or not
    Return values:
      in_data:        distance data
      ndim:           number of dimensions
    """
    in_data = []
    num = len(data)
    ndim = len(data[0])
    for i in range(num):
        for j in range(num):
            if i < j:
                dist = 0.0
                for k in range(ndim): dist += (data[i][k] - data[j][k])**2
                if is_square_root: dist = sqrt(dist)
                in_data.append(dist)
            elif i > j:
                in_data.append(in_data[j*num+i])
            elif i == j:
                in_data.append(0.0)
    return in_data, ndim

def clustering(in_data, data, ele_file, cluster_method="complete", eps_file=None):
    """Clustering.
    Arguments:
      in_data:        distance data
      data:           position data
      ele_file:       element filename (height/merge data)
      cluster_method: clustering method [complete]
      eps_file:       EPS filename [None]
    """
    efile = file(ele_file, "w")

    if len(in_data) == 2:
        efile.write("%5.3f [-1 -2]\n" % in_data[1])
        efile.close()
        return

    mat = in_data[:]
    print "%d x %d = %d" % (len(data), len(data), len(mat))

    mat = with_mode(NO_CONVERSION, r.matrix)(mat, nrow=len(data))
    d = with_mode(NO_CONVERSION, r.as_dist)(mat)
    hc = r.hclust(d, method=cluster_method)

    for h, m in zip(r["$"](hc, "height"), r["$"](hc, "merge")):
        efile.write("%s %s\n" % (h, m))
    efile.close()

    if eps_file:
        r.postscript(eps_file, title=eps_file)
        r.plclust(hc, hang=-0.1, ann=r.FALSE)
        r.dev_off()

def expand_group(m, n):
    """Expand group list."""
    group = []
    for x in m[n-1]:
        if x < 0: group.append(-x)
        else: group.extend(expand_group(m, x))
    return group

def arrange_cluster(ele_file, data, ndim, threshold, out_file):
    """Arrange clustering data.
    Arguments:
      ele_file:    element filename (height/merge data)
      data:        position data
      ndim:        number of dimensions
      threshold:   threshold of clustering
      out_file:    output data filename
    Return value:
      groups:      pair list of hierarchical clustering
    """
    if len(data) == 2:
        print "Cluster 1  : 1"
        print "Total      : 1"
        return []
    elif len(data) < 2:
        print "No cluster"
        print "Total      : 0"
        return []

    efile = file(ele_file)
    ofile = file(out_file, "w")
    h = []
    m = []
    for l in efile:
        e = l.replace("[", "").replace("]", "").replace(",", " ").strip().rstrip("\n").split()
        h.append(float(e[0]))
        m.append([int(e[1]), int(e[2])])
    tt = [[i, x] for i, (x, d) in enumerate(zip(m, h)) if d > threshold]
    t = []
    for d in tt:
        for x in d[1]:
            if x < tt[0][0]+1: t.append(x)
    groups = []
    all = []
    for x in t:
        g = []
        if x < 0: g = [-x]
        else: g = expand_group(m, x)
        groups.append(g)
    if not groups: groups = [range(1, len(h) + 2)]
    for i, g in enumerate(groups):
        print "Cluster %-3d: %d" % (i+1, len(g))
        g_data = [data[j-1] for j in g]
        for d in range(ndim): ofile.write("%f " % average(mat(g_data).T[d]))
        for j in g: ofile.write("%d " % j)
        ofile.write("\n")
    efile.close()
    ofile.close()

    s = 0
    for x in groups: s += len(x)
    print "Total      : %d" % s
    return groups

def write_cluster(groups, cluster_out):
    """Write clustering result."""
    clust_file = file(cluster_out, "w")
    print "Number of clusters: %d" % len(groups)
    count = 1
    for c in groups:
        clust_file.write("%03d:" % count)
        for d in c: clust_file.write(" %d" % d)
        clust_file.write("\n")
        count += 1
    clust_file.close()

def main(args):
    if len(args) < 2:
        print >>sys.stderr, "Usage: %s data_file [threshold=5.0]>" % os.path.basename(args[0])
        sys.exit(1)
    elif len(args) == 2:
        th = 5.0
    elif len(args) > 2:
        th = float(args[2])

    DATA_FILE    = args[1]
    ELEMENT_FILE = "element.out"
    OUT_FILE     = "data.out"
    CLUSTER_FILE = "cluster.out"
    EPS_FILE     = "cluster.eps"
    IS_SQUARE_ROOT = True

    print "Data file:    %s" % DATA_FILE
    print "Element file: %s" % ELEMENT_FILE
    print "Output file:  %s" % OUT_FILE
    print "Cluster file: %s" % CLUSTER_FILE
    print "EPS file:     %s" % EPS_FILE
    if IS_SQUARE_ROOT:
        print "Threshold: %f (distance)" % th
    else:
        th = th**2
        print "Threshold: %f (distance**2)" % th

    # position data
    data = [[float(d) for d in l.split()] for l in file(DATA_FILE)]

    if len(data) > 1:
        # distance data
        in_data, ndim = create_data(data, is_square_root=IS_SQUARE_ROOT)
        # clustering by position and distance data and output element file
        clustering(in_data, data, ELEMENT_FILE, eps_file=EPS_FILE)
    else:
        print >>sys.stderr, "Error: no data."
        sys.exit(1)

    # arrange clustering data by element file and threshold, and output group data
    groups = arrange_cluster(ELEMENT_FILE, data, ndim, th, OUT_FILE)
    # output ordered clustering data by using group data
    write_cluster(groups, CLUSTER_FILE)

if __name__ == "__main__": main(sys.argv)
