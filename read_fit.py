import logging                 # logging:             https://docs.python.org/3.6/howto/logging.html
import sys                    
from run_record import *
import matplotlib.pyplot as plt

def read_file( ffitname):
  rrd = run_record( ffitname )
  if rrd is None:
    logging.error(" run_record() failed. Check! ")
    return None

  stime = rrd.getStartTime()
  f = open( stime.strftime('%Y%m%d_%Hh%M') + "_summary.txt", "w")
  f.write( "Run time: %s \n" % ( stime.strftime('%Y.%m.%d at %Hh%M') ) )
  f.write( " average altitude in meters: %.1f meters. \n" %    rrd.getAverageAltitude() )
  f.write( " the number of meters assended: %.1f meters. \n" % rrd.getAssendMeters() )
  f.write( " the number of meters desended: %.1f meters. \n" % rrd.getDesendMeters() )
  f.write( " the time of fastest 1Km in h:m:s is:  %s\n" %        rrd.getFastestKmTime() )
  f.write( " the slowest speed in: %.2f m/s.  \n" % rrd.getMinimumSpeed() )
  f.write( " the fastest speed in: %.2f m/s.  \n" % rrd.getMaximumSpeed() )
  f.write( " the average speed in: %.2f m/s.  \n" % rrd.getAverageSpeed() )
  f.write( " the slowest pace in h:m:s per Km:  %s\n" % rrd.getMinimumPaceKm() )
  f.write( " the fastest pace in h:m:s per Km:  %s\n" % rrd.getMaximumPaceKm() )
  f.write( " the average pace in h:m:s per Km:  %s\n" % rrd.getAveragePaceKm() )
  f.write( " the slowest pace in h:m:s per mile:  %s\n" % rrd.getMinimumPaceMile() )
  f.write( " the fastest pace in h:m:s per mile:  %s\n" % rrd.getMaximumPaceMile() )
  f.write( " the average pace in h:m:s per mile:  %s\n" % rrd.getAveragePaceMile() )
  f.write( " the minimum cadence in rpm:  %s\n" % rrd.getMinimumCadence() )
  f.write( " the maximum cadence in rpm:  %s\n" % rrd.getMaximumCadence() )
  f.write( " the average cadence in rpm:  %s\n" % rrd.getAverageCadence() )
  f.write( " the minimum heart rate in bpm :  %s\n" % rrd.getMinimumHeartRate() )
  f.write( " the maximum heart rate in bpm :  %s\n" % rrd.getMaximumHeartRate() )
  f.write( " the average heart rate in bpm :  %s\n" % rrd.getAverageHeartRate() )
  f.write( " the total distance is: %.1f miles.  \n" % rrd.getTotalDistanceMile() )
  f.write( " the total distance is: %.1f km.  \n" % rrd.getTotalDistanceKm() )
  f.write( " the total time used in h:m:s is:  %s\n" % rrd.getTotalTimePassed() )
  f.write( " the starting time point in h:m:s is:  %s\n" % rrd.getStartTime() )
  f.write( " the stopping time point in h:m:s is:  %s\n" % rrd.getEndTime() )

  f.close()
  
  return rrd


def draw_xyplot( xlist, ylist, xlab, ylab, title, out, leg, legloc = 'upper right', xsize_inch = 10, ysize_inch = 8, scatter = False):
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

def draw( rrd ):
  if rrd is None:
    logging.error('Instance of run_record class is not found.') 
    return None
  starttime = rrd.getStartTime()

  hmtime = starttime.strftime('%H:%M')
  mdytime = starttime.strftime('%m/%d/%Y')
  period = "Morning"
  if starttime.hour > 18 :
    period = "Evening"
  elif starttime.hour > 12 :
    period = "Afternoon"
  title_name = period + " Run at "+hmtime + " on " + mdytime

  outtime_tag = starttime.strftime('%Y%m%d_%Hh%M')

  time_list = rrd.getElapsedMinutesList()
  alti_list = rrd.getAltitudeList()
  pace_list = rrd.getPaceKmList()
  hart_list = rrd.getHeartRateList()
  cade_list = rrd.getCadenceList()
  sped_list = rrd.getSpeedList()
  dist_list = rrd.getDistanceList()

  # 
  # Plot altitude vs time
  # 
  draw_xyplot( time_list, alti_list, 
    xlab = "Elapsed Time (minutes)", ylab = "Altitude(meters)", title = title_name,
    out = outtime_tag+"_altitude_v_time.pdf", leg = None)

  # 
  # Plot pace vs time
  # 
  draw_xyplot( time_list, pace_list, 
    xlab = "Elapsed Time (minutes)", ylab = "Pace (minutes per Km)", title = title_name,
    out = outtime_tag+"_altitude_v_pace.pdf", leg = None)

  # 
  # Plot heart rate vs time
  # 
  draw_xyplot( time_list, hart_list, 
    xlab = "Elapsed Time (minutes)", ylab = "Heart Rate (BPM)", title = title_name,
    out = outtime_tag+"_altitude_v_heartrate.pdf", leg = None)

  # 
  # Plot pace vs heart_rate
  # 
  draw_xyplot( hart_list, pace_list,
    xlab = "Heart Rate (BPM)", ylab = "Pace (minutes per Km)", title = title_name,
    out = outtime_tag+"_heartrate_v_pace.pdf", leg = None, scatter = True)

  # 
  # Plot pace vs cadence
  # 
  draw_xyplot( cade_list, pace_list,
    xlab = "Cadence (RPM)", ylab = "Pace (minutes per Km)", title = title_name,
    out = outtime_tag+"_cadence_v_pace.pdf", leg = None, scatter = True)

def main():
  if len(sys.argv) < 2:
    print 'Usage: ', sys.argv[0], ' [ a.fit ] [outname.txt] ' 
    return 0

  if '.fit' not in sys.argv[1]:
    print 'Usage: ', sys.argv[0], ' [ a.fit ] [outname.txt] ' 
    return 1

  outname = 'out.txt'
  if len(sys.argv) >= 3:
    outname = sys.argv[2]

  rrd = read_file( sys.argv[1] )
  if rrd is not None:
    draw( rrd )
    

if __name__ == '__main__' : 

  main()

   

