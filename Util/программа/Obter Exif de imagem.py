from Util.cfg import *
from Util.Config import *
try:
    import piexif
    import exifread
    import base64
    import os
    import tkinter
    from PIL import Image, ExifTags
    from tkinter import filedialog
    import webbrowser
    from datetime import datetime
except Exception as e:
   ErrorModule(e)

Title("Get Image Exif - Enhanced")

try:
    def ChooseImageFile():
        try:
            print(f"{BEFORE + current_time_hour() + AFTER} {INPUT} Enter the path to the image -> {reset}")
            image_file_types = [("Image files", "*.png;*.jpg;*.jpeg;*.gif;*.bmp;*.tiff;*.webp"), ("All files", "*.*")]

            if sys.platform.startswith("win"):
                root = tkinter.Tk()
                root.iconbitmap(os.path.join(tool_path, "Img", "SOMALIA_icon.ico"))
                root.withdraw()
                root.attributes('-topmost', True)
                file = filedialog.askopenfilename(parent=root, title=f"{name_tool} {version_tool} - Choose an image file", filetypes=image_file_types)
            elif sys.platform.startswith("linux"):
                file = filedialog.askopenfilename(title=f"{name_tool} {version_tool} - Choose an image file", filetypes=image_file_types)
            print(f"{BEFORE + current_time_hour() + AFTER} {INFO} File path: {white + file}")
            return file
        except:
            return input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} Enter the path to the image -> {reset}")

    def CleanValue(value):
        if isinstance(value, bytes):
            try:
                return value.decode('utf-8', errors='replace')
            except:
                return base64.b64encode(value).decode('utf-8')
        elif isinstance(value, (list, tuple)):
            return ', '.join(str(v) for v in value)
        elif isinstance(value, dict):
            return {k: CleanValue(v) for k, v in value.items()}
        else:
            return value

    def ConvertToDegrees(value):
        """Convert GPS coordinates to degrees"""
        if isinstance(value, tuple):
            d, m, s = value
            return d + (m / 60.0) + (s / 3600.0)
        elif isinstance(value, list) and len(value) == 3:
            d, m, s = value
            return d + (m / 60.0) + (s / 3600.0)
        else:
            return float(value)

    def GetGPSCoordinates(exif_dict):
        """Extract GPS coordinates from EXIF data"""
        gps_info = {}
        
        try:
            gps_data = exif_dict.get('GPS', {})
            
            # GPS Latitude
            if piexif.GPSIFD.GPSLatitude in gps_data and piexif.GPSIFD.GPSLatitudeRef in gps_data:
                lat = ConvertToDegrees(gps_data[piexif.GPSIFD.GPSLatitude])
                lat_ref = gps_data[piexif.GPSIFD.GPSLatitudeRef]
                if lat_ref == b'S':
                    lat = -lat
                gps_info['Latitude'] = lat
                gps_info['Latitude Ref'] = lat_ref.decode('utf-8') if isinstance(lat_ref, bytes) else str(lat_ref)
            
            # GPS Longitude
            if piexif.GPSIFD.GPSLongitude in gps_data and piexif.GPSIFD.GPSLongitudeRef in gps_data:
                lon = ConvertToDegrees(gps_data[piexif.GPSIFD.GPSLongitude])
                lon_ref = gps_data[piexif.GPSIFD.GPSLongitudeRef]
                if lon_ref == b'W':
                    lon = -lon
                gps_info['Longitude'] = lon
                gps_info['Longitude Ref'] = lon_ref.decode('utf-8') if isinstance(lon_ref, bytes) else str(lon_ref)
            
            # GPS Altitude
            if piexif.GPSIFD.GPSAltitude in gps_data:
                alt = gps_data[piexif.GPSIFD.GPSAltitude]
                if isinstance(alt, tuple) and len(alt) == 2:
                    gps_info['Altitude'] = f"{float(alt[0]) / float(alt[1])} meters"
            
            # GPS Time Stamp
            if piexif.GPSIFD.GPSTimeStamp in gps_data:
                gps_info['GPS Time Stamp'] = str(gps_data[piexif.GPSIFD.GPSTimeStamp])
            
            # GPS Date
            if piexif.GPSIFD.GPSDateStamp in gps_data:
                gps_date = gps_data[piexif.GPSIFD.GPSDateStamp]
                gps_info['GPS Date'] = gps_date.decode('utf-8') if isinstance(gps_date, bytes) else str(gps_date)
                
        except Exception as e:
            gps_info['GPS Error'] = str(e)
            
        return gps_info

    def GetCameraInfo(exif_dict):
        """Extract detailed camera information"""
        camera_info = {}
        
        try:
            # Camera Make and Model
            if piexif.ImageIFD.Make in exif_dict.get('0th', {}):
                camera_info['Camera Make'] = CleanValue(exif_dict['0th'][piexif.ImageIFD.Make])
            if piexif.ImageIFD.Model in exif_dict.get('0th', {}):
                camera_info['Camera Model'] = CleanValue(exif_dict['0th'][piexif.ImageIFD.Model])
            
            # Camera Settings
            exif_data = exif_dict.get('Exif', {})
            if piexif.ExifIFD.ExposureTime in exif_data:
                exp_time = exif_data[piexif.ExifIFD.ExposureTime]
                if isinstance(exp_time, tuple) and len(exp_time) == 2:
                    camera_info['Exposure Time'] = f"{exp_time[0]}/{exp_time[1]} sec"
            
            if piexif.ExifIFD.FNumber in exif_data:
                fnumber = exif_data[piexif.ExifIFD.FNumber]
                if isinstance(fnumber, tuple) and len(fnumber) == 2:
                    camera_info['FNumber'] = f"f/{float(fnumber[0]) / float(fnumber[1])}"
            
            if piexif.ExifIFD.ISOSpeedRatings in exif_data:
                camera_info['ISO'] = CleanValue(exif_data[piexif.ExifIFD.ISOSpeedRatings])
            
            if piexif.ExifIFD.FocalLength in exif_data:
                focal = exif_data[piexif.ExifIFD.FocalLength]
                if isinstance(focal, tuple) and len(focal) == 2:
                    camera_info['Focal Length'] = f"{float(focal[0]) / float(focal[1])} mm"
            
            if piexif.ExifIFD.DateTimeOriginal in exif_data:
                camera_info['Date Taken'] = CleanValue(exif_data[piexif.ExifIFD.DateTimeOriginal])
                
        except Exception as e:
            camera_info['Camera Info Error'] = str(e)
            
        return camera_info

    def OpenGoogleMaps(lat, lon):
        """Open Google Maps with the coordinates"""
        url = f"https://www.google.com/maps?q={lat},{lon}"
        try:
            webbrowser.open(url)
            print(f"{BEFORE + current_time_hour() + AFTER} {INFO} Opening Google Maps: {url}")
        except Exception as e:
            print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} Could not open Google Maps: {e}")

    def GetAllExif(image_path):
        exif_data = {}
        gps_coordinates = {}

        # Get basic image info using PIL
        try:
            with Image.open(image_path) as img:
                width, height = img.size
                depth = len(img.getbands())
                format_info = img.format
                mode_info = img.mode
                
                exif_data['Dimension'] = f"{width}x{height}"
                exif_data['Width'] = width
                exif_data['Height'] = height
                exif_data['Depth'] = depth
                exif_data['Format'] = format_info
                exif_data['Color Mode'] = mode_info
                
                # Try to get EXIF using PIL
                try:
                    exif_pil = img._getexif()
                    if exif_pil:
                        for tag_id, value in exif_pil.items():
                            tag = ExifTags.TAGS.get(tag_id, tag_id)
                            exif_data[f"PIL_{tag}"] = CleanValue(value)
                except:
                    pass
                    
        except Exception as e:
            exif_data["Image Error"] = str(e)

        # Get EXIF using piexif
        try:
            exif_dict = piexif.load(image_path)
            
            # Extract camera information
            camera_info = GetCameraInfo(exif_dict)
            exif_data.update(camera_info)
            
            # Extract GPS information
            gps_coordinates = GetGPSCoordinates(exif_dict)
            exif_data.update(gps_coordinates)
            
            # Extract other EXIF data
            for ifd in exif_dict:
                if ifd != 'thumbnail' and isinstance(exif_dict[ifd], dict):
                    for tag in exif_dict[ifd]:
                        try:
                            tag_name = piexif.TAGS[ifd].get(tag, {"name": f"Unknown_{tag}"})["name"]
                            raw_value = exif_dict[ifd][tag]
                            exif_data[f"{ifd}_{tag_name}"] = CleanValue(raw_value)
                        except:
                            continue
        except Exception as e:
            exif_data["PIEXIF_ERROR"] = str(e)

        # Get EXIF using exifread
        try:
            with open(image_path, 'rb') as f:
                tags = exifread.process_file(f, details=True)
                for tag in tags:
                    label = str(tag).replace('EXIF ', '').replace('Image ', '')
                    if label not in exif_data:
                        exif_data[f"EXIFREAD_{label}"] = CleanValue(str(tags[tag]))
        except Exception as e:
            exif_data["EXIFREAD_ERROR"] = str(e)

        # Get file system information
        try:
            file_stats = os.stat(image_path)
            exif_data['File Name'] = os.path.basename(image_path)
            exif_data['File Extension'] = os.path.splitext(image_path)[1].lower()
            exif_data['File Size'] = f"{file_stats.st_size} bytes ({file_stats.st_size / 1024:.2f} KB)"
            exif_data['Creation Date'] = datetime.fromtimestamp(file_stats.st_ctime).strftime('%Y-%m-%d %H:%M:%S')
            exif_data['Modification Date'] = datetime.fromtimestamp(file_stats.st_mtime).strftime('%Y-%m-%d %H:%M:%S')
            exif_data['Access Date'] = datetime.fromtimestamp(file_stats.st_atime).strftime('%Y-%m-%d %H:%M:%S')
            exif_data['File Permissions'] = oct(file_stats.st_mode)
            exif_data['File Accessibility'] = 'Readable' if os.access(image_path, os.R_OK) else 'Not Readable'
            exif_data['File Exists'] = 'Yes' if os.path.exists(image_path) else 'No'
            exif_data['Absolute Path'] = os.path.abspath(image_path)
        except Exception as e:
            exif_data["File Stats Error"] = str(e)
        
        # Display results
        if exif_data:
            categories = {
                'File Information': ['File Name', 'File Extension', 'File Size', 'Absolute Path', 
                                   'Creation Date', 'Modification Date', 'Access Date', 
                                   'File Permissions', 'File Accessibility', 'File Exists'],
                'Image Properties': ['Dimension', 'Width', 'Height', 'Depth', 'Format', 'Color Mode'],
                'Camera Information': ['Camera Make', 'Camera Model', 'Exposure Time', 'FNumber', 
                                     'ISO', 'Focal Length', 'Date Taken'],
                'GPS Information': ['Latitude', 'Longitude', 'Latitude Ref', 'Longitude Ref', 
                                  'Altitude', 'GPS Time Stamp', 'GPS Date'],
                'Other EXIF Data': [key for key in exif_data.keys() if not any(key in cat for cat in [
                    'File Information', 'Image Properties', 'Camera Information', 'GPS Information',
                    'Error', 'GPS Error', 'Camera Info Error', 'PIEXIF_ERROR', 'EXIFREAD_ERROR'
                ])]
            }
            
            print(f"\n{white}────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────")
            
            for category, keys in categories.items():
                category_keys = [k for k in keys if k in exif_data and exif_data[k] not in [None, '', 'None']]
                if category_keys:
                    print(f"\n{INFO_ADD} {yellow}{category}:{reset}")
                    max_key_length = max(len(k) for k in category_keys)
                    
                    for key in sorted(category_keys):
                        value = exif_data[key]
                        print(f" {INFO_ADD} {key.ljust(max_key_length)} : {white + str(value)}")
                        time.sleep(0.01)
            
            print(f"{white}────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────\n")
            
            # Offer to open Google Maps if GPS coordinates are available
            if 'Latitude' in gps_coordinates and 'Longitude' in gps_coordinates:
                print(f"{BEFORE + current_time_hour() + AFTER} {INFO} GPS coordinates found!")
                response = input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} Open Google Maps with these coordinates? (y/n) -> {reset}")
                if response.lower() in ['y', 'yes']:
                    OpenGoogleMaps(gps_coordinates['Latitude'], gps_coordinates['Longitude'])
                    
        else:
            print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} No EXIF information found.")

    Slow(osint_banner)
    image_path = ChooseImageFile()
    if image_path:
        print(f"{BEFORE + current_time_hour() + AFTER} {WAIT} Extracting comprehensive EXIF data from image...")
        GetAllExif(image_path)
    else:
        print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} No file selected.")
    
    Continue()
    Reset()
except Exception as e:
    Error(e)
