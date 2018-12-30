## @package read_sequence
#  @author Jie Yu (jie.yu@cern.ch)
#  @date October 1, 2018
#
#  @brief Read a series of raw garmin or strava fit files and make outputs of interest. \par
#
#  @detail
#    This code makes use of a list of input .fit files and extract / calculate useful information about the runs. 
#    These output variables include total distance, average mileage per run, average cadence per run, average 
#    heart rate per run, etc. These help to see a patten in the list of runs during a longer period of time.
#

import os
import logging
import sys                    
from run_record import *
from read_sequence import *
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime
  

def draw_xyplot(xlist, ylist, xlab, ylab, title, out, leg, legloc = 'upper right', xsize_inch = 10, ysize_inch = 8, plot_type = "Normal",
                xmin = 999., xmax = 0., ymin = 999., ymax = 0.):
  '''Draw plots with data from x-axis and y-axis.

    Parameters:
    -- xlist  x-axis data in list<>.
    -- ylist  y-ayis data in list<>.
    -- xlab   x-axis label.
    -- ylab   y-ayis label.
    -- title  title of the plot.
    -- out    output name of the plot.
    -- leg    instance of a legend object.
    -- legloc location of the legend.
    -- xsize_inch number of inches in x-axis.
    -- ysize_inch number of inches in y-ayis.
    -- plot_type  "Normal":  plot()
    --            "Hist":    hist()
    --            "Scatter": scatter()
    -- xmin   minimum of x-axis
    -- xmax   maximum of x-axis
    -- ymin   minimum of y-axis
    -- ymax   maximum of y-axis
  '''

  plt.clf()
  plt.gcf().set_size_inches(xsize_inch, ysize_inch) # default 8., 6.
  if "Scatter" in plot_type:
    plt.scatter( xlist, ylist, marker='o', s = 200, c='#E3CF57', alpha=0.4) # color= #E3CF57 (banana)
    #,markeredgecolor='b', markerfacecolor='b'
  elif "Hist" in plot_type:
    plt.hist(x=xlist, bins='auto', color='#0504aa', alpha=0.5, rwidth=0.8)
  else:
    plt.plot( xlist, ylist )
  if "Datetime" in plot_type:
    plt.gcf().autofmt_xdate()

    #plt.gcf().autofmt_xdate()
    #xdate = [ datetime.strptime(d,'%m/%d/%Y').date() for d in xlist]
    #xdate = [ datetime.datetime.strftime(d,'%m/%d/%Y') for d in xlist]
    #plt.plot( xdate, ylist )

    #plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m/%d/%Y'))
    #plt.gca().xaxis.set_major_locator(mdates.DayLocator())


  if xmin < xmax:
    plt.xlim( xmin, xmax)
  if ymin < ymax:
    plt.ylim( ymin, ymax)
  plt.ylabel( ylab )
  plt.xlabel( xlab )
  if leg is not None:
    plt.legend( leg, loc=legloc)
  plt.title( title )
  #plt.show()
  plt.savefig( out )

def write_summary(seq, outdir):
  if seq.size() <= 1:
    logging.error( ' Number of runs <= 1. Return! ')
    return None

  statime = seq.getStartTime()[0]
  endtime = seq.getStartTime()[ seq.size() - 1 ]

  f = open( outdir+"/"+statime.strftime('%Y%m%d') + "_to_" +endtime.strftime('%Y%m%d') + "_summary.txt", "w")
  if "time" in seq.getMeasuredList():
    f.write( "Run time: %s to %s \n" % ( statime.strftime('%Y.%m.%d'), endtime.strftime('%Y.%m.%d') ) )
    f.write( "Number of runs: %d \n" % seq.size() )
    f.write( " the average total time elapsed in h:m:s is: %s\n" % datetime.timedelta( seconds= sum(seq.getTotalTimePassed(), datetime.timedelta()).total_seconds() / seq.size() ) )
    f.write( " the average total time moving in h:m:s is: %s\n" % datetime.timedelta( seconds= sum(seq.getTotalTimeMoving(), datetime.timedelta()).total_seconds() / seq.size() ) )
  if "altitude" in seq.getMeasuredList():
    f.write( " the average number of meters assended: %.1f meters. \n" % ( sum( seq.getAscendMeters() ) / seq.size() ) )
    f.write( " the average number of meters desended: %.1f meters. \n" % ( sum( seq.getDescendMeters() ) / seq.size() ) )
  if "speed" in seq.getMeasuredList():
    f.write( " the time of fastest 1Km in h:m:s is:  %s\n" %  min(seq.getFastestKmTime()) )
    f.write( " the slowest speed in: %.2f m/s.  \n" % min(seq.getMinimumSpeed()) )
    f.write( " the fastest speed in: %.2f m/s.  \n" % max(seq.getMaximumSpeed()) )
    f.write( " the average speed in: %.2f m/s.  \n" % (sum(seq.getAverageSpeed()) / seq.size() ) )
    f.write( " the slowest pace in h:m:s per Km:  %s\n" % max(seq.getMinimumPaceKm()) )
    f.write( " the fastest pace in h:m:s per Km:  %s\n" % min(seq.getMaximumPaceKm()) )
    f.write( " the average pace in h:m:s per Km:  %s\n" % datetime.timedelta( seconds= sum(seq.getfltAveragePaceKm()) * 60. ) ) 
    f.write( " the slowest pace in h:m:s per mile:  %s\n" % max(seq.getMinimumPaceMile() ) )
    f.write( " the fastest pace in h:m:s per mile:  %s\n" % min(seq.getMaximumPaceMile() ) )
    f.write( " the average pace in h:m:s per mile:  %s\n" % datetime.timedelta( seconds= sum(seq.getfltAveragePaceMile()) * 60. ) ) 
  if "cadence" in seq.getMeasuredList():
    f.write( " the minimum cadence in rpm:  %s\n" % min( seq.getMinimumCadence() ) )
    f.write( " the maximum cadence in rpm:  %s\n" % max( seq.getMaximumCadence() ) )
    f.write( " the best average cadence in rpm:  %s\n" % max(seq.getAverageCadence() ) )
    f.write( " the worst average cadence in rpm:  %s\n" % min(seq.getAverageCadence() ) )
    f.write( " the overall average cadence in rpm:  %s\n" % (sum(seq.getAverageCadence() ) / seq.size() ) )
  if "heart_rate" in seq.getMeasuredList():
    f.write( " the minimum heart rate in bpm :  %s\n" % min(seq.getMinimumHeartRate()) )
    f.write( " the maximum heart rate in bpm :  %s\n" % max(seq.getMaximumHeartRate()) )
    f.write( " the lowest average heart rate in bpm :  %s\n" % min(seq.getAverageHeartRate()) )
    f.write( " the highest average heart rate in bpm :  %s\n" % max(seq.getAverageHeartRate()) )
    f.write( " the overall average heart rate in bpm :  %s\n" % (sum(seq.getAverageHeartRate()) / seq.size() ) )
  if "distance" in seq.getMeasuredList():
    f.write( " the overall total distance is: %.1f miles.  \n" % (sum(seq.getTotalDistanceMile()) ) )
    f.write( " the average distance per run is: %.1f miles.  \n" % (sum(seq.getTotalDistanceMile()) / seq.size() ) )
    f.write( " the longest distance per run is: %.1f miles.  \n" % max(seq.getTotalDistanceMile()) )
    f.write( " the shortest distance per run is: %.1f miles.  \n" % min(seq.getTotalDistanceMile()) )
    f.write( " the overall total distance is: %.1f km.  \n" % (sum(seq.getTotalDistanceKm()) ) )
    f.write( " the average distance per run is: %.1f km.  \n" % (sum(seq.getTotalDistanceKm()) / seq.size() ) )
    f.write( " the longest distance per run is: %.1f km.  \n" % max(seq.getTotalDistanceKm()) )
    f.write( " the shortest distance per run is: %.1f km.  \n" % min(seq.getTotalDistanceKm()) )

  f.close()
 

def draw(seq, outdir):
  if seq.size() <= 1:
    logging.error( ' Number of runs <= 1. No plot today. Return! ')
    return None

  firsttime = seq.getStartTime()[0]
  lasttime = seq.getStartTime()[ seq.size() - 1 ]
  outtime_tag = firsttime.strftime('%Y%m%d_') + lasttime.strftime('%Y%m%d')

  if "distance" in seq.getMeasuredList():
    draw_xyplot( seq.getTotalDistanceKm(), None, xlab = "Distance per Run (Km)", ylab = "Number of Runs", title = "",
      out = outdir+"/"+outtime_tag+"_distanceKm.pdf", leg = None, plot_type = "Hist")
    draw_xyplot( seq.getTotalDistanceMile(), None, xlab = "Distance per Run (Mile)", ylab = "Number of Runs", title = "",
      out = outdir+"/"+outtime_tag+"_distanceMile.pdf", leg = None, plot_type = "Hist")

  if "distance" in seq.getMeasuredList() and "speed" in seq.getMeasuredList():
    draw_xyplot( seq.getTotalDistanceKm(), seq.getfltAveragePaceKm(), xlab = "Distance per Run (Km)", ylab = "Pace (minutes per Km)", title = "",
      out = outdir+"/"+outtime_tag+"_distanceKm_vs_pace.pdf", leg = None, plot_type = "Scatter")

  if "heart_rate" in seq.getMeasuredList():
    draw_xyplot( seq.getAverageHeartRate(), None,
      xlab = "Heart Rate (BPM)", ylab = "Number of Runs", title = "",
      out = outdir+"/"+outtime_tag+"_heartrate.pdf", leg = None, plot_type = "Hist", ymin = 100, ymax = 200)

  # 
  # Plot altitude vs time
  # 
  if "altitude" in seq.getMeasuredList() and "time" in seq.getMeasuredList():
    draw_xyplot( seq.getStartTime(), seq.getAscendMeters(), 
      xlab = "running date", ylab = "Ascend per Run (meters)", title = "",
      out = outdir+"/"+outtime_tag+"_altitude_v_date.pdf", leg = None, plot_type = "Datetime_Scatter")

  # 
  # Plot pace vs time
  # 
  if "speed" in seq.getMeasuredList() and "time" in seq.getMeasuredList():
    # seq.getAveragePaceKm is in deltatime
    #avgPaceKmFloat = [ pc.total_seconds() / 60.0 for pc in seq.getAveragePaceKm ]
    draw_xyplot( seq.getStartTime(), seq.getfltAveragePaceKm(),
      xlab = "running date", ylab = "Pace (minutes per Km)", title = "",
      out = outdir+"/"+outtime_tag+"_pace_v_date.pdf", leg = None, plot_type = "Datetime_Scatter")
    draw_xyplot( seq.getfltAveragePaceKm(), None, xlab = "Pace (minutes per Km)", ylab = "Number of Runs", title = "",
      out = outdir+"/"+outtime_tag+"_pace.pdf", leg = None, plot_type = "Hist")
 
  # 
  # Plot heart rate vs time
  # 
  if "heart_rate" in seq.getMeasuredList() and "time" in seq.getMeasuredList():
    draw_xyplot( seq.getStartTime(), seq.getAverageHeartRate(), 
      xlab = "running date", ylab = "Heart Rate (BPM)", title = "",
      out = outdir+"/"+outtime_tag+"_heartrate_v_date.pdf", leg = None, plot_type = "Datetime_Scatter", ymin = 100, ymax = 200)
    draw_xyplot( seq.getAverageHeartRate(), None, xlab = "Average Heart Rate (RPM) per Run", ylab = "Number of Runs", title = "",
      out = outdir+"/"+outtime_tag+"_heartrate.pdf", leg = None, plot_type = "Hist", xmin = 100, xmax = 200)

  # 
  # Plot pace vs heart_rate
  # 
  if "heart_rate" in seq.getMeasuredList() and "speed" in seq.getMeasuredList():
    draw_xyplot( seq.getAverageHeartRate(), seq.getfltAveragePaceKm(),
      xlab = "Heart Rate (BPM)", ylab = "Pace (minutes per Km)", title = "",
      out = outdir+"/"+outtime_tag+"_pace_v_heartrate.pdf", leg = None, plot_type = "Scatter", xmin = 100, xmax = 200)

  # 
  # Plot pace vs cadence
  # 
  if "cadence" in seq.getMeasuredList() and "speed" in seq.getMeasuredList():
    draw_xyplot( seq.getAverageCadence(), seq.getfltAveragePaceKm(),
      xlab = "Cadence (RPM)", ylab = "Pace (minutes per Km)", title = "",
      out = outdir+"/"+outtime_tag+"_pace_v_cadence.pdf", leg = None, plot_type = "Scatter", xmin = 75, xmax = 95)
  
def main():
  '''
    Example: python read_sequence.py input.txt out_dir 
    Note:    this example is tested with python version 2.7
    Argu:  input.txt contains the list of all *fit* inputs.
           out_dir   the output folder.
  '''

  if len(sys.argv) < 2:
    print 'Usage: ', sys.argv[0], ' in_dir [out_dir] ' 
    return 0

  outdir = '.'
  if len(sys.argv) >= 3:
    outdir = sys.argv[2]

  if outdir == "": outdir = "."
  elif not os.path.isdir( outdir ):
    logging.warning('Output folder: ' + outdir + ' NOT found. Create one now! ')
    os.makedirs( outdir )


  rrf = read_sequence( sys.argv[1] )
  print 'Reading input: ', sys.argv[1], '.'
  if rrf.size() <= 0:
    print 'input ', sys.argv[1], ' not correct.'
    return None

  print 'Start writing summary to: ', outdir, '!'
  write_summary(rrf, outdir )

  print 'Start making plots to: ', outdir, '.'
  draw(rrf, outdir )
      

if __name__ == '__main__' : 

  main()

   

