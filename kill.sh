#!/usr/bin/env bash
kill $(ps aux | grep ww_robot.py)
kill $(ps aux | grep timebot.py)