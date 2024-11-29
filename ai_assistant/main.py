from flask import Flask, render_template, request, jsonify
import os
import cv2
import numpy as np
import base64
import mediapipe as mp
import whois
import dns.resolver
import requests
from urllib.parse import urlparse
import socket
import json
import psutil
import platform
from datetime import datetime

app = Flask(__name__)

# Initialize MediaPipe Face Detection
mp_face_detection = mp.solutions.face_detection
face_detection = mp_face_detection.FaceDetection(min_detection_confidence=0.5)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/test', methods=['GET'])
def test():
    return jsonify({"status": "success", "message": "API is working!"})

@app.route('/visual_detection', methods=['POST'])
def visual_detection():
    try:
        data = request.get_json()
        if not data or 'image' not in data:
            return jsonify({"error": "No image data provided"})

        # Get the base64 image data
        image_data = data['image']
        if ',' in image_data:
            image_data = image_data.split(',')[1]

        # Convert base64 to image
        image_bytes = base64.b64decode(image_data)
        nparr = np.frombuffer(image_bytes, np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        if image is None:
            return jsonify({"error": "Invalid image data"})

        # Convert BGR to RGB
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
        # Process the image
        results = face_detection.process(image_rgb)
        
        # Initialize detections list
        detections = []
        
        if results.detections:
            for detection in results.detections:
                bbox = detection.location_data.relative_bounding_box
                detections.append({
                    "confidence": float(detection.score[0]),
                    "bbox": {
                        "xmin": float(bbox.xmin),
                        "ymin": float(bbox.ymin),
                        "width": float(bbox.width),
                        "height": float(bbox.height)
                    }
                })
                
                # Draw detection on image
                h, w, _ = image.shape
                x = int(bbox.xmin * w)
                y = int(bbox.ymin * h)
                width = int(bbox.width * w)
                height = int(bbox.height * h)
                cv2.rectangle(image, (x, y), (x + width, y + height), (0, 255, 0), 2)

        # Convert processed image back to base64
        _, buffer = cv2.imencode('.jpg', image)
        processed_image = base64.b64encode(buffer).decode('utf-8')

        return jsonify({
            "success": True,
            "processed_image": processed_image,
            "detections": detections
        })

    except Exception as e:
        print(f"Error in visual detection: {str(e)}")
        return jsonify({"error": str(e)})

@app.route('/osint', methods=['POST'])
def osint_analysis():
    try:
        data = request.get_json()
        if not data or 'target' not in data:
            return jsonify({"error": "No target provided"})

        target = data['target'].strip()
        if not target:
            return jsonify({"error": "Empty target provided"})

        # Add http:// if no protocol specified
        if not target.startswith(('http://', 'https://')):
            target = 'http://' + target

        # Parse URL
        parsed_url = urlparse(target)
        domain = parsed_url.netloc if parsed_url.netloc else parsed_url.path
        if not domain:
            return jsonify({"error": "Invalid domain"})

        # Initialize results dictionary
        results = {
            "domain_info": {},
            "dns_records": {},
            "headers": {},
            "ip_info": {}
        }

        # Get WHOIS information
        try:
            domain_info = whois.whois(domain)
            results["domain_info"] = {
                "registrar": str(domain_info.registrar) if domain_info.registrar else "N/A",
                "creation_date": str(domain_info.creation_date) if domain_info.creation_date else "N/A",
                "expiration_date": str(domain_info.expiration_date) if domain_info.expiration_date else "N/A",
                "name_servers": domain_info.name_servers if isinstance(domain_info.name_servers, list) else [str(domain_info.name_servers)] if domain_info.name_servers else ["N/A"]
            }
        except Exception as e:
            results["domain_info"] = {"error": f"WHOIS lookup failed: {str(e)}"}

        # Get DNS records
        for record_type in ['A', 'MX', 'NS']:
            try:
                records = dns.resolver.resolve(domain, record_type)
                if record_type == 'MX':
                    results["dns_records"][record_type] = [str(record.exchange) for record in records]
                else:
                    results["dns_records"][record_type] = [str(record) for record in records]
            except Exception as e:
                results["dns_records"][record_type] = [f"Error: {str(e)}"]

        # Get HTTP headers
        try:
            response = requests.head(target, timeout=5, allow_redirects=True)
            results["headers"] = dict(response.headers)
        except Exception as e:
            results["headers"] = {"error": f"Failed to get headers: {str(e)}"}

        # Get IP information
        try:
            ip = socket.gethostbyname(domain)
            ip_response = requests.get(f"https://ipapi.co/{ip}/json/", timeout=5).json()
            results["ip_info"] = {
                "ip": ip,
                "country": ip_response.get("country_name", "N/A"),
                "region": ip_response.get("region", "N/A"),
                "city": ip_response.get("city", "N/A"),
                "org": ip_response.get("org", "N/A")
            }
        except Exception as e:
            results["ip_info"] = {"error": f"IP lookup failed: {str(e)}"}

        return jsonify({
            "success": True,
            "target": target,
            "results": results
        })

    except Exception as e:
        print(f"Error in OSINT analysis: {str(e)}")
        return jsonify({"error": str(e)})

@app.route('/device_status', methods=['GET'])
def device_status():
    try:
        # System information
        system_info = {
            "system": platform.system(),
            "version": platform.version(),
            "machine": platform.machine(),
            "processor": platform.processor()
        }

        # CPU information
        cpu_info = {
            "physical_cores": psutil.cpu_count(logical=False),
            "total_cores": psutil.cpu_count(logical=True),
            "cpu_percent": psutil.cpu_percent(interval=1),
            "frequency": {
                "current": psutil.cpu_freq().current,
                "min": psutil.cpu_freq().min,
                "max": psutil.cpu_freq().max
            }
        }

        # Memory information
        memory = psutil.virtual_memory()
        memory_info = {
            "total": memory.total,
            "available": memory.available,
            "used": memory.used,
            "percent": memory.percent
        }

        # Disk information
        disk = psutil.disk_usage('/')
        disk_info = {
            "total": disk.total,
            "used": disk.used,
            "free": disk.free,
            "percent": disk.percent
        }

        # Network information
        network_info = {}
        for interface, stats in psutil.net_if_stats().items():
            network_info[interface] = {
                "isup": stats.isup,
                "speed": stats.speed
            }

        # Battery information
        battery = psutil.sensors_battery()
        battery_info = None
        if battery:
            battery_info = {
                "percent": battery.percent,
                "power_plugged": battery.power_plugged,
                "time_left": battery.secsleft if battery.secsleft != -2 else "Calculating..."
            }

        return jsonify({
            "success": True,
            "timestamp": datetime.now().isoformat(),
            "system": system_info,
            "cpu": cpu_info,
            "memory": memory_info,
            "disk": disk_info,
            "network": network_info,
            "battery": battery_info
        })

    except Exception as e:
        print(f"Error in device status: {str(e)}")
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
