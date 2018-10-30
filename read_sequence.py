import os
import logging
import sys                    
from run_record import *
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime
  

def draw_xyplot(xlist, ylist, xlab, ylab, title, out, leg, legloc = 'upper right', xsize_inch = 10, ysize_inch = 8, plot_type = "Normal",
                xmin = 999., xmax = 0., ymin = 999., ymax = 0.):
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
 
class read_sequence:
  '''
    Purpose: read a list of files of *.fit and make a summary and a few plots of interest.
    Example: 
  '''

  def __init__(self, fit_input_name ):
    self._TheRuns           = [ ]
    self._TotalTimePassed   = [ ] 
    self._StartTime         = [ ]
    self._EndTime           = [ ]
    self._AverageAltitude   = [ ]
    self._AssendMeters      = [ ]
    self._DesendMeters      = [ ]
    self._FastestKmTime     = [ ]
    self._MinimumSpeed      = [ ]
    self._MaximumSpeed      = [ ]
    self._AverageSpeed      = [ ]
    self._MinimumPaceKm     = [ ]
    self._MaximumPaceKm     = [ ]
    self._AveragePaceKm     = [ ]
    self._fltAveragePaceKm  = [ ]
    self._MinimumPaceMile   = [ ]
    self._MaximumPaceMile   = [ ]
    self._AveragePaceMile   = [ ]
    self._fltAveragePaceMile= [ ]
    self._MinimumCadence    = [ ]
    self._MaximumCadence    = [ ]
    self._AverageCadence    = [ ]
    self._MinimumHeartRate  = [ ]
    self._MaximumHeartRate  = [ ]
    self._AverageHeartRate  = [ ]
    self._TotalDistanceMile = [ ]
    self._TotalDistanceKm   = [ ]
 
    #
    # supported list: "altitude", "cadence", "distance", "heart_rate", "speed", "time"
    #
    self._MeasuredList = [ ]

    fitfiles_list = [ ]
    #if os.path.isdir(fit_input_name) :
    #  fitfiles_list = [f for f in os.listdir(fit_input_name) if os.path.isfile(os.path.join(fit_input_name, f))]
    if os.path.isdir(fit_input_name) :
      for f in os.listdir(fit_input_name) :
        if ".fit" in f:
          fitfiles_list.append( fit_input_name + "/" + f )
        else:
          logging.warning( 'file: ' + f + ' in folder: ' + fit_input_name + ' is not a fit file.')
          continue
    else:
      # in case input is a txt file
      with open( fit_input_name ) as fp:
        cnt = 0
        # every line ends with \n, remove it
        for line in fp:
          if line[0] == '#':
            continue
          if ".fit" in line:
            fitfiles_list.append( line[:-1] )
          else:
            logging.warning( 'file: ' + line[:-1] + ' from input: ' + fit_input_name + ' is not a fit file.')
            continue
 
    for ffitname in fitfiles_list:
      _rrd = run_record( ffitname )
      if _rrd is None:
        logging.warning( ' Input ' + ffitname + ' has no record installed. Check! ')
        continue
      else:
        if len( self._MeasuredList ) <= 0:
          self._MeasuredList  = _rrd.getListMeasures()
        selected = True
        if "distance" not in self._MeasuredList or _rrd.getTotalDistanceKm() < 2.0:
          selected = False
        if "speed" not in self._MeasuredList or _rrd.getAverageSpeed() < 0.1:
          selected = False

        if not selected:
            logging.warning( ' Input %s found distance %.1f, average speed %.1f. Failed to pass selection. Skip!', ffitname, _rrd.getTotalDistanceKm(), _rrd.getAverageSpeed() )
            continue


        if "distance" in self._MeasuredList:
          self._TotalDistanceMile.append( _rrd.getTotalDistanceMile() )
          self._TotalDistanceKm.append( _rrd.getTotalDistanceKm() )
        if "time" in self._MeasuredList:
          self._TotalTimePassed.append( _rrd.getTotalTimePassed() )
          self._StartTime.append( _rrd.getStartTime() )
          self._EndTime.append( _rrd.getEndTime() )
        if "altitude" in self._MeasuredList:
          self._AverageAltitude.append( _rrd.getAverageAltitude() )
          self._AssendMeters.append( _rrd.getAssendMeters() )
          self._DesendMeters.append( _rrd.getDesendMeters() )
        if "speed" in self._MeasuredList:
          self._FastestKmTime.append( _rrd.getFastestKmTime() )
          self._MinimumSpeed.append( _rrd.getMinimumSpeed() )
          self._MaximumSpeed.append( _rrd.getMaximumSpeed() )
          self._AverageSpeed.append( _rrd.getAverageSpeed() )
          self._MinimumPaceKm.append( _rrd.getMinimumPaceKm() )
          self._MaximumPaceKm.append( _rrd.getMaximumPaceKm() )
          self._AveragePaceKm.append( _rrd.getAveragePaceKm() )
          self._fltAveragePaceKm.append( _rrd.getAveragePaceKm().total_seconds() / 60. )
          self._MinimumPaceMile.append( _rrd.getMinimumPaceMile() )
          self._MaximumPaceMile.append( _rrd.getMaximumPaceMile() )
          self._AveragePaceMile.append( _rrd.getAveragePaceMile() )
          self._fltAveragePaceMile.append( _rrd.getAveragePaceMile().total_seconds() / 60. )
        if "cadence" in self._MeasuredList:
          self._MinimumCadence.append( _rrd.getMinimumCadence() )
          self._MaximumCadence.append( _rrd.getMaximumCadence() )
          self._AverageCadence.append( _rrd.getAverageCadence() )
        if "heart_rate" in self._MeasuredList:
          self._MinimumHeartRate.append( _rrd.getMinimumHeartRate() )
          self._MaximumHeartRate.append( _rrd.getMaximumHeartRate() )
          self._AverageHeartRate.append( _rrd.getAverageHeartRate() )
        #
        # at the end, keep also the run!
        #
        self._TheRuns.append( _rrd )

    self._number_runs = len( self._TheRuns )
    logging.info( ' Number of runs loaded  ' + ffitname + ' has no record installed. Check! ')
   
  def size(self):
    return self._number_runs

  def write_summary(self, outdir ):
    if self._number_runs <= 1:
      logging.error( ' Number of runs <= 1. Return! ')
      return None
  
    statime = self._StartTime[0]
    endtime = self._StartTime[ self._number_runs - 1 ]

    f = open( outdir+"/"+statime.strftime('%Y%m%d') + "_to_" +endtime.strftime('%Y%m%d') + "_summary.txt", "w")
    if "time" in self._MeasuredList:
      f.write( "Run time: %s to %s \n" % ( statime.strftime('%Y.%m.%d'), endtime.strftime('%Y.%m.%d') ) )
      f.write( "Number of runs: %d \n " % self._number_runs )
      f.write( " the average total time used in h:m:s is: %s\n" % datetime.timedelta( seconds= sum(self._TotalTimePassed, datetime.timedelta()).total_seconds() / self._number_runs ) )
    if "altitude" in self._MeasuredList:
      f.write( " the average number of meters assended: %.1f meters. \n" % ( sum( self._AssendMeters ) / self._number_runs ) )
      f.write( " the average number of meters desended: %.1f meters. \n" % ( sum( self._DesendMeters ) / self._number_runs ) )
    if "speed" in self._MeasuredList:
      f.write( " the time of fastest 1Km in h:m:s is:  %s\n" %  min(self._FastestKmTime) )
      f.write( " the slowest speed in: %.2f m/s.  \n" % min(self._MinimumSpeed) )
      f.write( " the fastest speed in: %.2f m/s.  \n" % max(self._MaximumSpeed) )
      f.write( " the average speed in: %.2f m/s.  \n" % (sum(self._AverageSpeed) / self._number_runs ) )
      f.write( " the slowest pace in h:m:s per Km:  %s\n" % max(self._MinimumPaceKm) )
      f.write( " the fastest pace in h:m:s per Km:  %s\n" % min(self._MaximumPaceKm) )
      f.write( " the average pace in h:m:s per Km:  %s\n" % datetime.timedelta( seconds= sum(self._fltAveragePaceKm) * 60. ) ) 
      f.write( " the slowest pace in h:m:s per mile:  %s\n" % max(self._MinimumPaceMile ) )
      f.write( " the fastest pace in h:m:s per mile:  %s\n" % min(self._MaximumPaceMile ) )
      f.write( " the average pace in h:m:s per mile:  %s\n" % datetime.timedelta( seconds= sum(self._fltAveragePaceMile) * 60. ) ) 
    if "cadence" in self._MeasuredList:
      f.write( " the minimum cadence in rpm:  %s\n" % min( self._MinimumCadence ) )
      f.write( " the maximum cadence in rpm:  %s\n" % max( self._MaximumCadence ) )
      f.write( " the best average cadence in rpm:  %s\n" % max(self._AverageCadence ) )
      f.write( " the worst average cadence in rpm:  %s\n" % min(self._AverageCadence ) )
      f.write( " the overall average cadence in rpm:  %s\n" % (sum(self._AverageCadence ) / self._number_runs ) )
    if "heart_rate" in self._MeasuredList:
      f.write( " the minimum heart rate in bpm :  %s\n" % min(self._MinimumHeartRate) )
      f.write( " the maximum heart rate in bpm :  %s\n" % max(self._MaximumHeartRate) )
      f.write( " the lowest average heart rate in bpm :  %s\n" % min(self._AverageHeartRate) )
      f.write( " the highest average heart rate in bpm :  %s\n" % max(self._AverageHeartRate) )
      f.write( " the overall average heart rate in bpm :  %s\n" % (sum(self._AverageHeartRate) / self._number_runs ) )
    if "distance" in self._MeasuredList:
      f.write( " the overall total distance is: %.1f miles.  \n" % (sum(self._TotalDistanceMile) ) )
      f.write( " the average distance per run is: %.1f miles.  \n" % (sum(self._TotalDistanceMile) / self._number_runs ) )
      f.write( " the longest distance per run is: %.1f miles.  \n" % max(self._TotalDistanceMile) )
      f.write( " the shortest distance per run is: %.1f miles.  \n" % min(self._TotalDistanceMile) )
      f.write( " the overall total distance is: %.1f km.  \n" % (sum(self._TotalDistanceKm) ) )
      f.write( " the average distance per run is: %.1f km.  \n" % (sum(self._TotalDistanceKm) / self._number_runs ) )
      f.write( " the longest distance per run is: %.1f km.  \n" % max(self._TotalDistanceKm) )
      f.write( " the shortest distance per run is: %.1f km.  \n" % min(self._TotalDistanceKm) )
  
    f.close()
   
 
  def draw(self, outdir):
    if self._number_runs <= 1:
      logging.error( ' Number of runs <= 1. No plot today. Return! ')
      return None
  
    firsttime = self._StartTime[0]
    lasttime = self._StartTime[ self._number_runs - 1 ]
    outtime_tag = firsttime.strftime('%Y%m%d_') + lasttime.strftime('%Y%m%d')


    if "distance" in self._MeasuredList:
      draw_xyplot( self._TotalDistanceKm, None, xlab = "Distance per Run (Km)", ylab = "Number of Runs", title = "",
        out = outdir+"/"+outtime_tag+"_distanceKm.pdf", leg = None, plot_type = "Hist")
      draw_xyplot( self._TotalDistanceMile, None, xlab = "Distance per Run (Mile)", ylab = "Number of Runs", title = "",
        out = outdir+"/"+outtime_tag+"_distanceMile.pdf", leg = None, plot_type = "Hist")

    if "distance" in self._MeasuredList and "speed" in self._MeasuredList:
      draw_xyplot( self._TotalDistanceKm, self._fltAveragePaceKm, xlab = "Distance per Run (Km)", ylab = "Pace (minutes per Km)", title = "",
        out = outdir+"/"+outtime_tag+"_distanceKm.pdf", leg = None, plot_type = "Scatter")

    if "heart_rate" in self._MeasuredList:
      draw_xyplot( self._AverageHeartRate, None,
        xlab = "Heart Rate (BPM)", ylab = "Number of Runs", title = "",
        out = outdir+"/"+outtime_tag+"_heartrate.pdf", leg = None, plot_type = "Hist", ymin = 100, ymax = 200)
  
    # 
    # Plot altitude vs time
    # 
    if "altitude" in self._MeasuredList and "time" in self._MeasuredList:
      draw_xyplot( self._StartTime, self._AssendMeters, 
        xlab = "running date", ylab = "Ascend per Run (meters)", title = "",
        out = outdir+"/"+outtime_tag+"_altitude_v_date.pdf", leg = None, plot_type = "Datetime_Scatter")
  
    # 
    # Plot pace vs time
    # 
    if "speed" in self._MeasuredList and "time" in self._MeasuredList:
      # self._AveragePaceKm is in deltatime
      #avgPaceKmFloat = [ pc.total_seconds() / 60.0 for pc in self._AveragePaceKm ]
      draw_xyplot( self._StartTime, self._fltAveragePaceKm,
        xlab = "running date", ylab = "Pace (minutes per Km)", title = "",
        out = outdir+"/"+outtime_tag+"_pace_v_date.pdf", leg = None, plot_type = "Datetime_Scatter")
      draw_xyplot( self._fltAveragePaceKm, None, xlab = "Pace (minutes per Km)", ylab = "Number of Runs", title = "",
        out = outdir+"/"+outtime_tag+"_pace.pdf", leg = None, plot_type = "Hist")
   
    # 
    # Plot heart rate vs time
    # 
    if "heart_rate" in self._MeasuredList and "time" in self._MeasuredList:
      draw_xyplot( self._StartTime, self._AverageHeartRate, 
        xlab = "running date", ylab = "Heart Rate (BPM)", title = "",
        out = outdir+"/"+outtime_tag+"_heartrate_v_date.pdf", leg = None, plot_type = "Datetime_Scatter", ymin = 100, ymax = 200)
      draw_xyplot( self._AverageHeartRate, None, xlab = "Average Heart Rate (RPM) per Run", ylab = "Number of Runs", title = "",
        out = outdir+"/"+outtime_tag+"_heartrate.pdf", leg = None, plot_type = "Hist", xmin = 100, xmax = 200)
  
    # 
    # Plot pace vs heart_rate
    # 
    if "heart_rate" in self._MeasuredList and "speed" in self._MeasuredList:
      draw_xyplot( self._AverageHeartRate, self._fltAveragePaceKm,
        xlab = "Heart Rate (BPM)", ylab = "Pace (minutes per Km)", title = "",
        out = outdir+"/"+outtime_tag+"_pace_v_heartrate.pdf", leg = None, plot_type = "Scatter", xmin = 100, xmax = 200)
  
    # 
    # Plot pace vs cadence
    # 
    if "cadence" in self._MeasuredList and "speed" in self._MeasuredList:
      draw_xyplot( self._AverageCadence, self._fltAveragePaceKm,
        xlab = "Cadence (RPM)", ylab = "Pace (minutes per Km)", title = "",
        out = outdir+"/"+outtime_tag+"_pace_v_cadence.pdf", leg = None, plot_type = "Scatter", xmin = 70, xmax = 110)
  
def main():
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
  rrf.write_summary( outdir )

  print 'Start making plots to: ', outdir, '.'
  rrf.draw( outdir )
      

if __name__ == '__main__' : 

  main()

   

