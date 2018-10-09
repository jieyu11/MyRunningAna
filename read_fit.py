import sys                    
from run_record import *

def read_file( ffitname):
  rrd = run_record( ffitname )


  print " average altitude in meters: %.1f meters." %    rrd.getAverageAltitude()
  print " the number of meters assended: %.1f meters." % rrd.getAssendMeters()
  print " the number of meters desended: %.1f meters." % rrd.getDesendMeters()
  print " the time of fastest 1Km in h:m:s is: ",        rrd.getFastestKmTime()
  print " the slowest speed in: %.2f m/s. " % rrd.getMinimumSpeed()
  print " the fastest speed in: %.2f m/s. " % rrd.getMaximumSpeed()
  print " the average speed in: %.2f m/s. " % rrd.getAverageSpeed()
  print " the slowest pace in h:m:s per Km: ", rrd.getMinimumPaceKm()
  print " the fastest pace in h:m:s per Km: ", rrd.getMaximumPaceKm()
  print " the average pace in h:m:s per Km: ", rrd.getAveragePaceKm()
  print " the slowest pace in h:m:s per mile: ", rrd.getMinimumPaceMile()
  print " the fastest pace in h:m:s per mile: ", rrd.getMaximumPaceMile()
  print " the average pace in h:m:s per mile: ", rrd.getAveragePaceMile()
  print " the minimum cadence in rpm: ", rrd.getMinimumCadence()
  print " the maximum cadence in rpm: ", rrd.getMaximumCadence()
  print " the average cadence in rpm: ", rrd.getAverageCadence()
  print " the minimum heart rate in bpm : ", rrd.getMinimumHeartRate()
  print " the maximum heart rate in bpm : ", rrd.getMaximumHeartRate()
  print " the average heart rate in bpm : ", rrd.getAverageHeartRate()
  print " the total distance is: %.1f miles. " % rrd.getTotalDistanceMile()
  print " the total distance is: %.1f km. " % rrd.getTotalDistanceKm()
  print " the total time used in h:m:s is: ", rrd.getTotalTimePassed()
  print " the starting time point in h:m:s is: ", rrd.getStartTime()
  print " the stopping time point in h:m:s is: ", rrd.getEndTime()

  
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

  read_file( sys.argv[1] )


if __name__ == '__main__' : 

  main()

   

