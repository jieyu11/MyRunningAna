import os
import logging
import sys                    
from run_record import *
import matplotlib.pyplot as plt
  

def draw_xyplot(xlist, ylist, xlab, ylab, title, out, leg, legloc = 'upper right', xsize_inch = 10, ysize_inch = 8, scatter = False):
  plt.clf()
  plt.gcf().set_size_inches(xsize_inch, ysize_inch) # default 8., 6.
  if scatter:
    plt.scatter( xlist, ylist, marker='o', s = 200, c='#E3CF57', alpha=0.4) # color= #E3CF57 (banana)
    #,markeredgecolor='b', markerfacecolor='b'
  else:
    plt.plot( xlist, ylist )

  plt.ylabel( ylab )
  plt.xlabel( xlab )
  if leg is not None:
    plt.legend( leg, loc=legloc)
  plt.title( title )
  #plt.show()
  plt.savefig( out )
 
class read_fit:
  '''
    Purpose: read one running record of garmin.fit file and make a summary and a few plots of interest.
    Example: 
      rrf = read_fit( "garmin.fit" )
      if rrf.isValid() is None:
        return None
      else:
        rrf.write_summary( strOutdir )
        rrf.draw( strOutdir )
  '''

  def __init__(self, ffitname ):
    self._TotalTimePassed   = None 
    self._StartTime         = None
    self._EndTime           = None
    self._AverageAltitude   = None
    self._AssendMeters      = None
    self._DesendMeters      = None
    self._FastestKmTime     = None
    self._MinimumSpeed      = None
    self._MaximumSpeed      = None
    self._AverageSpeed      = None
    self._MinimumPaceKm     = None
    self._MaximumPaceKm     = None
    self._AveragePaceKm     = None
    self._MinimumPaceMile   = None
    self._MaximumPaceMile   = None
    self._AveragePaceMile   = None
    self._MinimumCadence    = None
    self._MaximumCadence    = None
    self._AverageCadence    = None
    self._MinimumHeartRate  = None
    self._MaximumHeartRate  = None
    self._AverageHeartRate  = None
    self._TotalDistanceMile = None
    self._TotalDistanceKm   = None

    self._time_list = [] 
    self._alti_list = [] 
    self._pace_list = [] 
    self._hart_list = [] 
    self._cade_list = [] 
    self._sped_list = [] 
    self._dist_list = [] 
 
    self._rrd = run_record( ffitname )
    if self._rrd is None:
      logging.error(" run_record() failed. Check! ")
    else:
      measured_list = self._rrd.getListMeasures()
      if "time" in measured_list:
        self._TotalTimePassed = self._rrd.getTotalTimePassed()
        self._StartTime = self._rrd.getStartTime()
        self._EndTime = self._rrd.getEndTime()
      if "altitude" in measured_list:
        self._AverageAltitude = self._rrd.getAverageAltitude()
        self._AssendMeters = self._rrd.getAssendMeters()
        self._DesendMeters = self._rrd.getDesendMeters()
      if "speed" in measured_list:
        self._FastestKmTime = self._rrd.getFastestKmTime()
        self._MinimumSpeed = self._rrd.getMinimumSpeed()
        self._MaximumSpeed = self._rrd.getMaximumSpeed()
        self._AverageSpeed = self._rrd.getAverageSpeed()
        self._MinimumPaceKm = self._rrd.getMinimumPaceKm()
        self._MaximumPaceKm = self._rrd.getMaximumPaceKm()
        self._AveragePaceKm = self._rrd.getAveragePaceKm()
        self._MinimumPaceMile = self._rrd.getMinimumPaceMile()
        self._MaximumPaceMile = self._rrd.getMaximumPaceMile()
        self._AveragePaceMile = self._rrd.getAveragePaceMile()
      if "cadence" in measured_list:
        self._MinimumCadence = self._rrd.getMinimumCadence()
        self._MaximumCadence = self._rrd.getMaximumCadence()
        self._AverageCadence = self._rrd.getAverageCadence()
      if "heart_rate" in measured_list:
        self._MinimumHeartRate = self._rrd.getMinimumHeartRate()
        self._MaximumHeartRate = self._rrd.getMaximumHeartRate()
        self._AverageHeartRate = self._rrd.getAverageHeartRate()
      if "distance" in measured_list:
        self._TotalDistanceMile = self._rrd.getTotalDistanceMile()
        self._TotalDistanceKm = self._rrd.getTotalDistanceKm()

      self._time_list = self._rrd.getElapsedMinutesList()
      self._alti_list = self._rrd.getAltitudeList()
      self._pace_list = self._rrd.getPaceKmList()
      self._hart_list = self._rrd.getHeartRateList()
      self._cade_list = self._rrd.getCadenceList()
      self._sped_list = self._rrd.getSpeedList()
      self._dist_list = self._rrd.getDistanceList()
   
  def isValid(self):
    if self._rrd is None:
      return None
    return True
    
  def write_summary(self, outdir ):
    if self._rrd is None:
      return None
  
    #
    # supported list: "altitude", "cadence", "distance", "heart_rate", "speed", "time"
    #
    measured_list = self._rrd.getListMeasures()
  
    stime = self._rrd.getStartTime()
    f = open( outdir+"/"+stime.strftime('%Y%m%d_%Hh%M') + "_summary.txt", "w")
    if "time" in measured_list:
      f.write( "Run time: %s \n" % ( stime.strftime('%Y.%m.%d at %Hh%M') ) )
      f.write( " the total time used in h:m:s is:  %s\n" % self._TotalTimePassed )
      f.write( " the starting time point in h:m:s is:  %s\n" % self._StartTime )
      f.write( " the stopping time point in h:m:s is:  %s\n" % self._EndTime )
    if "altitude" in measured_list:
      f.write( " average altitude in meters: %.1f meters. \n" %    self._AverageAltitude )
      f.write( " the number of meters assended: %.1f meters. \n" % self._AssendMeters )
      f.write( " the number of meters desended: %.1f meters. \n" % self._DesendMeters )
    if "speed" in measured_list:
      f.write( " the time of fastest 1Km in h:m:s is:  %s\n" %        self._FastestKmTime )
      f.write( " the slowest speed in: %.2f m/s.  \n" % self._MinimumSpeed )
      f.write( " the fastest speed in: %.2f m/s.  \n" % self._MaximumSpeed )
      f.write( " the average speed in: %.2f m/s.  \n" % self._AverageSpeed )
      f.write( " the slowest pace in h:m:s per Km:  %s\n" % self._MinimumPaceKm )
      f.write( " the fastest pace in h:m:s per Km:  %s\n" % self._MaximumPaceKm )
      f.write( " the average pace in h:m:s per Km:  %s\n" % self._AveragePaceKm )
      f.write( " the slowest pace in h:m:s per mile:  %s\n" % self._MinimumPaceMile )
      f.write( " the fastest pace in h:m:s per mile:  %s\n" % self._MaximumPaceMile )
      f.write( " the average pace in h:m:s per mile:  %s\n" % self._AveragePaceMile )
    if "cadence" in measured_list:
      f.write( " the minimum cadence in rpm:  %s\n" % self._MinimumCadence )
      f.write( " the maximum cadence in rpm:  %s\n" % self._MaximumCadence )
      f.write( " the average cadence in rpm:  %s\n" % self._AverageCadence )
    if "heart_rate" in measured_list:
      f.write( " the minimum heart rate in bpm :  %s\n" % self._MinimumHeartRate )
      f.write( " the maximum heart rate in bpm :  %s\n" % self._MaximumHeartRate )
      f.write( " the average heart rate in bpm :  %s\n" % self._AverageHeartRate )
    if "distance" in measured_list:
      f.write( " the total distance is: %.1f miles.  \n" % self._TotalDistanceMile )
      f.write( " the total distance is: %.1f km.  \n" % self._TotalDistanceKm )
  
    f.close()
   
 
  def draw(self, outdir):
    if self._rrd is None:
      logging.error('Instance of run_record class is not found.') 
      return None
  
    starttime = self._StartTime
  
    hmtime = starttime.strftime('%H:%M')
    mdytime = starttime.strftime('%m/%d/%Y')
    period = "Morning"
    if starttime.hour > 18 :
      period = "Evening"
    elif starttime.hour > 12 :
      period = "Afternoon"
    title_name = period + " Run at "+hmtime + " on " + mdytime
  
    outtime_tag = starttime.strftime('%Y%m%d_%Hh%M')
  
 
    #
    # supported list: "altitude", "cadence", "distance", "heart_rate", "speed", "time"
    #
    measured_list = self._rrd.getListMeasures()
  
    # 
    # Plot altitude vs time
    # 
    if "altitude" in measured_list and "time" in measured_list:
      draw_xyplot( self._time_list, self._alti_list, 
        xlab = "Elapsed Time (minutes)", ylab = "Altitude(meters)", title = title_name,
        out = outdir+"/"+outtime_tag+"_altitude_v_time.pdf", leg = None)
  
    # 
    # Plot pace vs time
    # 
    if "speed" in measured_list and "time" in measured_list:
      draw_xyplot( self._time_list, self._pace_list, 
        xlab = "Elapsed Time (minutes)", ylab = "Pace (minutes per Km)", title = title_name,
        out = outdir+"/"+outtime_tag+"_pace_v_time.pdf", leg = None)
  
    # 
    # Plot heart rate vs time
    # 
    if "heart_rate" in measured_list and "time" in measured_list:
      draw_xyplot( self._time_list, self._hart_list, 
        xlab = "Elapsed Time (minutes)", ylab = "Heart Rate (BPM)", title = title_name,
        out = outdir+"/"+outtime_tag+"_heartrate_v_time.pdf", leg = None)
  
    # 
    # Plot pace vs heart_rate
    # 
    if "heart_rate" in measured_list and "speed" in measured_list:
      draw_xyplot( self._hart_list, self._pace_list,
        xlab = "Heart Rate (BPM)", ylab = "Pace (minutes per Km)", title = title_name,
        out = outdir+"/"+outtime_tag+"_pace_v_heartrate.pdf", leg = None, scatter = True)
  
    # 
    # Plot pace vs cadence
    # 
    if "cadence" in measured_list and "speed" in measured_list:
      draw_xyplot( self._cade_list, self._pace_list,
        xlab = "Cadence (RPM)", ylab = "Pace (minutes per Km)", title = title_name,
        out = outdir+"/"+outtime_tag+"_pace_v_cadence.pdf", leg = None, scatter = True)
  
def main():
  if len(sys.argv) < 2:
    print 'Usage: ', sys.argv[0], ' [ a.fit ] [out_dir] ' 
    return 0

  if '.fit' not in sys.argv[1]:
    print 'Usage: ', sys.argv[0], ' [ a.fit ] [out_dir] ' 
    return 1

  outdir = '.'
  if len(sys.argv) >= 3:
    outdir = sys.argv[2]

  if outdir == "": outdir = "."
  elif not os.path.isdir( outdir ):
    logging.warning('Output folder: ' + outdir + ' NOT found. Create one now! ')
    os.makedirs( outdir )


  rrf = read_fit( sys.argv[1] )
  print 'Reading input: ', sys.argv[1], '.'
  if rrf.isValid() is None:
    print 'input ', sys.argv[1], ' not correct.'
    return None

  print 'Start writing summary to: ', outdir, '.'
  rrf.write_summary( outdir )

  print 'Start making plots to: ', outdir, '.'
  rrf.draw( outdir )
      

if __name__ == '__main__' : 

  main()

   

