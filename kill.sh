#!/usr/bin/env bash
kill $(ps aux | grep ww_robot)
kill $(ps aux | grep timebot.py)