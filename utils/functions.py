import ee
import os
import requests
import shutil
from retry import retry


def get_files_info(directory):
    """
    Get information about files in a specified directory.
    This function ensures the specified directory exists, retrieves a list of all files
    in the directory, and returns the total number of files along with their names.
    Args:
        directory (str): The path to the directory to inspect.
    Returns:
        tuple: A tuple containing:
            - num_files (int): The total number of files in the directory.
            - img_ids (list of str): A list of file names in the directory.
    """
    # Ensure the directory exists
    os.makedirs(directory, exist_ok=True)

    # Get the list of all files and directories
    file_list = os.listdir(directory)

    # Filter only files
    file_list = [file for file in file_list if os.path.isfile(os.path.join(directory, file))]

    # Get the number of files
    num_files = len(file_list)

    print(f'Total number of files: {num_files}')

    img_ids = file_list  # Directly assign the list of file names
    
    return num_files, img_ids

def getRequests(params, image, region):
    img = ee.Image(1).rename("Class").addBands(image)
    points = img.stratifiedSample(
        numPoints=params["count"],
        region=region,
        scale=params["scale"],
        seed=params["seed"],
        geometries=True,
    )
    
    return points.aggregate_array(".geo").getInfo()

@retry(tries=10, delay=1, backoff=2)
def getResult(index, point, image, params, id):
    import re

    point = ee.Geometry.Point(point["coordinates"])
    region = point.buffer(params["buffer"]).bounds()

    # Escolhe URL conforme formato
    if params["format"] in ["png", "jpg"]:
        url = image.getThumbURL(
            {
                "region": region,
                "dimensions": params["dimensions"],
                "format": params["format"],
            }
        )
    else:
        url = image.getDownloadURL(
            {
                "region": region,
                "dimensions": params["dimensions"],
                "format": params["format"],
                "bands": params["bands"],
                "crs": params["crs"],
            }
        )

    # Define extensão
    if params["format"] == "GEO_TIFF":
        ext = "tif"
    else:
        ext = params["format"]

    # ==============================
    # 🟩 Extrair a data do ID (ex: 20240901)
    # ==============================
    date_match = re.search(r"_(\d{8})T", id)
    if date_match:
        date_prefix = date_match.group(1)
    else:
        date_prefix = "unknown_date"

    # ==============================
    # 🟩 Criar nome do arquivo com data na frente
    # ==============================
    out_dir = os.path.abspath(params["out_dir"])
    basename = str(index).zfill(len(str(params["count"])))
    filename = f"{out_dir}/{date_prefix}_{id}_{params['prefix']}{basename}.{ext}"

    # ==============================
    # 🟩 Fazer download e salvar
    # ==============================
    r = requests.get(url, stream=True)
    if r.status_code != 200:
        r.raise_for_status()

    with open(filename, "wb") as out_file:
        shutil.copyfileobj(r.raw, out_file)

    print("Download Completed:", filename)
