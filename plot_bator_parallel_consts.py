#!/usr/bin/env python

'''
Produce plots regarding the Bator's parallelisation constants.

Using the --reg option, it is possible to compute an estimate of the parallelisation
constants using statistical regressions. In such a case, the python's **statsmodels**
package is required (you may install it using pip).
'''

from __future__ import print_function, division, absolute_import, unicode_literals

from argparse import ArgumentParser, RawDescriptionHelpFormatter
from collections import defaultdict
import matplotlib as mpl
import numpy as np
import os
import sys

from bronx.graphics.axes import set_nice_time_axis
from bronx.stdtypes.date import Date, Period, daterange
from bronx.system.memory import convert_bytes_in_unit

import vortex
import common  # @UnusedImport
from vortex import toolbox

mpl.use('agg')
import matplotlib.pyplot as plt


def fetchjson(date, args):
    """Retrieve a JSON file and return associated data."""
    data = None
    rh = None
    try:
        rh = toolbox.input(date=date, cutoff=('production' if args.prod else 'assim'),
                           model='[vapp]', kind='taskinfo', scope=args.scope, task=args.task,
                           namespace=args.ns, block=args.block, experiment=args.xpid,
                           member=args.mb, vapp=args.vapp, vconf=args.vconf,
                           shouldfly=True, now=True)

        data = rh[0].contents.data
    finally:
        if rh:
            rh[0].container.clear()
    return data


def do_boxplot(output, datastack):
    """Produce a box & whiskers plot for a timeserie of measured data."""
    titles = list()
    populations = list()
    for k, d in datastack.items():
        titles.append(k)
        populations.append(d)
    for (title, filesuffix, index) in zip(('Estimated memory constant (B/B)',
                                           'Estimated time constant (s/MB)'),
                                          ('memory_constant', 'time_constant'),
                                          (3, 4)):
        # Create a figure instance
        fig = plt.figure(1, figsize=(9, 1 + 0.35 * len(titles)))
        # Create an axes instance
        ax = fig.add_subplot(111)
        # Create the boxplot
        bp = ax.boxplot([np.ma.compressed(d[:, index]) for d in populations],
                        vert=False)
        ax.set_yticklabels(titles)
        ax.get_xaxis().tick_bottom()
        ax.get_yaxis().tick_left()
        ax.set_xlabel(title)
        # Save the figure
        fig.savefig(output.format(suffix=filesuffix), bbox_inches='tight')
        plt.close()


def do_timeseries(output, datastack, times, dates):
    """Produce a plot for a timeserie of measured data."""
    for db, data in datastack.items():
        # Create axes instances
        fig, (ax1, ax2, ax3) = plt.subplots(3, sharex=True, figsize=(7, 10))
        # Create the plot
        ax1.plot(times, data[:, 1])
        ax1.set_ylabel('Memory (GiB)')
        ax1.grid()
        ax1b = ax1.twinx()
        ax1b.plot(times, data[:, 3], ':')
        ax1b.set_ylabel('Est. memory cte (B/B) (dots)')
        ax2.plot(times, data[:, 2])
        ax2.set_ylabel('Time (s)')
        ax2.grid()
        ax2b = ax2.twinx()
        ax2b.plot(times, data[:, 4], ':')
        ax2b.set_ylabel('Est. time cte (s/MiB) (dots)')
        ax3.plot(times, data[:, 0])
        ax3.set_ylabel('Input Size (MiB)')
        ax3.grid()
        set_nice_time_axis(ax3, 'x', dt_min=dates[0], dt_max=dates[-1])
        #
        fig.suptitle('Timeserie for ODB database {:s}'.format(db))
        # Save the figure
        fig.savefig(output.format(db=db))
        plt.close()


def do_reg(datastack, idx=1, regtype='ols', obsscale=1., obsoffset=0.):
    """Compute regresions for a given timeserie of measured data."""
    import statsmodels.api as sm

    prednames = list()
    samplesize = 0
    for k in sorted(datastack.keys()):
        prednames.append(k)
        samplesize += datastack[k].shape[0]

    obsarray = np.empty((samplesize, ), dtype=np.float64)
    predarray = np.zeros((samplesize, len(prednames)), dtype=np.float64)

    padding = 0
    for i, k in enumerate(prednames):
        ilen = datastack[k].shape[0]
        obsarray[padding:padding + ilen] = (datastack[k][:, idx] * obsscale) - obsoffset
        predarray[padding:padding + ilen, i] = datastack[k][:, 0]
        padding += ilen

    if regtype.endswith('+int'):
        predarray = sm.add_constant(predarray)

    if regtype.startswith('rlm'):
        model = sm.RLM(obsarray, predarray, M=sm.robust.norms.HuberT())
    elif regtype.startswith('ols'):
        model = sm.OLS(obsarray, predarray)
    else:
        raise ValueError("Unkown regression method")
    results = model.fit()

    print(results.summary())
    for i, n in enumerate(prednames):
        print('{:02d}: {:s}'.format(i + 1, n))


def main():
    '''Process command line options.'''

    program_name = os.path.basename(sys.argv[0])
    program_shortdesc = program_name + ' -- ' + __import__('__main__').__doc__.lstrip("\n")
    program_desc = program_shortdesc

    def splitlist(mystr):
        return mystr.split(',')

    # Setup argument parser
    parser = ArgumentParser(description=program_desc,
                            formatter_class=RawDescriptionHelpFormatter)

    parser.add_argument("-m", "--memoffset", dest="memoff", action="store",
                        type=float, default=1024.,
                        help="Memory offset used when computing regression and estimating constants (in MB) [default: %(default).0f]")
    parser.add_argument("--only", dest="only", action="store", type=splitlist,
                        help="Use only a subset of ODB databases (comma-separated list of names).")
    parser.add_argument("--reg", dest="reg", action="store", choices=['ols', 'ols+int', 'rlm', 'rlm+int'],
                        help=("Perform a regression to estimate constants. " +
                              "(ols -> OrdinaryLeastSquares, rlm -> RobustLinearMethod with Huber norm, " +
                              "+int -> Add a constant to  the regression)."))
    parser.add_argument("--scope", dest='scope', default='parallelisation',
                        help="Scope of the input resource [default: %(default)s]")
    parser.add_argument("-t", "--task", dest='task', default='batodb',
                        help="Task name of the input resource [default: %(default)s]")
    parser.add_argument("-p", "--prod", dest='prod', action="store_true",
                        help="Use the early-delivery cutoff.")
    parser.add_argument("--namespace", dest='ns', default='vortex.multi.fr',
                        help="Namespace of the input provider [default: %(default)s]")
    parser.add_argument("--block", dest='block', default='observations',
                        help="Block for the input provider [default: %(default)s]")
    parser.add_argument("--member", dest='mb', type=int, default=None,
                        help="Member's number for the input provider [default: %(default)s]")
    parser.add_argument("vapp", help="The Vortex's application to look into.")
    parser.add_argument("vconf", help="The Vortex's configuration to look into.")
    parser.add_argument("xpid", help="The Vortex's experiment ID.")
    parser.add_argument("begin", type=Date, help="The begin date for the stats.")
    parser.add_argument("end", type=Date, help="The end date for the stats.")
    parser.add_argument("step", type=Period,
                        help="The assimilation cycle step in Vortex's Period format (e.g. PT6H for a 6 hours step).")

    # Process arguments
    args = parser.parse_args()

    dates = list(daterange(args.begin, args.end, args.step))
    times = [mpl.dates.date2num(d) for d in dates]

    def build_nparray():
        return np.ma.masked_all((len(times), 5), dtype=np.float64)

    datastack = defaultdict(build_nparray)
    with vortex.sh().ftppool():
        for i, date in enumerate(dates):
            for db, data in fetchjson(date, args).items():
                if args.only and db not in args.only:
                    continue
                datastack[db][i, 0] = convert_bytes_in_unit(data['inputsize'], 'MiB')
                datastack[db][i, 1] = convert_bytes_in_unit(data['mem_real'], 'GiB')
                datastack[db][i, 2] = data['time_real']
                datastack[db][i, 3] = max((float(data['mem_real']) - (args.memoff * 1024. * 1024.)) / data['inputsize'],
                                          0)
                datastack[db][i, 4] = max(float(data['time_real']) / convert_bytes_in_unit(data['inputsize'], 'MiB'),
                                          0)

    if args.reg:
        print('\nTIME REGRESSION')
        do_reg(datastack, idx=2, regtype=args.reg)
        print('\nMEMORY REGRESSION')
        do_reg(datastack, idx=1, regtype=args.reg, obsscale=1024., obsoffset=args.memoff)

    if len(times) > 1:
        with vortex.sh().cdcontext('plots_{0:s}_{1.ymdh}to{2.ymdh}_s{3!s}_{4:s}_memoff{5:.0f}MB'.
                                   format(args.xpid, args.begin, args.end, args.step, ('prod' if args.prod else 'assim'), args.memoff),
                                   create=True):
            do_boxplot('boxplot_{suffix:s}.png', datastack)
            do_timeseries('timeserie_{db:s}.png', datastack, times, dates)


if __name__ == "__main__":
    sys.exit(main())
