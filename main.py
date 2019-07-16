import os
import requests
from datetime import date, datetime, timedelta

url    = "https://s5phub.copernicus.eu/dhus/odata/v1/Products"
usr    = "s5pguest"
passwd = "s5pguest"

def get_product_list(gas, year, month, day):
    # magic strings gotten from somewhere, not sure where tho, can ask around
    prod_name = "substringof ('{}', Name)".format(gas)
    start_range = f"year(ContentDate/Start) eq {year} and month(ContentDate/Start) eq {month} and day(ContentDate/Start) eq {day}"
    end_range   = f"year(ContentDate/End) eq {year} and month(ContentDate/End) eq {month} and day(ContentDate/End) eq {day}"

    prod_date = f"{start_range} and {end_range}"

    # product types can be OFFLINE and NearRealTime (somewhere on the API hub)
    prod_type     = "OFFL"
    prod_name_off = f"substringof ('{prod_type}', Name)"
    filter_string_offline = f"{prod_name} and {prod_name_off} and {prod_date}"

    req_offline = requests.get(url, auth=(usr, passwd), params={"$format": "json", "$filter": filter_string_offline})

    try:
        products = req_offline.json()["d"]["results"]
        
    except Exception as err:
        print(f"[GET_PRODUCT_LIST] Error while downloading: {err}")
    else:
        if products:
            print(f"OFFLINE products available for {gas}")
            print(f"Number of .nc files to download: {len(products)}")
            product_ID_list   = []
            product_name_list = []
            for p in products:
                ID   = p["Id"]
                name = p["Name"]
                contentLength = int(p["ContentLength"])

                print(f"ID: {ID}, size: {contentLength / (1024**2) :.2f}MB")
                product_name_list += [name]
                product_ID_list   += [ID]

            return product_name_list, product_ID_list, prod_type
        else:
            # there are only NearRealTime files available or there are no files available
            pass

def download_NC(prod_ID, prod_name, MAX_REDOWN):
    product_ID_list   = []
    product_name_list = []

    n_attempts = 0

    while n_attempts < MAX_REDOWN:
        print(f"[DOWNLOAD_NC] Downloading {prod_ID}... (attempt {n_attempts+1}/{MAX_REDOWN})")
        try:
            download = requests.get(f"{url}('{prod_ID}')/$value", auth=(usr, passwd))
            print(f"Status code: {download.status_code}")
            with open(f"downloaded_data/{prod_name}.nc", "wb") as fout:
                fout.write(download.content)
            break
        except Exception as error:
            print(error)
        n_attempts += 1


def download_daily_data(gas, year, month, day):
    n_attempts     = 0
    MAX_N_ATTEMPTS = 2
    product_ID_list   = []
    product_name_list = []

    # in case the connection times out
    while n_attempts < MAX_N_ATTEMPTS:
        try:
            product_name_list, product_ID_list, product_type = get_product_list(gas, year, month, day)
        except Exception as e:
            print(f"[DOWNLOAD_DAILY_DATA] Error: {e}")
        else:
            for prod_name, prod_ID in zip(product_name_list, product_ID_list):
                if (os.path.exists(f"./downloaded_data/{prod_name}.nc")):
                    print(f"[DOWNLOAD_DAILY_DATA] File {prod_name} already downloaded")
                    print("[DOWNLOAD_DAILY_DATA] Skipping!")
                    continue
                try:
                    download_NC(prod_ID, prod_name, MAX_N_ATTEMPTS)
                except Exception as err:
                    print(f"[DOWNLOAD_DAILY_DATA] Error: {e}")
            return product_name_list, product_ID_list

        n_attempts += 1

def main():
    # the date of the data to download
    start_date = date(2018, 7, 28)

    # which gasses to download
    gasses = ["CO", "O3"]

    # but we only take the first gas anyway
    download_daily_data(gasses[0], start_date.year, start_date.month, start_date.day)

if __name__ == "__main__":
    main()
