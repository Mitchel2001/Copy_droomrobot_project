**Alpha Mini Animation Test based on manufacturer documentation**
02-04 april 2025

## Context
Early test based on defined filenames in sheet shared in Droomrobot Google Drive folder.
Expanded to actions filenames found in the manufacturer demo code and deduced from filename sequencing 

## General observations so far - resuming Monday April 7

- A lot of actions from the sheet consistently didn't work, examples: 007, 009, 011, action_004, action_007

## Setup description
- VU Windows laptop
- VU Alpha Mini
- iPhone hotspot connecting both devices
- iPhone to film robot behaviour

## Test animations_test.py
Simulating interaction and attempting to loop animations while playing TTS
*Notes*
- didn't execute all animations

## Test short-ani.py
Running selected single and sequenced animations as defined in sheet shared in Droomrobot Google Drive folder
*Notes*
- didn't execute all animations

## Test seq-ani.py
Running all animations as defined in sheet shared in Droomrobot Google Drive folder
*Notes*
- didn't execute all animations

## Test 731-dance-ani.py
Sequentially plays dance actions 7 to 31
*Notes*
- exploring dance action numbers using numbers from sheet 
- observed new expressions during dances

## Test 1-6-810-dance-ani.py
Sequentially plays dance actions 1 to 6, 8 and 10 (format: dance_0001)
*Notes*
- discovered new dance actions 
- observed new expressions during dances

## Test 15sec-ani.py
Initiates timeout command of defined (dance_0001) action after 15 seconds
*Observed behaviour*
- 49s visually observed duration of complete animation: dance_0001 
- 24s visually observed stop of dance_0001 
- 10 seconds between “animation stopped at 15 seconds” in terminal and robot actually stopping dance_001



