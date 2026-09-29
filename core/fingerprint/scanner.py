import serial
import serial.tools.list_ports
import time

from pathlib import Path
from datetime import datetime

from PIL import Image, ImageEnhance, ImageFilter


# ============================================================
# CONFIGURATION
# ============================================================

# Preferred port.
# The scanner will try this first.
PREFERRED_PORT = "COM7"

BAUDRATE = 115200

MAGIC = b"RAWF"


# ============================================================
# AS608 FINGERPRINT IMAGE
# ============================================================

# 256 pixels wide
# 288 pixels high
#
# 4-bit grayscale = 2 pixels per byte
#
# 256 * 288 / 2 = 36864 bytes

WIDTH = 256
HEIGHT = 288

EXPECTED_IMAGE_BYTES = (
    WIDTH * HEIGHT
) // 2


# ============================================================
# PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent

CAPTURE_DIR = (
    BASE_DIR
    / "captures"
)

CAPTURE_DIR.mkdir(
    parents=True,
    exist_ok=True
)


# ============================================================
# SERIAL PORT DISCOVERY
# ============================================================

def list_serial_ports():

    ports = list(
        serial.tools.list_ports.comports()
    )

    if not ports:

        print()
        print("No serial ports detected.")
        print()

        return []

    print()
    print("Available serial ports:")
    print("----------------------------------------")

    for port in ports:

        print(
            f"Port        : {port.device}"
        )

        print(
            f"Description : {port.description}"
        )

        if port.manufacturer:

            print(
                f"Manufacturer: {port.manufacturer}"
            )

        if port.hwid:

            print(
                f"Hardware ID : {port.hwid}"
            )

        print("----------------------------------------")

    return ports


# ============================================================
# OPEN SERIAL PORT
# ============================================================

def open_serial(port):

    print()
    print("Opening serial port...")
    print(f"PORT     : {port}")
    print(f"BAUDRATE : {BAUDRATE}")

    ser = serial.Serial(
        port=port,
        baudrate=BAUDRATE,
        timeout=0.2
    )

    time.sleep(0.5)

    print("Serial connected.")

    return ser


# ============================================================
# FIND RAWF WITHOUT BLOCKING FOREVER
# ============================================================

def wait_for_magic(
    ser,
    timeout=3
):

    buffer = bytearray()

    start_time = time.time()

    while (
        time.time() - start_time
        < timeout
    ):

        byte = ser.read(1)

        if not byte:

            continue

        buffer.extend(byte)

        if len(buffer) > len(MAGIC):

            buffer = buffer[
                -len(MAGIC):
            ]

        if bytes(buffer) == MAGIC:

            return True

    return False


# ============================================================
# DETECT ESP32 PORT
# ============================================================

def detect_esp32_port():

    print()
    print("========================================")
    print("SCANNING FOR ESP32")
    print("========================================")

    ports = list(
        serial.tools.list_ports.comports()
    )

    if not ports:

        print()
        print(
            "ERROR: No serial ports detected."
        )

        return None


    # ========================================================
    # PUT PREFERRED PORT FIRST
    # ========================================================

    ordered_ports = []

    preferred = None

    for port in ports:

        if port.device.upper() == PREFERRED_PORT.upper():

            preferred = port

            break


    if preferred:

        ordered_ports.append(
            preferred
        )


    for port in ports:

        if preferred:

            if (
                port.device
                == preferred.device
            ):
                continue

        ordered_ports.append(port)


    # ========================================================
    # TEST EACH PORT
    # ========================================================

    for port_info in ordered_ports:

        port = port_info.device

        print()
        print("----------------------------------------")
        print(
            f"Testing port: {port}"
        )

        print(
            f"Description : "
            f"{port_info.description}"
        )

        ser = None

        try:

            ser = serial.Serial(
                port=port,
                baudrate=BAUDRATE,
                timeout=0.2
            )

            time.sleep(0.5)


            # ------------------------------------------------
            # Clear old data
            # ------------------------------------------------

            ser.reset_input_buffer()


            print(
                "Waiting for RAWF..."
            )


            # ------------------------------------------------
            # Wait for ESP32 signal
            # ------------------------------------------------

            detected = wait_for_magic(
                ser,
                timeout=3
            )


            if detected:

                print()
                print(
                    "========================================"
                )

                print(
                    "ESP32 DETECTED"
                )

                print(
                    f"Port: {port}"
                )

                print(
                    "========================================"
                )

                return ser


            print(
                f"No RAWF detected on {port}."
            )


        except Exception as e:

            print(
                f"Cannot use {port}: {e}"
            )


        finally:

            if ser is not None:

                if ser.is_open:

                    # Do NOT close the port if
                    # this is the detected ESP32.

                    pass


    print()
    print(
        "========================================"
    )

    print(
        "ESP32 NOT FOUND"
    )

    print(
        "========================================"
    )

    return None


# ============================================================
# READ EXACT BYTES
# ============================================================

def read_exact(
    ser,
    size
):

    data = bytearray()

    while len(data) < size:

        chunk = ser.read(
            size - len(data)
        )

        if not chunk:

            continue

        data.extend(chunk)

    return bytes(data)


# ============================================================
# FIND RAWF
# ============================================================

def find_magic(ser):

    print()
    print(
        "Waiting for ESP32 RAWF signal..."
    )
    print()

    buffer = bytearray()

    while True:

        byte = ser.read(1)

        if not byte:

            continue

        buffer.extend(byte)

        if len(buffer) > len(MAGIC):

            buffer = buffer[
                -len(MAGIC):
            ]

        if bytes(buffer) == MAGIC:

            print(
                "RAWF DETECTED"
            )

            return True


# ============================================================
# FIND AS608 PACKET HEADER
# ============================================================

def find_packet_header(ser):

    buffer = bytearray()

    while True:

        byte = ser.read(1)

        if not byte:

            continue

        buffer.extend(byte)

        if len(buffer) > 2:

            buffer = buffer[-2:]


        if bytes(buffer) == b"\xEF\x01":

            return b"\xEF\x01"


# ============================================================
# READ AS608 PACKET
# ============================================================

def read_as608_packet(ser):

    # --------------------------------------------------------
    # Start code
    # --------------------------------------------------------

    start = find_packet_header(
        ser
    )


    # --------------------------------------------------------
    # Address: 4 bytes
    # --------------------------------------------------------

    address = read_exact(
        ser,
        4
    )


    # --------------------------------------------------------
    # Packet type
    # --------------------------------------------------------

    packet_type = read_exact(
        ser,
        1
    )[0]


    # --------------------------------------------------------
    # Length
    # --------------------------------------------------------

    length_bytes = read_exact(
        ser,
        2
    )

    length = int.from_bytes(
        length_bytes,
        byteorder="big"
    )


    # --------------------------------------------------------
    # Payload + checksum
    # --------------------------------------------------------

    payload_and_checksum = read_exact(
        ser,
        length
    )


    packet = (
        start
        + address
        + bytes([packet_type])
        + length_bytes
        + payload_and_checksum
    )


    return (
        packet,
        packet_type,
        length,
        payload_and_checksum
    )


# ============================================================
# CAPTURE FINGERPRINT
# ============================================================

def capture_fingerprint():

    ser = None

    image_bytes = bytearray()

    packet_stream = bytearray()


    try:

        # ====================================================
        # AUTOMATICALLY DETECT ESP32
        # ====================================================

        ser = detect_esp32_port()


        if ser is None:

            print()
            print(
                "Fingerprint scanner could not "
                "be detected."
            )

            return None


        # ====================================================
        # RAWF
        # ====================================================

        print()
        print(
            "Waiting for ESP32 RAWF signal..."
        )

        find_magic(ser)


        print()
        print(
            "Waiting for AS608 image packets..."
        )


        packet_number = 0


        # ====================================================
        # RECEIVE AS608 PACKETS
        # ====================================================

        while True:

            (
                packet,
                packet_type,
                length,
                payload_and_checksum
            ) = read_as608_packet(
                ser
            )


            packet_number += 1


            packet_stream.extend(
                packet
            )


            # ------------------------------------------------
            # AS608 packet length
            #
            # length =
            # payload + checksum
            # ------------------------------------------------

            if length < 2:

                print(
                    f"Packet {packet_number}: "
                    f"invalid length={length}"
                )

                continue


            payload = (
                payload_and_checksum[:-2]
            )


            print(
                f"Packet {packet_number}: "
                f"type=0x{packet_type:02X}, "
                f"length={length}, "
                f"image={len(payload)}"
            )


            # ------------------------------------------------
            # IMAGE DATA PACKET
            # ------------------------------------------------

            if packet_type == 0x02:

                image_bytes.extend(
                    payload
                )


            # ------------------------------------------------
            # END DATA PACKET
            # ------------------------------------------------

            elif packet_type == 0x08:

                image_bytes.extend(
                    payload
                )


                print()
                print(
                    "AS608 image transmission "
                    "complete."
                )

                break


            # ------------------------------------------------
            # OTHER PACKETS
            # ------------------------------------------------

            else:

                print(
                    f"Warning: unexpected "
                    f"packet type "
                    f"0x{packet_type:02X}"
                )


        # ====================================================
        # VALIDATE IMAGE SIZE
        # ====================================================

        print()
        print(
            "========================================"
        )

        print(
            f"Received image bytes : "
            f"{len(image_bytes)}"
        )

        print(
            f"Expected image bytes : "
            f"{EXPECTED_IMAGE_BYTES}"
        )

        print(
            "========================================"
        )

        print()


        # ====================================================
        # SAVE PACKET STREAM
        # ====================================================

        timestamp = datetime.now().strftime(
            "%Y%m%d_%H%M%S"
        )


        bin_path = (
            CAPTURE_DIR
            / f"fingerprint_{timestamp}.bin"
        )


        with open(
            bin_path,
            "wb"
        ) as f:

            f.write(
                packet_stream
            )


        print(
            "Packet stream saved:"
        )

        print(
            bin_path
        )


        # ====================================================
        # CHECK IMAGE SIZE
        # ====================================================

        if (
            len(image_bytes)
            != EXPECTED_IMAGE_BYTES
        ):

            print()
            print(
                "ERROR:"
            )

            print(
                "Image byte count does not "
                "match the expected size."
            )

            return None


        # ====================================================
        # CREATE PNG
        # ====================================================

        print()
        print(
            "Starting PNG conversion..."
        )


        png_path = decode_and_save_png(
            bytes(image_bytes),
            timestamp
        )


        return png_path


    except Exception as e:

        print()
        print(
            "========================================"
        )

        print(
            "ERROR"
        )

        print(
            "========================================"
        )

        print(
            str(e)
        )


        import traceback

        traceback.print_exc()


        return None


    finally:

        if (
            ser is not None
            and ser.is_open
        ):

            ser.close()

            print()
            print(
                "Serial connection closed."
            )


# ============================================================
# DECODE 4-BIT FINGERPRINT IMAGE
# ============================================================

def decode_fingerprint_image(
    image_bytes
):

    if (
        len(image_bytes)
        != EXPECTED_IMAGE_BYTES
    ):

        raise ValueError(
            f"Invalid image size. "
            f"Received {len(image_bytes)}, "
            f"expected "
            f"{EXPECTED_IMAGE_BYTES}."
        )


    # ========================================================
    # TWO PIXELS PER BYTE
    # ========================================================

    pixels = bytearray(
        WIDTH * HEIGHT
    )


    pixel_index = 0


    for value in image_bytes:

        high_nibble = (
            value >> 4
        ) & 0x0F


        low_nibble = (
            value & 0x0F
        )


        pixels[pixel_index] = (
            high_nibble * 17
        )

        pixel_index += 1


        pixels[pixel_index] = (
            low_nibble * 17
        )

        pixel_index += 1


    image = Image.frombytes(
        "L",
        (
            WIDTH,
            HEIGHT
        ),
        bytes(pixels)
    )


    return image


# ============================================================
# ENHANCE IMAGE
# ============================================================

def enhance_fingerprint(
    image
):

    # --------------------------------------------------------
    # Grayscale
    # --------------------------------------------------------

    image = image.convert(
        "L"
    )


    # --------------------------------------------------------
    # Increase contrast
    # --------------------------------------------------------

    contrast = ImageEnhance.Contrast(
        image
    )

    image = contrast.enhance(
        2.0
    )


    # --------------------------------------------------------
    # Slight sharpening
    # --------------------------------------------------------

    image = image.filter(
        ImageFilter.SHARPEN
    )


    return image


# ============================================================
# SAVE PNG
# ============================================================

def decode_and_save_png(
    image_bytes,
    timestamp
):

    print()
    print(
        "Decoding fingerprint image..."
    )


    # ========================================================
    # DECODE RAW AS608 IMAGE
    # ========================================================

    image = decode_fingerprint_image(
        image_bytes
    )


    print(
        f"Decoded image size: "
        f"{image.width} x "
        f"{image.height}"
    )


    # ========================================================
    # ENHANCE
    # ========================================================

    image = enhance_fingerprint(
        image
    )


    # ========================================================
    # PNG PATH
    # ========================================================

    png_path = (
        CAPTURE_DIR
        / f"fingerprint_{timestamp}.png"
    )


    # ========================================================
    # SAVE
    # ========================================================

    image.save(
        png_path,
        format="PNG"
    )


    # ========================================================
    # VERIFY
    # ========================================================

    if not png_path.exists():

        raise RuntimeError(
            "PNG file was not created."
        )


    file_size = (
        png_path.stat().st_size
    )


    if file_size <= 0:

        raise RuntimeError(
            "PNG file was created "
            "but is empty."
        )


    print()
    print(
        "========================================"
    )

    print(
        "PNG CREATED SUCCESSFULLY"
    )

    print(
        "========================================"
    )

    print(
        f"PNG path : {png_path}"
    )

    print(
        f"PNG size : {file_size:,} bytes"
    )

    print(
        f"Image    : "
        f"{image.width} x "
        f"{image.height}"
    )

    print(
        "========================================"
    )

    print()


    return png_path


# ============================================================
# CAPTURE LEFT FINGER
# ============================================================

def capture_left_finger():

    return capture_fingerprint()


# ============================================================
# CAPTURE RIGHT FINGER
# ============================================================

def capture_right_finger():

    return capture_fingerprint()


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    png_path = capture_fingerprint()


    if png_path:

        print()
        print(
            "Fingerprint capture completed."
        )

        print()
        print(
            "Open this PNG:"
        )

        print(
            png_path
        )

    else:

        print()
        print(
            "Fingerprint capture failed."
        )