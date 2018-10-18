import logging                 # logging:             https://docs.python.org/3.6/howto/logging.html
import sys                     # system specific:     https://docs.python.org/3.6/library/sys.html
import time                    # Time access:         https://docs.python.org/3.6/library/time.html
from datetime import datetime, timedelta  # Date and time types: https://docs.python.org/3.6/library/datetime.html
from fitparse import FitFile

class run_record:
  '''
    Purpose: read running record of garmin.fit file and do the simple analysis to provide results about the run.

    Attributes:
        [ variable ]       [ value ]              [ type ]                    [ unit ]
      -- altitude:           303.0                (<type 'float'>)             m 
      -- cadence:            0                    (<type 'int'>  )             rpm 
      -- distance:           0.0                  (<type 'float'>)             m 
      -- enhanced_altitude:  303.0                (<type 'float'>)             m 
      -- enhanced_speed:     0.0                  (<type 'float'>)             m/s 
      -- fractional_cadence: 0.0                  (<type 'float'>)             rpm 
      -- heart_rate:         103                  (<type 'int'>  )             bpm 
      -- position_lat:       501744197            (<type 'int'>  )             semicircles 
      -- position_long:      -1116949763          (<type 'int'>  )             semicircles 
      -- speed:              0.0                  (<type 'float'>)             m/s 
      -- timestamp:          2016-11-24 00:07:12  (<type 'datetime.datetime'>) 
      -- unknown_87:         0                    (<type 'int'>) 
      -- unknown_88:         300                  (<type 'int'>) 

    Process:
      1. read garmin.fit file by calling the class rcd = run_record( "garmin.fit" ) 
      2. keep the data of _speed_, _heart_rate_, etc, into vectors
      3. calculate the interested variables, e.g. _average_speed_, total_passed_time, etc.
      4. make the interesting plots, e.g. speed_vs_time, heart_vs_time, heart_vs_time, etc.
      5. show the results by calling 

    Functions:
      -- getListMeasures():       return the list of measured variables: altitude, cadence, distance, etc.
      -- getAverageAltitude():    return average altitude in meters
      -- getAssendMeters():       return the number of meters assended
      -- getDesendMeters():       return the number of meters desended
      -- getFastestKmTime():      return the time of fastest 1Km in <timedelta>
      -- getMinimumSpeed():       return the slowest speed in m/s
      -- getMaximumSpeed():       return the fastest speed in m/s
      -- getAverageSpeed():       return the average speed in m/s
      -- getMinimumPaceKm():      return the slowest pace in <timedelta> per Km
      -- getMaximumPaceKm():      return the fastest pace in <timedelta> per Km
      -- getAveragePaceKm():      return the average pace in <timedelta> per Km
      -- getMinimumPaceMile():    return the slowest pace in <timedelta> per mile
      -- getMaximumPaceMile():    return the fastest pace in <timedelta> per mile
      -- getAveragePaceMile():    return the average pace in <timedelta> per mile
      -- getMinimumCadence():     return the minimum cadence in rpm
      -- getMaximumCadence():     return the maximum cadence in rpm
      -- getAverageCadence():     return the average cadence in rpm
      -- getMinimumHeartRate():   return the minimum heart rate in bpm 
      -- getMaximumHeartRate():   return the maximum heart rate in bpm 
      -- getAverageHeartRate():   return the average heart rate in bpm 
      -- getTotalDistanceMile():  return the total distance in mile
      -- getTotalDistanceKm():    return the total distance in Km
      -- getTotalDistanceMeter(): return the total distance in meter
      -- getTotalTimePassed():    return the total time used 
      -- getStartTime():          return the starting time point in <datetime>
      -- getEndTime():            return the stopping time point in <datetime>
      -- getAltitudeList():       return the list of altitude data in meter
      -- getCadenceList():        return the list of cadence data in rpm
      -- getDistanceList():       return the list of distance data in meter
      -- getHeartRateList():      return the list of heart rate data in bpm
      -- getSpeedList():          return the list of speed data in m/s
      -- getPaceKmList():         return the list of the pace in minutes per km
      -- getDateTimeList():       return the list of time stamps in <datetime>
      -- getElapsedTimeList():    return the list of the elapsed time in <timedelta>
      -- getElapsedMinutesList(): return the list of the elapsed minutes in <float> minutes
  '''

  _mile_in_meter = 1609.34 # number of meters in a mile

  def __init__(self, ffitname, hours_dif = timedelta(hours = -6)):
    #
    # ffitname: input file name.fit
    # hours_dif: difference of hours compared to UTC,
    #  US Central is 6 hours later, so set to -6
    # 
    self._exist_vars = [] # existing variable in the data from input file: altitude, etc
    self._altitude = [] # <float> meter
    self._cadence = []  # <int> rpm
    self._distance = [] # <float> meter
    self._heart_rate = [] # <int> bpm
    self._speed = [] # <float> m/s
    self._pacekm = [] # <float> minutes per km 
    self._timestamp = [] # <'datetime.datetime'> 
    self._elapsedtime = [] # <timedelta>
    self._elapsedminutes = [] #  <float> of minutes

    self._altitude_up = 0.
    self._altitude_down = 0.
    self._avg_altitude = 0.
    self._min_cadence = 0
    self._avg_cadence = 0
    self._max_cadence = 0
    self._min_heart_rate = 0
    self._avg_heart_rate = 0
    self._max_heart_rate = 0
    self._min_speed = 0.
    self._avg_speed = 0.
    self._max_speed = 0.
    self._passed_time = timedelta(0)
    self._fast1km_time = timedelta(0) # 1 km
    self._fast1ml_time = timedelta(0) # 1 mile
    self._total_distance = 0.;

    self._num_records = 0 # number of data points

    #
    # private functions called for calculation
    #
    self._read_fit_file( ffitname, hours_dif )
    self._calculation()

  # default is 1Km = 1000 m, use 1609.34 for mile
  def _calculatePaceFromSpeed(self, speed_m_per_s, unit=1000.):
    if speed_m_per_s <= 0.001:
      logging.warning( ' Speed is %6.3f m/s. Too slow! Skip. ' % speed_m_per_s )
      return timedelta(0)
    nsec = int( unit / speed_m_per_s )
    nminute = int( nsec / 60 )
    nsec = nsec % 60
    # return (nminute, nsec) 
    return timedelta(minutes=nminute, seconds=nsec) 


  def _read_fit_file(self, ffitname, hours_dif ):
    #
    # read in all the records associated to this run
    #
 
    fitfile = FitFile( ffitname )

    #
    # A record is a data point during the run, which records one's 
    #   position, speed, heart_rate, time and so on
    # With all the record information, one can calculate the more interesting
    #   variables during the run, like average pace, elapsed time, etc.
    #
    self._num_records = 0
    for record in fitfile.get_messages('record'):

      skip = False
      for record_data in record:
        #
        # 0.2 m / s == 0.72 Km / hour, walking or running cannot be that slow!!!!
        #
        if record_data.name == "speed" and record_data.value < 0.2:
          skip = True
          break

      if skip: continue
      self._num_records = self._num_records + 1

      # Go through all the data entries in this record
      for record_data in record:
        #if record_data.units:
        #    print " * %s: %s %s" % ( record_data.name, record_data.value, record_data.units)
        #else:
        #    print " * %s: %s" % (record_data.name, record_data.value)

 
        if record_data.name == "altitude":
          self._altitude.append( record_data.value ) #<float> meter
        elif record_data.name == "cadence": 
          self._cadence.append( record_data.value ) #<int> rpm
        elif record_data.name == "distance": 
          self._distance.append( record_data.value ) #<float> meter
        elif record_data.name == "heart_rate":
          self._heart_rate.append( record_data.value ) #<int> bpm
        elif record_data.name == "speed":
          self._speed.append( record_data.value ) #<float> meter/second
          pace_dt = self._calculatePaceFromSpeed( record_data.value )
          if pace_dt.total_seconds() < 1:
            self._pacekm.append( 15. ) # 15 minutes per Km, impossibly slow!
          #elif pace_dt.total_seconds() > 900: # if it is over 15 minutes, why???
          #  logging.warning( "Found record with pace: " + str(pace_dt.total_seconds() / 60.) + " minutes / Km. Convert to 15 minutes / Km. " )
          #  logging.warning( "Found speed: " + str(record_data.value) )
          #  self._pacekm.append( 15. ) 
          else:
            self._pacekm.append( pace_dt.total_seconds() / 60. )
        elif record_data.name == "timestamp":
          time_pos = record_data.value + hours_dif #<datetime>
          self._timestamp.append( time_pos ) #<datetime>
          dtm = time_pos - self._timestamp[0]
          self._elapsedtime.append( dtm )
          self._elapsedminutes.append( dtm.total_seconds() / 60. )
        else:
          continue

    if len( self._altitude   ) == self._num_records : self._exist_vars.append( "altitude"   )
    if len( self._cadence    ) == self._num_records : self._exist_vars.append( "cadence"    )
    if len( self._distance   ) == self._num_records : self._exist_vars.append( "distance"   )
    if len( self._heart_rate ) == self._num_records : self._exist_vars.append( "heart_rate" )
    if len( self._speed      ) == self._num_records : self._exist_vars.append( "speed"      )
    if len( self._timestamp  ) == self._num_records : self._exist_vars.append( "time"  )

      
    if self._num_records <= 0:
      logging.error( ' Input ' + ffitname + ' has no record installed. Check! ')
    else:
      logging.info( ' Input ' + ffitname + ' has ',self._num_records, ' records installed.')
    return None

  def _time_of_fastest(self, dist_set = 1000. ):
    #
    # time for fastest pace with defined distance, default of 1Km
    # use dist_set = 1609.34
    
    idx_1 = 0 # ending point
    delta_dist = 0 # distance so far recorded from idx_0
    time_min = timedelta(days=2, hours = 1) # initialize with a huge number
    if not "time" in self._exist_vars:
      return time_min 

    for idx in range( self._num_records ):
      while( idx_1 < self._num_records and self._distance[ idx_1 ] - self._distance[ idx ] < dist_set ):
        idx_1 = idx_1 + 1

      if (idx_1 >= self._num_records ): break;

      dtime = self._timestamp[ idx_1 ] - self._timestamp[ idx ]
      if ( dtime < time_min ): time_min = dtime

    if( time_min > timedelta(days=2) ):
      logging.error( ' Running distance shorter than ', dist_set, '! Cannot calculate the minimum time.')

    return time_min 
    
  def _calculation(self ):
    if self._num_records <= 0:
      logging.error( ' No record. Cannot do calculation. ')
      return None

    if "cadence" in self._exist_vars:
      self._min_cadence = min( self._cadence )
      self._avg_cadence = sum( self._cadence ) / self._num_records
      self._max_cadence = max( self._cadence ) 
    if "heart_rate" in self._exist_vars:
      self._min_heart_rate = min( self._heart_rate )
      self._avg_heart_rate = sum( self._heart_rate ) / self._num_records
      self._max_heart_rate = max( self._heart_rate ) 

    if "distance" in self._exist_vars:
      self._total_distance = self._distance[ self._num_records - 1] # in meters
    if "time" in self._exist_vars:
      self._passed_time = self._timestamp[ self._num_records - 1] - self._timestamp[0] 
    if "speed" in self._exist_vars:
      self._avg_speed = self._total_distance / self._passed_time.total_seconds()
      self._min_speed = 9999.

    for ispd in self._speed:
      if ispd < 0.1: continue
      if ispd < self._min_speed: self._min_speed = ispd
    if self._min_speed > 9998:
      logging.error( ' No minimum speed found : ', self._min_speed, ' m/s.' )
    self._max_speed = max( self._speed ) 


    self._altitude_up = 0.
    self._altitude_down = 0.
    if "altitude" in self._exist_vars:
      self._avg_altitude = sum( self._altitude ) / self._num_records
      for idx in range( self._num_records ):
        if idx == 0: continue
        if self._altitude[ idx - 1 ] < self._altitude[ idx ]:
          self._altitude_up = self._altitude_up + ( self._altitude[ idx ] - self._altitude[ idx-1 ] )
        elif self._altitude[ idx - 1 ] > self._altitude[ idx ]:
          self._altitude_down = self._altitude_down + ( self._altitude[ idx - 1 ] - self._altitude[ idx ] )

    self._fast1km_time = self._time_of_fastest()
    self._fast1ml_time = self._time_of_fastest( self._mile_in_meter )

  #############################################
  ############# Public Functions ##############
  #############################################

  def getListMeasures( self ):
    return self._exist_vars 

  def getAverageAltitude( self ):
    return self._avg_altitude

  def getAssendMeters( self ):
    return self._altitude_up

  def getDesendMeters( self ):
    return self._altitude_down

  def getFastestKmTime( self ):
    return self._fast1km_time

  def getMinimumSpeed( self ):
    return self._min_speed

  def getMaximumSpeed( self ):
    return self._max_speed

  def getAverageSpeed( self ):
    return self._avg_speed

   
  def getMinimumPaceKm( self ):
    return self._calculatePaceFromSpeed( self._min_speed ) 

  def getMaximumPaceKm( self ):
    return self._calculatePaceFromSpeed( self._max_speed ) 

  def getAveragePaceKm( self ):
    return self._calculatePaceFromSpeed( self._avg_speed ) 
    
  def getMinimumPaceMile( self ):
    return self._calculatePaceFromSpeed( self._min_speed, self._mile_in_meter ) 

  def getMaximumPaceMile( self ):
    return self._calculatePaceFromSpeed( self._max_speed, self._mile_in_meter ) 

  def getAveragePaceMile( self ):
    return self._calculatePaceFromSpeed( self._avg_speed, self._mile_in_meter ) 


  def getMinimumCadence( self ):
    return self._min_cadence

  def getMaximumCadence( self ):
    return self._max_cadence

  def getAverageCadence( self ):
    return self._avg_cadence

  def getMinimumHeartRate( self ):
    return self._min_heart_rate

  def getMaximumHeartRate( self ):
    return self._max_heart_rate

  def getAverageHeartRate( self ):
    return self._avg_heart_rate

  def getTotalDistanceMile( self ):
    return self._total_distance / self._mile_in_meter

  def getTotalDistanceKm( self ):
    return self._total_distance / 1000.

  def getTotalDistanceMeter( self ):
    return self._total_distance

  def getTotalTimePassed( self ):
    return self._passed_time

  def getStartTime( self ):
    return self._timestamp[ 0 ]

  def getEndTime( self ):
    return self._timestamp[ self._num_records - 1 ]

  def getAltitudeList( self ):
    return self._altitude

  def getCadenceList( self ):
    return self._cadence

  def getDistanceList( self ):
    return self._distance

  def getHeartRateList( self ):
    return self._heart_rate

  def getSpeedList( self ):
    return self._speed

  def getPaceKmList( self ):
    return self._pacekm

  def getDateTimeList( self ):
    return self._timestamp

  def getElapsedTimeList( self ):
    return self._elapsedtime

  def getElapsedMinutesList( self ):
    return self._elapsedminutes
