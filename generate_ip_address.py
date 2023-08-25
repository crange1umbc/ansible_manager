import os 
import ipaddress
from dotenv import load_dotenv

load_dotenv()

def generate_ip_range(start_ip,end_ip):
    start=ipaddress.ip_address(start_ip)
    end=ipaddress.ip_address(end_ip)

    ip_list=[]
    while start<=end:
        ip_list.append(str(start))
        start+=1
    return ip_list

def main(network):
    ip_ranges=os.environ.get(network)
    if not ip_ranges:
        print("IP_RANGES not defined in the environment.")
        return
    
    ip_ranges=ip_ranges.split(";")
    ip_list=[]
    for range_str in ip_ranges:
        
        start_ip,end_ip=range_str.split("-")
        start_ip=start_ip.strip().replace(" ","")
        end_ip=end_ip.strip().replace(" ","")

        ip_list.extend(generate_ip_range(start_ip,end_ip))
        filename=f"static/{network}.txt"

    with open(filename,"w") as file:
        file.write("\n".join(ip_list))

    os.chmod(filename,0o777)

    print(f"{len(ip_list)}")
    file.close()

main('IP_RANGE_3072')
main('IP_RANGE_4093')




