from datetime import datetime as dt
from hashlib import new
import platform
import shutil
from pathlib import WindowsPath, Path
from typing import Generator

from PIL import Image

ASSETS_PATH = WindowsPath.home() / 'AppData/Local/Packages/Microsoft.Windows.ContentDeliveryManager_cw5n1h2txyewy/LocalState/Assets'

DESKTOP = WindowsPath.home() / 'desktop'

DESTINATION_PATH = DESKTOP / 'Windows Wallpapers'

DATE_STR = dt.now().strftime('%Y%m%d')


def steal_windows_wallpapers(destinationDir: WindowsPath = DESTINATION_PATH):
    check_if_windows()
    destinationDir.mkdir(exist_ok=True, parents=True)
    windows_wallpaper_assets = get_image_assets()
    copy_and_transform_image_assets(windows_wallpaper_assets, destinationDir)


def check_if_windows():
    if platform.system() != 'Windows':
        raise SystemError('This app only works on Windows.')


def copy_and_transform_image_assets(image_assets, destinationDir):
    """
    Copies each image_asset file to a new directory and renames them
    chronologically with a .jpg suffix to transform them into images.
    """
    last_number = get_last_number()

    for i, image_asset in enumerate(image_assets, last_number+1):
        new_image_name = f'{i}.jpg'
        new_image_path = destinationDir / new_image_name
        shutil.copy(image_asset, new_image_path)


def get_last_number() -> int:
    processed_assets = get_processed_assets()
    last_file_name = get_last_filename(processed_assets)
    last_number = int(Path(last_file_name).stem)
    return last_number


def get_image_name(source) -> str:
    source = f'_{source}' if source else ""
    ext = '.jpg'
    number_fmt = '{number}'
    name = f'{DATE_STR}{source}_{number_fmt}.{ext}'


def get_number_from_filename(file: WindowsPath, regex='_(\d*)\.'):
    pass


def get_file_orientation(file_path: str) -> str:
    fpath = str(file.resolve())
    # (1920, 1080) = Horizontal
    # (1080, 1920) = Vertical

    with Image.open(fpath) as im:
        fsize = im.size
        ratio = fsize[0] / fsize[1]
        orientation = "P" if ratio <= 1 else "L"
        return orientation


def get_last_filename(assets):
    return max(assets)


def get_processed_assets() -> Generator[WindowsPath, None, None]:
    return DESTINATION_PATH.iterdir()


def get_image_assets():
    raw_assets = get_raw_assets()
    image_assets = filter_assets_for_images(raw_assets)
    return image_assets


def get_raw_assets() -> Generator[WindowsPath, None, None]:
    return ASSETS_PATH.iterdir()


def filter_assets_for_images(assets) -> list:
    return [asset for asset in assets if is_image(asset)]

# def filter_assets_for_horizontal_images(assets)->list:
#     return [asset for asset in assets if is_horizontal(asset)]

# def is_horizontal(file: WindowsPath):
#     file.lstat().


def is_image(asset: WindowsPath):
    # Asset files > 20000 bytes are typically images
    byte_size = 20000
    return get_file_size(asset) >= byte_size


def get_file_size(file: WindowsPath):
    file_size_in_bytes = file.lstat().st_size
    return file_size_in_bytes


if __name__ == '__main__':
    steal_windows_wallpapers()
