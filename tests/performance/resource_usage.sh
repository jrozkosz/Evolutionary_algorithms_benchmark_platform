#!/bin/bash

monitored_pids=()

while true; do
  pids=$(pgrep firecracker)

  for pid in $pids; do
    if [[ ! " ${monitored_pids[@]} " =~ " ${pid} " ]]; then
      monitored_pids+=("$pid")

      # RAM
      free_ram=$(free -h | grep Mem | awk '{print $4}')

      # CPU (średnie obciążenie systemu w ciągu 1 minuty)
      cpu_load=$(uptime | awk -F'[a-z]:' '{ print $2 }' | awk '{print $1}')

      # dysk
      free_disk=$(df --output=avail -m / | tail -1)

      echo "$(date), New Firecracker PID: $pid, Free RAM: $free_ram, CPU Load (1m avg): $cpu_load, Free Disk Space: $free_disk" >> resource_usage.csv
    fi
  done

  sleep 5
done
