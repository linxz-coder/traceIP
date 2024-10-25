import subprocess
import re
import requests
import time

def run_traceroute(target_ip):
    process = subprocess.Popen(['traceroute', target_ip], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)

    while True:
        output = process.stdout.readline()
        if output == '' and process.poll() is not None:
            break
        if output:
            print(output.strip())
            ip = parse_ip(output)
            if ip:
                display_ip_info(ip)

def parse_ip(traceroute_output):
    match = re.search(r'\((\d+\.\d+\.\d+\.\d+)\)', traceroute_output)
    if match:
        return match.group(1)
    return None

def get_ip_info(ip):
    response = requests.get(f'http://ip-api.com/json/{ip}')
    if response.status_code == 200:
        return response.json()
    else:
        return None

def display_ip_info(ip):
    info = get_ip_info(ip)
    if info and info['status'] == 'success':
        print(f"IP: {ip}, Country: {info['country']}, Region: {info['regionName']}, City: {info['city']}, ISP: {info['isp']}")
    else:
        print(f"IP: {ip}, Info: No information available")
    time.sleep(1)  # 暂停1秒以便于阅读

if __name__ == '__main__':
    target_ip = input("Enter target IP for traceroute: ")
    run_traceroute(target_ip)
