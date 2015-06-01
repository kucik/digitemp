#!/bin/sh

dt_path="/home/pi/scripts/digitemp/"
#lockfile="/var/www/localhost/htdocs/digitemp/logs/sensors.lock"
lockfile="${dt_path}/logs/sensors.lock"
#logfile=/var/www/localhost/htdocs/digitemp/logs/sensors.log
logfile="${dt_path}/logs/sensors.log"
ln_cut=1440
sensors=3

cd ${dt_path}/src/

######### Check temperature lock ################
#echo "Check lock"
if [ -e $lockfile ]; then
#  echo "Stats locked"
  pid=`head -n 1 $lockfile`
#  echo $pid
  if [ -n "$pid" ]; then
    if `ps -A | grep "^[ ]*$pid " > /dev/null`; then
#      echo "Locked"
      exit 0;
     else 
#      echo "Unlocking"
      rm $lockfile
    fi
  fi
fi

########3 Lock sensors ##############
pid=$$
echo $pid > $lockfile

########## Temperature check ##########
get_sensor() {
  sensor=$1
  try=$(($2 - 1))
#  temp=`/home/kucik/src/digitemp-3.6.0/digitemp_DS9097 -q -t $sensor -o"%C"`
  temp=`cat "$sensor" | tail -n 1 | sed -e 's/.*=\([0-9]\{1,2\}\)\([0-9]\{3\}\)/\1.\2/g'`
  if [ -z "$temp" ]; then
      temp=0;
  fi
  if [ "$temp" = "85.000" ]; then
    temp=0;
  fi
  if [ "$temp" = "0" -a $try -gt 0 ]; then
    temp=`get_sensor $sensor $try`
  fi
  echo "$temp"
}


dt=`date "+%Y/%m/%d %H:%M:%S"`
echo -n "$dt" >> ${logfile}.temp
sensor=0;

while read line
do
  temp=`get_sensor "$line" 3`
  eval temperatures$sensor=$temp
  echo -n " $temp"
  sensor=$(($sensor + 1))
done < ../cfg/sensors >> ${logfile}.temp
echo "" >> ${logfile}.temp # newline


#while [ $sensor -lt $sensors ]; do
#    temp=`get_sensor $sensor 3`
#    eval temperatures$sensor=$temp
#    echo -n " $temp"
#    sensor=$(($sensor + 1))
#done >> ${logfile}.temp
#echo "" >> ${logfile}.temp


#echo `date "+%Y/%m/%d %H:%M:%S"` "$sensor0 $sensor1 " >> ${logfile}.temp
tail -n $ln_cut ${logfile}.temp >  ${logfile}.minute

sensor=0;
if [ `date +%M` -eq 59 ]; then
#if [ 59 -eq 59 ]; then
#  dt=`date "+%Y/%m/%d %H:%M:%S"`
  echo -n "$dt" >> ${logfile}.hour
  while [ $sensor -lt $sensors ]; do
    col=$(($sensor + 3))
    regexp=`date "+%Y/%m/%d %H:"`  
    eval=`cat ${logfile}.minute | grep "$regexp" | cut -d ' ' -f $col | tr '\n' '+' | sed -e 's/+$//' `
    cnt=`cat ${logfile}.minute | grep "$regexp" | wc -l`
    avg=`echo " ($eval) / ($cnt.0 + 1.0)" | bc -l`
#    echo " ($eval) / ($cnt.0 + 1.0)"
    echo -n " $avg"
    sensor=$(($sensor + 1))
  done >> ${logfile}.hour
  echo "" >> ${logfile}.hour
fi 

sensor=0;
dt=`date +%H:%M`
if [ "$dt" = '23:59' ]; then
#if [ 59 -eq 59 ]; then
  dt=`date "+%Y/%m/%d %H:%M:%S"`
  echo -n "$dt" >> ${logfile}.day
  while [ $sensor -lt $sensors ]; do
    col=$(($sensor + 3))
    regexp=`date "+%Y/%m/%d "`  
    eval=`cat ${logfile}.hour | grep "$regexp" | cut -d ' ' -f $col | tr '\n' '+' | sed -e 's/+$//' `
    cnt=`cat ${logfile}.hour | grep "$regexp" | wc -l`
    avg=`echo " ($eval) / ($cnt.0 + 1.0)" | bc -l`
#    echo " ($eval) / ($cnt.0 + 1.0)"
    echo -n " $avg"
    sensor=$(($sensor + 1))
  done >> ${logfile}.day
  echo "" >> ${logfile}.day
fi

logfile=$logfile.minute
NUM_RECORDS=`cat  $logfile | wc -l`
#START_TIME=$(head -n 1 $logfile | cut -f 1,2 -d ' ' | sed -e 's/\//\\\//g');
START_TIME=$(date -d '1 day ago' "+%Y/%m/%d %H:%M:%S" | sed -e 's/\//\\\//g')
STOP_TIME=$(tail -n 1 $logfile | cut -f 1,2 -d ' ' | sed -e 's/\//\\\//g')
X_FORMAT="%H:%M"

cd ${dt_path}/logs
log="sensors.log.minute"
cat ../cfg/tempplot.conf | sed -e "s/\$logfile/$log/g" \
               | sed -e "s/\$NUM_RECORDS/$NUM_RECORDS/g" \
               | sed -e "s/\$START_TIME/$START_TIME/g" \
               | sed -e "s/\$STOP_TIME/$STOP_TIME/g" \
               | sed -e "s/\$SENSOR0/$temperatures0/g" \
               | sed -e "s/\$SENSOR1/$temperatures1/g" \
               | sed -e "s/\$SENSOR2/$temperatures2/g" \
               | sed -e "s/\$X_FORMAT/$X_FORMAT/g" \
               | sed -e "s/\$IMG_OUTPUT/sensors.log.minute.gif/g" \
               | gnuplot

logfile=`echo "$logfile" | sed -e 's/minute/hour/g'`
NUM_RECORDS=`cat  $logfile | wc -l`
#START_TIME=$(head -n 1 $logfile | cut -f 1,2 -d ' ' | sed -e 's/\//\\\//g');
START_TIME=$(date -d '1 week ago' "+%Y/%m/%d %H:%M:%S" | sed -e 's/\//\\\//g') 
STOP_TIME=$(tail -n 1 $logfile | cut -f 1,2 -d ' ' | sed -e 's/\//\\\//g')
X_FORMAT="%A"

log="sensors.log.hour"
cat ../cfg/tempplot.conf | sed -e "s/\$logfile/$log/g" \
               | sed -e "s/\$NUM_RECORDS/$NUM_RECORDS/g" \
               | sed -e "s/\$START_TIME/$START_TIME/g" \
               | sed -e "s/\$STOP_TIME/$STOP_TIME/g" \
               | sed -e "s/\$SENSOR0/$temperatures0/g" \
               | sed -e "s/\$SENSOR1/$temperatures1/g" \
               | sed -e "s/\$SENSOR2/$temperatures2/g" \
               | sed -e "s/\$X_FORMAT/$X_FORMAT/g" \
               | sed -e "s/\$IMG_OUTPUT/sensors.log.hour.gif/g" \
               | gnuplot

logfile=`echo "$logfile" | sed -e 's/minute/hour/g'`
NUM_RECORDS=`cat  $logfile | wc -l`
#START_TIME=$(head -n 1 $logfile | cut -f 1,2 -d ' ' | sed -e 's/\//\\\//g');
START_TIME=$(date -d '1 month ago' "+%Y/%m/%d %H:%M:%S" | sed -e 's/\//\\\//g')
STOP_TIME=$(tail -n 1 $logfile | cut -f 1,2 -d ' ' | sed -e 's/\//\\\//g')
X_FORMAT="%m\/%d"

log="sensors.log.hour"
cat ../cfg/tempplot.conf | sed -e "s/\$logfile/$log/g" \
               | sed -e "s/\$NUM_RECORDS/$NUM_RECORDS/g" \
               | sed -e "s/\$START_TIME/$START_TIME/g" \
               | sed -e "s/\$STOP_TIME/$STOP_TIME/g" \
               | sed -e "s/\$SENSOR0/$temperatures0/g" \
               | sed -e "s/\$SENSOR1/$temperatures1/g" \
               | sed -e "s/\$SENSOR2/$temperatures2/g" \
               | sed -e "s/\$X_FORMAT/$X_FORMAT/g" \
               | sed -e "s/\$IMG_OUTPUT/sensors.log.monthly.gif/g" \
               | gnuplot

logfile=`echo "$logfile" | sed -e 's/hour/day/g'`
NUM_RECORDS=`cat  $logfile | wc -l`
#START_TIME=$(head -n 1 $logfile | cut -f 1,2 -d ' ' | sed -e 's/\//\\\//g');
START_TIME=$(date -d '12 month ago' "+%Y/%m/%d %H:%M:%S" | sed -e 's/\//\\\//g')
STOP_TIME=$(tail -n 1 $logfile | cut -f 1,2 -d ' ' | sed -e 's/\//\\\//g')
X_FORMAT="%m\/%d"

log="sensors.log.day"
cat ../cfg/tempplot.conf | sed -e "s/\$logfile/$log/g" \
               | sed -e "s/\$NUM_RECORDS/$NUM_RECORDS/g" \
               | sed -e "s/\$START_TIME/$START_TIME/g" \
               | sed -e "s/\$STOP_TIME/$STOP_TIME/g" \
               | sed -e "s/\$SENSOR0/$temperatures0/g" \
               | sed -e "s/\$SENSOR1/$temperatures1/g" \
               | sed -e "s/\$SENSOR2/$temperatures2/g" \
               | sed -e "s/\$X_FORMAT/$X_FORMAT/g" \
               | sed -e "s/\$IMG_OUTPUT/sensors.log.year.gif/g" \
               | gnuplot

rm $lockfile

sudo cp ../img/*.gif /usr/share/nginx/www/img/ 
