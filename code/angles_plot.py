import os
import numpy
import utilrsw

axis = 'z'
run = f'{axis}-delta=1days_20100101-20150101'

in_file = os.path.join('data','angles', f'{run}.pkl')
out_dir = os.path.join('figures', 'angles', run)


def fig_prep():
  from matplotlib import pyplot as plt
  gs = plt.gcf().add_gridspec(3, hspace=0.07)
  axes = gs.subplots(sharex=True)
  return axes


def plot(df, tranform_str):

  from matplotlib.dates import DateFormatter, YearLocator
  from matplotlib.ticker import MultipleLocator

  fontsize = 22

  line_map = {
    'geopack_08_dp': ['black', '-'],
    'spacepy': ['blue', '-'],
    'spacepy-irbem': ['blue', '--'],
    'spiceypy1': ['red', '-'],
    'spiceypy2': ['red', '--'],
    'sunpy': ['orange', '-'],
    'pyspedas': ['green', '-'],
    'sscweb': ['purple', '-'],
    'cxform': ['brown', '-'],
    '|max-min|': ['black', '-']
  }

  axes = fig_prep()

  lib = 'geopack_08_dp'
  kwargs = {
    'label': lib,
    'color': line_map[lib][0],
    'linestyle': line_map[lib][1]
  }
  # Plot and adjust y-limits and major ticks for axes[0]
  y0 = df['values'][lib].min()
  y1 = df['values'][lib].max()
  # Choose a reasonable major tick interval (auto or fixed)
  from matplotlib.ticker import MaxNLocator
  axes[0].plot(df['values'].index, df['values'][lib], **kwargs)
  axes[0].grid(True)
  axes[0].set_ylabel(f"{tranform_str} [deg]", fontsize=fontsize)
  # Use MaxNLocator to get nice ticks that enclose the data
  locator0 = MaxNLocator(nbins='auto', prune=None)
  axes[0].yaxis.set_major_locator(locator0)
  axes[0].legend(handlelength=1.0, fontsize=fontsize)

  # Plot and adjust y-limits and major ticks for axes[1]
  y1_min = df['diffs'].min(axis=1).min()
  y1_max = df['diffs'].max(axis=1).max()
  for column in df['diffs'].columns:
    if column == '|max-min|':
      continue

    stat = utilrsw.mpl.format_exponent(numpy.mean(numpy.abs(df['diffs'][column])), 0)
    label = f"{column} (${stat}$)"
    kwargs = {
      'label': label,
      'color': line_map[column][0],
      'linestyle': line_map[column][1]
    }
    axes[1].plot(df['diffs'].index, df['diffs'][column], **kwargs)

  #locator1 = MaxNLocator(nbins='auto', prune=None)
  #axes[1].yaxis.set_major_locator(locator1)

  axes[1].grid(True)
  axes[1].set_ylabel('$\\Delta$ [deg]', fontsize=fontsize)

  # Add zero line to the difference subplot
  axes[1].axhline(0, color='black', linestyle='-', linewidth=1, zorder=0)

  # Force symmetric y-limits for the difference subplot
  yl = axes[1].get_ylim()
  ymax = abs(max(yl, key=abs))
  axes[1].set_ylim(-ymax, ymax)

  # Set y-axis major tick increment to 0.01 for the difference subplot
  axes[1].grid(which='minor', axis='y', linestyle=':', linewidth=0.5)
  #axes[1].yaxis.set_minor_locator(MultipleLocator(0.01))
  axes[1].legend(ncols=2, fontsize=fontsize, columnspacing=0.65, handlelength=1.0, loc='upper center')

  # Plot and adjust y-limits and major ticks for axes[2]
  kwargs = {
    #'label': '|max-min|',
    'color': line_map['|max-min|'][0],
    'linestyle': line_map['|max-min|'][1]
  }
  axes[2].plot(df['diffs'].index, df['diffs']['|max-min|'], **kwargs)
  y2 = df['diffs']['|max-min|']

  axes[2].grid(True)
  axes[2].set_ylabel('|max-min| [deg]', fontsize=fontsize)
  axes[2].set_xlabel('Year', fontsize=fontsize)
  axes[2].xaxis.set_major_locator(YearLocator())
  axes[2].xaxis.set_major_formatter(DateFormatter('%Y'))
  yticks = axes[2].get_yticks()
  ytick_delta = yticks[1] - yticks[0]
  axes[2].set_ylim(axes[2].get_ylim()[0] - 0.1*ytick_delta, axes[2].get_ylim()[1])

  min_date = df['values'].index.min()
  max_date = df['values'].index.max() + numpy.timedelta64(1, 'D')

  for ax in axes:
    # Prevent offset notation on y-axis (e.g., 2.01e4)
    ax.get_yaxis().get_major_formatter().set_useOffset(False)
    # Remove short tick lines next to axis numbers
    ax.tick_params(axis='x', length=0)
    ax.tick_params(axis='y', which='minor', length=0)
    ax.tick_params(axis='y', length=0)
    ax.spines['bottom'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.set_xlim(min_date, max_date)

    if False:
      yticks = ax.get_yticks()
      ytick_delta = ax.get_yticks()[1] - ax.get_yticks()[0]
      ax.set_yticks(numpy.arange(yticks[0], yticks[-1], ytick_delta))
      print(yticks)
      all_y = numpy.concatenate([line.get_ydata() for line in ax.get_lines()])
      min_y = all_y.min()
      max_y = all_y.max()
      print(min_y, max_y)
      # If no data below second tick label, remove that tick label
      if min_y > yticks[1]:
        print(f"Removing y-tick {yticks[1]} for {ax} since min_y={min_y} > {yticks[1]}")
        ax.set_yticks(yticks[1:])
      continue
    if False:
      # Now set y-limits after legend adjustment
      if ax == axes[0]:
        ax.set_ylim(locator0.tick_values(y0, y1)[0], locator0.tick_values(y0, y1)[-1])
      elif ax == axes[1]:
        ax.set_ylim(locator1.tick_values(y1_min, y1_max)[0], locator1.tick_values(y1_min, y1_max)[-1])
      elif ax == axes[2]:
        ax.set_ylim(locator2.tick_values(y2.min(), y2.max())[0], locator2.tick_values(y2.min(), y2.max())[-1])
    utilrsw.mpl.adjust_legend(ax)

  fig = axes[0].get_figure()
  fig.align_ylabels()


utilrsw.mpl.plt_config()
data = utilrsw.read(in_file)

for transform_key in list(data.keys()):
  df = data[transform_key]
  frames = transform_key.split('_')
  frame1 = frames[0]
  frame2 = frames[1]
  axis = axis.upper()
  pair = f"(${axis}_{{{frame1}}}$, ${axis}_{{{frame2}}}$)"
  tranform_str = fr"$\angle$ {pair}"

  plot(df, tranform_str)
  #from matplotlib import pyplot as plt
  #plt.savefig('a.png')
  utilrsw.mpl.savefig(f'{transform_key}', fdir=out_dir, subdirs=['svg', 'png'], bbox_inches=None)
