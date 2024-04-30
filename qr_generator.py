"""
This file is used to generate QR code for the VPN client .conf file.

#### Script Requirements ####
1. segno (https://pypi.org/project/segno/)
"""
import argparse
import os
from pathlib import Path

from segno import make


def get_terminal_working_dir():
    """Get the working directory of the current directory
    the user's terminal is on.
    """
    return os.getcwd()


def get_working_dir():
    """Get the working directory of the script.
    """
    return os.path.dirname(os.path.abspath(__file__))


def generate_qr_code(conf_file_path: str, qr_code_path: str):
    """Generate QR code from the .conf file.

    Args:
    - conf_file_path (str): The path to the .conf file.
    - qr_code_path (str): The path to save the QR code.
    """
    with open(conf_file_path, 'r', encoding="utf-8") as file:
        conf_content = file.read()

    qr_code = make(conf_content)
    qr_code.save(qr_code_path, scale=10, border=12,
                 )
    return qr_code


def get_filename_from_path(file_path: str):
    """Get the filename from the file path.

    Args:
    - file_path (str): The path to the file.

    Returns:
    - str: The filename.
    """
    return os.path.basename(file_path)


def get_filename_without_ext(filename: str):
    """Remove the extension from the filename.

    Args:
    - filename (str): The filename.

    Returns:
    - str: The filename without the extension.
    - str: The extension.
    """
    return filename.split('.')[0]


def delete_file(file_path: str):
    """Delete the file.

    Args:
    - file_path (str): The path to the file.
    """
    os.remove(file_path)


parser = argparse.ArgumentParser(
    description="""
Generate QR code for the VPN client '.conf' file.\n
The '.conf' file is the configuration file for the VPN client.\n
The QR code is used to easily import the VPN client configuration.\n
The QR code is saved as a '.png' file.    
""",
    add_help=True,
)

parser.add_argument("vpn_conf_file", type=str,
                    help="The path to the .conf file.")
parser.add_argument("--save-img", action="store_true",
                    default=False, help="Save the QR code as a .png file.")
parser.add_argument("--img-path", default=get_terminal_working_dir(), type=str,
                    help="""
                    The path to save the QR code png. 
                    Default is the current working directory.""")

args = parser.parse_args()

conf_file = os.path.join(os.getcwd(), Path(args.vpn_conf_file))
should_save_img = args.save_img
conf_filename = get_filename_without_ext(get_filename_from_path(conf_file))
img_file = os.path.join(args.img_path, f"{conf_filename}-qr.png")


qr = generate_qr_code(conf_file, img_file)


qr.terminal(border=8, compact=True)

if should_save_img is False:
    print(should_save_img)
    print(img_file)
    delete_file(img_file)
