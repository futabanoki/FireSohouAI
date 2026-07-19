#!/usr/bin/env python3
"""
FireSohouAI Raspberry Pi video capture script.

Example:
    python3 capture_video.py \
        --role no1 \
        --session 1 \
        --take 1 \
        --camera cam01

Stop recording:
    Ctrl+C
"""

from __future__ import annotations

import argparse
import json
import re
import signal
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Any

from picamera2 import Picamera2
from picamera2.encoders import H264Encoder
from picamera2.outputs import FfmpegOutput


VALID_ROLES = (
    "commander",
    "no1",
    "no2",
    "no3",
    "team",
    "equipment",
    "test",
)

DEFAULT_WIDTH = 1920
DEFAULT_HEIGHT = 1080
DEFAULT_FPS = 30
DEFAULT_BITRATE = 10_000_000
DEFAULT_OUTPUT_DIR = Path("recordings/raw")


class RecordingStopRequested(Exception):
    """Raised when the user requests recording termination."""


def positive_integer(value: str) -> int:
    """Validate a positive integer command-line argument."""
    try:
        number = int(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError(
            f"整数を指定してください: {value}"
        ) from exc

    if number < 1:
        raise argparse.ArgumentTypeError(
            f"1以上の整数を指定してください: {value}"
        )

    return number


def valid_camera_id(value: str) -> str:
    """Validate the camera ID, such as cam01."""
    if not re.fullmatch(r"cam\d{2}", value):
        raise argparse.ArgumentTypeError(
            "カメラIDは cam01 のような形式で指定してください。"
        )

    return value


def parse_arguments() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="FireSohouAI用の動画撮影スクリプト"
    )

    parser.add_argument(
        "--role",
        required=True,
        choices=VALID_ROLES,
        help="解析対象の役割",
    )

    parser.add_argument(
        "--session",
        required=True,
        type=positive_integer,
        help="セッション番号",
    )

    parser.add_argument(
        "--take",
        required=True,
        type=positive_integer,
        help="テイク番号",
    )

    parser.add_argument(
        "--camera",
        default="cam01",
        type=valid_camera_id,
        help="カメラID。初期値: cam01",
    )

    parser.add_argument(
        "--output-dir",
        type=Path,
        default=DEFAULT_OUTPUT_DIR,
        help="動画保存先",
    )

    parser.add_argument(
        "--width",
        type=positive_integer,
        default=DEFAULT_WIDTH,
        help=f"動画幅。初期値: {DEFAULT_WIDTH}",
    )

    parser.add_argument(
        "--height",
        type=positive_integer,
        default=DEFAULT_HEIGHT,
        help=f"動画高さ。初期値: {DEFAULT_HEIGHT}",
    )

    parser.add_argument(
        "--fps",
        type=positive_integer,
        default=DEFAULT_FPS,
        help=f"フレームレート。初期値: {DEFAULT_FPS}",
    )

    parser.add_argument(
        "--bitrate",
        type=positive_integer,
        default=DEFAULT_BITRATE,
        help=f"H.264ビットレート。初期値: {DEFAULT_BITRATE}",
    )

    parser.add_argument(
        "--duration",
        type=positive_integer,
        default=None,
        help="録画時間（秒）。省略時はCtrl+Cまで録画",
    )

    parser.add_argument(
        "--camera-height",
        type=float,
        default=None,
        help="カメラ高さ（メートル）",
    )

    parser.add_argument(
        "--camera-distance",
        type=float,
        default=None,
        help="対象までの距離（メートル）",
    )

    parser.add_argument(
        "--camera-angle",
        type=float,
        default=None,
        help="対象進行方向に対するカメラ角度（度）",
    )

    parser.add_argument(
        "--weather",
        default="unknown",
        help="天候。例: sunny, cloudy, rain",
    )

    parser.add_argument(
        "--notes",
        default="",
        help="撮影時の備考",
    )

    return parser.parse_args()


def create_base_name(
    recording_date: str,
    role: str,
    session: int,
    take: int,
    camera: str,
) -> str:
    """Create a file base name using the Version 0.1 naming rules."""
    if session > 99:
        raise ValueError("セッション番号はVersion 0.1では99以下です。")

    if take > 99:
        raise ValueError("テイク番号はVersion 0.1では99以下です。")

    return (
        f"{recording_date}_{role}_"
        f"s{session:02d}_t{take:02d}_{camera}"
    )


def ensure_paths_available(
    video_path: Path,
    metadata_path: Path,
) -> None:
    """Prevent accidental overwriting of existing files."""
    existing_files = [
        path for path in (video_path, metadata_path) if path.exists()
    ]

    if existing_files:
        formatted_paths = "\n".join(
            f"  - {path}" for path in existing_files
        )

        raise FileExistsError(
            "同名ファイルがすでに存在します。\n"
            "テイク番号などを変更してください。\n"
            f"{formatted_paths}"
        )


def write_metadata(
    metadata_path: Path,
    metadata: dict[str, Any],
) -> None:
    """Write recording metadata as UTF-8 JSON."""
    with metadata_path.open("w", encoding="utf-8") as file:
        json.dump(
            metadata,
            file,
            ensure_ascii=False,
            indent=2,
        )

        file.write("\n")


def signal_handler(
    signum: int,
    frame: object,
) -> None:
    """Convert Ctrl+C and termination signals to a controlled stop."""
    del signum, frame
    raise RecordingStopRequested


def main() -> int:
    args = parse_arguments()

    recording_start = datetime.now().astimezone()
    recording_date = recording_start.strftime("%Y%m%d")

    base_name = create_base_name(
        recording_date=recording_date,
        role=args.role,
        session=args.session,
        take=args.take,
        camera=args.camera,
    )

    output_dir: Path = args.output_dir.expanduser().resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    video_path = output_dir / f"{base_name}.mp4"
    metadata_path = output_dir / f"{base_name}.json"

    try:
        ensure_paths_available(
            video_path=video_path,
            metadata_path=metadata_path,
        )
    except FileExistsError as exc:
        print(f"\nエラー: {exc}", file=sys.stderr)
        return 1

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    picam2: Picamera2 | None = None
    recording_started = False
    recording_status = "completed"
    error_message = ""
    monotonic_start: float | None = None

    try:
        print("カメラを初期化しています...")

        picam2 = Picamera2()

        video_configuration = picam2.create_video_configuration(
            main={
                "size": (args.width, args.height),
                "format": "YUV420",
            },
            controls={
                "FrameRate": args.fps,
            },
            buffer_count=6,
        )

        picam2.configure(video_configuration)

        encoder = H264Encoder(
            bitrate=args.bitrate,
        )

        output = FfmpegOutput(
            str(video_path),
        )

        print()
        print("録画設定")
        print(f"  保存先       : {video_path}")
        print(f"  対象役割     : {args.role}")
        print(f"  セッション   : {args.session:02d}")
        print(f"  テイク       : {args.take:02d}")
        print(f"  カメラ       : {args.camera}")
        print(f"  解像度       : {args.width}x{args.height}")
        print(f"  FPS          : {args.fps}")
        print(f"  ビットレート : {args.bitrate}")
        print()

        if args.duration is None:
            print("録画を開始します。停止するにはCtrl+Cを押してください。")
        else:
            print(f"{args.duration}秒間録画します。")

        picam2.start_recording(
            encoder,
            output,
        )

        recording_started = True
        monotonic_start = time.monotonic()

        if args.duration is None:
            while True:
                time.sleep(1)
        else:
            recording_end_target = (
                monotonic_start + args.duration
            )

            while time.monotonic() < recording_end_target:
                time.sleep(0.2)

    except RecordingStopRequested:
        print("\n停止要求を受け付けました。")

    except KeyboardInterrupt:
        print("\nCtrl+Cを受け付けました。")

    except Exception as exc:
        recording_status = "failed"
        error_message = str(exc)

        print(
            f"\n撮影中にエラーが発生しました: {exc}",
            file=sys.stderr,
        )

    finally:
        if picam2 is not None:
            if recording_started:
                try:
                    print("録画ファイルを終了処理しています...")
                    picam2.stop_recording()
                except Exception as exc:
                    recording_status = "failed"

                    if error_message:
                        error_message += f"; stop error: {exc}"
                    else:
                        error_message = f"stop error: {exc}"

                    print(
                        f"録画停止処理でエラーが発生しました: {exc}",
                        file=sys.stderr,
                    )

            try:
                picam2.close()
            except Exception as exc:
                print(
                    f"カメラ終了処理で警告が発生しました: {exc}",
                    file=sys.stderr,
                )

    recording_end = datetime.now().astimezone()

    if monotonic_start is None:
        duration_seconds = 0.0
    else:
        duration_seconds = round(
            time.monotonic() - monotonic_start,
            3,
        )

    if recording_status == "completed" and not video_path.exists():
        recording_status = "failed"
        error_message = "録画ファイルが生成されませんでした。"

    metadata: dict[str, Any] = {
        "schema_version": "0.1.0",
        "file_name": video_path.name,
        "metadata_file_name": metadata_path.name,
        "recording_date": recording_start.date().isoformat(),
        "recording_start": recording_start.isoformat(),
        "recording_end": recording_end.isoformat(),
        "duration_seconds": duration_seconds,
        "role": args.role,
        "session": args.session,
        "take": args.take,
        "camera_id": args.camera,
        "recording_type": "practice",
        "resolution": {
            "width": args.width,
            "height": args.height,
        },
        "fps": args.fps,
        "codec": "H.264",
        "container": "MP4",
        "bitrate_bps": args.bitrate,
        "camera_height_m": args.camera_height,
        "camera_distance_m": args.camera_distance,
        "camera_angle_deg": args.camera_angle,
        "weather": args.weather,
        "notes": args.notes,
        "status": recording_status,
        "error": error_message,
    }

    try:
        write_metadata(
            metadata_path=metadata_path,
            metadata=metadata,
        )
    except OSError as exc:
        print(
            f"メタデータを保存できませんでした: {exc}",
            file=sys.stderr,
        )
        return 1

    print()
    print("録画処理が終了しました。")
    print(f"  状態     : {recording_status}")
    print(f"  録画時間 : {duration_seconds:.3f}秒")
    print(f"  動画     : {video_path}")
    print(f"  メタデータ: {metadata_path}")

    if recording_status == "failed":
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())