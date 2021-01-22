from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS

images_folder = "images/"
tempates_folder = "templates/"



async def save_file_locally(files):
    import datetime
    filenames = []
    for file in files:
        filedata = await file.read()
        filename = f"{images_folder}{datetime.datetime.now().timestamp()}_{file.filename}"
        with open(filename,"wb") as f:
            f.write(filedata)
        filenames.append(filename)
    return filenames

async def add_to_db(data):
    with open("location.csv","a") as f:
        f.write(f"{data['filename']},{data['lat']},{data['lon']}\n")
        return True
    return False

def get_loc(fn):
    ret = {}
    i = Image.open(fn)
    info = i._getexif()
    try:
        for tag, value in info.items():
            decoded = TAGS.get(tag, tag)
            ret[decoded] = value
        print(f"Done fetching metadata for {fn}")
        lat = ret['GPSInfo'][2]
        latref = ret['GPSInfo'][1]
        lon = ret['GPSInfo'][4]
        lonref = ret['GPSInfo'][3]
        lat = lat[0] + lat[1]/60 + lat[2]/3600
        lon = lon[0] + lon[1]/60 + lon[2]/3600
        if latref == 'S':
            lat = -lat
        if lonref == 'W':
            lon = -lon
        from math import isnan
        if isnan(lat) or isnan(lon):
            raise Exception(f"The value is NaN for {fn}")
        lat = float(lat)
        lon = float(lon)
    except Exception as ex:
        print(ex)
        lat = None
        lon = None

    return {
        "filename": fn,
        "lat" : lat,
        "lon" : lon
        }

async def is_good(files):
    files = await save_file_locally(files)
    status = []
    for file in files:
        data = get_loc(file)
        if((data['lat'] and data['lon']) and (data['lat']!='nan' and data['lon']!='nan')):
            await add_to_db(data)
            status.append(f"lat: {data['lat']}, lon: {data['lon']} ")
        else:
            status.append("No Exec data")
    return status



def create_map():
    import folium, os
    m = folium.Map(zoom_start=10)
    data = open("location.csv","r").read().split("\n")[:-1]
    print(data)
    for i in data:
        try:
            n, l1, l2 = i.split(',')
            if(len(n)<0 or l1!="None" or l2!="None" or l1!='nan' or l2!='nan'):
                n = n.replace("\\","/")
                folium.Marker([l1, l2], tooltip=f"<img src='{n}' height=100 width=100></img>").add_to(m)
        except Exception as ex:
            print("[ - ]",ex)
    m.save(os.path.join(tempates_folder, "loc.html"))
    return os.path.join(tempates_folder, "loc.html")
