
import numpy as np
import scipy
import dsna as ds
from autotimeit import autotimeit

__all__ = ['benchit']

def benchit(verbose=True):
    statements, setups = suite()
    results = []
    for key in statements:
        if verbose:
            print
            print key
        for stmt in statements[key]:
            for shortname in setups:
                t = autotimeit(stmt, setups[shortname])
                results.append((stmt, shortname, t))
                if verbose:
                    print
                    print '\t' + stmt
                    print '\t' + shortname         
                    print '\t' + str(t)
    return display(results)                

def geta(shape, dtype, nans=False):
    arr = np.arange(np.prod(shape), dtype=dtype).reshape(*shape)
    if nans:
        arr[:] = np.nan
    return arr 
    
def suite():

    statements = {}
    setups = {}
    
    setups['(10000,) float64'] = "import numpy as np; import scipy.stats as sp; import dsna as ds; from dsna.bench.bench import geta; N=10000; a = geta((N,), 'float64')"
    setups['(500,500) float64'] = "import numpy as np; import scipy.stats as sp; import dsna as ds; from dsna.bench.bench import geta; N=500; a = geta((N, N), 'float64')"
    setups['(10000,) float64 NaN'] = "import numpy as np; import scipy.stats as sp; import dsna as ds; from dsna.bench.bench import geta; N=10000; a = geta((N,), 'float64', True)"
    setups['(500,500) float64 NaN'] = "import numpy as np; import scipy.stats as sp; import dsna as ds; from dsna.bench.bench import geta; N=500; a = geta((N, N), 'float64', True)"
    setups['(10000,) int32'] = "import numpy as np; import scipy.stats as sp; import dsna as ds; from dsna.bench.bench import geta; N=10000; a = geta((N,), 'int32')"
    setups['(500,500) int32'] = "import numpy as np; import scipy.stats as sp; import dsna as ds; from dsna.bench.bench import geta; N=500; a = geta((N, N), 'int32')"
    setups['(10000,) int64'] = "import numpy as np; import scipy.stats as sp; import dsna as ds; from dsna.bench.bench import geta; N=10000; a = geta((N,), 'int64')"
    setups['(500,500) int64'] = "import numpy as np; import scipy.stats as sp; import dsna as ds; from dsna.bench.bench import geta; N=500; a = geta((N, N), 'int64')"

    # DSNA
    s = ['ds.sum(a, axis=-1)', 'ds.max(a, axis=-1)',
         'ds.min(a, axis=-1)', 'ds.mean(a, axis=-1)',
         'ds.std(a, axis=-1)']
    statements['dsna'] = s
    
    # Numpy
    s = ['np.nansum(a, axis=-1)', 'np.nanmax(a, axis=-1)',
         'np.nanmin(a, axis=-1)', 'sp.nanmean(a, axis=-1)',
         'sp.nanstd(a, axis=-1)']
    statements['numpy/scipy'] = s
    
    return statements, setups

def display(results):
    results = list(results)
    na = [i for i in results if i[0].startswith('ds.')]
    nu = [i for i in results if i[0].startswith('np.') or
                                                    i[0].startswith('sp.')]
    print 'DSNA performance benchmark'
    print "\tDSNA  %s" % ds.__version__
    print "\tNumpy %s" % np.__version__
    print "\tScipy %s" % scipy.__version__
    print "\tSpeed is numpy (or scipy) time divided by dsna time"
    print "\tNaN means all NaNs"
    print "   Speed   Test                  Shape        dtype    NaN?"
    for nai in na:
        nui = [i for i in nu if i[0][6:]==nai[0][3:] and i[1]==nai[1]]
        if len(nui) != 1:
            raise RuntimeError, "Cannot parse benchmark results."
        nui = nui[0]
        des = nai[1].split(' ')
        tup = [nui[2]/nai[2], nui[0][3:].ljust(20), des[0].ljust(13), des[1]]
        if len(des) ==  3:
            tup += [des[2]]
        else:
            tup += ['']
        print '%9.4f  %s  %s%s  %s' % tuple(tup)
