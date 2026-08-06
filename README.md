# Motion Detection Alarm System

Webcam motion detector that arms on a keypress, triggers an alarm sound when sustained motion is detected, and saves a snapshot of the scene.

Built with OpenCV. Uses macOS `afplay` for audio (not Windows `winsound`).

## Requirements

- macOS
- Python 3.9+
- Webcam
- Camera permission for Terminal (or Cursor, if you run it from there)

## Setup

```bash
cd "path/to/Motion Detection Alarm System"
python3 -m pip install -r requirements.txt
```

Alarm sound file (already included):

`resources/mixkit-classic-alarm-995.wav`

## Run

```bash
python3 main.py
```

1. Allow camera access if macOS asks.
2. A **Cam** window should open.
3. Click that window so keyboard shortcuts work.
4. Press **`t`** to arm / disarm motion detection.
5. When armed, the window shows a black-and-white motion mask.
6. Sustained motion starts the alarm and saves a photo under `captures/`.
7. Press **`q`** to quit.

## Controls

| Key | Action              |
| --- | ------------------- |
| `t` | Toggle alarm mode   |
| `q` | Quit                |

## How it works

1. Capture a baseline frame from the webcam.
2. While armed, convert each new frame to grayscale, blur it, and compare it to the previous frame.
3. Large enough differences increment a motion counter.
4. When the counter stays high, the app:
   - saves a color snapshot to `captures/motion_YYYYMMDD_HHMMSS.jpg`
   - plays the alarm sound on a background thread (so the camera keeps running)

## Project layout

```text
Motion Detection Alarm System/
├── main.py
├── requirements.txt
├── README.md
├── resources/
│   └── mixkit-classic-alarm-995.wav
└── captures/          # created automatically; snapshots saved here
```

## Troubleshooting

**Camera permission error / green light blinks then exits**

- System Settings → Privacy & Security → Camera
- Enable **Terminal** or **Cursor**, then restart that app and run again

**No window appears**

- Make sure you saved `main.py` before running
- Run from the project folder so relative paths resolve correctly

**Keys do nothing**

- Click the **Cam** window first; shortcuts go to that window, not the terminal

**False alarms or not sensitive enough**

- In `main.py`, adjust:
  - `threshold` value (`25`)
  - motion sum check (`300000`)
  - `alarm_counter > 20`
