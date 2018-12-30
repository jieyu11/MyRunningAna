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
import datetime
  
class read_sequence:
  '''Document for class read_sequence

    Purpose: read a list of files of *.fit and calculate a few fun properties including:
      * The average pace during each run
      * The distance during each run
      * The average heart-rate during each run
      * The average cadence during each run
  '''

  def __init__(self, fit_input_name ):
    '''Constructor of class read_sequence.
      Parameter fit_input_name
    '''
    self._TheRuns           = [ ]
    self._TotalTimePassed   = [ ] 
    self._TotalTimeMoving   = [ ] 
    self._StartTime         = [ ]
    self._EndTime           = [ ]
    self._AverageAltitude   = [ ]
    self._AscendMeters      = [ ]
    self._DescendMeters     = [ ]
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
          self._TotalTimeMoving.append( _rrd.getTotalTimeMoving() )
          self._StartTime.append( _rrd.getStartTime() )
          self._EndTime.append( _rrd.getEndTime() )
        if "altitude" in self._MeasuredList:
          self._AverageAltitude.append( _rrd.getAverageAltitude() )
          self._AscendMeters.append( _rrd.getAscendMeters() )
          self._DescendMeters.append( _rrd.getDescendMeters() )
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

  def getTheRuns(self):
    ''' Return the list of instances for each run_record '''
    return self._TheRuns           

  def getMeasuredList(self):
    ''' Return the list of measured variables: 
        altitude, cadence, distance, heart_rate, speed, time  
    '''
    return self._MeasuredList

  def getTotalTimePassed(self):
    ''' Return the list of total time passed for each run '''
    return self._TotalTimePassed    

  def getTotalTimeMoving(self):
    ''' Return the list of total time while moving for each run '''
    return self._TotalTimeMoving

  def getStartTime(self):
    ''' Return the list of starting time for each run '''
    return self._StartTime

  def getEndTime(self):
    ''' Return the list of ending time for each run '''
    return self._EndTime

  def getAverageAltitude(self):
    ''' Return the list of average altitude for each run '''
    return self._AverageAltitude

  def getAscendMeters(self):
    ''' Return the list of ascended distance in meters for each run '''
    return self._AscendMeters

  def getDescendMeters(self):
    ''' Return the list of descended distance in meters for each run '''
    return self._DescendMeters

  def getFastestKmTime(self):
    ''' Return the list of fastest 1Km time in timedelta for each run '''
    return self._FastestKmTime

  def getMinimumSpeed(self):
    ''' Return the list of lowest speed in m/s for each run '''
    return self._MinimumSpeed

  def getMaximumSpeed(self):
    ''' Return the list of highest speed in m/s for each run '''
    return self._MaximumSpeed

  def getAverageSpeed(self):
    ''' Return the list of average speed in m/s for each run '''
    return self._AverageSpeed      

  def getMinimumPaceKm(self):
    ''' Return the list of lowest pace in timedelta per Km for each run '''
    return self._MinimumPaceKm

  def getMaximumPaceKm(self):
    ''' Return the list of highest pace in timedelta per Km for each run '''
    return self._MaximumPaceKm

  def getAveragePaceKm(self):
    ''' Return the list of average pace in timedelta per Km for each run '''
    return self._AveragePaceKm

  def getfltAveragePaceKm (self):
    ''' Return the list of average pace in minutes/Km for each run '''
    return self._fltAveragePaceKm

  def getMinimumPaceMile(self):
    ''' Return the list of lowest pace in timedelta per mile for each run '''
    return self._MinimumPaceMile   

  def getMaximumPaceMile(self):
    ''' Return the list of highest pace in timedelta per mile for each run '''
    return self._MaximumPaceMile   

  def getAveragePaceMile(self):
    ''' Return the list of average pace in timedelta per mile for each run '''
    return self._AveragePaceMile   

  def getfltAveragePaceMile(self):
    ''' Return the list of average pace in minutes/mile for each run '''
    return self._fltAveragePaceMile

  def getMinimumCadence(self):
    ''' Return the list of minimum cadence while moving for each run '''
    return self._MinimumCadence

  def getMaximumCadence(self):
    ''' Return the list of maximum cadence while moving for each run '''
    return self._MaximumCadence

  def getAverageCadence(self):
    ''' Return the list of average cadence while moving for each run '''
    return self._AverageCadence

  def getMinimumHeartRate(self):
    ''' Return the list of minimum heart rate while moving for each run '''
    return self._MinimumHeartRate

  def getMaximumHeartRate(self):
    ''' Return the list of maximum heart rate while moving for each run '''
    return self._MaximumHeartRate  

  def getAverageHeartRate(self):
    ''' Return the list of average heart rate while moving for each run '''
    return self._AverageHeartRate

  def getTotalDistanceMile(self):
    ''' Return the list of total distance in miles for each run '''
    return self._TotalDistanceMile 

  def getTotalDistanceKm(self):
    ''' Return the list of total distance in Km for each run '''
    return self._TotalDistanceKm   
  
def main():
  '''
    Example: python read_sequence.py input.txt 
    Note:    this example is tested with python version 2.7
    Argu:  input.txt contains the list of all *fit* inputs.
  '''

  if len(sys.argv) < 1:
    print 'Usage: ', sys.argv[0], ' in_dir' 
    return 0

  rrf = read_sequence( sys.argv[1] )
  print 'Reading input: ', sys.argv[1], '. Number of runs: %d ' % rrf.size()
  if rrf.size() <= 0:
    print 'input ', sys.argv[1], ' not correct.'
    return None

if __name__ == '__main__' : 

  main()

   

